"""
Remedy Calculator Module for Mobile
Wrapper around the existing RemedyEngine for mobile app integration
"""

import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.remedy_engine import RemedyEngine

def get_remedies(chart_json):
    """
    Get remedies based on chart data
    
    Args:
        chart_json: JSON string containing chart data
    
    Returns:
        JSON string with remedy recommendations
    """
    try:
        chart_data = json.loads(chart_json)
        
        # Create remedy engine
        engine = RemedyEngine()
        
        # For now, return sample remedies
        # TODO: Integrate with actual chart analysis
        result = {
            'gemstones': [
                {
                    'name': 'Ruby',
                    'planet': 'Sun',
                    'benefits': 'Boosts confidence, leadership, and vitality',
                    'wearing_day': 'Sunday',
                    'metal': 'Gold',
                    'finger': 'Ring finger'
                }
            ],
            'mantras': [
                {
                    'planet': 'Sun',
                    'mantra': 'Om Suryaya Namaha',
                    'repetitions': 108,
                    'time': 'Early morning facing east',
                    'benefits': 'Strengthens Sun, improves health and status'
                }
            ],
            'fasting': [
                {
                    'day': 'Sunday',
                    'for_planet': 'Sun',
                    'instructions': 'Avoid salt, eat once after sunset',
                    'duration': 'Full day or partial'
                }
            ],
            'charity': [
                {
                    'day': 'Sunday',
                    'items': 'Wheat, jaggery, red cloth',
                    'beneficiary': 'Temples, poor people',
                    'planet': 'Sun'
                }
            ],
            'daily_practices': [
                'Offer water to Sun at sunrise',
                'Chant Gayatri Mantra 108 times',
                'Light ghee lamp in front of deity'
            ]
        }
        
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    # Test
    sample_chart = json.dumps({'name': 'Test', 'planets': []})
    print(get_remedies(sample_chart))
