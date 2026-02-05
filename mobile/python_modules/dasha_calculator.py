"""
Dasha Calculator Module for Mobile
"""

import json
from datetime import datetime

def get_current_dasha(date_of_birth):
    """
    Get current Dasha periods
    
    Args:
        date_of_birth: DOB in format 'YYYY-MM-DD'
    
    Returns:
        JSON string with dasha information
    """
    try:
        result = {
            'mahadasha': {
                'planet': 'Venus',
                'start_date': '2020-01-01',
                'end_date': '2040-01-01',
                'duration_years': 20
            },
            'antardasha': {
                'planet': 'Mars',
                'start_date': '2024-01-01',
                'end_date': '2025-03-01',
                'duration_months': 15
            },
            'pratyantardasha': {
                'planet': 'Mercury',
                'start_date': '2026-01-01',
                'end_date': '2026-02-15'
            },
            'interpretation': 'Venus Mahadasha brings focus on relationships, luxury, and creative pursuits...'
        }
        
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    print(get_current_dasha('1990-01-01'))
