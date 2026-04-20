"""
Vedic Calculator Module for Mobile (Using Pre-computed Database)
SQLite-based ephemeris for Android compatibility
"""

import json
import sys
import os
from datetime import datetime
import pytz
import inspect

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Ensure bundled mobile python modules are resolved before workspace-level packages.
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

try:
    # Prefer full Swiss Ephemeris engine when available for accurate ascendant/lagna.
    from src.astrology_engine.vedic_calculator import (
        VedicAstrologyEngine, BirthDetails
    )
    CALCULATOR_TYPE = "Swiss Ephemeris"
except ImportError as e:
    print(f"Failed to import Swiss Ephemeris calculator: {e}")
    try:
        # Fallback to database-based calculator (for mobile compatibility)
        from src.astrology_engine.vedic_calculator_lite import (
            VedicAstrologyEngine, BirthDetails
        )
        CALCULATOR_TYPE = "Ephemeris Database (Swiss Ephemeris Quality)"
    except ImportError:
        # Last resort - basic calculator
        CALCULATOR_TYPE = "Basic"
        VedicAstrologyEngine = None
        BirthDetails = None


def _engine_calculate_chart(engine, birth_details):
    if hasattr(engine, 'calculate_chart'):
        return engine.calculate_chart(birth_details)
    if hasattr(engine, 'calculate_birth_chart'):
        return engine.calculate_birth_chart(birth_details)
    raise RuntimeError('No compatible chart calculation method found on engine')


def _to_plain_planets(chart):
    raw = chart.get('planets', []) if isinstance(chart, dict) else getattr(chart, 'planets', [])
    if isinstance(raw, dict):
        return list(raw.values())
    if isinstance(raw, list):
        return raw
    return []


def _parse_birth_datetime(date_str, time_str):
    """Parse flexible date/time input from mobile form.

    Accepts date formats like YYYY-MM-DD or YYYY/MM/DD and time formats
    like HH:MM, HH.MM, HH, HH:MM:SS.
    """
    date_clean = str(date_str).strip().replace('/', '-')
    date_parts = date_clean.split('-')
    if len(date_parts) != 3:
        raise ValueError("Date must be in YYYY-MM-DD format")

    year = int(float(date_parts[0]))
    month = int(float(date_parts[1]))
    day = int(float(date_parts[2]))

    time_clean = str(time_str).strip().replace('.', ':')
    time_parts = [p for p in time_clean.split(':') if p != '']
    if len(time_parts) == 0:
        raise ValueError("Time must be in HH:MM format")

    hour = int(float(time_parts[0]))
    minute = int(float(time_parts[1])) if len(time_parts) > 1 else 0

    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23")
    if minute < 0 or minute > 59:
        raise ValueError("Minute must be between 0 and 59")

    return datetime(year, month, day, hour, minute)


def _get_sign_and_degree(longitude):
    sign_num = int(longitude / 30) % 12
    sign_name = SIGNS[sign_num]
    degree_in_sign = longitude % 30
    return sign_num, sign_name, degree_in_sign


def _calculate_divisional_longitude(planet_longitude, division):
    """Mirror main engine divisional logic for mobile-safe output."""
    sign_num = int(planet_longitude / 30)
    degree_in_sign = planet_longitude % 30
    portion_size = 30.0 / division
    portion_num = int(degree_in_sign / portion_size)

    if division == 2:  # D2 Hora
        if sign_num % 2 == 0:
            div_sign = 3 if portion_num == 0 else 4
        else:
            div_sign = 4 if portion_num == 0 else 3
    elif division == 9:  # D9 Navamsa
        if sign_num in [0, 3, 6, 9]:
            div_sign = (sign_num + portion_num) % 12
        elif sign_num in [1, 4, 7, 10]:
            div_sign = (sign_num + 8 + portion_num) % 12
        else:
            div_sign = (sign_num + 4 + portion_num) % 12
    elif division == 10:  # D10 Dasamsa
        if sign_num % 2 == 0:
            div_sign = (sign_num + 8 + portion_num) % 12
        else:
            div_sign = (sign_num + portion_num) % 12
    elif division == 7:  # D7 Saptamsa
        if sign_num % 2 == 0:
            div_sign = (sign_num + 6 + portion_num) % 12
        else:
            div_sign = (sign_num + portion_num) % 12
    else:
        div_sign = (sign_num * division + portion_num) % 12

    return (div_sign * 30) + (portion_size / 2)


