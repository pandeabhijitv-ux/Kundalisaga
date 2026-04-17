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

# Ensure bundled mobile python modules are resolved before workspace-level packages.
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

try:
    # Import database-based calculator (for mobile)
    from src.astrology_engine.vedic_calculator_lite import (
        VedicAstrologyEngine, BirthDetails
    )
    CALCULATOR_TYPE = "Ephemeris Database (Swiss Ephemeris Quality)"
except ImportError as e:
    print(f"Failed to import lite calculator: {e}")
    try:
        # Fallback to Swiss Ephemeris (for desktop)
        from src.astrology_engine.vedic_calculator import (
            VedicAstrologyEngine, BirthDetails
        )
        CALCULATOR_TYPE = "Swiss Ephemeris"
    except ImportError:
        # Last resort - basic calculator
        CALCULATOR_TYPE = "Basic"
        VedicAstrologyEngine = None
        BirthDetails = None


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
        chart = engine.calculate_chart(birth_details)

        chart_planets = chart.get('planets', []) if isinstance(chart, dict) else getattr(chart, 'planets', [])
        chart_asc = chart.get('ascendant') if isinstance(chart, dict) else getattr(chart, 'ascendant', None)
        
        # Convert to JSON-serializable format
        result = {
            'name': name,
            'birth_date': date_str,
            'birth_time': time_str,
            'location': location,
            'planets': [],
            'houses': [],
            'ascendant': {
                'sign': getattr(chart_asc, 'sign', 'Unknown') if chart_asc else 'Unknown',
                'degree': getattr(chart_asc, 'degree_in_sign', 0) if chart_asc else 0
            },
            'dasha': {}
        }
        
        # Add planets
        for planet in chart_planets:
            result['planets'].append({
                'name': getattr(planet, 'name', 'Unknown'),
                'sign': getattr(planet, 'sign', 'Unknown'),
                'degree': round(getattr(planet, 'degree_in_sign', 0), 4),
                'longitude': round(getattr(planet, 'longitude', 0), 4),
                'house': getattr(planet, 'house', 1),
                'is_retrograde': getattr(planet, 'is_retrograde', False),
            })
        
        # Add houses
        if hasattr(chart, 'houses'):
            for i, house in enumerate(chart.houses, 1):
                result['houses'].append({
                    'number': i,
                    'sign': house.sign,
                    'degree': house.degree
                })

        # Add current dasha summary where possible.
        moon = next((p for p in result['planets'] if p['name'] == 'Moon'), None)
        if moon:
            try:
                dasha_fn = engine.calculate_vimshottari_dasha
                params = list(inspect.signature(dasha_fn).parameters.keys())
                if len(params) >= 2 and params[0] == 'moon_longitude':
                    dashas = dasha_fn(moon['longitude'], birth_date)
                else:
                    dashas = dasha_fn(birth_date, moon['longitude'])
                now = datetime.now()
                active = None
                for d in dashas:
                    d_start = datetime.strptime(d['start_date'], '%Y-%m-%d')
                    d_end = datetime.strptime(d['end_date'], '%Y-%m-%d')
                    if d_start <= now <= d_end:
                        active = d
                        break
                if active:
                    result['dasha'] = {
                        'mahadasha': active['lord'],
                        'start_date': active['start_date'],
                        'end_date': active['end_date']
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
