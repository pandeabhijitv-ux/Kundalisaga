"""Varshaphal (Solar Return) Analysis Entry Point for Chaquopy"""
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SIGN_ELEMENTS = {
    'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
    'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
    'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
    'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water',
}

HOUSE_THEMES = {
    1: 'Self, health, personality, new beginnings',
    2: 'Wealth, family, speech, assets',
    3: 'Courage, siblings, communication, short journeys',
    4: 'Home, mother, property, inner peace',
    5: 'Children, creativity, romance, education, speculation',
    6: 'Health challenges, debts, service, enemies',
    7: 'Partnerships, marriage, business, contracts',
    8: 'Transformation, inheritance, hidden matters, longevity',
    9: 'Fortune, spirituality, higher learning, father, travel',
    10: 'Career, status, authority, achievements, public recognition',
    11: 'Gains, aspirations, social networks, elder siblings',
    12: 'Expenses, foreign lands, spirituality, loss, liberation',
}

PLANET_THEMES = {
    'Sun': 'authority, recognition, confidence, leadership, government',
    'Moon': 'emotions, domestic life, mother, public, mental health',
    'Mars': 'energy, courage, property, brothers, disputes, surgery',
    'Mercury': 'communication, trade, intellect, writing, technology',
    'Jupiter': 'wisdom, wealth, children, marriage, education, spirituality',
    'Venus': 'love, luxury, arts, partnerships, vehicles, pleasures',
    'Saturn': 'discipline, delays, hard work, old age, property, karma',
    'Rahu': 'foreign connections, technology, unconventional gains, ambition',
    'Ketu': 'spirituality, detachment, past karma, research, liberation',
}


def analyze_varshaphal(chart_json: str) -> str:
    """
    Simplified Varshaphal (annual chart) analysis based on natal chart.
    Without live ephemeris, we analyze the natal chart as a base
    and project themes for the current year.
    """
    try:
        chart = json.loads(chart_json)
        planets = chart.get('planets', {})
        ascendant = chart.get('ascendant', {})
        
        asc_sign = ascendant.get('sign', 'Aries') if isinstance(ascendant, dict) else 'Aries'
        current_year = datetime.now().year
        
        # Identify strong planets (own sign / exaltation)
        EXALTATION = {'Sun': 'Aries', 'Moon': 'Taurus', 'Mercury': 'Virgo',
                      'Venus': 'Pisces', 'Mars': 'Capricorn', 'Jupiter': 'Cancer', 'Saturn': 'Libra'}
        OWN_SIGNS = {
            'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
            'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
            'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius'],
        }
        
        strong_planets = []
        weak_planets = []
        
        for planet_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p = planets.get(planet_name, {})
            if not isinstance(p, dict):
                continue
            sign = p.get('sign', '')
            if sign == EXALTATION.get(planet_name) or sign in OWN_SIGNS.get(planet_name, []):
                strong_planets.append(planet_name)
            elif sign:
                # Check debilitation (opposite of exaltation)
                exalt_idx = ['Aries', 'Taurus', 'Cancer', 'Virgo', 'Capricorn', 'Pisces', 'Libra'].index(EXALTATION.get(planet_name, 'Aries')) if EXALTATION.get(planet_name) in ['Aries', 'Taurus', 'Cancer', 'Virgo', 'Capricorn', 'Pisces', 'Libra'] else -1
                # Simple debilitation check
                debil = {'Sun': 'Libra', 'Moon': 'Scorpio', 'Mercury': 'Pisces',
                         'Venus': 'Virgo', 'Mars': 'Cancer', 'Jupiter': 'Capricorn', 'Saturn': 'Aries'}
                if sign == debil.get(planet_name):
                    weak_planets.append(planet_name)
        
        # Year themes based on strong planets
        year_highlights = []
        for p in strong_planets[:3]:
            year_highlights.append({
                'planet': p,
                'theme': PLANET_THEMES[p],
                'forecast': f'{p} is strong in your chart — this year brings opportunities in {PLANET_THEMES[p].split(",")[0]}',
            })
        
        if not year_highlights:
            year_highlights.append({
                'planet': 'Jupiter',
                'theme': PLANET_THEMES['Jupiter'],
                'forecast': 'Jupiter influences this year with wisdom, growth, and blessings',
            })
        
        # Areas of focus this year
        focus_areas = []
        for p in strong_planets:
            for planet_data in [planets.get(p, {})]:
                if isinstance(planet_data, dict):
                    house = planet_data.get('house', 0)
                    if house and house in HOUSE_THEMES:
                        focus_areas.append({
                            'house': house,
                            'planet': p,
                            'theme': HOUSE_THEMES[house],
                            'prediction': f'Strong {p} in house {house} highlights: {HOUSE_THEMES[house]}',
                        })
        
        if not focus_areas:
            focus_areas.append({
                'house': 1,
                'planet': 'Ascendant',
                'theme': HOUSE_THEMES[1],
                'prediction': 'This is a year for personal growth and new beginnings',
            })
        
        # Challenges
        challenges = []
        for p in weak_planets:
            p_data = planets.get(p, {})
            if isinstance(p_data, dict):
                house = p_data.get('house', 0)
                if house:
                    challenges.append(f'Weak {p} in house {house} — be cautious with {HOUSE_THEMES.get(house, "related matters")}')
        
        if not challenges:
            challenges.append('No major planetary challenges identified. Focus on consistent effort.')
        
        # Remedies
        remedies = []
        if weak_planets:
            for p in weak_planets[:2]:
                if p == 'Sun':
                    remedies.append('Offer water to rising Sun; chant Aditya Hridayam on Sundays')
                elif p == 'Moon':
                    remedies.append('Offer white flowers to Shiva; chant Om Namah Shivaya on Mondays')
                elif p == 'Mars':
                    remedies.append('Donate red lentils on Tuesdays; chant Hanuman Chalisa')
                elif p == 'Mercury':
                    remedies.append('Feed green grass to cows; worship Lord Ganesha on Wednesdays')
                elif p == 'Jupiter':
                    remedies.append('Donate yellow items on Thursdays; chant Brihaspati Stotram')
                elif p == 'Venus':
                    remedies.append('Offer white flowers on Fridays; worship Lakshmi Devi')
                elif p == 'Saturn':
                    remedies.append('Light sesame oil lamp on Saturdays; help the elderly')
        else:
            remedies.append('Continue your regular spiritual practice to maintain planetary harmony')
            remedies.append('Donate to charity on your birth nakshatra day each month')
        
        return json.dumps({
            'success': True,
            'year': current_year,
            'ascendant_sign': asc_sign,
            'strong_planets': strong_planets,
            'weak_planets': weak_planets,
            'year_highlights': year_highlights,
            'focus_areas': focus_areas[:4],
            'challenges': challenges[:3],
            'remedies': remedies[:4],
            'overall_forecast': f'Year {current_year} for {asc_sign} ascendant: ' + (
                'Excellent with multiple strong planets supporting your endeavors.' if len(strong_planets) >= 3
                else 'Moderate with balanced planetary influences — steady progress through consistent effort.' if len(strong_planets) >= 1
                else 'Introspective year — focus on spiritual growth and overcoming challenges patiently.'
            ),
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
