"""
Vedic Calculator Module for Mobile
Wrapper around the existing VedicAstrologyEngine for mobile app integration
"""

import json
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.astrology_engine import VedicAstrologyEngine, BirthDetails
from datetime import datetime
import pytz

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
        # Parse date and time
        date_parts = date_str.split('-')
        time_parts = time_str.split(':')
        
        birth_date = datetime(
            int(date_parts[0]), int(date_parts[1]), int(date_parts[2]),
            int(time_parts[0]), int(time_parts[1])
        )
        
        # Create BirthDetails
        birth_details = BirthDetails(
            name=name,
            birth_date=birth_date,
            birth_time=birth_date.time(),
            location=location,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone_str
        )
        
        # Calculate chart
        engine = VedicAstrologyEngine()
        chart = engine.calculate_chart(birth_details)
        
        # Convert to JSON-serializable format
        result = {
            'name': name,
            'birth_date': date_str,
            'birth_time': time_str,
            'location': location,
            'planets': [],
            'houses': [],
            'ascendant': {
                'sign': chart.ascendant.sign if hasattr(chart, 'ascendant') else 'Unknown',
                'degree': chart.ascendant.degree if hasattr(chart, 'ascendant') else 0
            }
        }
        
        # Add planets
        if hasattr(chart, 'planets'):
            for planet in chart.planets:
                result['planets'].append({
                    'name': planet.name,
                    'sign': planet.sign,
                    'degree': planet.degree,
                    'house': planet.house,
                    'is_retrograde': planet.is_retrograde if hasattr(planet, 'is_retrograde') else False
                })
        
        # Add houses
        if hasattr(chart, 'houses'):
            for i, house in enumerate(chart.houses, 1):
                result['houses'].append({
                    'number': i,
                    'sign': house.sign,
                    'degree': house.degree
                })
        
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
