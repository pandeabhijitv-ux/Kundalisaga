"""
Remedy Suggestion Engine
Personalized, actionable remedies based on chart + current situation
"""
from typing import Dict, List, Optional
from datetime import datetime
from src.utils import logger


class RemedyEngine:
    """Generate personalized astrological remedies based on chart and goals"""
    
    def __init__(self, rag_system=None):
        self.logger = logger
        self.rag_system = rag_system
        
        # Map goals to relevant planets
        self.goal_planets = {
            'career': ['Sun', 'Saturn', 'Jupiter', 'Mercury'],
            'promotion': ['Sun', 'Jupiter', 'Saturn'],
            'marriage': ['Venus', 'Jupiter', 'Moon'],
            'relationship': ['Venus', 'Jupiter', 'Moon'],
            'love': ['Venus', 'Moon'],
            'partner': ['Venus', 'Jupiter', 'Moon'],
            'wealth': ['Jupiter', 'Mercury', 'Venus'],
            'money': ['Jupiter', 'Mercury', 'Venus'],
            'finance': ['Jupiter', 'Mercury', 'Venus'],
            'education': ['Mercury', 'Jupiter'],
            'study': ['Mercury', 'Jupiter'],
            'health': ['Sun', 'Moon', 'Mars'],
            'property': ['Mars', 'Saturn'],
            'children': ['Jupiter', 'Moon'],
            'business': ['Mercury', 'Jupiter', 'Sun']
        }
    
    def analyze_chart_for_remedies(self, chart_data: Dict) -> List[str]:
        """
        Analyze birth chart to identify areas needing remedies
        
        Args:
            chart_data: Birth chart calculation results
        
        Returns:
            List of identified issues/weak areas
        """
        issues = []
        planets = chart_data.get('planets', {})
        
        # Check for debilitated planets
        debilitation_signs = {
            'Sun': 'Libra',
            'Moon': 'Scorpio',
            'Mars': 'Cancer',
            'Mercury': 'Pisces',
            'Jupiter': 'Capricorn',
            'Venus': 'Virgo',
            'Saturn': 'Aries'
        }
        
        for planet_name, debil_sign in debilitation_signs.items():
            if planet_name in planets:
                planet = planets[planet_name]
                if hasattr(planet, 'sign') and planet.sign == debil_sign:
                    issues.append(f"{planet_name} is debilitated in {debil_sign}")
        
        # Check for retrograde planets
        for planet_name, planet in planets.items():
            if hasattr(planet, 'is_retrograde') and planet.is_retrograde:
                if planet_name not in ['Rahu', 'Ketu']:  # These are always retrograde
                    issues.append(f"{planet_name} is retrograde")
        
        # Check for malefic planets in key houses (1st, 4th, 7th, 10th)
        malefics = ['Mars', 'Saturn', 'Rahu', 'Ketu']
        key_houses = [1, 4, 7, 10]
        
        for planet_name in malefics:
            if planet_name in planets:
                planet = planets[planet_name]
                if hasattr(planet, 'house') and planet.house in key_houses:
                    issues.append(f"{planet_name} in {planet.house}th house")
        
        return issues
    
    def get_general_remedies(self, planet: str) -> List[Dict]:
        """
        Get general remedies for a planet
        
        Args:
            planet: Planet name
        
        Returns:
            List of remedy dictionaries
        """
        remedies_database = {
            'Sun': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः',
                    'description': 'Surya Graha Mantra: "Om Hraam Hreem Hraum Sah Suryaya Namaha"',
                    'frequency': 'Daily, 108 times, preferably at sunrise',
                    'benefits': 'Strengthens Sun, enhances vitality, confidence, career success'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ सूर्याय नमः',
                    'description': 'Chant "Om Suryaya Namaha" 108 times daily',
                    'frequency': 'Daily, preferably at sunrise'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Ruby (Manikya) on ring finger',
                    'weight': '3-6 carats',
                    'metal': 'Gold or copper',
                    'day': 'Sunday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate wheat, jaggery, or red cloth on Sundays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Fasting',
                    'description': 'Fast on Sundays, eat one meal after sunset',
                    'frequency': 'Weekly'
                }
            ],
            'Moon': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ श्रां श्रीं श्रौं सः चन्द्राय नमः',
                    'description': 'Chandra Graha Mantra: "Om Shraam Shreem Shraum Sah Chandraya Namaha"',
                    'frequency': 'Daily, 108 times, preferably in evening or Monday',
                    'benefits': 'Strengthens Moon, improves mental peace, emotional stability, relationships'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ चन्द्राय नमः',
                    'description': 'Chant "Om Chandraya Namaha" 108 times',
                    'frequency': 'Daily, preferably in evening'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Pearl (Moti) on little finger',
                    'weight': '5-7 carats',
                    'metal': 'Silver',
                    'day': 'Monday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate rice, white cloth, or milk on Mondays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Spend time near water bodies, practice meditation',
                    'frequency': 'Regular'
                }
            ],
            'Mars': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ क्रां क्रीं क्रौं सः भौमाय नमः',
                    'description': 'Mangal Graha Mantra: "Om Kraam Kreem Kraum Sah Bhaumaya Namaha"',
                    'frequency': 'Daily, 108 times, preferably Tuesday morning',
                    'benefits': 'Strengthens Mars, increases courage, energy, property gains, sibling harmony'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ मंगलाय नमः',
                    'description': 'Chant "Om Mangalaya Namaha" 108 times',
                    'frequency': 'Daily, preferably Tuesday morning'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Red Coral (Moonga) on ring finger',
                    'weight': '5-8 carats',
                    'metal': 'Copper or gold',
                    'day': 'Tuesday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate red lentils, jaggery on Tuesdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Practice anger management, physical exercise',
                    'frequency': 'Daily'
                }
            ],
            'Mercury': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः',
                    'description': 'Budh Graha Mantra: "Om Braam Breem Braum Sah Budhaya Namaha"',
                    'frequency': 'Daily, 108 times, preferably Wednesday morning',
                    'benefits': 'Strengthens Mercury, enhances intelligence, communication, business success'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ बुधाय नमः',
                    'description': 'Chant "Om Budhaya Namaha" 108 times',
                    'frequency': 'Daily, preferably Wednesday morning'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Emerald (Panna) on little finger',
                    'weight': '3-6 carats',
                    'metal': 'Gold or silver',
                    'day': 'Wednesday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate green vegetables, books on Wednesdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Read spiritual texts, practice communication skills',
                    'frequency': 'Regular'
                }
            ],
            'Jupiter': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः',
                    'description': 'Guru Graha Mantra: "Om Graam Greem Graum Sah Gurave Namaha"',
                    'frequency': 'Daily, 108 times, preferably Thursday morning',
                    'benefits': 'Strengthens Jupiter, brings wisdom, wealth, children blessings, marriage prospects'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ गुरवे नमः',
                    'description': 'Chant "Om Gurave Namaha" 108 times',
                    'frequency': 'Daily, preferably Thursday morning'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Yellow Sapphire (Pukhraj) on index finger',
                    'weight': '5-7 carats',
                    'metal': 'Gold',
                    'day': 'Thursday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate yellow items, turmeric, or gold on Thursdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Study scriptures, help teachers/gurus',
                    'frequency': 'Regular'
                }
            ],
            'Venus': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ द्रां द्रीं द्रौं सः शुक्राय नमः',
                    'description': 'Shukra Graha Mantra: "Om Draam Dreem Draum Sah Shukraya Namaha"',
                    'frequency': 'Daily, 108 times, preferably Friday morning',
                    'benefits': 'Strengthens Venus, enhances love, marriage, luxury, artistic abilities'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ शुक्राय नमः',
                    'description': 'Chant "Om Shukraya Namaha" 108 times',
                    'frequency': 'Daily, preferably Friday morning'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Diamond or White Sapphire on middle finger',
                    'weight': '1-2 carats (diamond) or 5-7 carats (sapphire)',
                    'metal': 'Silver or platinum',
                    'day': 'Friday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate white items, sweets on Fridays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Appreciate art, maintain good hygiene',
                    'frequency': 'Daily'
                }
            ],
            'Saturn': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः',
                    'description': 'Shani Graha Mantra: "Om Praam Preem Praum Sah Shanaischaraya Namaha"',
                    'frequency': 'Daily, 108 times, preferably Saturday morning',
                    'benefits': 'Strengthens Saturn, reduces delays, improves discipline, longevity, removes Shani dosha'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ शनये नमः',
                    'description': 'Chant "Om Shanaye Namaha" 108 times',
                    'frequency': 'Daily, preferably Saturday morning'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Blue Sapphire (Neelam) on middle finger',
                    'weight': '5-7 carats',
                    'metal': 'Silver or iron',
                    'day': 'Saturday',
                    'caution': 'Test for 3 days before permanent wear'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate black items, oil, iron on Saturdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Serve elderly, practice discipline and patience',
                    'frequency': 'Regular'
                }
            ],
            'Rahu': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः',
                    'description': 'Rahu Graha Mantra: "Om Bhraam Bhreem Bhraum Sah Rahave Namaha"',
                    'frequency': 'Daily, 108 times, preferably during Rahu Kaal',
                    'benefits': 'Strengthens Rahu, brings foreign gains, reduces confusion, material success'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ राहवे नमः',
                    'description': 'Chant "Om Rahave Namaha" 108 times',
                    'frequency': 'Daily'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Hessonite (Gomed) on middle finger',
                    'weight': '5-8 carats',
                    'metal': 'Silver',
                    'day': 'Saturday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate blue/black items, mustard oil on Saturdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Practice meditation, avoid deception',
                    'frequency': 'Daily'
                }
            ],
            'Ketu': [
                {
                    'type': 'Navagraha Mantra',
                    'sanskrit': 'ॐ स्रां स्रीं स्रौं सः केतवे नमः',
                    'description': 'Ketu Graha Mantra: "Om Sraam Sreem Sraum Sah Ketave Namaha"',
                    'frequency': 'Daily, 108 times, preferably Thursday',
                    'benefits': 'Strengthens Ketu, enhances spirituality, moksha, removes past karma effects'
                },
                {
                    'type': 'Simple Mantra',
                    'sanskrit': 'ॐ केतवे नमः',
                    'description': 'Chant "Om Ketave Namaha" 108 times',
                    'frequency': 'Daily'
                },
                {
                    'type': 'Gemstone',
                    'description': 'Wear Cat\'s Eye (Lehsunia) on middle finger',
                    'weight': '5-7 carats',
                    'metal': 'Silver',
                    'day': 'Thursday'
                },
                {
                    'type': 'Charity',
                    'description': 'Donate multi-colored items on Thursdays',
                    'frequency': 'Weekly'
                },
                {
                    'type': 'Practice',
                    'description': 'Spiritual practices, help animals (especially dogs)',
                    'frequency': 'Regular'
                }
            ]
        }
        
        return remedies_database.get(planet, [])
    
    def get_universal_spiritual_remedies(self) -> List[Dict]:
        """
        Get universal spiritual remedies that work for all issues
        
        Returns:
            List of powerful universal remedies
        """
        universal_remedies = [
            {
                'type': 'Ganesh Vandana',
                'title': 'Lord Ganesha Prayer - Remove All Obstacles',
                'sanskrit': 'वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ। निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥',
                'mantra': 'Vakratunda Mahakaya Suryakoti Samaprabha | Nirvighnam Kuru Me Deva Sarva-Kaaryeshu Sarvada ||',
                'meaning': 'O Lord with curved trunk, large body, brilliance of million suns, please make my endeavors obstacle-free always',
                'frequency': 'Daily, before starting any new work or at morning',
                'benefits': 'Removes obstacles, brings success in new ventures, improves wisdom and intellect',
                'best_for': 'New beginnings, business, education, removing difficulties'
            },
            {
                'type': 'Ganesh Mantra',
                'title': 'Simple Ganesha Mantra',
                'sanskrit': 'ॐ गं गणपतये नमः',
                'mantra': 'Om Gam Ganapataye Namaha',
                'frequency': '108 times daily',
                'benefits': 'Quick removal of obstacles, success in ventures',
                'best_for': 'Daily practice, exams, interviews, new projects'
            },
            {
                'type': 'Vishnu Sahasranama',
                'title': 'Thousand Names of Lord Vishnu - Ultimate Protection',
                'description': 'Recitation of 1000 names of Lord Vishnu',
                'frequency': 'Daily or weekly (full recitation takes 30-45 minutes)',
                'benefits': 'Overall protection, peace of mind, removes all doshas, spiritual growth, health, wealth',
                'best_for': 'Overall well-being, protection from negative energies, mental peace, spiritual elevation',
                'note': 'Even partial recitation (100-200 names) is highly beneficial. Listening to recorded version also works.',
                'special_days': 'Thursday, Ekadashi, Dwadashi are most auspicious'
            },
            {
                'type': 'Vishnu Mantra',
                'title': 'Simple Vishnu Mantra',
                'sanskrit': 'ॐ नमो नारायणाय',
                'mantra': 'Om Namo Narayanaya',
                'frequency': '108 times daily',
                'benefits': 'Divine protection, peace, removes all fears and negativity',
                'best_for': 'Peace of mind, protection, overall well-being'
            },
            {
                'type': 'Gayatri Mantra',
                'title': 'Universal Vedic Mantra',
                'sanskrit': 'ॐ भूर्भुवः स्वः। तत्सवितुर्वरेण्यं। भर्गो देवस्य धीमहि। धियो यो नः प्रचोदयात्॥',
                'mantra': 'Om Bhur Bhuvah Swaha | Tat Savitur Varenyam | Bhargo Devasya Dhimahi | Dhiyo Yo Nah Prachodayat ||',
                'frequency': '108 times daily, preferably at sunrise',
                'benefits': 'Removes all doshas, enhances all planets, brings wisdom and enlightenment',
                'best_for': 'Overall spiritual growth, removing all negative influences'
            },
            {
                'type': 'Mahamrityunjaya Mantra',
                'title': 'Victory Over Death - Ultimate Healing Mantra',
                'sanskrit': 'ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय मामृतात्॥',
                'mantra': 'Om Tryambakam Yajamahe Sugandhim Pushtivardhanam | Urvarukamiva Bandhanan Mrityor Mukshiya Maamritat ||',
                'frequency': '108 times daily',
                'benefits': 'Health, healing, protection from accidents, longevity, removes fear of death',
                'best_for': 'Health issues, protection, overcoming serious obstacles, Saturn/Rahu/Ketu afflictions'
            },
            {
                'type': 'Durga Saptashati/Devi Mahatmya',
                'title': '700 Verses of Goddess Durga',
                'description': 'Recitation of Durga Saptashati (Chandi Path)',
                'frequency': 'Weekly or on special occasions (Navratri)',
                'benefits': 'Protection from enemies, removes all difficulties, wealth, power',
                'best_for': 'Overcoming enemies, court cases, debts, serious obstacles',
                'note': 'Can be listened to or recited. Extremely powerful during Navratri'
            },
            {
                'type': 'Hanuman Chalisa',
                'title': '40 Verses Praising Lord Hanuman',
                'description': 'Recitation of Hanuman Chalisa',
                'frequency': 'Daily, especially Tuesday and Saturday',
                'benefits': 'Removes Saturn afflictions, gives courage, removes fear, protection',
                'best_for': 'Saturn issues, Mars afflictions, removing fear, gaining strength',
                'note': 'Very effective for Shani Sade Sati period'
            }
        ]
        
        return universal_remedies
    
    def suggest_remedies(self, chart_data: Dict, 
                        specific_concern: str = None) -> Dict:
        """
        Suggest remedies based on chart analysis
        
        Args:
            chart_data: Birth chart data
            specific_concern: Optional specific area of concern
        
        Returns:
            Dict with remedy suggestions
        """
        self.logger.info("Generating remedy suggestions")
        
        # Analyze chart for issues
        issues = self.analyze_chart_for_remedies(chart_data)
        
        # Collect remedies
        all_remedies = {}
        
        for issue in issues:
            # Extract planet name from issue
            for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 
                          'Venus', 'Saturn', 'Rahu', 'Ketu']:
                if planet in issue:
                    if planet not in all_remedies:
                        all_remedies[planet] = {
                            'issue': issue,
                            'remedies': self.get_general_remedies(planet)
                        }
        
        # If RAG system available, get book-based recommendations
        book_recommendations = None
        if self.rag_system and specific_concern:
            query = f"What remedies are suggested for {specific_concern}?"
            result = self.rag_system.ask(query)
            book_recommendations = result.get('answer')
        
        return {
            'identified_issues': issues,
            'planet_remedies': all_remedies,
            'universal_remedies': self.get_universal_spiritual_remedies(),
            'book_recommendations': book_recommendations,
            'general_advice': self._get_general_advice()
        }
    
    def _get_general_advice(self) -> List[str]:
        """Get general spiritual/vedic advice"""
        return [
            "Maintain regularity in spiritual practices",
            "Practice daily meditation or pranayama",
            "Recite Gayatri Mantra for overall well-being",
            "Perform acts of charity without expectation",
            "Respect elders and teachers",
            "Avoid alcohol, non-vegetarian food on spiritual days",
            "Keep your living space clean and positive",
            "Practice gratitude daily"
        ]
    
    def get_remedies_for_goal(self, goal: str, chart_data: Dict = None, 
                               current_dasha: str = None) -> Dict:
        """
        Get personalized remedies for specific life goal
        
        Args:
            goal: Life goal (career, marriage, wealth, etc.)
            chart_data: Birth chart data (optional)
            current_dasha: Current dasha period (optional)
        
        Returns:
            Personalized remedy package
        """
        goal_lower = goal.lower()
        
        # Identify key word from goal
        goal_key = None
        for key in self.goal_planets.keys():
            if key in goal_lower:
                goal_key = key
                break
        
        if not goal_key:
            goal_key = 'career'  # Default
        
        # Get relevant planets
        relevant_planets = self.goal_planets.get(goal_key, ['Jupiter'])
        
        # For relationship goals, analyze chart for specific issues
        chart_analysis = []
        if chart_data and goal_key in ['marriage', 'relationship', 'love', 'partner']:
            chart_analysis = self._analyze_relationship_chart(chart_data)
        
        # Build remedy package
        remedies = {
            'goal': goal,
            'chart_issues': chart_analysis,
            'immediate_actions': self._get_immediate_actions(goal_key, current_dasha),
            'planet_remedies': {},
            'power_times': self._get_power_times(goal_key),
            'lifestyle_changes': self._get_lifestyle_changes(goal_key),
            'quick_wins': self._get_quick_wins(goal_key)
        }
        
        # Add specific planet remedies
        for planet in relevant_planets[:2]:  # Top 2 most relevant
            remedies['planet_remedies'][planet] = self._get_focused_remedies(planet, goal_key)
        
        return remedies
    
    def _analyze_relationship_chart(self, chart_data: Dict) -> List[str]:
        """Analyze chart specifically for relationship factors"""
        issues = []
        planets = chart_data.get('planets', {})
        
        # Check 7th house (marriage/partnerships)
        if 'Ascendant' in planets:
            asc_house = getattr(planets['Ascendant'], 'house', 1)
            seventh_house = (asc_house + 6) % 12
            if seventh_house == 0:
                seventh_house = 12
        
        # Check Venus (Shukra) - significator of love/relationships
        if 'Venus' in planets:
            venus = planets['Venus']
            venus_sign = getattr(venus, 'sign', '')
            venus_house = getattr(venus, 'house', 0)
            
            # Venus debilitated in Virgo
            if venus_sign == 'Virgo':
                issues.append("🔸 Venus is debilitated in Virgo - affecting relationship harmony")
                issues.append("   → Remedy: Worship Goddess Lakshmi on Fridays, wear white")
            
            # Venus in 6th, 8th, or 12th house (challenging positions)
            if venus_house in [6, 8, 12]:
                issues.append(f"🔸 Venus in {venus_house}th house - creating relationship obstacles")
                issues.append("   → Remedy: Donate white sweets/clothes on Fridays")
        
        # Check Moon - emotional compatibility
        if 'Moon' in planets:
            moon = planets['Moon']
            moon_sign = getattr(moon, 'sign', '')
            
            # Moon debilitated in Scorpio
            if moon_sign == 'Scorpio':
                issues.append("🔸 Moon debilitated in Scorpio - emotional challenges")
                issues.append("   → Remedy: Wear pearl, offer milk to Shiva on Mondays")
        
        # Check Mars - compatibility and passion
        if 'Mars' in planets:
            mars = planets['Mars']
            mars_house = getattr(mars, 'house', 0)
            
            # Mangal Dosha check (Mars in 1st, 4th, 7th, 8th, 12th)
            if mars_house in [1, 4, 7, 8, 12]:
                issues.append(f"🔸 Mars in {mars_house}th house - Mangal Dosha affecting marriage")
                issues.append("   → Remedy: Fast on Tuesdays, visit Hanuman temple")
        
        if not issues:
            issues.append("✅ No major astrological obstacles in relationship house")
            issues.append("   → Focus on Venus and 7th house strengthening for enhancement")
        
        return issues
    
    def _get_goal_specific_planets(self, goal: str) -> List[str]:
        """Get planets relevant to specific goal for Lal Kitab remedies"""
        goal_lower = goal.lower() if goal else ''
        
        # Map goals to relevant planets
        if any(word in goal_lower for word in ['marriage', 'relationship', 'love', 'partner', 'spouse']):
            return ['Venus', 'Moon', 'Mars', 'Jupiter']  # 7th house matters
        elif any(word in goal_lower for word in ['career', 'job', 'profession', 'work']):
            return ['Sun', 'Saturn', 'Jupiter', 'Mercury']  # 10th house matters
        elif any(word in goal_lower for word in ['wealth', 'money', 'finance', 'prosperity']):
            return ['Jupiter', 'Venus', 'Mercury', 'Moon']  # 2nd/11th house matters
        elif any(word in goal_lower for word in ['health', 'fitness', 'wellness']):
            return ['Sun', 'Moon', 'Mars', 'Saturn']  # 1st/6th house matters
        elif any(word in goal_lower for word in ['education', 'study', 'learning', 'knowledge']):
            return ['Jupiter', 'Mercury', 'Sun']  # 5th/9th house matters
        elif any(word in goal_lower for word in ['children', 'pregnancy', 'child']):
            return ['Jupiter', 'Moon', 'Sun']  # 5th house matters
        elif any(word in goal_lower for word in ['spiritual', 'meditation', 'enlightenment']):
            return ['Jupiter', 'Ketu', 'Moon']  # 9th/12th house matters
        else:
            # Return None to show all planets if no specific goal
            return None
    
    def _get_immediate_actions(self, goal: str, current_dasha: str = None) -> List[str]:
        """Get immediate actionable steps"""
        actions = {
            'career': [
                "🌅 Wake up during Brahma Muhurta (4:30-6:00 AM) for mental clarity",
                "📿 Chant Sun mantra 'Om Hreem Suryaya Namaha' 21 times before important meetings",
                "🙏 Offer water to Sun every morning facing east",
                "💼 Keep a clear quartz crystal on your work desk (left side)"
            ],
            'promotion': [
                "🔴 Wear red or orange on Tuesdays and Sundays",
                "📅 Schedule important career discussions on Thursday mornings",
                "🌟 Place a Sun yantra in your workspace",
                "💪 Do 11 Surya Namaskars daily"
            ],
            'marriage': [
                "💐 Offer white flowers to Goddess Lakshmi on Fridays",
                "🌙 Look at the moon on Purnima (full moon) and pray for partner",
                "💍 Wear white or light pink on Fridays",
                "🕉️ Chant 'Om Shukraya Namaha' 108 times every Friday"
            ],
            'relationship': [
                "💐 Offer white flowers to Goddess Lakshmi on Fridays",
                "🌙 Look at the moon on Purnima (full moon) and pray for harmony",
                "💍 Wear white or light pink on Fridays",
                "🕉️ Chant 'Om Shukraya Namaha' 108 times every Friday"
            ],
            'love': [
                "💖 Offer red roses to your deity on Fridays",
                "🌹 Wear pink or white clothes on Fridays",
                "🕉️ Chant Venus mantra 'Om Shukraya Namaha' 108 times",
                "💝 Keep a pair of rose quartz stones in your bedroom"
            ],
            'partner': [
                "💐 Offer white flowers to Goddess Lakshmi on Fridays",
                "🌙 Pray for a suitable partner during Purnima (full moon)",
                "💍 Wear white or light pink on Fridays",
                "🕉️ Chant 'Om Shukraya Namaha' 108 times every Friday"
            ],
            'wealth': [
                "🪔 Light ghee lamp in north-east corner of house every evening",
                "📿 Chant Lakshmi mantra 'Om Shreem Mahalakshmiyei Namaha' 108 times",
                "💰 Keep a silver coin in your wallet/purse",
                "🌿 Water a peepal tree every Saturday"
            ],
            'money': [
                "🪔 Light ghee lamp in north-east corner of house every evening",
                "📿 Chant Lakshmi mantra 'Om Shreem Mahalakshmiyei Namaha' 108 times",
                "💰 Keep a silver coin in your wallet/purse",
                "🌿 Water a peepal tree every Saturday"
            ],
            'finance': [
                "🪔 Light ghee lamp in north-east corner of house every evening",
                "📿 Chant Lakshmi mantra 'Om Shreem Mahalakshmiyei Namaha' 108 times",
                "💰 Keep a silver coin in your wallet/purse",
                "🌿 Water a peepal tree every Saturday"
            ]
        }
        
        return actions.get(goal, actions['marriage'])  # Default to marriage/relationship if not found
    
    def _get_focused_remedies(self, planet: str, goal: str) -> Dict:
        """Get focused remedies for planet-goal combination"""
        # Get basic planet remedies
        base_remedies = self.get_general_remedies(planet)
        
        # Add goal-specific context
        focused = {
            'planet': planet,
            'mantras': [],
            'actions': [],
            'timing': ''
        }
        
        # Extract and enhance
        for remedy in base_remedies:
            if remedy['type'] == 'Mantra':
                focused['mantras'].append({
                    'text': remedy['description'],
                    'count': '108 times daily',
                    'best_time': remedy.get('frequency', 'Morning')
                })
            elif remedy['type'] == 'Practice':
                focused['actions'].append(remedy['description'])
        
        # Add goal-specific power action
        power_actions = {
            ('Sun', 'career'): "Place Sun's photo or painting facing east in office",
            ('Sun', 'promotion'): "Donate wheat/jaggery to needy every Sunday",
            ('Venus', 'marriage'): "Gift white sweets to unmarried girls on Fridays",
            ('Jupiter', 'career'): "Teach/mentor someone weekly - share your knowledge",
            ('Jupiter', 'marriage'): "Seek blessings from married couples on Thursdays",
            ('Saturn', 'career'): "Help elderly/disabled people - especially on Saturdays",
        }
        
        key = (planet, goal)
        if key in power_actions:
            focused['actions'].insert(0, f"⭐ POWER ACTION: {power_actions[key]}")
        
        return focused
    
    def _get_power_times(self, goal: str) -> Dict:
        """Get auspicious timings for goal"""
        power_times = {
            'career': {
                'best_day': 'Sunday',
                'best_time': '6:00 AM - 7:30 AM (Sunrise hour)',
                'monthly': 'Shukla Paksha (Waxing moon fortnight)',
                'avoid': 'Amavasya (New moon), Saturdays after sunset'
            },
            'promotion': {
                'best_day': 'Thursday or Sunday',
                'best_time': 'First hour after sunrise',
                'monthly': 'Days when Moon is in Leo, Aries, or Sagittarius',
                'avoid': 'Rahu Kaal timings'
            },
            'marriage': {
                'best_day': 'Friday',
                'best_time': 'Evening 5:00 PM - 7:00 PM',
                'monthly': 'Purnima (Full moon), Thursdays in Shukla Paksha',
                'avoid': 'Tuesdays, Saturdays, Eclipse days'
            },
            'wealth': {
                'best_day': 'Thursday or Friday',
                'best_time': 'Early morning or evening (Lakshmi time)',
                'monthly': 'Diwali, Dhanteras, Akshaya Tritiya',
                'avoid': 'Never spend heavily on Amavasya'
            }
        }
        
        return power_times.get(goal, power_times['career'])
    
    def _get_lifestyle_changes(self, goal: str) -> List[str]:
        """Get lifestyle recommendations"""
        changes = {
            'career': [
                "Wake before sunrise consistently",
                "Face east while working/studying",
                "Eat sattvic food (avoid onion/garlic on important days)",
                "Maintain a clean, organized workspace",
                "Practice 10 minutes of silence/meditation daily"
            ],
            'promotion': [
                "Improve communication - speak clearly and confidently",
                "Build relationships with seniors - seek their guidance",
                "Dress in bright, confident colors",
                "Exercise regularly - build physical strength and stamina"
            ],
            'marriage': [
                "Maintain good personal grooming and hygiene",
                "Develop hobbies - music, art, cooking",
                "Be social - attend family/community functions",
                "Practice kindness and empathy in all relationships",
                "Avoid negative talk about opposite gender"
            ],
            'relationship': [
                "Spend quality time with partner - no phones",
                "Practice active listening and understanding",
                "Wear pleasant fragrances - rose, jasmine, sandalwood",
                "Keep bedroom clean, romantic with soft lighting",
                "Express gratitude and appreciation daily"
            ],
            'love': [
                "Work on self-confidence and self-love first",
                "Wear white or light pink on Fridays",
                "Keep fresh flowers in living space",
                "Practice forgiveness - let go of past hurts",
                "Socialize in positive, uplifting environments"
            ],
            'partner': [
                "Be authentic - don't pretend to be someone else",
                "Develop emotional intelligence and empathy",
                "Stay physically active and healthy",
                "Pursue your passions - be interesting",
                "Keep home welcoming - plants, cleanliness, good energy"
            ],
            'wealth': [
                "Start saving minimum 10% of income monthly",
                "Invest in gold/silver on auspicious days",
                "Avoid unnecessary expenses on Saturdays",
                "Keep home entrance clean and well-lit",
                "Donate 1% of income monthly to genuine causes"
            ],
            'money': [  # Alias for wealth
                "Start saving minimum 10% of income monthly",
                "Invest in gold/silver on auspicious days",
                "Avoid unnecessary expenses on Saturdays",
                "Keep home entrance clean and well-lit",
                "Donate 1% of income monthly to genuine causes"
            ],
            'finance': [  # Alias for wealth
                "Start saving minimum 10% of income monthly",
                "Invest in gold/silver on auspicious days",
                "Avoid unnecessary expenses on Saturdays",
                "Keep home entrance clean and well-lit",
                "Donate 1% of income monthly to genuine causes"
            ],
            'health': [
                "Wake up early - practice Surya Namaskar (Sun Salutation)",
                "Eat fresh, warm food - avoid stale or frozen meals",
                "Drink water from copper vessel after storing overnight",
                "Practice Pranayama - 15 minutes daily breathing exercises",
                "Walk barefoot on grass for 10 minutes daily"
            ],
            'education': [
                "Study during Brahma Muhurta (4:30-6 AM) for retention",
                "Face east or north while studying for better concentration",
                "Keep study area clean, organized, and well-lit",
                "Avoid studying in bedroom - use dedicated study space",
                "Read for 30 minutes daily beyond curriculum"
            ],
            'study': [  # Alias for education
                "Study during Brahma Muhurta (4:30-6 AM) for retention",
                "Face east or north while studying for better concentration",
                "Keep study area clean, organized, and well-lit",
                "Avoid studying in bedroom - use dedicated study space",
                "Read for 30 minutes daily beyond curriculum"
            ],
            'children': [
                "Maintain harmonious relationship with spouse",
                "Keep bedroom clean, uncluttered, and positive",
                "Avoid sleeping under beams or keeping mirrors facing bed",
                "Spend time with children - play, help, teach",
                "Keep northeast corner of home clean and sacred"
            ],
            'business': [
                "Start important deals on auspicious days",
                "Keep accounts clear - pay dues on time",
                "Maintain good relationships with partners and employees",
                "Keep workplace entrance clean and welcoming",
                "Review finances every Saturday"
            ],
            'property': [
                "Visit properties on auspicious days (avoid Tuesdays/Saturdays)",
                "Keep Mars favorable - donate red items on Tuesdays",
                "Strengthen Saturn - help elderly, donate black items",
                "Check Vastu before buying - consult expert",
                "Keep documents organized and secure"
            ]
        }
        
        return changes.get(goal, changes['career'])
    
    def _get_quick_wins(self, goal: str) -> List[str]:
        """Get quick, easy remedies that show fast results"""
        quick_wins = {
            'career': [
                "✅ Keep a Ganesha idol on your work desk - remove obstacles",
                "✅ Write your goal 21 times daily for 21 days",
                "✅ Offer jaggery to ants near your home - 7 Saturdays",
                "✅ Keep a copper coin in your pocket during interviews/meetings"
            ],
            'promotion': [
                "✅ Light a ghee lamp facing north for 5 minutes daily - 21 days",
                "✅ Donate red lentils (masoor dal) on 3 Tuesdays",
                "✅ Wear ruby or red coral (if suitable) or red thread on right wrist",
                "✅ Apply red tilak on forehead before leaving for work"
            ],
            'marriage': [
                "✅ Keep fresh roses/jasmine flowers in bedroom",
                "✅ Apply kumkum/sindoor daily (even if unmarried)",
                "✅ Tie 7 knots in red thread, keep under pillow - 7 Fridays",
                "✅ Feed birds daily (pigeons especially) - shows results in 40 days"
            ],
            'relationship': [
                "✅ Wear white clothes and silver jewelry on Fridays",
                "✅ Keep a pair of lovebirds or swans picture in bedroom",
                "✅ Offer white sweets at temple on 7 consecutive Fridays",
                "✅ Chant 'Om Shukraya Namaha' 108 times on Friday mornings"
            ],
            'love': [
                "✅ Keep rose quartz crystal near bed or wear as pendant",
                "✅ Apply a dot of saffron/kumkum on forehead daily",
                "✅ Donate milk or white sweets on Fridays for 21 days",
                "✅ Light a ghee lamp for Goddess Parvati every Friday evening"
            ],
            'partner': [
                "✅ Keep 2 white candles together in bedroom (relationship unity)",
                "✅ Tie red and white threads together, wear on right wrist",
                "✅ Feed cows with green grass on Wednesdays and Fridays",
                "✅ Keep a small silver item under pillow while sleeping"
            ],
            'wealth': [
                "✅ Keep a coin under Tulsi plant - never remove it",
                "✅ Sprinkle salt in all corners of house every Saturday",
                "✅ Keep Kuber Yantra in cash box/wallet",
                "✅ Never keep empty purse/wallet - always have at least 1 coin"
            ],
            'money': [  # Alias for wealth
                "✅ Keep a coin under Tulsi plant - never remove it",
                "✅ Sprinkle salt in all corners of house every Saturday",
                "✅ Keep Kuber Yantra in cash box/wallet",
                "✅ Never keep empty purse/wallet - always have at least 1 coin"
            ],
            'finance': [  # Alias for wealth
                "✅ Keep a coin under Tulsi plant - never remove it",
                "✅ Sprinkle salt in all corners of house every Saturday",
                "✅ Keep Kuber Yantra in cash box/wallet",
                "✅ Never keep empty purse/wallet - always have at least 1 coin"
            ],
            'health': [
                "✅ Offer water to Sun at sunrise with copper vessel",
                "✅ Keep a Rudraksha bead or wear if suitable",
                "✅ Donate fruits to hospital patients on Sundays",
                "✅ Touch feet of elders daily - especially parents"
            ],
            'education': [
                "✅ Keep yellow flower or cloth on study desk",
                "✅ Write 'Om Namah Saraswatyai' on paper, keep in books",
                "✅ Donate books or stationery to poor students",
                "✅ Offer yellow sweets to Goddess Saraswati on Thursdays"
            ],
            'study': [  # Alias for education
                "✅ Keep yellow flower or cloth on study desk",
                "✅ Write 'Om Namah Saraswatyai' on paper, keep in books",
                "✅ Donate books or stationery to poor students",
                "✅ Offer yellow sweets to Goddess Saraswati on Thursdays"
            ],
            'children': [
                "✅ Worship Banana plant on Thursdays",
                "✅ Feed yellow gram to cows on Thursdays",
                "✅ Keep orange/yellow flowers in northeast corner",
                "✅ Donate yellow clothes or sweets to temple"
            ],
            'business': [
                "✅ Keep Ganesha idol at business entrance",
                "✅ Sprinkle Ganga jal (holy water) in shop/office weekly",
                "✅ Light a lamp at business place every morning",
                "✅ Feed green fodder to cow on Wednesdays"
            ],
            'property': [
                "✅ Bury a silver square piece at property corner",
                "✅ Donate red lentils on Tuesdays for Mars strength",
                "✅ Keep Hanuman photo facing south in home",
                "✅ Feed ants with flour and sugar on property"
            ]
        }
        
        return quick_wins.get(goal, quick_wins['career'])    
    def get_lal_kitab_remedies(self, chart_data: Dict, current_dasha: Optional[Dict] = None, goal: str = None) -> List[Dict]:
        """
        Get Lal Kitab specific remedies based on planetary positions, current dasha, and goal
        
        Args:
            chart_data: Birth chart data with planets and houses
            current_dasha: Current Mahadasha information
            goal: Life goal to get specific remedies (career, marriage, wealth, etc.)
        
        Returns:
            List of Lal Kitab remedy dictionaries
        """
        remedies = []
        planets = chart_data.get('planets', {})
        
        # Determine which planets to focus on based on goal
        goal_specific_planets = self._get_goal_specific_planets(goal) if goal else None
        
        # Debug: log what we're getting
        self.logger.info(f"Lal Kitab: Processing {len(planets)} planets")
        if planets:
            first_planet = list(planets.keys())[0]
            planet_data = planets[first_planet]
            self.logger.info(f"First planet '{first_planet}' type: {type(planet_data)}")
            if isinstance(planet_data, dict):
                self.logger.info(f"First planet keys: {planet_data.keys()}")
            else:
                self.logger.info(f"First planet attrs: {dir(planet_data)}")
        
        # Lal Kitab remedies database based on house positions (all 12 houses covered)
        lal_kitab_house_remedies = {
            'Sun': {
                1: ["Donate wheat and jaggery on Sundays", "Keep copper coin in red cloth at home"],
                2: ["Help your father or paternal relatives", "Donate copper items to temples"],
                3: ["Serve food to needy on Sundays", "Keep fast on Sundays if health permits"],
                4: ["Float copper coin in flowing water", "Never take government property for personal use"],
                5: ["Respect your father and elders", "Donate red clothes to poor"],
                6: ["Serve your father or father figures", "Donate copper items on Sundays"],
                7: ["Wear copper ring on ring finger", "Help people without expecting returns"],
                8: ["Float copper coin in flowing water on Sundays", "Never accept free items from father or government"],
                9: ["Visit religious places, offer water to Sun", "Donate books to students"],
                10: ["Donate wheat to poor on Sundays", "Help government employees or father figures"],
                11: ["Offer water to Sun daily at sunrise", "Keep copper vessel at home"],
                12: ["Offer water to Sun with copper vessel daily", "Help needy people without expecting anything"]
            },
            'Moon': {
                1: ["Keep silver in home, wear silver ring", "Donate milk on Mondays"],
                2: ["Respect your mother and maternal relatives", "Keep water in silver vessel overnight"],
                3: ["Serve milk to poor children", "Never waste water"],
                4: ["Respect your mother, serve elderly women", "Keep water in silver vessel near bed"],
                5: ["Donate white sweets to children", "Keep relationship with mother sweet"],
                6: ["Feed cows with green grass", "Donate rice to poor"],
                7: ["Never insult women or your mother", "Donate milk on Mondays"],
                8: ["Float milk in flowing water on Mondays", "Never drink milk at night"],
                9: ["Visit holy places with mother", "Donate rice and milk to temples"],
                10: ["Keep silver at workplace", "Respect female colleagues"],
                11: ["Maintain good relations with mother", "Keep moonstone or pearl (if suitable)"],
                12: ["Feed white cows, donate rice", "Wear pearl or moonstone (if suitable)"]
            },
            'Mars': {
                1: ["Donate red lentils on Tuesdays", "Keep red handkerchief in pocket"],
                2: ["Help your brothers, donate sweets", "Keep Hanuman photo at home"],
                3: ["Respect siblings and neighbors", "Donate jaggery on Tuesdays"],
                4: ["Respect brothers and relatives", "Bury copper nails in foundation of house"],
                5: ["Feed monkeys, visit Hanuman temple", "Donate red clothes to poor"],
                6: ["Serve siblings and cousins", "Donate sweets at temple on Tuesdays"],
                7: ["Never wear red on Tuesdays", "Float red flowers in flowing water"],
                8: ["Donate sweets at Hanuman temple on Tuesdays", "Never keep damaged knives/weapons at home"],
                9: ["Visit Hanuman temple regularly", "Help your brothers in their work"],
                10: ["Donate red lentils to laborers", "Keep Mars favorable items at workplace"],
                11: ["Maintain good relations with brothers", "Donate to martial or sports causes"],
                12: ["Recite Hanuman Chalisa", "Feed monkeys with jaggery and gram"]
            },
            'Mercury': {
                1: ["Feed green grass to cows", "Donate green items on Wednesdays"],
                2: ["Help maternal relatives", "Keep bronze vessel at home"],
                3: ["Feed green fodder to cows", "Donate pens/books to students"],
                4: ["Keep parrot or green plants", "Respect your maternal uncle/aunt"],
                5: ["Donate books to students", "Help in education of poor children"],
                6: ["Serve your sisters and daughters", "Donate green moong dal"],
                7: ["Help your maternal aunt/uncle", "Keep parrot or green plants at home"],
                8: ["Float green items in flowing water", "Never take free items from sisters or daughters"],
                9: ["Donate green clothes to eunuchs", "Keep good relations with maternal relatives"],
                10: ["Use green items at workplace", "Help colleagues and subordinates"],
                11: ["Donate educational materials", "Keep bronze items at home"],
                12: ["Donate green moong dal", "Bury bronze items in foundation"]
            },
            'Jupiter': {
                1: ["Worship peepal tree, pour water on Thursdays", "Donate yellow items"],
                2: ["Respect your teachers and gurus", "Donate turmeric and gram dal"],
                3: ["Help your teachers and gurus", "Plant banana or peepal tree"],
                4: ["Keep saffron at home", "Apply tilak daily"],
                5: ["Respect teachers and priests", "Help poor students with education"],
                6: ["Donate yellow clothes to priests", "Keep turmeric in worship place"],
                7: ["Never disrespect your guru or teacher", "Donate books to libraries"],
                8: ["Never accept turmeric, saffron, or gold as gift", "Donate books or teach poor children"],
                9: ["Serve elderly Brahmins", "Keep gold or yellow items in worship place"],
                10: ["Respect elders at workplace", "Donate to educational institutions"],
                11: ["Maintain good relations with teachers", "Apply saffron tilak on Thursdays"],
                12: ["Donate yellow items to temples", "Never insult learned people"]
            },
            'Venus': {
                1: ["Donate white items on Fridays", "Keep sugar/rice in earthen pot"],
                2: ["Respect your wife and women", "Donate cow's milk or curd"],
                3: ["Help women in need", "Keep fragrant items at home"],
                4: ["Respect women in family", "Donate white clothes"],
                5: ["Never disrespect your wife", "Keep silver items at home"],
                6: ["Serve cows, donate curd", "Keep white flowers at home"],
                7: ["Never disrespect your wife or women", "Donate cow's ghee or curd"],
                8: ["Float camphor in flowing water on Fridays", "Never wear diamonds without proper consultation"],
                9: ["Visit temples with wife", "Donate white sweets to poor"],
                10: ["Respect female colleagues", "Keep Venus favorable items at work"],
                11: ["Donate to causes supporting women", "Keep good marital relations"],
                12: ["Serve cows with fodder", "Keep fragrant flowers in home"]
            },
            'Saturn': {
                1: ["Feed crows and black dogs", "Donate mustard oil on Saturdays"],
                2: ["Help laborers and servants", "Donate black sesame seeds"],
                3: ["Serve old people and handicapped", "Never disrespect workers"],
                4: ["Keep iron horseshoe at home", "Help poor and needy"],
                5: ["Serve handicapped children", "Donate black blankets"],
                6: ["Feed crows daily", "Donate iron items"],
                7: ["Serve old and handicapped people", "Keep iron nails under bed legs"],
                8: ["Flow mustard oil with iron in flowing water", "Never keep old broken items at home"],
                9: ["Serve old saints and sadhus", "Donate to old age homes"],
                10: ["Feed laborers and workers", "Donate black sesame seeds"],
                11: ["Help workers and laborers", "Serve old people"],
                12: ["Serve handicapped and poor", "Donate mustard oil and black items"]
            },
            'Rahu': {
                1: ["Keep silver snake (nag) at worship place", "Donate to orphanages"],
                2: ["Donate radish or coconut", "Keep saunf (fennel) in blue cloth"],
                3: ["Feed ants with flour and sugar", "Never keep snake images"],
                4: ["Keep silver square piece at home", "Donate blue/black cloth"],
                5: ["Donate to religious places", "Keep silver items at home"],
                6: ["Keep silver square piece (chandi ka sikka) in home", "Donate radish or coconut"],
                7: ["Float coconut in flowing water", "Never keep false promises"],
                8: ["Keep saunf (fennel seeds) in blue cloth", "Never keep snake images at home"],
                9: ["Donate to spiritual causes", "Keep silver snake at home"],
                10: ["Be honest in work", "Donate to charitable causes"],
                11: ["Keep good company", "Donate blue/black items"],
                12: ["Donate blue/black cloth", "Float coconut in flowing water on Saturday evenings"]
            },
            'Ketu': {
                1: ["Keep a dog as pet if possible", "Donate multicolored blanket"],
                2: ["Feed dogs daily", "Donate to spiritual places"],
                3: ["Serve dogs and donate blankets", "Keep kusa grass at home"],
                4: ["Keep silver under pillow", "Feed street dogs"],
                5: ["Donate multicolored clothes", "Serve dogs regularly"],
                6: ["Keep a dog as pet if possible", "Donate multicolored blanket"],
                7: ["Feed dogs regularly", "Tie black and white thread on ankle"],
                8: ["Feed dogs regularly", "Keep silver in your pillow"],
                9: ["Donate to spiritual institutions", "Keep worship area clean"],
                10: ["Help spiritual causes", "Keep dogs at workplace if possible"],
                11: ["Donate blankets to poor", "Feed street dogs"],
                12: ["Donate to spiritual or religious places", "Keep kusa grass in worship area"]
        }
        }
        
        # Add remedies based on planetary positions
        for planet_name, planet in planets.items():
            # Skip planets not relevant to the goal (if goal specified)
            if goal_specific_planets and planet_name not in goal_specific_planets:
                continue
                
            self.logger.info(f"Lal Kitab: Checking planet '{planet_name}'")
            if planet_name in lal_kitab_house_remedies:
                # Handle both dict and object formats for planet data
                if isinstance(planet, dict):
                    house = planet.get('house')
                    self.logger.info(f"  Planet is dict, house={house}")
                elif hasattr(planet, 'house'):
                    house = planet.house
                    self.logger.info(f"  Planet is object, house={house}")
                else:
                    self.logger.info(f"  Planet has no house attribute, skipping")
                    continue
                
                if house and house in lal_kitab_house_remedies[planet_name]:
                    self.logger.info(f"  Found remedies for {planet_name} in house {house}")
                    for remedy in lal_kitab_house_remedies[planet_name][house]:
                        remedies.append({
                            'planet': planet_name,
                            'house': house,
                            'remedy': remedy,
                            'type': 'Lal Kitab - House Based'
                        })
                else:
                    self.logger.info(f"  No remedies for {planet_name} in house {house}")
        
        # Dasha-specific Lal Kitab remedies
        if current_dasha:
            dasha_lord = current_dasha.get('lord', '')
            dasha_remedies = {
                'Sun': [
                    "Offer water to Sun daily at sunrise using copper vessel",
                    "Never accept donations or gifts during Sun Mahadasha",
                    "Wear copper ring on ring finger"
                ],
                'Moon': [
                    "Keep silver square piece under pillow",
                    "Donate milk and rice on Mondays",
                    "Never waste water or milk"
                ],
                'Mars': [
                    "Keep Hanuman Chalisa in pocket, recite on Tuesdays",
                    "Donate jaggery and red cloth to laborers",
                    "Never cut neem tree or peepal tree"
                ],
                'Mercury': [
                    "Feed spinach to cows",
                    "Donate green clothes to eunuchs or transgenders",
                    "Keep bronze utensil at home"
                ],
                'Jupiter': [
                    "Apply saffron tilak daily",
                    "Donate turmeric, gram dal, and banana to temple",
                    "Plant banana or peepal tree"
                ],
                'Venus': [
                    "Donate white sweets on Fridays",
                    "Keep small silver ball in home",
                    "Never disrespect women or wife"
                ],
                'Saturn': [
                    "Feed oil-soaked bread to black dog on Saturdays",
                    "Donate iron, black sesame, or mustard oil",
                    "Serve old people and physically challenged"
                ],
                'Rahu': [
                    "Keep silver nag (snake) in worship place",
                    "Donate radish or coconut in flowing water",
                    "Feed ants with sugar and flour mix"
                ],
                'Ketu': [
                    "Tie black and white thread on right ankle",
                    "Donate multicolored blanket to temple",
                    "Feed and serve dogs regularly"
                ]
            }
            
            if dasha_lord in dasha_remedies:
                for remedy in dasha_remedies[dasha_lord]:
                    remedies.append({
                        'planet': dasha_lord,
                        'dasha': True,
                        'remedy': remedy,
                        'type': f'Lal Kitab - {dasha_lord} Mahadasha'
                    })
        
        return remedies