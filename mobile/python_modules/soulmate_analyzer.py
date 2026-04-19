"""Soulmate Analysis Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

SIGN_TRAITS = {
    'Aries': {'physical': 'Athletic, sharp features, medium height', 'personality': 'Bold, passionate, independent', 'profession': 'Military, sports, engineering'},
    'Taurus': {'physical': 'Well-built, attractive, charming eyes', 'personality': 'Stable, loving, patient', 'profession': 'Finance, arts, hospitality'},
    'Gemini': {'physical': 'Slim, youthful, expressive', 'personality': 'Witty, communicative, curious', 'profession': 'Media, education, IT'},
    'Cancer': {'physical': 'Round face, medium build, expressive eyes', 'personality': 'Caring, emotional, nurturing', 'profession': 'Healthcare, hospitality, food'},
    'Leo': {'physical': 'Tall, well-groomed, commanding presence', 'personality': 'Confident, generous, ambitious', 'profession': 'Management, politics, arts'},
    'Virgo': {'physical': 'Neat, graceful, intelligent look', 'personality': 'Analytical, helpful, perfectionistic', 'profession': 'Healthcare, analytics, service'},
    'Libra': {'physical': 'Attractive, balanced features, pleasant', 'personality': 'Diplomatic, romantic, fair-minded', 'profession': 'Law, design, arts'},
    'Scorpio': {'physical': 'Intense eyes, magnetic, athletic', 'personality': 'Passionate, mysterious, determined', 'profession': 'Research, psychology, finance'},
    'Sagittarius': {'physical': 'Tall, athletic, joy-filled face', 'personality': 'Optimistic, philosophical, adventurous', 'profession': 'Education, travel, philosophy'},
    'Capricorn': {'physical': 'Strong features, lean, dignified', 'personality': 'Ambitious, disciplined, responsible', 'profession': 'Business, government, engineering'},
    'Aquarius': {'physical': 'Unconventional, modern, expressive', 'personality': 'Unique, humanitarian, independent', 'profession': 'Technology, social work, research'},
    'Pisces': {'physical': 'Soft features, dreamy eyes, graceful', 'personality': 'Compassionate, artistic, intuitive', 'profession': 'Arts, spirituality, healthcare'},
}

TIMING_BY_PLANET = {
    'Venus': {'period': 'Venus mahadasha or antardasha', 'place': 'Social gatherings, parties, cultural events', 'how': 'Through mutual friends or social circle', 'first_impression': 'Attraction at first sight'},
    'Jupiter': {'period': 'Jupiter mahadasha or antardasha', 'place': 'Educational institutions or spiritual places', 'how': 'Through family introduction or auspicious events', 'first_impression': 'Deep intellectual connection'},
    'Mars': {'period': 'Mars mahadasha or antardasha', 'place': 'Sports, gym, competitive events', 'how': 'Sudden or unexpected meeting', 'first_impression': 'Instant chemistry and energy'},
    'Moon': {'period': 'Moon mahadasha or antardasha', 'place': 'Family events or water-related places', 'how': 'Through mother, family, or home connections', 'first_impression': 'Comforting and emotionally familiar'},
    'Mercury': {'period': 'Mercury mahadasha or antardasha', 'place': 'Work, business, or communication-related venue', 'how': 'Through professional or intellectual interaction', 'first_impression': 'Witty and engaging conversation'},
    'Saturn': {'period': 'Saturn mahadasha or antardasha', 'place': 'Work environment or serious settings', 'how': 'Slow and steady development of relationship', 'first_impression': 'Reliable and grounded person'},
    'Sun': {'period': 'Sun mahadasha or antardasha', 'place': 'Prestigious events or government settings', 'how': 'Through father, boss, or authority figure', 'first_impression': 'Impressive and confident personality'},
    'Rahu': {'period': 'Rahu mahadasha or antardasha', 'place': 'Foreign lands, online, unconventional settings', 'how': 'Unexpected or unusual circumstances', 'first_impression': 'Unusual and fascinating connection'},
    'Ketu': {'period': 'Ketu mahadasha or antardasha', 'place': 'Spiritual or isolated settings', 'how': 'Karmic connection from past life', 'first_impression': 'Inexplicable familiarity and bond'},
}

COMPATIBILITY_FACTORS = {
    'Aries': ['Leo', 'Sagittarius', 'Aquarius'],
    'Taurus': ['Virgo', 'Capricorn', 'Cancer'],
    'Gemini': ['Libra', 'Aquarius', 'Aries'],
    'Cancer': ['Scorpio', 'Pisces', 'Taurus'],
    'Leo': ['Aries', 'Sagittarius', 'Gemini'],
    'Virgo': ['Taurus', 'Capricorn', 'Cancer'],
    'Libra': ['Gemini', 'Aquarius', 'Leo'],
    'Scorpio': ['Cancer', 'Pisces', 'Virgo'],
    'Sagittarius': ['Aries', 'Leo', 'Libra'],
    'Capricorn': ['Taurus', 'Virgo', 'Scorpio'],
    'Aquarius': ['Gemini', 'Libra', 'Aries'],
    'Pisces': ['Cancer', 'Scorpio', 'Capricorn'],
}


def analyze_soulmate(chart_json: str, gender: str = 'male') -> str:
    try:
        chart = json.loads(chart_json)
        planets = chart.get('planets', {})
        
        # Get ascendant sign
        asc = chart.get('ascendant', {})
        if isinstance(asc, dict):
            asc_sign = asc.get('sign', 'Aries')
        else:
            asc_sign = 'Aries'
        
        # 7th house sign (opposite ascendant)
        asc_idx = SIGNS.index(asc_sign) if asc_sign in SIGNS else 0
        house_7_sign = SIGNS[(asc_idx + 6) % 12]
        
        # Primary planet for analysis
        def get_planet(name):
            p = planets.get(name, {})
            return p if isinstance(p, dict) else {}
        
        venus = get_planet('Venus')
        mars = get_planet('Mars')
        jupiter = get_planet('Jupiter')
        
        primary = mars if gender == 'male' else venus
        primary_sign = primary.get('sign', house_7_sign)
        
        traits = SIGN_TRAITS.get(primary_sign, SIGN_TRAITS['Libra'])
        h7_traits = SIGN_TRAITS.get(house_7_sign, SIGN_TRAITS['Libra'])
        
        # Physical
        physical = {
            'description': traits['physical'],
            'build': 'Athletic and well-proportioned' if primary_sign in ['Aries', 'Leo', 'Scorpio'] else 'Graceful and balanced',
            'complexion': 'Fair to wheatish' if primary_sign in ['Taurus', 'Libra', 'Pisces', 'Cancer'] else 'Wheatish to dusky',
            'eyes': 'Expressive and attractive',
            'style': 'Well-groomed and presentable',
        }
        
        # Add Jupiter influence
        jup_house = jupiter.get('house', 0)
        if jup_house in [1, 7, 9, 11]:
            physical['build'] = 'Tall and well-built'
        
        # Personality
        personality = {
            'positive_traits': traits['personality'].split(', '),
            '7th_house_influence': h7_traits['personality'],
            'emotional_nature': 'Sensitive and caring' if house_7_sign in ['Cancer', 'Pisces', 'Scorpio'] else 'Balanced and rational',
        }
        
        # Background
        background = {
            'profession': traits['profession'],
            'education': 'Well-educated' if jupiter.get('house') in [1, 2, 4, 5, 9] else 'Practical skills-based',
            'family': 'Good family background' if venus.get('sign') in ['Taurus', 'Libra', 'Pisces'] else 'Self-made individual',
            'financial': 'Financially stable' if jupiter.get('sign') in ['Cancer', 'Sagittarius', 'Pisces'] else 'Working towards stability',
        }
        
        # Meeting Timing
        # Find dasha lord or use Venus/Jupiter
        timing_planet = 'Venus'
        if gender == 'female':
            timing_planet = 'Jupiter'
        timing = TIMING_BY_PLANET[timing_planet]
        
        # Compatibility
        compatible_signs = COMPATIBILITY_FACTORS.get(asc_sign, [])
        compat_list = [
            f'Best compatibility with {sign} ascendants' for sign in compatible_signs
        ]
        compat_list.append(f'Your 7th house in {house_7_sign} indicates a {h7_traits["personality"]} partner')
        
        # Remedies
        remedies = {
            'daily': [
                'Offer water to rising Sun every morning',
                'Chant Om Namah Shivaya 108 times on Mondays',
                'Keep fast on Fridays and offer white flowers to Lakshmi',
            ],
            'special': [
                'Worship Shiva-Parvati together for harmonious marriage',
                'Read Sundarkand on Tuesdays for finding ideal partner',
            ],
        }
        if primary_sign in ['Aries', 'Scorpio']:
            remedies['daily'].append('Chant Hanuman Chalisa daily for courage and right partner')
        
        return json.dumps({
            'success': True,
            'ascendant_sign': asc_sign,
            'seventh_house_sign': house_7_sign,
            'physical': physical,
            'personality': personality,
            'background': background,
            'timing': timing,
            'compatibility': compat_list,
            'remedies': remedies,
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
