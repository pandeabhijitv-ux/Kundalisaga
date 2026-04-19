"""Muhurat (Auspicious Timing) Analysis Entry Point for Chaquopy"""
import json
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MUHURAT_TYPES = {
    'marriage': {
        'favorable_months': ['November', 'December', 'January', 'February', 'March', 'April', 'May'],
        'favorable_tithis': ['2', '3', '5', '7', '10', '11', '12', '13'],
        'favorable_days': ['Monday', 'Wednesday', 'Thursday', 'Friday'],
        'avoid_tithis': ['4', '8', '9', '14', 'Amavasya', 'Purnima'],
        'avoid_days': ['Tuesday', 'Saturday'],
        'nakshatra_favorable': ['Rohini', 'Mrigashira', 'Magha', 'Uttara Phalguni', 'Hasta', 'Swati',
                                 'Anuradha', 'Mula', 'Uttara Ashadha', 'Uttara Bhadrapada', 'Revati'],
        'description': 'Marriage muhurat requires strong Venus and Jupiter with auspicious lagna.',
    },
    'business': {
        'favorable_months': ['January', 'February', 'April', 'May', 'September', 'October', 'November'],
        'favorable_tithis': ['1', '2', '3', '5', '6', '7', '10', '11', '12'],
        'favorable_days': ['Monday', 'Wednesday', 'Thursday', 'Friday'],
        'avoid_tithis': ['4', '8', '9', '14', 'Amavasya'],
        'avoid_days': ['Saturday', 'Sunday'],
        'nakshatra_favorable': ['Ashwini', 'Rohini', 'Mrigashira', 'Punarvasu', 'Pushya', 'Hasta',
                                 'Chitra', 'Swati', 'Anuradha', 'Uttara Ashadha', 'Revati'],
        'description': 'Business muhurat requires strong Mercury and Jupiter with wealth-oriented lagna.',
    },
    'housewarming': {
        'favorable_months': ['January', 'February', 'March', 'April', 'May', 'September', 'October', 'November'],
        'favorable_tithis': ['2', '3', '5', '6', '7', '10', '11', '12', '13'],
        'favorable_days': ['Monday', 'Wednesday', 'Thursday', 'Friday'],
        'avoid_tithis': ['4', '8', '9', '14', 'Amavasya'],
        'avoid_days': ['Tuesday', 'Saturday'],
        'nakshatra_favorable': ['Rohini', 'Mrigashira', 'Punarvasu', 'Pushya', 'Uttara Phalguni',
                                 'Hasta', 'Anuradha', 'Uttara Ashadha', 'Uttara Bhadrapada', 'Revati'],
        'description': 'Griha Pravesh muhurat should have strong 4th house and Moon.',
    },
    'travel': {
        'favorable_months': ['All months except Adhik Maas'],
        'favorable_tithis': ['2', '3', '5', '7', '10', '11', '12'],
        'favorable_days': ['Wednesday', 'Thursday', 'Friday'],
        'avoid_tithis': ['4', '8', '9', '14', 'Amavasya'],
        'avoid_days': ['Tuesday', 'Saturday'],
        'nakshatra_favorable': ['Ashwini', 'Rohini', 'Mrigashira', 'Punarvasu', 'Hasta',
                                 'Chitra', 'Swati', 'Anuradha', 'Shravana', 'Revati'],
        'description': 'Travel muhurat should have strong 3rd house and favorable Moon nakshatra.',
    },
    'education': {
        'favorable_months': ['June', 'July', 'January', 'February'],
        'favorable_tithis': ['2', '5', '6', '7', '10', '11', '12'],
        'favorable_days': ['Wednesday', 'Thursday'],
        'avoid_tithis': ['4', '8', '9', '14', 'Amavasya'],
        'avoid_days': ['Saturday', 'Sunday'],
        'nakshatra_favorable': ['Rohini', 'Mrigashira', 'Punarvasu', 'Ashlesha', 'Hasta',
                                 'Chitra', 'Swati', 'Anuradha', 'Uttara Ashadha', 'Revati'],
        'description': 'Vidyarambha muhurat requires strong Mercury and Jupiter, 5th house favorable.',
    },
}

UPCOMING_DAYS_FAVORABLE = {
    'Monday': 'Moon — good for emotional and nurturing activities',
    'Wednesday': 'Mercury — ideal for business, learning, communication',
    'Thursday': 'Jupiter — best for new beginnings, marriage, education',
    'Friday': 'Venus — favorable for arts, marriage, luxury, relationships',
}


def get_muhurat_analysis(chart_json: str, event_type: str = 'general') -> str:
    try:
        chart = json.loads(chart_json)
        planets = chart.get('planets', {})
        
        event_type = event_type.lower().strip()
        muhurat_info = MUHURAT_TYPES.get(event_type, MUHURAT_TYPES['business'])
        
        # Get current month recommendation
        now = datetime.now()
        current_month = now.strftime('%B')
        current_favorable = current_month in muhurat_info['favorable_months']
        
        # Build upcoming favorable dates (next 30 days)
        upcoming_dates = []
        for i in range(1, 31):
            day = now + timedelta(days=i)
            day_name = day.strftime('%A')
            if day_name in muhurat_info['favorable_days']:
                upcoming_dates.append({
                    'date': day.strftime('%d %b %Y'),
                    'day': day_name,
                    'planet': UPCOMING_DAYS_FAVORABLE.get(day_name, ''),
                })
        
        # Chart-based personalization
        ascendant = chart.get('ascendant', {})
        asc_sign = ascendant.get('sign', 'Aries') if isinstance(ascendant, dict) else 'Aries'
        
        jupiter = planets.get('Jupiter', {})
        jup_sign = jupiter.get('sign', '') if isinstance(jupiter, dict) else ''
        venus = planets.get('Venus', {})
        venus_sign = venus.get('sign', '') if isinstance(venus, dict) else ''
        
        personal_tips = [muhurat_info['description']]
        if event_type == 'marriage':
            if jup_sign in ['Cancer', 'Sagittarius', 'Pisces']:
                personal_tips.append(f'Your Jupiter in {jup_sign} is strong — very favorable for marriage.')
            if venus_sign in ['Taurus', 'Libra', 'Pisces']:
                personal_tips.append(f'Your Venus in {venus_sign} is strong — marriage prospects are excellent.')
        elif event_type == 'business':
            mercury = planets.get('Mercury', {})
            if isinstance(mercury, dict) and mercury.get('sign', '') in ['Gemini', 'Virgo']:
                personal_tips.append('Your Mercury is strong — excellent for business/communication launches.')
        
        return json.dumps({
            'success': True,
            'event_type': event_type,
            'current_month_favorable': current_favorable,
            'current_month': current_month,
            'favorable_days': muhurat_info['favorable_days'],
            'favorable_days_detail': {d: UPCOMING_DAYS_FAVORABLE[d] for d in muhurat_info['favorable_days'] if d in UPCOMING_DAYS_FAVORABLE},
            'favorable_tithis': muhurat_info['favorable_tithis'],
            'avoid_days': muhurat_info['avoid_days'],
            'avoid_tithis': muhurat_info['avoid_tithis'],
            'favorable_nakshatras': muhurat_info['nakshatra_favorable'],
            'upcoming_dates': upcoming_dates[:8],
            'personal_tips': personal_tips,
            'ascendant_sign': asc_sign,
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
