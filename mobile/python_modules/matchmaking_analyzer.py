"""Matchmaking/Compatibility Analysis Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati',
]

NAKSHATRA_LORDS = {
    'Ashwini': 'Ketu', 'Bharani': 'Venus', 'Krittika': 'Sun', 'Rohini': 'Moon',
    'Mrigashira': 'Mars', 'Ardra': 'Rahu', 'Punarvasu': 'Jupiter', 'Pushya': 'Saturn',
    'Ashlesha': 'Mercury', 'Magha': 'Ketu', 'Purva Phalguni': 'Venus', 'Uttara Phalguni': 'Sun',
    'Hasta': 'Moon', 'Chitra': 'Mars', 'Swati': 'Rahu', 'Vishakha': 'Jupiter',
    'Anuradha': 'Saturn', 'Jyeshtha': 'Mercury', 'Mula': 'Ketu', 'Purva Ashadha': 'Venus',
    'Uttara Ashadha': 'Sun', 'Shravana': 'Moon', 'Dhanishtha': 'Mars', 'Shatabhisha': 'Rahu',
    'Purva Bhadrapada': 'Jupiter', 'Uttara Bhadrapada': 'Saturn', 'Revati': 'Mercury',
}

KUTA_TABLE = {
    # Varna (1), Vashya (2), Tara (3), Yoni (4), Graha Maitri (5),
    # Gana (6), Bhakoot (7), Nadi (8) — total 36
    'compatibility_matrix': {
        ('Aries', 'Leo'): 30, ('Aries', 'Sagittarius'): 28, ('Aries', 'Aquarius'): 26,
        ('Taurus', 'Virgo'): 30, ('Taurus', 'Capricorn'): 28, ('Taurus', 'Cancer'): 26,
        ('Gemini', 'Libra'): 30, ('Gemini', 'Aquarius'): 28, ('Gemini', 'Aries'): 24,
        ('Cancer', 'Scorpio'): 30, ('Cancer', 'Pisces'): 28, ('Cancer', 'Taurus'): 26,
        ('Leo', 'Aries'): 30, ('Leo', 'Sagittarius'): 28, ('Leo', 'Gemini'): 24,
        ('Virgo', 'Taurus'): 30, ('Virgo', 'Capricorn'): 28, ('Virgo', 'Cancer'): 24,
        ('Libra', 'Gemini'): 30, ('Libra', 'Aquarius'): 28, ('Libra', 'Leo'): 24,
        ('Scorpio', 'Cancer'): 30, ('Scorpio', 'Pisces'): 28, ('Scorpio', 'Virgo'): 26,
        ('Sagittarius', 'Aries'): 30, ('Sagittarius', 'Leo'): 28, ('Sagittarius', 'Libra'): 24,
        ('Capricorn', 'Taurus'): 30, ('Capricorn', 'Virgo'): 28, ('Capricorn', 'Scorpio'): 26,
        ('Aquarius', 'Gemini'): 30, ('Aquarius', 'Libra'): 28, ('Aquarius', 'Aries'): 22,
        ('Pisces', 'Cancer'): 30, ('Pisces', 'Scorpio'): 28, ('Pisces', 'Capricorn'): 24,
    }
}


def _get_moon_sign(chart):
    planets = chart.get('planets', {})
    moon = planets.get('Moon', {})
    if isinstance(moon, dict):
        return moon.get('sign', 'Aries')
    return 'Aries'


def analyze_compatibility(chart_a_json: str, chart_b_json: str) -> str:
    try:
        chart_a = json.loads(chart_a_json)
        chart_b = json.loads(chart_b_json)

        moon_a = _get_moon_sign(chart_a)
        moon_b = _get_moon_sign(chart_b)

        asc_a = chart_a.get('ascendant', {})
        asc_b = chart_b.get('ascendant', {})
        asc_sign_a = asc_a.get('sign', 'Aries') if isinstance(asc_a, dict) else 'Aries'
        asc_sign_b = asc_b.get('sign', 'Aries') if isinstance(asc_b, dict) else 'Aries'

        # Gunas based on moon signs
        pair = (moon_a, moon_b)
        pair_rev = (moon_b, moon_a)
        gunas = KUTA_TABLE['compatibility_matrix'].get(pair,
                KUTA_TABLE['compatibility_matrix'].get(pair_rev, 18))

        # Ascendant compatibility bonus
        if asc_sign_a == asc_sign_b:
            gunas = min(36, gunas + 2)
        elif (SIGNS.index(asc_sign_b) - SIGNS.index(asc_sign_a)) % 12 == 6:
            gunas = max(0, gunas - 3)

        # Category
        if gunas >= 28:
            category = 'Excellent Match'
            verdict = '⭐⭐⭐⭐⭐ Very highly compatible — blessed union'
        elif gunas >= 24:
            category = 'Very Good Match'
            verdict = '⭐⭐⭐⭐ Good compatibility — harmonious partnership'
        elif gunas >= 18:
            category = 'Good Match'
            verdict = '⭐⭐⭐ Average compatibility — workable with effort'
        elif gunas >= 12:
            category = 'Acceptable Match'
            verdict = '⭐⭐ Below average — differences need management'
        else:
            category = 'Challenging Match'
            verdict = '⭐ Low compatibility — significant challenges'

        strengths = []
        challenges = []

        if gunas >= 24:
            strengths.append(f'Strong Moon sign harmony ({moon_a} ↔ {moon_b})')
            strengths.append('Emotional bonding and mutual understanding')
        if asc_sign_a == asc_sign_b:
            strengths.append('Same ascendant — similar life outlook')
        elif (SIGNS.index(asc_sign_b) - SIGNS.index(asc_sign_a)) % 12 in [4, 8]:
            challenges.append('Trine ascendants — need compromise on goals')

        if not strengths:
            strengths.append('Complementary qualities that can build strength')
        if not challenges:
            challenges.append('Minor differences in habits — manageable')

        remedies = [
            'Perform Satyanarayan Katha together before marriage',
            'Both should worship Shiva-Parvati on Mondays',
            'Consult a Jyotishi for full Ashtakuta matching analysis',
        ]

        return json.dumps({
            'success': True,
            'gunas': gunas,
            'max_gunas': 36,
            'percentage': round(gunas / 36 * 100),
            'category': category,
            'verdict': verdict,
            'moon_sign_a': moon_a,
            'moon_sign_b': moon_b,
            'ascendant_a': asc_sign_a,
            'ascendant_b': asc_sign_b,
            'strengths': strengths,
            'challenges': challenges,
            'remedies': remedies,
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
