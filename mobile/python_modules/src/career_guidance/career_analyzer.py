"""
Career Sector Analyzer
Maps planetary positions and strengths to business/career sectors
"""

from typing import Dict, List, Tuple
try:
    import swisseph as swe
    HAS_SWE = True
except ImportError:
    HAS_SWE = False
from datetime import datetime


class CareerAnalyzer:
    """Analyzes birth chart for career and business sector recommendations"""
    
    # Sector to Planet mapping with weightage
    SECTOR_MAPPINGS = {
        'IT & Technology': {
            'planets': ['Mercury', 'Rahu'],
            'houses': [3, 10],  # Communication, Career
            'description': 'Software, IT Services, Tech Startups, Digital Marketing'
        },
        'Finance & Banking': {
            'planets': ['Jupiter', 'Venus', 'Mercury'],
            'houses': [2, 11],  # Wealth, Gains
            'description': 'Banking, Investment, Stock Market, Financial Services, Accounting'
        },
        'Real Estate & Construction': {
            'planets': ['Mars', 'Saturn'],
            'houses': [4, 10],  # Property, Career
            'description': 'Real Estate, Construction, Architecture, Property Development'
        },
        'Engineering & Manufacturing': {
            'planets': ['Mars', 'Saturn'],
            'houses': [6, 10],  # Service, Career
            'description': 'Mechanical, Civil, Electrical Engineering, Manufacturing'
        },
        'Healthcare & Pharmaceuticals': {
            'planets': ['Moon', 'Jupiter', 'Sun'],
            'houses': [6, 8],  # Health, Research
            'description': 'Medicine, Pharmacy, Healthcare Services, Medical Devices'
        },
        'Education & Training': {
            'planets': ['Jupiter', 'Mercury'],
            'houses': [5, 9],  # Knowledge, Higher Learning
            'description': 'Teaching, Coaching, EdTech, Research, Publishing'
        },
        'Arts & Entertainment': {
            'planets': ['Venus', 'Moon'],
            'houses': [5, 3],  # Creativity, Media
            'description': 'Film, Music, Fashion, Design, Advertising, Media'
        },
        'Government & Administration': {
            'planets': ['Sun', 'Saturn'],
            'houses': [10, 6],  # Authority, Service
            'description': 'Civil Services, Public Administration, Politics, Law'
        },
        'Agriculture & Food': {
            'planets': ['Saturn', 'Moon', 'Venus'],
            'houses': [4, 12],  # Land, Expenses
            'description': 'Farming, Food Processing, Organic Products, Agribusiness'
        },
        'Consulting & Advisory': {
            'planets': ['Jupiter', 'Mercury'],
            'houses': [9, 10],  # Wisdom, Career
            'description': 'Business Consulting, Legal Services, Financial Advisory'
        },
        'Trade & Commerce': {
            'planets': ['Mercury', 'Venus'],
            'houses': [2, 3, 7],  # Wealth, Communication, Partnership
            'description': 'Import-Export, E-commerce, Retail, Distribution'
        },
        'Energy & Mining': {
            'planets': ['Sun', 'Mars'],
            'houses': [8, 12],  # Hidden Resources
            'description': 'Oil & Gas, Mining, Renewable Energy, Power Generation'
        },
        'Hospitality & Tourism': {
            'planets': ['Venus', 'Moon'],
            'houses': [4, 9, 12],  # Comfort, Travel, Foreign
            'description': 'Hotels, Restaurants, Travel, Event Management'
        },
        'Sports & Fitness': {
            'planets': ['Mars', 'Sun'],
            'houses': [1, 5],  # Physical Body, Competition
            'description': 'Professional Sports, Fitness Centers, Sports Equipment'
        },
        'Spiritual & Religious': {
            'planets': ['Jupiter', 'Ketu'],
            'houses': [9, 12],  # Dharma, Liberation
            'description': 'Spiritual Teaching, Temple Management, Yoga, Meditation'
        }
    }
    
    PLANET_NAMES = {
        0: 'Sun', 1: 'Moon', 2: 'Mercury', 3: 'Venus',
        4: 'Mars', 5: 'Jupiter', 6: 'Saturn',
        10: 'Rahu', 11: 'Ketu'
    }
    
    def __init__(self):
        """Initialize career analyzer"""
        pass
    
    def analyze_career_sectors(self, chart_data: Dict) -> Dict:
        """
        Analyze birth chart and recommend suitable business/career sectors
        
        Args:
            chart_data: Birth chart data with planetary positions
            
        Returns:
            Dictionary with sector recommendations and analysis
        """
        try:
            # Extract key houses and planets
            houses = chart_data.get('house_cusps', {})
            planets = chart_data.get('planets', {})
            
            # Analyze key career houses
            tenth_house = self._analyze_house(houses, planets, 10)  # Career
            second_house = self._analyze_house(houses, planets, 2)   # Wealth
            ascendant = self._analyze_house(houses, planets, 1)      # Personality
            
            # Calculate planetary strengths
            planet_strengths = self._calculate_planet_strengths(planets)
            
            # Score each sector
            sector_scores = self._score_sectors(
                planet_strengths,
                tenth_house,
                second_house,
                houses
            )
            
            # Get top recommendations
            top_sectors = sorted(
                sector_scores.items(),
                key=lambda x: x[1]['score'],
                reverse=True
            )[:5]
            
            # Generate detailed recommendations
            recommendations = self._generate_recommendations(
                top_sectors,
                planet_strengths,
                tenth_house,
                second_house
            )
            
            return {
                'success': True,
                'recommendations': recommendations,
                'planetary_strengths': planet_strengths,
                'key_indicators': {
                    'career_house': tenth_house,
                    'wealth_house': second_house,
                    'ascendant': ascendant
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'recommendations': []
            }
    
    def _analyze_house(self, houses: Dict, planets: Dict, house_num: int) -> Dict:
        """Analyze a specific house for career indicators"""
        house_info = {
            'number': house_num,
            'sign': None,
            'lord': None,
            'planets_in_house': [],
            'strength': 0
        }
        
        try:
            # Get house cusp
            if str(house_num) in houses:
                house_cusp = houses[str(house_num)]
                house_info['sign'] = self._get_sign(house_cusp)
                house_info['lord'] = self._get_house_lord(house_info['sign'])
            
            # Find planets in this house
            for planet_name, planet_data in planets.items():
                if planet_name == 'Ascendant':
                    continue
                    
                # Handle both object and dict formats
                if hasattr(planet_data, 'house'):
                    planet_house = planet_data.house
                elif isinstance(planet_data, dict):
                    planet_house = planet_data.get('house')
                else:
                    continue
                
                if planet_house == house_num:
                    house_info['planets_in_house'].append(planet_name)
            
            # Calculate strength
            house_info['strength'] = len(house_info['planets_in_house']) * 20
            
        except Exception:
            pass
        
        return house_info
    
    def _get_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude"""
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        sign_num = int(longitude / 30)
        return signs[sign_num % 12]
    
    def _get_house_lord(self, sign: str) -> str:
        """Get ruling planet of a sign"""
        lords = {
            'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
            'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
            'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
            'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
        }
        return lords.get(sign, 'Unknown')
    
    def _calculate_planet_strengths(self, planets: Dict) -> Dict:
        """Calculate strength of each planet"""
        strengths = {}
        
        for planet_name, planet_data in planets.items():
            # Skip Ascendant as it's not a planet
            if planet_name == 'Ascendant':
                continue
            
            strength = 0
            
            # Get planet attributes (handle both object and dict formats)
            if hasattr(planet_data, 'sign'):
                sign = planet_data.sign
                degree = planet_data.degree_in_sign
                is_retrograde = planet_data.is_retrograde
            elif isinstance(planet_data, dict):
                sign = planet_data.get('sign', '')
                degree = planet_data.get('degree_in_sign', 0)
                is_retrograde = planet_data.get('is_retrograde', False)
            else:
                continue
            
            # Sign strength (exaltation, own sign, etc.)
            strength += self._get_sign_strength(planet_name, sign)
            
            # Degree strength
            if 5 < degree < 25:  # Middle degrees are stronger
                strength += 20
            
            # Retrograde consideration
            if is_retrograde:
                strength += 10  # Retrograde planets have special significance
            
            strengths[planet_name] = min(strength, 100)  # Cap at 100
        
        return strengths
    
    def _get_sign_strength(self, planet: str, sign: str) -> int:
        """Get planet strength in a particular sign"""
        # Exaltation signs
        exaltation = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mercury': 'Virgo',
            'Venus': 'Pisces', 'Mars': 'Capricorn', 'Jupiter': 'Cancer',
            'Saturn': 'Libra'
        }
        
        # Own signs
        own_signs = {
            'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
            'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
            'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius']
        }
        
        if sign == exaltation.get(planet):
            return 50
        elif sign in own_signs.get(planet, []):
            return 40
        else:
            return 20
    
    def _score_sectors(self, planet_strengths: Dict, tenth_house: Dict,
                       second_house: Dict, houses: Dict) -> Dict:
        """Score each sector based on planetary strengths and house analysis"""
        sector_scores = {}
        
        for sector, mapping in self.SECTOR_MAPPINGS.items():
            score = 0
            factors = []
            considered_planets = []
            
            # Score based on relevant planets
            for planet in mapping['planets']:
                if planet in planet_strengths:
                    planet_score = planet_strengths[planet]
                    score += planet_score
                    considered_planets.append(planet)
                    factors.append(f"{planet}: {planet_score}/100")
            
            # Bonus for planets in relevant houses
            for house_num in mapping['houses']:
                if house_num == 10:
                    house_planets = tenth_house['planets_in_house']
                elif house_num == 2:
                    house_planets = second_house['planets_in_house']
                else:
                    house_planets = []
                
                for planet in house_planets:
                    if planet in mapping['planets']:
                        score += 30
                        factors.append(f"{planet} in House {house_num}")

            max_score = len(mapping['planets']) * 100 + len(mapping['houses']) * 30
            score_percent = round((score / max_score) * 100, 1) if max_score else 0.0
            
            sector_scores[sector] = {
                'score': score,
                'max_score': max_score,
                'score_percent': score_percent,
                'considered_planets': mapping['planets'],
                'considered_planets_count': len(mapping['planets']),
                'factors': factors,
                'description': mapping['description']
            }
        
        return sector_scores
    
    def _generate_recommendations(self, top_sectors: List[Tuple],
                                  planet_strengths: Dict,
                                  tenth_house: Dict,
                                  second_house: Dict) -> List[Dict]:
        """Generate detailed recommendations"""
        recommendations = []
        
        for rank, (sector, data) in enumerate(top_sectors, 1):
            max_score = data.get('max_score', 0)
            score_percent = data.get('score_percent', 0.0)
            
            recommendation = {
                'rank': rank,
                'sector': sector,
                'score': data['score'],
                'max_score': max_score,
                'score_percent': score_percent,
                'description': data['description'],
                'strength': self._get_strength_label(score_percent),
                'considered_planets': data.get('considered_planets', []),
                'considered_planets_count': data.get('considered_planets_count', 0),
                'factors': data['factors'][:3],  # Top 3 factors
                'advice': self._get_sector_advice(sector, data['score'])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_strength_label(self, score_percent: float) -> str:
        """Get strength label based on normalized score percentage"""
        if score_percent >= 80:
            return "Excellent"
        elif score_percent >= 65:
            return "Very Good"
        elif score_percent >= 45:
            return "Good"
        else:
            return "Moderate"
    
    def _get_sector_advice(self, sector: str, score: float) -> str:
        """Get personalized advice for a sector"""
        if score >= 150:
            return f"Highly recommended! Your planetary alignment strongly supports {sector}. This could be your primary career focus."
        elif score >= 100:
            return f"Very favorable! {sector} aligns well with your strengths. Consider this as a major career option."
        elif score >= 60:
            return f"Good potential in {sector}. With proper effort and skill development, this could be rewarding."
        else:
            return f"{sector} shows moderate potential. Consider as a secondary option or side venture."
