"""
Gemstone Recommendation System
Based on Birth Chart Analysis (D1, D2, D9) and Question Context
"""
from typing import Dict, List
from src.utils import logger


class GemstoneRecommender:
    """Recommend gemstones based on chart analysis and specific concerns"""
    
    def __init__(self):
        self.logger = logger
        
        # Planetary gemstones (primary and alternative)
        self.planetary_gemstones = {
            'Sun': {
                'primary': 'Ruby (Manik)',
                'alternative': 'Red Garnet, Red Spinel',
                'weight': '3-7 carats',
                'metal': 'Gold or Copper',
                'finger': 'Ring finger',
                'day': 'Sunday',
                'benefits': 'Leadership, confidence, vitality, father relationships, career authority'
            },
            'Moon': {
                'primary': 'Pearl (Moti)',
                'alternative': 'Moonstone, White Coral',
                'weight': '3-7 carats',
                'metal': 'Silver',
                'finger': 'Little finger',
                'day': 'Monday',
                'benefits': 'Emotional stability, mental peace, mother relationships, intuition'
            },
            'Mars': {
                'primary': 'Red Coral (Moonga)',
                'alternative': 'Carnelian, Red Agate',
                'weight': '5-8 carats',
                'metal': 'Gold, Copper, or Silver',
                'finger': 'Ring finger',
                'day': 'Tuesday',
                'benefits': 'Courage, energy, property matters, siblings, blood-related issues'
            },
            'Mercury': {
                'primary': 'Emerald (Panna)',
                'alternative': 'Green Tourmaline, Peridot',
                'weight': '3-6 carats',
                'metal': 'Gold or Silver',
                'finger': 'Little finger',
                'day': 'Wednesday',
                'benefits': 'Intelligence, communication, business, education, nervous system'
            },
            'Jupiter': {
                'primary': 'Yellow Sapphire (Pukhraj)',
                'alternative': 'Citrine, Yellow Topaz',
                'weight': '3-7 carats',
                'metal': 'Gold',
                'finger': 'Index finger',
                'day': 'Thursday',
                'benefits': 'Wisdom, wealth, children, marriage, spiritual growth, education'
            },
            'Venus': {
                'primary': 'Diamond (Heera)',
                'alternative': 'White Sapphire, Zircon',
                'weight': '1-2 carats (diamond), 3-6 carats (alternative)',
                'metal': 'Silver, White Gold, or Platinum',
                'finger': 'Middle or Little finger',
                'day': 'Friday',
                'benefits': 'Love, marriage, luxury, arts, beauty, relationships, comfort'
            },
            'Saturn': {
                'primary': 'Blue Sapphire (Neelam)',
                'alternative': 'Amethyst, Blue Tourmaline',
                'weight': '3-7 carats',
                'metal': 'Silver, Iron, or Panchdhatu',
                'finger': 'Middle finger',
                'day': 'Saturday',
                'benefits': 'Discipline, longevity, career stability, property, chronic issues',
                'warning': '⚠️ Blue Sapphire must be tested for 7 days before permanent wearing'
            },
            'Rahu': {
                'primary': 'Hessonite Garnet (Gomed)',
                'alternative': 'Brown Zircon',
                'weight': '5-8 carats',
                'metal': 'Silver or Panchdhatu',
                'finger': 'Middle finger',
                'day': 'Saturday',
                'benefits': 'Foreign connections, unconventional success, technology, sudden gains'
            },
            'Ketu': {
                'primary': "Cat's Eye (Lehsunia)",
                'alternative': 'Chrysoberyl',
                'weight': '5-8 carats',
                'metal': 'Silver or Panchdhatu',
                'finger': 'Middle finger',
                'day': 'Tuesday or Thursday',
                'benefits': 'Spirituality, moksha, intuition, hidden knowledge, detachment'
            }
        }
        
        # Question category to relevant planets mapping
        self.concern_planets = {
            'career': ['Sun', 'Saturn', 'Mercury', 'Jupiter'],
            'job': ['Sun', 'Saturn', 'Jupiter', 'Mercury'],
            'business': ['Mercury', 'Jupiter', 'Sun', 'Mars'],
            'wealth': ['Jupiter', 'Venus', 'Mercury', 'Moon'],
            'finance': ['Jupiter', 'Venus', 'Mercury'],
            'money': ['Jupiter', 'Venus', 'Mercury'],
            'marriage': ['Venus', 'Jupiter', 'Moon', 'Mars'],
            'relationship': ['Venus', 'Moon', 'Mars'],
            'love': ['Venus', 'Moon', 'Mars'],
            'spouse': ['Venus', 'Jupiter', 'Mars'],
            'health': ['Sun', 'Moon', 'Mars', 'Saturn'],
            'children': ['Jupiter', 'Sun', 'Moon'],
            'education': ['Mercury', 'Jupiter', 'Sun'],
            'property': ['Mars', 'Saturn', 'Moon'],
            'legal': ['Saturn', 'Sun', 'Mars'],
            'foreign': ['Rahu', 'Jupiter', 'Moon'],
            'spiritual': ['Ketu', 'Jupiter', 'Moon'],
            'promotion': ['Sun', 'Jupiter', 'Saturn']
        }
        
        # Divisional chart focus
        self.chart_relevance = {
            'D1': 'Overall life, personality, general strength',
            'D2': 'Wealth, finances, family assets',
            'D9': 'Marriage, spouse, dharma, spiritual strength'
        }
    
    def get_recommendations(self, question: str, d1_chart: Dict, 
                           d2_chart: Dict = None, d9_chart: Dict = None) -> Dict:
        """
        Get gemstone recommendations based on question and charts
        
        Args:
            question: User's question
            d1_chart: D1 (Rashi) chart data
            d2_chart: D2 (Hora) chart data (optional)
            d9_chart: D9 (Navamsa) chart data (optional)
        
        Returns:
            Dict with gemstone recommendations
        """
        self.logger.info(f"Generating gemstone recommendations for: {question}")
        
        # Identify relevant planets based on question
        relevant_planets = self._identify_relevant_planets(question)
        
        # Analyze D1 chart (primary analysis)
        d1_analysis = self._analyze_chart(d1_chart, 'D1')
        weak_planets_d1 = d1_analysis['weak_planets']
        strong_planets_d1 = d1_analysis['strong_planets']
        
        # Analyze D2 chart if available (wealth/finance questions)
        weak_planets_d2 = []
        if d2_chart and any(word in question.lower() for word in ['wealth', 'money', 'finance', 'business']):
            d2_analysis = self._analyze_chart(d2_chart, 'D2')
            weak_planets_d2 = d2_analysis['weak_planets']
        
        # Analyze D9 chart if available (marriage/relationship questions)
        weak_planets_d9 = []
        if d9_chart and any(word in question.lower() for word in ['marriage', 'spouse', 'relationship', 'love']):
            d9_analysis = self._analyze_chart(d9_chart, 'D9')
            weak_planets_d9 = d9_analysis['weak_planets']
        
        # Priority 1: Weak planets that are relevant to the question
        primary_recommendations = []
        for planet in relevant_planets:
            if planet in weak_planets_d1:
                primary_recommendations.append({
                    'planet': planet,
                    'priority': 'High',
                    'reason': f'{planet} is weak in your D1 chart and directly relevant to {self._get_question_category(question)}',
                    'chart_basis': 'D1 (Primary)',
                    **self.planetary_gemstones[planet]
                })
        
        # Priority 2: Weak planets in divisional charts relevant to question
        secondary_recommendations = []
        
        if weak_planets_d2:
            for planet in weak_planets_d2:
                if planet in relevant_planets and planet not in [r['planet'] for r in primary_recommendations]:
                    secondary_recommendations.append({
                        'planet': planet,
                        'priority': 'Medium',
                        'reason': f'{planet} is weak in D2 (Wealth chart), affecting financial prosperity',
                        'chart_basis': 'D2 (Hora/Wealth)',
                        **self.planetary_gemstones[planet]
                    })
        
        if weak_planets_d9:
            for planet in weak_planets_d9:
                if planet in relevant_planets and planet not in [r['planet'] for r in primary_recommendations]:
                    secondary_recommendations.append({
                        'planet': planet,
                        'priority': 'Medium',
                        'reason': f'{planet} is weak in D9 (Marriage chart), affecting relationships',
                        'chart_basis': 'D9 (Navamsa)',
                        **self.planetary_gemstones[planet]
                    })
        
        # Priority 3: Supporting gemstones (strong planets to maintain strength)
        supporting_recommendations = []
        for planet in relevant_planets:
            if planet in strong_planets_d1 and planet not in [r['planet'] for r in primary_recommendations + secondary_recommendations]:
                supporting_recommendations.append({
                    'planet': planet,
                    'priority': 'Low (Optional)',
                    'reason': f'{planet} is strong but can be enhanced for maximum benefits',
                    'chart_basis': 'D1 (Support)',
                    **self.planetary_gemstones[planet]
                })
        
        return {
            'question_category': self._get_question_category(question),
            'relevant_planets': relevant_planets,
            'primary_recommendations': primary_recommendations[:2],  # Top 2
            'secondary_recommendations': secondary_recommendations[:2],
            'supporting_recommendations': supporting_recommendations[:1],
            'general_guidelines': self._get_wearing_guidelines(),
            'charts_analyzed': {
                'D1': True,
                'D2': d2_chart is not None,
                'D9': d9_chart is not None
            }
        }
    
    def _identify_relevant_planets(self, question: str) -> List[str]:
        """Identify which planets are relevant based on the question"""
        question_lower = question.lower()
        relevant = []
        
        for concern, planets in self.concern_planets.items():
            if concern in question_lower:
                relevant.extend(planets)
        
        # Remove duplicates while preserving order
        seen = set()
        return [p for p in relevant if not (p in seen or seen.add(p))]
    
    def _get_question_category(self, question: str) -> str:
        """Get the primary category of the question"""
        question_lower = question.lower()
        
        for concern in self.concern_planets.keys():
            if concern in question_lower:
                return concern.title()
        
        return "General Life"
    
    def _analyze_chart(self, chart_data: Dict, chart_type: str) -> Dict:
        """
        Analyze chart to identify weak and strong planets
        
        Args:
            chart_data: Chart data
            chart_type: 'D1', 'D2', or 'D9'
        
        Returns:
            Dict with weak_planets and strong_planets lists
        """
        weak_planets = []
        strong_planets = []
        
        if not chart_data or 'planets' not in chart_data:
            return {'weak_planets': [], 'strong_planets': []}
        
        planets = chart_data['planets']
        
        for planet_name, planet_data in planets.items():
            if planet_name in ['Ascendant', 'MC']:
                continue
            
            # Check if planet has position data
            if not hasattr(planet_data, 'sign') and not isinstance(planet_data, dict):
                continue
            
            # Get planet sign
            if hasattr(planet_data, 'sign'):
                sign = planet_data.sign
                is_retrograde = getattr(planet_data, 'retrograde', False)
            elif isinstance(planet_data, dict):
                sign = planet_data.get('sign', '')
                is_retrograde = planet_data.get('retrograde', False)
            else:
                continue
            
            # Debilitation check
            if self._is_debilitated(planet_name, sign):
                weak_planets.append(planet_name)
            # Exaltation check
            elif self._is_exalted(planet_name, sign):
                strong_planets.append(planet_name)
            # Retrograde planets are generally weak (except Jupiter & Venus can be okay)
            elif is_retrograde and planet_name not in ['Jupiter', 'Venus']:
                if planet_name not in weak_planets:
                    weak_planets.append(planet_name)
        
        return {
            'weak_planets': weak_planets,
            'strong_planets': strong_planets
        }
    
    def _is_debilitated(self, planet: str, sign: str) -> bool:
        """Check if planet is debilitated in given sign"""
        debilitation = {
            'Sun': 'Libra',
            'Moon': 'Scorpio',
            'Mars': 'Cancer',
            'Mercury': 'Pisces',
            'Jupiter': 'Capricorn',
            'Venus': 'Virgo',
            'Saturn': 'Aries',
            'Rahu': 'Scorpio',  # Approximate
            'Ketu': 'Taurus'    # Approximate
        }
        return debilitation.get(planet) == sign
    
    def _is_exalted(self, planet: str, sign: str) -> bool:
        """Check if planet is exalted in given sign"""
        exaltation = {
            'Sun': 'Aries',
            'Moon': 'Taurus',
            'Mars': 'Capricorn',
            'Mercury': 'Virgo',
            'Jupiter': 'Cancer',
            'Venus': 'Pisces',
            'Saturn': 'Libra',
            'Rahu': 'Taurus',    # Approximate
            'Ketu': 'Scorpio'    # Approximate
        }
        return exaltation.get(planet) == sign
    
    def _get_wearing_guidelines(self) -> List[str]:
        """Get general guidelines for wearing gemstones"""
        return [
            "🔸 **Consult an astrologer** before wearing any gemstone, especially Blue Sapphire",
            "🔸 **Wear on the specified day** in the morning after sunrise (6-8 AM preferred)",
            "🔸 **Energize the gemstone** by dipping in Ganga water or raw milk, then recite planet's mantra 108 times",
            "🔸 **Minimum weight matters** - Too small gemstones may not give results",
            "🔸 **Natural gemstones only** - Avoid synthetic, heated, or treated stones",
            "🔸 **Touch the skin** - Gemstone should touch your skin (leave bottom open in setting)",
            "🔸 **Trial period** - Wear for 7 days first, observe any negative effects",
            "🔸 **Don't combine opposites** - Don't wear Sun & Saturn, Moon & Rahu, Mars & Venus together",
            "🔸 **Remove during sleep** (optional) or while entering bathroom",
            "🔸 **Clean regularly** with soft brush in lukewarm water"
        ]
