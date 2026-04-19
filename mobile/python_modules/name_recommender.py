"""Name Recommendation Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Nakshatra starting syllables (traditional Vedic)
NAKSHATRA_TO_SYLLABLES = {
    'Ashwini': ['Chu', 'Che', 'Cho', 'La'],
    'Bharani': ['Li', 'Lu', 'Le', 'Lo'],
    'Krittika': ['A', 'E', 'U', 'Ea'],
    'Rohini': ['O', 'Va', 'Vi', 'Vu'],
    'Mrigashira': ['Ve', 'Vo', 'Ka', 'Ki'],
    'Ardra': ['Ku', 'Gha', 'Ing', 'Na'],
    'Punarvasu': ['Ke', 'Ko', 'Ha', 'Hi'],
    'Pushya': ['Hu', 'He', 'Ho', 'Da'],
    'Ashlesha': ['Di', 'Du', 'De', 'Do'],
    'Magha': ['Ma', 'Mi', 'Mu', 'Me'],
    'Purva Phalguni': ['Mo', 'Ta', 'Ti', 'Tu'],
    'Uttara Phalguni': ['Te', 'To', 'Pa', 'Pi'],
    'Hasta': ['Pu', 'Sha', 'Na', 'Tha'],
    'Chitra': ['Pe', 'Po', 'Ra', 'Ri'],
    'Swati': ['Ru', 'Re', 'Ro', 'Ta'],
    'Vishakha': ['Ti', 'Tu', 'Te', 'To'],
    'Anuradha': ['Na', 'Ni', 'Nu', 'Ne'],
    'Jyeshtha': ['No', 'Ya', 'Yi', 'Yu'],
    'Mula': ['Ye', 'Yo', 'Bha', 'Bhi'],
    'Purva Ashadha': ['Bhu', 'Dha', 'Bha', 'Dha'],
    'Uttara Ashadha': ['Be', 'Bo', 'Ja', 'Ji'],
    'Shravana': ['Ju', 'Je', 'Jo', 'Sha'],
    'Dhanishtha': ['Ga', 'Gi', 'Gu', 'Ge'],
    'Shatabhisha': ['Go', 'Sa', 'Si', 'Su'],
    'Purva Bhadrapada': ['Se', 'So', 'Da', 'Di'],
    'Uttara Bhadrapada': ['Du', 'Tha', 'Jha', 'Da'],
    'Revati': ['De', 'Do', 'Cha', 'Chi'],
}

NAKSHATRA_LORDS = {
    'Ashwini': 'Ketu', 'Bharani': 'Venus', 'Krittika': 'Sun', 'Rohini': 'Moon',
    'Mrigashira': 'Mars', 'Ardra': 'Rahu', 'Punarvasu': 'Jupiter', 'Pushya': 'Saturn',
    'Ashlesha': 'Mercury', 'Magha': 'Ketu', 'Purva Phalguni': 'Venus', 'Uttara Phalguni': 'Sun',
    'Hasta': 'Moon', 'Chitra': 'Mars', 'Swati': 'Rahu', 'Vishakha': 'Jupiter',
    'Anuradha': 'Saturn', 'Jyeshtha': 'Mercury', 'Mula': 'Ketu', 'Purva Ashadha': 'Venus',
    'Uttara Ashadha': 'Sun', 'Shravana': 'Moon', 'Dhanishtha': 'Mars', 'Shatabhisha': 'Rahu',
    'Purva Bhadrapada': 'Jupiter', 'Uttara Bhadrapada': 'Saturn', 'Revati': 'Mercury',
}

PLANET_QUALITIES = {
    'Sun': 'leadership, authority, vitality, confidence',
    'Moon': 'nurturing, emotional sensitivity, intuition, grace',
    'Mars': 'courage, energy, drive, protection',
    'Mercury': 'intelligence, communication, wit, adaptability',
    'Jupiter': 'wisdom, prosperity, spirituality, optimism',
    'Venus': 'beauty, love, creativity, charm',
    'Saturn': 'discipline, perseverance, karma, endurance',
    'Rahu': 'innovation, ambition, uniqueness, technology',
    'Ketu': 'spirituality, research, liberation, mysticism',
}

# Sample name suggestions per nakshatra lord (inspirational)
LORD_NAME_THEMES = {
    'Sun': {'male': ['Arjun', 'Aditya', 'Surya', 'Tejas', 'Ravi', 'Deva', 'Aarav', 'Kiran'],
            'female': ['Aditi', 'Surya', 'Tejasvi', 'Ravi', 'Kiranmala', 'Subha', 'Arunima', 'Prabhavati']},
    'Moon': {'male': ['Chandra', 'Shashi', 'Inder', 'Milind', 'Himanshu', 'Nikhil', 'Shivam', 'Om'],
             'female': ['Chandra', 'Shashi', 'Indu', 'Nisha', 'Shivani', 'Priya', 'Nandini', 'Sarita']},
    'Mars': {'male': ['Veer', 'Vijay', 'Mangal', 'Kiran', 'Arjun', 'Dhruv', 'Laksh', 'Ranbir'],
             'female': ['Veera', 'Vijaya', 'Mangala', 'Durga', 'Shakti', 'Gargi', 'Lalita', 'Kiran']},
    'Mercury': {'male': ['Budh', 'Vivek', 'Varad', 'Gyan', 'Tarun', 'Pranav', 'Dev', 'Siddharth'],
                'female': ['Vidya', 'Viveka', 'Prajna', 'Gyanavi', 'Taruna', 'Devika', 'Shruti', 'Medhavi']},
    'Jupiter': {'male': ['Guru', 'Brij', 'Anand', 'Mangesh', 'Dev', 'Dharm', 'Nitesh', 'Parmanand'],
                'female': ['Guru', 'Brinda', 'Anandi', 'Devika', 'Dharma', 'Niti', 'Poornam', 'Ananya']},
    'Venus': {'male': ['Shukra', 'Mohit', 'Prem', 'Kamal', 'Rajan', 'Sudhir', 'Madhav', 'Subham'],
              'female': ['Shukra', 'Madhuri', 'Premi', 'Kamala', 'Rajni', 'Sudhira', 'Madhavi', 'Lalitha']},
    'Saturn': {'male': ['Shani', 'Karm', 'Dhruv', 'Narendra', 'Sthir', 'Mohan', 'Nitesh', 'Amrit'],
               'female': ['Shani', 'Karma', 'Dhruva', 'Nari', 'Sthira', 'Mridula', 'Amrita', 'Nirmala']},
    'Rahu': {'male': ['Rahul', 'Vihan', 'Dev', 'Parth', 'Vikram', 'Advait', 'Ayan', 'Kabir'],
             'female': ['Rahul', 'Vihana', 'Devika', 'Partha', 'Vikrama', 'Advaita', 'Aayana', 'Kabira']},
    'Ketu': {'male': ['Kedar', 'Kiran', 'Mohan', 'Atma', 'Bodh', 'Anand', 'Tapas', 'Vyas'],
             'female': ['Ketaki', 'Kirnamayi', 'Atmaja', 'Bodhi', 'Ananda', 'Tapasya', 'Veda', 'Moksha']},
}


def get_name_recommendations(chart_json: str, gender: str = 'male') -> str:
    try:
        chart = json.loads(chart_json)
        planets = chart.get('planets', {})
        
        # Get Moon's nakshatra for primary syllable
        moon = planets.get('Moon', {})
        moon_sign = moon.get('sign', 'Aries') if isinstance(moon, dict) else 'Aries'
        moon_long = moon.get('longitude', 0) if isinstance(moon, dict) else 0
        
        # Calculate nakshatra from Moon longitude (27 nakshatras, each 13.333°)
        nakshatra_num = int(float(moon_long) / (360 / 27)) % 27
        nakshatra_names = list(NAKSHATRA_TO_SYLLABLES.keys())
        moon_nakshatra = nakshatra_names[nakshatra_num] if nakshatra_num < len(nakshatra_names) else 'Rohini'
        
        syllables = NAKSHATRA_TO_SYLLABLES.get(moon_nakshatra, ['A', 'Vi', 'Ka', 'Sa'])
        nakshatra_lord = NAKSHATRA_LORDS.get(moon_nakshatra, 'Moon')
        planet_qualities = PLANET_QUALITIES.get(nakshatra_lord, '')
        
        # Name suggestions based on lord
        gender_key = 'male' if gender == 'male' else 'female'
        suggested_names = LORD_NAME_THEMES.get(nakshatra_lord, LORD_NAME_THEMES['Moon'])[gender_key]
        
        # Filter names by starting syllable if possible
        syllable_based = []
        for syl in syllables:
            matches = [n for n in suggested_names if n.upper().startswith(syl.upper()[:2])]
            for m in matches:
                if m not in syllable_based:
                    syllable_based.append(m)
        
        if not syllable_based:
            syllable_based = suggested_names[:3]
        
        # Ascendant-based secondary suggestions
        ascendant = chart.get('ascendant', {})
        asc_sign = ascendant.get('sign', 'Aries') if isinstance(ascendant, dict) else 'Aries'
        
        # Numerology complement (sum of birth digits)
        lucky_letters = syllables[:2]
        
        return json.dumps({
            'success': True,
            'moon_nakshatra': moon_nakshatra,
            'moon_sign': moon_sign,
            'nakshatra_lord': nakshatra_lord,
            'planet_qualities': planet_qualities,
            'traditional_syllables': syllables,
            'recommended_starting_letters': lucky_letters,
            'name_suggestions': syllable_based[:6] if syllable_based else suggested_names[:6],
            'additional_names': suggested_names[:8],
            'naming_guidance': [
                f'Names starting with {syllables[0]} or {syllables[1]} are most auspicious for this nakshatra',
                f'The ruling planet {nakshatra_lord} bestows qualities of {planet_qualities}',
                f'Names with meanings related to {planet_qualities.split(",")[0]} are favorable',
                'Avoid names with harsh consonants; prefer melodious, flowing sounds',
                'The name should feel natural and not forced when called aloud',
            ],
            'ascendant_sign': asc_sign,
            'traditional_note': 'In Vedic tradition, the name (Namakarana) is given by the family Jyotishi based on the birth nakshatra pada on the 11th or 12th day after birth.',
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