def _build_divisional_charts(planets_map, ascendant_longitude):
    divisional_charts = {}
    for division in [2, 3, 7, 9, 10]:
        div_planets = {}
        div_asc = _calculate_divisional_longitude(ascendant_longitude, division)
        div_asc_sign_num, div_asc_sign, _ = _get_sign_and_degree(div_asc)

        for planet_name, p in planets_map.items():
            base_lon = div_asc if planet_name == 'Ascendant' else float(p.get('longitude', 0))
            div_lon = _calculate_divisional_longitude(base_lon, division)
            sign_num, sign_name, degree_in_sign = _get_sign_and_degree(div_lon)
            house = ((sign_num - div_asc_sign_num) % 12) + 1

            div_planets[planet_name] = {
                'sign': sign_name,
                'sign_num': sign_num,
                'house': house,
                'degree_in_sign': round(degree_in_sign, 4),
                'longitude': round(div_lon, 4),
                'is_retrograde': bool(p.get('is_retrograde', False)),
            }

        divisional_charts[f'D{division}'] = {
            'division': division,
            'ascendant_sign': div_asc_sign,
            'planets': div_planets,
        }

    return divisional_charts

def calculate_chart(name, date_str, time_str, location, latitude, longitude, timezone_str):
    """
    Calculate Vedic birth chart
    
    Args:
        name: Person's name
        date_str: Birth date in format 'YYYY-MM-DD'
        time_str: Birth time in format 'HH:MM'
        location: Location name
        latitude: Latitude as float
        longitude: Longitude as float
        timezone_str: Timezone string (e.g., 'Asia/Kolkata')
    
    Returns:
        JSON string with chart data
    """
    try:
        # Parse flexible date/time from mobile input
        birth_date = _parse_birth_datetime(date_str, time_str)
        
        # Build BirthDetails compatible with both lite and full engines.
        birth_details = BirthDetails(
            date=birth_date,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone_str,
            name=name,
            place=location,
        )
        
        # Calculate chart
        engine = VedicAstrologyEngine()
        chart = _engine_calculate_chart(engine, birth_details)

        chart_planets = _to_plain_planets(chart)
        chart_asc = chart.get('ascendant') if isinstance(chart, dict) else getattr(chart, 'ascendant', None)
        
        # Convert to JSON-serializable format
        result = {
            'name': name,
            'birth_date': date_str,
            'birth_time': time_str,
            'location': location,
            'planets': {},
            'planets_list': [],
            'houses': [],
            'ascendant': {
                'sign': getattr(chart_asc, 'sign', 'Unknown') if chart_asc else 'Unknown',
                'degree': getattr(chart_asc, 'degree_in_sign', 0) if chart_asc else 0,
                'longitude': round(getattr(chart_asc, 'longitude', 0), 4) if chart_asc else 0,
                'nakshatra': getattr(chart_asc, 'nakshatra', 'Unknown') if chart_asc else 'Unknown',
                'nakshatra_pada': getattr(chart_asc, 'nakshatra_pada', 1) if chart_asc else 1,
            },
            'dasha': {},
            'divisional_charts': {},
        }
        
        # Add planets
        for planet in chart_planets:
            p_data = {
                'name': getattr(planet, 'name', 'Unknown'),
                'sign': getattr(planet, 'sign', 'Unknown'),
                'degree': round(getattr(planet, 'degree_in_sign', 0), 4),
                'longitude': round(getattr(planet, 'longitude', 0), 4),
                'house': getattr(planet, 'house', 1),
                'nakshatra': getattr(planet, 'nakshatra', 'Unknown'),
                'nakshatra_pada': getattr(planet, 'nakshatra_pada', 1),
                'is_retrograde': getattr(planet, 'is_retrograde', False),
            }
            result['planets'][p_data['name']] = p_data
            result['planets_list'].append(p_data)

        # Keep Ascendant inside planets map for analyzers that rely on it.
        result['planets']['Ascendant'] = {
            'name': 'Ascendant',
            'sign': result['ascendant']['sign'],
            'degree': round(result['ascendant']['degree'], 4),
            'longitude': round(result['ascendant']['longitude'], 4),
            'house': 1,
            'nakshatra': result['ascendant']['nakshatra'],
            'nakshatra_pada': result['ascendant']['nakshatra_pada'],
            'is_retrograde': False,
        }
        
        # Add houses
        if hasattr(chart, 'houses'):
            for i, house in enumerate(chart.houses, 1):
                result['houses'].append({
                    'number': i,
                    'sign': house.sign,
                    'degree': house.degree
                })

        # Build divisional charts from normalized D1 output to keep JSON serialization stable
        # across both lite and full engines.
        asc_lon = float(result['ascendant'].get('longitude', 0) or 0)
        result['divisional_charts'] = _build_divisional_charts(result['planets'], asc_lon)

        # Ensure requested D3 exists even when engine did not provide it.
        if 'D3' not in result['divisional_charts']:
            d3_only = _build_divisional_charts(result['planets'], asc_lon)
            if 'D3' in d3_only:
                result['divisional_charts']['D3'] = d3_only['D3']

        # Add current dasha summary where possible.
        moon = result['planets'].get('Moon')
        if moon:
            try:
                dasha_fn = engine.calculate_vimshottari_dasha
                params = list(inspect.signature(dasha_fn).parameters.keys())
                if len(params) >= 2 and params[0] == 'moon_longitude':
                    dashas = dasha_fn(float(moon['longitude']), birth_date)
                else:
                    dashas = dasha_fn(birth_date, float(moon['longitude']))
                now = datetime.now()
                active = None
                for d in dashas:
                    d_start_str = d.get('start_date') or d.get('maha_dasha_start')
                    d_end_str = d.get('end_date') or d.get('maha_dasha_end')
                    if not d_start_str or not d_end_str:
                        continue
                    d_start = datetime.strptime(d_start_str, '%Y-%m-%d')
                    d_end = datetime.strptime(d_end_str, '%Y-%m-%d')
                    if d_start <= now <= d_end:
                        active = d
                        break
                if active:
                    result['dasha'] = {
                        'mahadasha': active['lord'],
                        'start_date': active.get('start_date') or active.get('maha_dasha_start'),
                        'end_date': active.get('end_date') or active.get('maha_dasha_end')
                    }
            except Exception:
                result['dasha'] = {}
        
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_planet_positions(date_str, time_str, latitude, longitude):
    """
    Get current planetary positions
    
    Returns:
        JSON string with planet positions
    """
    try:
        engine = VedicAstrologyEngine()
        
        date_parts = date_str.split('-')
        time_parts = time_str.split(':')
        
        dt = datetime(
            int(date_parts[0]), int(date_parts[1]), int(date_parts[2]),
            int(time_parts[0]), int(time_parts[1])
        )
        
        # Get positions (implement based on your engine's methods)
        result = {
            'date': date_str,
            'time': time_str,
            'planets': []
        }
        
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    # Test the module
    result = calculate_chart(
        'Test User',
        '1990-01-01',
        '12:00',
        'Mumbai',
        19.0760,
        72.8777,
        'Asia/Kolkata'
    )
    print(result)
