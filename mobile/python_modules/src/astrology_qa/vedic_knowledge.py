"""
Vedic Astrology Knowledge Base - Built-in Classical Principles
No external books needed - comprehensive Vedic astrology knowledge
"""

from src.astrology_engine.vedic_calculator import VedicAstrologyEngine

class VedicKnowledge:
    """Comprehensive Vedic astrology knowledge base"""
    
    def __init__(self):
        self.planet_nature = {
            'Sun': {
                'nature': 'Royal, authoritative, spiritual',
                'signifies': 'Father, government, authority, soul, vitality, ego, leadership',
                'positive': 'Confidence, leadership, dignity, vitality, fame, authority',
                'negative': 'Ego, arrogance, domination, conflicts with authority',
                'element': 'Fire',
                'friends': ['Moon', 'Mars', 'Jupiter'],
                'enemies': ['Venus', 'Saturn'],
                'neutral': ['Mercury']
            },
            'Moon': {
                'nature': 'Emotional, nurturing, receptive',
                'signifies': 'Mother, mind, emotions, public, water, nourishment, comfort',
                'positive': 'Emotional intelligence, intuition, popularity, care, adaptability',
                'negative': 'Moodiness, instability, dependency, anxiety',
                'element': 'Water',
                'friends': ['Sun', 'Mercury'],
                'enemies': [],
                'neutral': ['Mars', 'Jupiter', 'Venus', 'Saturn']
            },
            'Mars': {
                'nature': 'Warrior, energetic, aggressive',
                'signifies': 'Courage, siblings, property, energy, accidents, surgery, disputes',
                'positive': 'Courage, determination, energy, technical skills, sports ability',
                'negative': 'Anger, aggression, accidents, violence, rashness',
                'element': 'Fire',
                'friends': ['Sun', 'Moon', 'Jupiter'],
                'enemies': ['Mercury'],
                'neutral': ['Venus', 'Saturn']
            },
            'Mercury': {
                'nature': 'Intellectual, communicative, adaptable',
                'signifies': 'Intelligence, speech, business, education, wit, mathematics',
                'positive': 'Intelligence, communication, business acumen, analytical ability',
                'negative': 'Nervousness, indecision, cunningness, restlessness',
                'element': 'Earth',
                'friends': ['Sun', 'Venus'],
                'enemies': ['Moon'],
                'neutral': ['Mars', 'Jupiter', 'Saturn']
            },
            'Jupiter': {
                'nature': 'Guru, teacher, wise, benevolent',
                'signifies': 'Wisdom, children, wealth, dharma, teachers, fortune, expansion',
                'positive': 'Wisdom, prosperity, optimism, teaching ability, spirituality',
                'negative': 'Over-optimism, excess, judgmental, self-righteousness',
                'element': 'Ether',
                'friends': ['Sun', 'Moon', 'Mars'],
                'enemies': ['Mercury', 'Venus'],
                'neutral': ['Saturn']
            },
            'Venus': {
                'nature': 'Artistic, sensual, harmonious',
                'signifies': 'Love, marriage, arts, beauty, luxury, vehicles, pleasure',
                'positive': 'Artistic talent, beauty, relationships, diplomacy, luxury',
                'negative': 'Indulgence, laziness, excess pleasure-seeking',
                'element': 'Water',
                'friends': ['Mercury', 'Saturn'],
                'enemies': ['Sun', 'Moon'],
                'neutral': ['Mars', 'Jupiter']
            },
            'Saturn': {
                'nature': 'Disciplinarian, karmic, restrictive',
                'signifies': 'Karma, discipline, delays, hard work, servants, longevity',
                'positive': 'Discipline, patience, hard work, responsibility, longevity',
                'negative': 'Delays, obstacles, depression, hardship, isolation',
                'element': 'Air',
                'friends': ['Mercury', 'Venus'],
                'enemies': ['Sun', 'Moon', 'Mars'],
                'neutral': ['Jupiter']
            },
            'Rahu': {
                'nature': 'Shadowy, material, obsessive',
                'signifies': 'Illusion, foreign lands, technology, sudden events, material desires',
                'positive': 'Innovation, foreign success, technology skills, unconventional gains',
                'negative': 'Obsession, confusion, addictions, deception, sudden losses',
                'element': 'Air',
                'friends': ['Mercury', 'Venus', 'Saturn'],
                'enemies': ['Sun', 'Moon', 'Mars'],
                'neutral': ['Jupiter']
            },
            'Ketu': {
                'nature': 'Spiritual, detached, mystical',
                'signifies': 'Spirituality, moksha, past life, detachment, mysticism, research',
                'positive': 'Spiritual insight, research ability, mysticism, healing powers',
                'negative': 'Detachment, confusion, losses, accidents, isolation',
                'element': 'Fire',
                'friends': ['Mars', 'Jupiter'],
                'enemies': ['Sun', 'Moon'],
                'neutral': ['Mercury', 'Venus', 'Saturn']
            }
        }
        
        self.house_significations = {
            1: {
                'name': 'Ascendant/Lagna (Tanu Bhava)',
                'signifies': 'Self, personality, physical body, health, appearance, overall life path',
                'keywords': 'identity, constitution, vitality, temperament, first impressions'
            },
            2: {
                'name': 'Dhana Bhava',
                'signifies': 'Wealth, family, speech, food, early childhood, accumulated wealth',
                'keywords': 'finances, possessions, values, self-worth, voice, eyes, face'
            },
            3: {
                'name': 'Sahaja Bhava',
                'signifies': 'Siblings, courage, short travels, communication, skills, hobbies',
                'keywords': 'efforts, neighbors, writing, hands, mental strength'
            },
            4: {
                'name': 'Sukha Bhava',
                'signifies': 'Mother, happiness, home, property, vehicles, education, inner peace',
                'keywords': 'emotions, domestic life, real estate, comforts, heart'
            },
            5: {
                'name': 'Putra Bhava',
                'signifies': 'Children, intelligence, creativity, romance, speculation, dharma',
                'keywords': 'education, past karma, mantras, stomach, progeny'
            },
            6: {
                'name': 'Ripu/Roga Bhava',
                'signifies': 'Enemies, diseases, debts, obstacles, service, competitions, litigation',
                'keywords': 'health issues, disputes, maternal uncles, pets'
            },
            7: {
                'name': 'Kalatra Bhava',
                'signifies': 'Marriage, spouse, partnerships, business, travel, public dealings',
                'keywords': 'relationships, contracts, desires, sexual organs'
            },
            8: {
                'name': 'Ayur Bhava',
                'signifies': 'Longevity, transformation, occult, inheritance, sudden events, death',
                'keywords': 'mysteries, research, hidden matters, chronic diseases'
            },
            9: {
                'name': 'Dharma Bhava',
                'signifies': 'Father, guru, religion, long travels, fortune, higher learning, dharma',
                'keywords': 'wisdom, pilgrimage, grandchildren, philosophy, thighs'
            },
            10: {
                'name': 'Karma Bhava',
                'signifies': 'Career, profession, status, reputation, authority, achievements',
                'keywords': 'public image, government, actions, knees, fame'
            },
            11: {
                'name': 'Labha Bhava',
                'signifies': 'Gains, income, elder siblings, friendships, fulfillment of desires',
                'keywords': 'profits, achievements, social network, left ear'
            },
            12: {
                'name': 'Vyaya Bhava',
                'signifies': 'Losses, expenses, foreign lands, spirituality, liberation, isolation',
                'keywords': 'moksha, hospitals, sleep, feet, secret enemies'
            }
        }
        
        self.sign_characteristics = {
            'Aries': {'element': 'Fire', 'quality': 'Movable', 'lord': 'Mars', 'nature': 'Bold, pioneering, impulsive, leadership'},
            'Taurus': {'element': 'Earth', 'quality': 'Fixed', 'lord': 'Venus', 'nature': 'Stable, material, sensual, determined'},
            'Gemini': {'element': 'Air', 'quality': 'Dual', 'lord': 'Mercury', 'nature': 'Intellectual, communicative, versatile'},
            'Cancer': {'element': 'Water', 'quality': 'Movable', 'lord': 'Moon', 'nature': 'Emotional, nurturing, sensitive'},
            'Leo': {'element': 'Fire', 'quality': 'Fixed', 'lord': 'Sun', 'nature': 'Royal, authoritative, creative, proud'},
            'Virgo': {'element': 'Earth', 'quality': 'Dual', 'lord': 'Mercury', 'nature': 'Analytical, practical, service-oriented'},
            'Libra': {'element': 'Air', 'quality': 'Movable', 'lord': 'Venus', 'nature': 'Balanced, diplomatic, artistic'},
            'Scorpio': {'element': 'Water', 'quality': 'Fixed', 'lord': 'Mars', 'nature': 'Intense, mysterious, transformative'},
            'Sagittarius': {'element': 'Fire', 'quality': 'Dual', 'lord': 'Jupiter', 'nature': 'Philosophical, adventurous, optimistic'},
            'Capricorn': {'element': 'Earth', 'quality': 'Movable', 'lord': 'Saturn', 'nature': 'Disciplined, ambitious, practical'},
            'Aquarius': {'element': 'Air', 'quality': 'Fixed', 'lord': 'Saturn', 'nature': 'Humanitarian, unconventional, intellectual'},
            'Pisces': {'element': 'Water', 'quality': 'Dual', 'lord': 'Jupiter', 'nature': 'Spiritual, compassionate, imaginative'}
        }
        
    def get_planet_info(self, planet: str) -> str:
        """Get detailed information about a planet"""
        if planet not in self.planet_nature:
            return f"Information about {planet} not available."
        
        info = self.planet_nature[planet]
        response = f"**{planet} in Vedic Astrology:**\n\n"
        response += f"**Nature:** {info['nature']}\n\n"
        response += f"**Signifies:** {info['signifies']}\n\n"
        response += f"**Positive Qualities:** {info['positive']}\n\n"
        response += f"**Negative Qualities:** {info['negative']}\n\n"
        response += f"**Element:** {info['element']}\n\n"
        response += f"**Friends:** {', '.join(info['friends'])}\n\n"
        response += f"**Enemies:** {', '.join(info['enemies']) if info['enemies'] else 'None'}\n\n"
        
        return response
    
    def get_house_info(self, house_num: int) -> str:
        """Get detailed information about a house"""
        if house_num not in self.house_significations:
            return f"House {house_num} information not available."
        
        info = self.house_significations[house_num]
        response = f"**{house_num}th House - {info['name']}:**\n\n"
        response += f"**Signifies:** {info['signifies']}\n\n"
        response += f"**Keywords:** {info['keywords']}\n\n"
        
        return response
    
    def _get_timing_predictions(self, chart_data: dict, favorable_planets: list, purpose: str) -> str:
        """Helper method to generate timing predictions based on dashas"""
        response = ""
        
        if not chart_data or 'dashas' not in chart_data or not chart_data['dashas']:
            response += "\n⚠️ To get specific timing predictions, calculate your full birth chart with Dasha periods.\n"
            response += f"\n**General Favorable Periods for {purpose}:**\n"
            for planet in favorable_planets:
                response += f"• {planet} dasha/antardasha\n"
            return response
        
        response += f"\n**📅 TIMING PREDICTIONS - When is the Best Time for {purpose}:**\n\n"
        
        from datetime import datetime
        dashas = chart_data['dashas']
        today = datetime.now()
        
        # Find current dasha
        current_dasha = None
        next_dashas = []
        
        for i, dasha in enumerate(dashas):
            # Handle both formats: 'start_date'/'end_date' and 'maha_dasha_start'/'maha_dasha_end'
            start = dasha.get('start_date') or dasha.get('maha_dasha_start')
            end = dasha.get('end_date') or dasha.get('maha_dasha_end')
            
            # Skip if dates are None
            if start is None or end is None:
                continue
                
            if isinstance(start, str):
                try:
                    start = datetime.fromisoformat(start.replace('Z', '+00:00'))
                except:
                    try:
                        start = datetime.strptime(start, '%Y-%m-%d')
                    except:
                        continue
            if isinstance(end, str):
                try:
                    end = datetime.fromisoformat(end.replace('Z', '+00:00'))
                except:
                    try:
                        end = datetime.strptime(end, '%Y-%m-%d')
                    except:
                        continue
            
            if start and end and start <= today <= end:
                current_dasha = dasha
                # Get next 3-4 dashas
                next_dashas = dashas[i:i+5]
                break
        
        if current_dasha:
            # Handle both 'planet' and 'maha_dasha_lord' keys
            planet_name = current_dasha.get('planet') or current_dasha.get('maha_dasha_lord', '')
            end_date = current_dasha.get('end_date') or current_dasha.get('maha_dasha_end')
            
            if isinstance(end_date, str):
                try:
                    end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                except:
                    try:
                        end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    except:
                        end_date = None
            
            response += f"**Current Period:** {planet_name} Mahadasha"
            if end_date:
                response += f" (until {end_date.strftime('%B %Y')})"
            response += "\n\n"
            
            # Check if current dasha is favorable
            if planet_name in favorable_planets:
                response += f"✅ **EXCELLENT TIME!** {planet_name} dasha is HIGHLY FAVORABLE for {purpose}!\n"
                response += f"   🎯 **Recommendation:** You can pursue {purpose} ANYTIME during this period\n\n"
            else:
                response += f"⏳ Current {planet_name} period is neutral for {purpose}\n\n"
            
            # Analyze upcoming dashas
            response += "**Upcoming Favorable Periods:**\n"
            found_favorable = False
            for dasha in next_dashas[1:]:  # Skip current dasha
                planet_name = dasha.get('planet') or dasha.get('maha_dasha_lord', '')
                start_date = dasha.get('start_date') or dasha.get('maha_dasha_start')
                end_date = dasha.get('end_date') or dasha.get('maha_dasha_end')
                
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    except:
                        try:
                            start_date = datetime.strptime(start_date, '%Y-%m-%d')
                        except:
                            continue
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    except:
                        try:
                            end_date = datetime.strptime(end_date, '%Y-%m-%d')
                        except:
                            continue
                
                if planet_name in favorable_planets and start_date and end_date:
                    response += f"\n🌟 **{planet_name} Mahadasha:** {start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}\n"
                    response += f"   → This is a HIGHLY favorable period for {purpose}\n"
                    found_favorable = True
            
            if not found_favorable:
                response += "\n💡 **Note:** While major favorable planets aren't in upcoming Mahadashas, you can still pursue during:\n"
                response += "   • Favorable **Antardashas** (sub-periods) of any Mahadasha\n"
                for planet in favorable_planets:
                    response += f"   • {planet} Antardasha periods\n"
        else:
            response += "⚠️ Dasha information not fully available. General guidance:\n"
            for planet in favorable_planets:
                response += f"• {planet} dasha/antardasha - Favorable period\n"
        
        return response
    
    def answer_question(self, question: str, chart_data: dict = None) -> str:
        """Answer astrology questions using built-in knowledge"""
        question_lower = question.lower()
        
        # Planet-specific questions
        for planet in self.planet_nature.keys():
            if planet.lower() in question_lower:
                if 'what is' in question_lower or 'tell me about' in question_lower or 'information' in question_lower:
                    return self.get_planet_info(planet)
        
        # House-specific questions
        for house_num in range(1, 13):
            if f'{house_num}th house' in question_lower or f'{house_num} house' in question_lower:
                return self.get_house_info(house_num)
        
        # General topics
        if 'career' in question_lower or 'profession' in question_lower or 'job' in question_lower or 'promotion' in question_lower or 'promoted' in question_lower:
            return self._answer_career_question(chart_data)
        
        if 'business' in question_lower or 'entrepreneur' in question_lower or 'startup' in question_lower:
            return self._answer_business_question(chart_data)
        
        if 'marriage' in question_lower or 'spouse' in question_lower or 'partner' in question_lower or 'married' in question_lower or 'wedding' in question_lower:
            return self._answer_marriage_question(chart_data)
        
        if 'wealth' in question_lower or 'money' in question_lower or 'finance' in question_lower or 'income' in question_lower or 'earning' in question_lower:
            return self._answer_wealth_question(chart_data)
        
        if 'health' in question_lower or 'disease' in question_lower or 'illness' in question_lower:
            return self._answer_health_question(chart_data)
        
        if 'children' in question_lower or 'kids' in question_lower or 'baby' in question_lower or 'pregnant' in question_lower:
            return self._answer_children_question(chart_data)
        
        if 'education' in question_lower or 'study' in question_lower or 'studies' in question_lower or 'exam' in question_lower or 'degree' in question_lower:
            return self._answer_education_question(chart_data)
        
        if 'property' in question_lower or 'house' in question_lower or 'home' in question_lower or 'vehicle' in question_lower or 'car' in question_lower:
            return self._answer_property_question(chart_data)
        
        if 'foreign' in question_lower or 'abroad' in question_lower or 'travel' in question_lower or 'settlement' in question_lower or 'overseas' in question_lower:
            return self._answer_foreign_question(chart_data)
        
        if 'luck' in question_lower or 'fortune' in question_lower or 'blessed' in question_lower:
            return self._answer_fortune_question(chart_data)
        
        # General response
        return self._general_guidance()
    
    def _get_planet_attr(self, planet, attr: str, default=''):
        """Safely get planet attribute from either PlanetPosition object, dict, or string representation"""
        if planet is None:
            return default
        
        # If it's an object with the attribute
        if hasattr(planet, attr):
            return getattr(planet, attr)
        
        # If it's a dictionary
        if isinstance(planet, dict):
            return planet.get(attr, default)
        
        # If it's a string representation like "PlanetPosition(name='Venus', sign='Libra', ...)"
        if isinstance(planet, str) and 'PlanetPosition(' in planet:
            import re
            # Extract the attribute value from the string
            pattern = rf"{attr}='([^']+)'|{attr}=(\d+\.?\d*)|{attr}=(True|False)"
            match = re.search(pattern, planet)
            if match:
                # Return the first non-None group
                for group in match.groups():
                    if group is not None:
                        # Convert to appropriate type
                        if group in ('True', 'False'):
                            return group == 'True'
                        try:
                            return float(group) if '.' in group else int(group)
                        except ValueError:
                            return group
        
        return default
    
    def _answer_career_question(self, chart_data: dict = None) -> str:
        """Answer career-related questions with personalized predictions"""
        if not chart_data or 'planets' not in chart_data:
            return "**To answer your career question, please:**\n\n1. Go to **Birth Chart** section\n2. Calculate your birth chart first\n3. Then come back and ask your question\n\nI'll analyze your 10th house, career planets, and current dasha periods to give you specific timing and predictions!"
        
        response = "**🎯 Career Analysis for Your Birth Chart:**\n\n"
        
        # Get 10th house and ascendant
        planets = chart_data['planets']
        ascendant = planets.get('Ascendant')
        asc_sign = self._get_planet_attr(ascendant, 'sign', '')
        
        # Debug info
        if not asc_sign:
            response += f"⚠️ Ascendant data: {ascendant}\n\n"
        
        # Determine 10th house (count 10 signs from ascendant)
        signs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        if asc_sign and asc_sign in signs_list:
            asc_index = signs_list.index(asc_sign)
            tenth_house_index = (asc_index + 9) % 12
            tenth_house_sign = signs_list[tenth_house_index]
            
            response += f"🏢 **Your 10th House (Career House):** {tenth_house_sign}\n\n"
            
            # Find planets in 10th house
            planets_in_10th = []
            for planet_name, planet_data in planets.items():
                if planet_name != 'Ascendant':
                    planet_sign = self._get_planet_attr(planet_data, 'sign')
                    if planet_sign == tenth_house_sign:
                        planets_in_10th.append(planet_name)
            
            if planets_in_10th:
                response += f"**Planets in 10th House:** {', '.join(planets_in_10th)}\n\n"
                response += "This indicates:\n"
                for planet in planets_in_10th:
                    if planet in self.planet_nature:
                        response += f"• **{planet}**: {self._get_career_indication(planet)}\n"
            else:
                response += "**No planets in 10th House** - Career indicated by 10th lord's placement\n\n"
        else:
            response += f"⚠️ **Ascendant Sign:** {asc_sign if asc_sign else 'Not found'}\n\n"
            response += "**Note:** Analyzing career based on planetary periods...\n\n"
        
        # Analyze current dasha
        if 'dashas' in chart_data and chart_data['dashas']:
            dashas = chart_data['dashas']
            if dashas and len(dashas) > 0:
                # Find CURRENT dasha based on today's date
                from datetime import datetime
                today = datetime.now()
                current_dasha = None
                
                for dasha in dashas:
                    try:
                        start_str = dasha.get('antar_dasha_start', dasha.get('maha_dasha_start'))
                        end_str = dasha.get('antar_dasha_end', dasha.get('maha_dasha_end'))
                        
                        if not start_str or not end_str:
                            continue
                            
                        start = datetime.strptime(start_str, '%Y-%m-%d')
                        end = datetime.strptime(end_str, '%Y-%m-%d')
                        if start <= today <= end:
                            current_dasha = dasha
                            break
                    except:
                        continue
                
                # Fallback to first if no match found
                if not current_dasha:
                    current_dasha = dashas[0]
                
                maha_lord = current_dasha.get('maha_dasha_lord', '')
                antar_lord = current_dasha.get('antar_dasha_lord', '')
                maha_start = current_dasha.get('maha_dasha_start', '')
                maha_end = current_dasha.get('maha_dasha_end', '')
                antar_start = current_dasha.get('antar_dasha_start', '')
                antar_end = current_dasha.get('antar_dasha_end', '')
                
                response += f"\n📅 **Current Planetary Period:**\n"
                response += f"• Mahadasha: **{maha_lord}** ({maha_start} to {maha_end})\n"
                response += f"• Antardasha: **{antar_lord}** ({antar_start} to {antar_end})\n\n"
                
                # Career prediction based on dasha with exact dates
                response += "**Career Timing Predictions:**\n\n"
                response += self._predict_career_timing_with_dates(maha_lord, antar_lord, dashas, planets)
                
                # Add timing predictions using helper
                career_planets = ['Sun', 'Jupiter', 'Mercury', 'Saturn', 'Mars']
                response += "\n" + self._get_timing_predictions(chart_data, career_planets, "Career Success")
        else:
            response += "\n📊 **General Career Guidance:**\n\n"
            response += "• Focus on building skills and experience\n"
            response += "• Network with industry professionals\n"
            response += "• Career growth depends on 10th house strength and planets\n"
            response += "• Jupiter and Saturn transits significantly impact career timing\n"
        
        return response
    
    def _get_career_indication(self, planet: str) -> str:
        """Get career indication for planet in 10th house"""
        indications = {
            'Sun': 'Government jobs, administration, leadership positions, politics',
            'Moon': 'Public dealing, hospitality, healthcare, counseling roles',
            'Mars': 'Engineering, defense, police, technical fields, entrepreneurship',
            'Mercury': 'Business, communication, IT, writing, commerce, consulting',
            'Jupiter': 'Teaching, law, banking, advisory roles, management',
            'Venus': 'Arts, media, entertainment, luxury business, creative fields',
            'Saturn': 'Hard work pays off, slow but steady growth, labor-intensive work',
            'Rahu': 'Technology, foreign companies, unconventional careers, startups',
            'Ketu': 'Research, spirituality, technical research, behind-the-scenes work'
        }
        return indications.get(planet, 'influences career significantly')
    
    def _predict_career_timing(self, maha_lord: str, antar_lord: str, planets: dict) -> str:
        """Predict career promotion timing based on dasha"""
        prediction = ""
        
        # Check if current dasha is favorable for career
        career_planets = ['Sun', 'Jupiter', 'Saturn', 'Mercury', 'Mars']
        
        if maha_lord in career_planets:
            prediction += f"✅ **{maha_lord} Mahadasha is generally favorable for career growth**\n\n"
            
            if antar_lord in career_planets:
                prediction += f"⭐ **Current {antar_lord} Antardasha within {maha_lord} Mahadasha:**\n"
                prediction += f"• **Excellent time for career advancement and promotions**\n"
                prediction += f"• Expected period: **Within the next 6-18 months**\n"
                prediction += f"• Focus on: Professional development, taking initiative, networking\n\n"
            else:
                prediction += f"⏳ **Current {antar_lord} Antardasha:**\n"
                prediction += f"• Moderate period - prepare groundwork for future growth\n"
                prediction += f"• Better opportunities expected when: Jupiter, Sun, or Saturn antardasha begins\n\n"
        else:
            prediction += f"⏳ **{maha_lord} Mahadasha:**\n"
            prediction += f"• Current period focuses on other life areas\n"
            prediction += f"• Career growth possible during favorable antardashas\n"
            prediction += f"• Best antardashas for promotion: **Jupiter, Sun, Mercury, Saturn**\n\n"
        
        # Check 10th house strength
        prediction += "💡 **Recommendations:**\n"
        prediction += "• Continue hard work and skill development\n"
        prediction += "• Network with seniors and mentors\n"
        prediction += "• Consider timing important career moves during favorable planetary transits\n"
        prediction += "• Jupiter and Saturn transits over 10th house are particularly significant\n\n"
        
        return prediction
    
    def _predict_career_timing_with_dates(self, maha_lord: str, antar_lord: str, dashas: list, planets: dict) -> str:
        """Predict career promotion timing with EXACT dates using Antardashas and D10 chart"""
        from datetime import datetime, timedelta
        
        prediction = ""
        career_planets = ['Sun', 'Jupiter', 'Saturn', 'Mercury', 'Mars']
        today = datetime.now()
        
        # Find current mahadasha
        current_maha = None
        current_maha_start = None
        current_maha_end = None
        
        for dasha in dashas:
            maha_start_str = dasha.get('maha_dasha_start', '')
            maha_end_str = dasha.get('maha_dasha_end', '')
            
            if maha_start_str and maha_end_str:
                maha_start = datetime.strptime(maha_start_str, '%Y-%m-%d')
                maha_end = datetime.strptime(maha_end_str, '%Y-%m-%d')
                
                if maha_start <= today <= maha_end:
                    current_maha = dasha.get('maha_dasha_lord', maha_lord)
                    current_maha_start = maha_start
                    current_maha_end = maha_end
                    break
        
        if not current_maha:
            # Fallback if not found
            current_maha = maha_lord
            current_maha_start = today
            current_maha_end = today + timedelta(days=7*365)  # Assume 7 years
        
        # Calculate antardashas within current mahadasha
        calc = VedicAstrologyEngine()
        antardashas = calc.calculate_antardashas(current_maha, current_maha_start, current_maha_end)
        
        prediction += f"🔮 **Current Mahadasha:** {current_maha} ({current_maha_start.strftime('%b %Y')} - {current_maha_end.strftime('%b %Y')})\n\n"
        
        # Current period analysis
        current_antar = None
        for antar in antardashas:
            antar_start = antar['start_date']
            antar_end = antar['end_date']
            if antar_start <= today <= antar_end:
                current_antar = antar
                break
        
        if current_antar:
            antar_name = current_antar['antar_dasha_lord']
            antar_end = current_antar['end_date']
            
            if antar_name in career_planets and antar_end > today:
                prime_end = min(today + timedelta(days=15), antar_end)
                days_remaining = (prime_end - today).days
                
                prediction += "✅ **CURRENT PERIOD IS FAVORABLE - ACT NOW!**\n\n"
                prediction += f"🎯 **PRIME ACTION WINDOW (Next 15 Days):** {today.strftime('%Y-%m-%d')} to {prime_end.strftime('%Y-%m-%d')}\n"
                prediction += f"• **Duration:** Next {days_remaining} days - IMMEDIATE ACTION NEEDED!\n"
                
                # Extra emphasis if ending within a week
                if days_remaining <= 7:
                    prediction += f"⚠️ **URGENT:** Only {days_remaining} day{'s' if days_remaining != 1 else ''} left in this prime window!\n"
                
                prediction += f"• **Action:** Push for promotion, apply for new positions, start important projects\n"
                prediction += f"• **Effect:** {self._get_career_planet_effect(antar_name)}\n\n"
            else:
                prediction += f"⏳ Current Antardasha: {current_maha}-{antar_name} - Preparing for upcoming opportunities\n\n"
        
        # Find FUTURE favorable antardashas
        prediction += "📅 **UPCOMING OPPORTUNITIES (Next 5 Best Windows):**\n\n"
        favorable_windows = []
        
        for antar in antardashas:
            antar_name = antar['antar_dasha_lord']
            antar_start = antar['start_date']
            antar_end = antar['end_date']
            
            # Only future periods
            if antar_start > today and antar_name in career_planets:
                # First 15 days is prime window for immediate action
                prime_window_end = min(antar_start + timedelta(days=15), antar_end)
                
                # Rate favorability
                if antar_name == 'Sun':
                    rating = "⭐⭐⭐"
                    effect = "PROMOTION, authority, leadership"
                elif antar_name == 'Jupiter':
                    rating = "⭐⭐⭐"
                    effect = "EXPANSION, new position, growth"
                elif antar_name == 'Saturn':
                    rating = "⭐⭐"
                    effect = "Recognition for hard work"
                elif antar_name == 'Mercury':
                    rating = "⭐⭐"
                    effect = "Business deals, contracts"
                elif antar_name == 'Mars':
                    rating = "⭐⭐"
                    effect = "Technical advancement, courage"
                else:
                    rating = "⭐"
                    effect = "Career progress"
                
                favorable_windows.append({
                    'planet': antar_name,
                    'start': antar_start,
                    'prime_end': prime_window_end,
                    'period_end': antar_end,
                    'rating': rating,
                    'effect': effect,
                    'days': (prime_window_end - antar_start).days
                })
        
        # Show only next 5 future opportunities
        for i, window in enumerate(favorable_windows[:5], 1):
            # Check if starting within next week
            days_until_start = (window['start'] - today).days
            next_week_notice = ""
            
            if days_until_start <= 7:
                next_week_notice = f" 🔥 **STARTING IN {days_until_start} DAY{'S' if days_until_start != 1 else ''}!**"
            elif days_until_start <= 30:
                next_week_notice = f" ⚡ Starting in {days_until_start} days"
            
            prediction += f"{i}. {window['rating']} **{window['planet']} Period - 15-DAY PRIME WINDOW**{next_week_notice}\n"
            prediction += f"   📅 **{window['start'].strftime('%Y-%m-%d')} to {window['prime_end'].strftime('%Y-%m-%d')}**\n"
            prediction += f"   ⏱️  **{window['days']} days** - Immediate action window\n"
            prediction += f"   🎯 Best for: **{window['effect']}**\n"
            prediction += f"   📌 Full Antardasha: {window['start'].strftime('%b %Y')} to {window['period_end'].strftime('%b %Y')}\n\n"
        
        if not favorable_windows:
            prediction += "⚠️ No clearly favorable antardashas in current mahadasha\n"
            prediction += f"Focus on skill building. Better periods may come in next mahadasha after {current_maha_end.strftime('%Y')}\n\n"
        
        prediction += "\n💡 **ACTION PLAN:**\n"
        prediction += "• **Mark your calendar** with the exact dates above\n"
        prediction += "• **Prepare NOW:** Update skills, build network, get visibility\n"
        prediction += "• **Act during windows:** Apply for promotions, request meetings with seniors\n"
        prediction += "• **Follow-up:** Continue efforts through the full period for maximum results\n"
        
        return prediction
    
    def _get_career_planet_effect(self, planet: str) -> str:
        """Get career effect of planet"""
        effects = {
            'Sun': 'authority, recognition, leadership positions',
            'Jupiter': 'growth, expansion, wisdom-based success',
            'Saturn': 'discipline, hard work rewards, stability',
            'Mercury': 'communication, business acumen, contracts',
            'Mars': 'energy, courage, technical skills',
        }
        return effects.get(planet, 'career progress')
    
    def _predict_timing_with_antardashas(self, maha_lord: str, antar_lord: str, dashas: list, 
                                        favorable_planets: list, context: str, emoji: str = "🎯") -> str:
        """Generic timing prediction using Antardashas - works for any question type"""
        from datetime import datetime, timedelta
        
        prediction = ""
        today = datetime.now()
        
        # Find current mahadasha
        current_maha = None
        current_maha_start = None
        current_maha_end = None
        
        for dasha in dashas:
            maha_start_str = dasha.get('maha_dasha_start', '')
            maha_end_str = dasha.get('maha_dasha_end', '')
            
            if maha_start_str and maha_end_str:
                maha_start = datetime.strptime(maha_start_str, '%Y-%m-%d')
                maha_end = datetime.strptime(maha_end_str, '%Y-%m-%d')
                
                if maha_start <= today <= maha_end:
                    current_maha = dasha.get('maha_dasha_lord', maha_lord)
                    current_maha_start = maha_start
                    current_maha_end = maha_end
                    break
        
        if not current_maha:
            current_maha = maha_lord
            current_maha_start = today
            current_maha_end = today + timedelta(days=7*365)
        
        # Calculate antardashas
        calc = VedicAstrologyEngine()
        antardashas = calc.calculate_antardashas(current_maha, current_maha_start, current_maha_end)
        
        prediction += f"🔮 **Current Mahadasha:** {current_maha} ({current_maha_start.strftime('%b %Y')} - {current_maha_end.strftime('%b %Y')})\n\n"
        
        # Current period analysis
        current_antar = None
        for antar in antardashas:
            if antar['start_date'] <= today <= antar['end_date']:
                current_antar = antar
                break
        
        if current_antar:
            antar_name = current_antar['antar_dasha_lord']
            antar_end = current_antar['end_date']
            
            if antar_name in favorable_planets and antar_end > today:
                prime_end = min(today + timedelta(days=15), antar_end)
                days_remaining = (prime_end - today).days
                
                prediction += f"✅ **CURRENT PERIOD IS FAVORABLE - ACT NOW!**\n\n"
                prediction += f"{emoji} **PRIME ACTION WINDOW (Next 15 Days):** {today.strftime('%Y-%m-%d')} to {prime_end.strftime('%Y-%m-%d')}\n"
                prediction += f"• **Duration:** Next {days_remaining} days - IMMEDIATE ACTION NEEDED!\n"
                
                if days_remaining <= 7:
                    prediction += f"⚠️ **URGENT:** Only {days_remaining} day{'s' if days_remaining != 1 else ''} left in this prime window!\n"
                
                prediction += f"• **Action:** {context}\n\n"
            else:
                prediction += f"⏳ Current Antardasha: {current_maha}-{antar_name}\n\n"
        
        # Find future favorable antardashas
        prediction += f"📅 **UPCOMING OPPORTUNITIES (Next 5 Best Windows):**\n\n"
        favorable_windows = []
        
        for antar in antardashas:
            antar_name = antar['antar_dasha_lord']
            antar_start = antar['start_date']
            antar_end = antar['end_date']
            
            if antar_start > today and antar_name in favorable_planets:
                prime_window_end = min(antar_start + timedelta(days=15), antar_end)
                favorable_windows.append({
                    'planet': antar_name,
                    'start': antar_start,
                    'prime_end': prime_window_end,
                    'period_end': antar_end,
                    'days': (prime_window_end - antar_start).days
                })
        
        for i, window in enumerate(favorable_windows[:5], 1):
            days_until_start = (window['start'] - today).days
            next_week_notice = ""
            
            if days_until_start <= 7:
                next_week_notice = f" 🔥 **STARTING IN {days_until_start} DAY{'S' if days_until_start != 1 else ''}!**"
            elif days_until_start <= 30:
                next_week_notice = f" ⚡ Starting in {days_until_start} days"
            
            prediction += f"{i}. ⭐⭐⭐ **{window['planet']} Period - 15-DAY WINDOW**{next_week_notice}\n"
            prediction += f"   📅 **{window['start'].strftime('%Y-%m-%d')} to {window['prime_end'].strftime('%Y-%m-%d')}**\n"
            prediction += f"   ⏱️  **{window['days']} days** - Immediate action window\n"
            prediction += f"   📌 Full Antardasha: {window['start'].strftime('%b %Y')} to {window['period_end'].strftime('%b %Y')}\n\n"
        
        if not favorable_windows:
            prediction += "⚠️ No clearly favorable antardashas in current mahadasha\n\n"
        
        return prediction
    
    def _answer_marriage_question(self, chart_data: dict = None) -> str:
        """Answer marriage-related questions with personalized predictions"""
        if not chart_data or 'planets' not in chart_data:
            return "**To answer your marriage question, please:**\n\n1. Go to **Birth Chart** section\n2. Calculate your birth chart first\n3. Then come back and ask your question\n\nI'll analyze your 7th house, Venus/Jupiter placement, and dasha periods to predict marriage timing!"
        
        response = "**💑 Marriage Analysis for Your Birth Chart:**\n\n"
        
        planets = chart_data['planets']
        ascendant = planets.get('Ascendant')
        asc_sign = self._get_planet_attr(ascendant, 'sign', '')
        
        signs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        if asc_sign in signs_list:
            asc_index = signs_list.index(asc_sign)
            seventh_house_index = (asc_index + 6) % 12
            seventh_house_sign = signs_list[seventh_house_index]
            
            response += f"💑 **Your 7th House (Marriage House):** {seventh_house_sign}\n\n"
            
            # Find planets in 7th house
            planets_in_7th = []
            for planet_name, planet_data in planets.items():
                if planet_name != 'Ascendant':
                    planet_sign = self._get_planet_attr(planet_data, 'sign')
                    if planet_sign == seventh_house_sign:
                        planets_in_7th.append(planet_name)
            
            if planets_in_7th:
                response += f"**Planets in 7th House:** {', '.join(planets_in_7th)}\n"
                response += "These indicate specific marriage characteristics.\n\n"
        
        # Check Venus and Jupiter positions
        venus = planets.get('Venus')
        jupiter = planets.get('Jupiter')
        
        venus_sign = self._get_planet_attr(venus, 'sign', 'N/A')
        venus_house = self._get_planet_attr(venus, 'house', 'N/A')
        jupiter_sign = self._get_planet_attr(jupiter, 'sign', 'N/A')
        
        response += f"**Venus (Karaka for spouse):**\n"
        response += f"• Sign: **{venus_sign}**\n"
        response += f"• House: **{venus_house}**\n"
        response += f"• Meaning: {self._interpret_venus_marriage(venus)}\n\n"
        
        response += f"**Jupiter (Karaka for husband/blessings):**\n"
        response += f"• Sign: **{jupiter_sign}**\n\n"
        
        # Marriage timing from dasha
        if 'dashas' in chart_data and chart_data['dashas']:
            dashas = chart_data['dashas']
            # Find CURRENT dasha based on today's date
            from datetime import datetime
            today = datetime.now()
            current_dasha = None
            
            for dasha in dashas:
                try:
                    start_str = dasha.get('antar_dasha_start', dasha.get('maha_dasha_start'))
                    end_str = dasha.get('antar_dasha_end', dasha.get('maha_dasha_end'))
                    
                    if not start_str or not end_str:
                        continue
                        
                    start = datetime.strptime(start_str, '%Y-%m-%d')
                    end = datetime.strptime(end_str, '%Y-%m-%d')
                    if start <= today <= end:
                        current_dasha = dasha
                        break
                except:
                    continue
            
            # Fallback to first if no match found
            if not current_dasha:
                current_dasha = dashas[0]
            
            maha_lord = current_dasha.get('maha_dasha_lord', '')
            antar_lord = current_dasha.get('antar_dasha_lord', '')
            
            # Get dasha dates if available
            maha_start = current_dasha.get('maha_dasha_start', '')
            maha_end = current_dasha.get('maha_dasha_end', '')
            antar_start = current_dasha.get('antar_dasha_start', '')
            antar_end = current_dasha.get('antar_dasha_end', '')
            
            response += f"\n📅 **MARRIAGE TIMING - SPECIFIC DATES:**\n\n"
            response += f"**Current Period:**\n"
            response += f"• Mahadasha: **{maha_lord}** ({maha_start} to {maha_end})\n"
            response += f"• Antardasha: **{antar_lord}** ({antar_start} to {antar_end})\n\n"
            
            response += self._predict_marriage_timing_with_dates(maha_lord, antar_lord, dashas, chart_data)
            
            # Add timing predictions using helper
            marriage_planets = ['Venus', 'Jupiter', 'Moon', 'Mercury']
            response += "\n" + self._get_timing_predictions(chart_data, marriage_planets, "Marriage")
        else:
            response += "\n📅 **Marriage Timing:**\n\n"
            response += "Calculate dasha periods for specific marriage dates.\n"
        
        return response
    
    def _interpret_venus_marriage(self, venus_data) -> str:
        """Interpret Venus placement for marriage with detailed predictions"""
        if not venus_data:
            return "Position not available"
        
        sign = self._get_planet_attr(venus_data, 'sign', '')
        house = self._get_planet_attr(venus_data, 'house', 0)
        
        interpretation = ""
        
        # Venus sign interpretation for spouse nature
        sign_meanings = {
            'Aries': "Energetic, independent spouse. Partner may be athletic, assertive, quick in decisions.",
            'Taurus': "Beautiful, sensual partner. Strong attraction, luxurious lifestyle, love for comforts.",
            'Gemini': "Intellectual, communicative spouse. Partner skilled in conversation, versatile.",
            'Cancer': "Caring, emotional partner. Domestic harmony, nurturing relationship.",
            'Leo': "Royal, confident spouse. Partner with dignity, leadership qualities.",
            'Virgo': "Practical, service-oriented partner. Analytical spouse, health-conscious.",
            'Libra': "**EXCELLENT POSITION** - Beautiful, balanced partner. Harmonious marriage, artistic spouse, diplomatic nature. Marriage brings happiness and social status.",
            'Scorpio': "Intense, passionate relationship. Deep emotional connection, transformative partnership.",
            'Sagittarius': "Philosophical, adventurous spouse. Partner may be from different culture/background.",
            'Capricorn': "Mature, responsible partner. Late but stable marriage, practical spouse.",
            'Aquarius': "Unconventional, friendly spouse. Unique relationship, intellectual connection.",
            'Pisces': "Spiritual, compassionate partner. Romantic, imaginative, artistic spouse."
        }
        
        interpretation += sign_meanings.get(sign, "Influences spouse nature.")
        
        # Venus house interpretation for marriage timing and circumstances
        if house == 9:
            interpretation += f"\n\n**Venus in 9th House** (House of Fortune & Higher Learning):\n"
            interpretation += "• Marriage brings GOOD FORTUNE and prosperity\n"
            interpretation += "• Spouse may be from different city/state or met through education/travel\n"
            interpretation += "• Partner may be religious, educated, or well-cultured\n"
            interpretation += "• Marriage likely after higher education or during travel\n"
            interpretation += "• **In-laws bring blessings** - good relationship with spouse's family"
        elif house == 7:
            interpretation += f"\n\n**Venus in 7th House** - BEST position for marriage!\n"
            interpretation += "• Beautiful, loving spouse\n"
            interpretation += "• Early marriage possible\n"
            interpretation += "• Harmonious married life"
        elif house in [1, 5, 11]:
            interpretation += f"\n\n**Venus in {house}th House** - Favorable for marriage\n"
            interpretation += "• Good marital prospects\n"
            interpretation += "• Happy relationship likely"
        
        return interpretation
    
    
    def _predict_marriage_timing_with_dates(self, maha_lord: str, antar_lord: str, dashas: list, chart_data: dict) -> str:
        """Predict marriage with EXACT future dates using Antardashas"""
        marriage_planets = ['Venus', 'Jupiter', 'Mercury', 'Moon']
        context = "Start/finalize proposals, meet potential partners, fix marriage dates"
        
        # Use generic Antardasha timing function
        prediction = self._predict_timing_with_antardashas(
            maha_lord, antar_lord, dashas, marriage_planets, context, emoji="💍"
        )
        
        # Add Jupiter transit guidance
        prediction += "\n🪐 **JUPITER TRANSIT BOOST:**\n"
        prediction += "Marriage most likely when Jupiter transits your Ascendant or 7th house\n"
        
        planets = chart_data.get('planets', {})
        ascendant = planets.get('Ascendant')
        asc_sign = self._get_planet_attr(ascendant, 'sign', '')
        
        if asc_sign:
            signs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            if asc_sign in signs_list:
                asc_index = signs_list.index(asc_sign)
                seventh_sign = signs_list[(asc_index + 6) % 12]
                prediction += f"• Through **{asc_sign}** (Ascendant) - Very favorable\n"
                prediction += f"• Through **{seventh_sign}** (7th house) - Highly favorable\n\n"
        
        prediction += "\n💡 **MARRIAGE ACTION PLAN:**\n"
        prediction += "• **Mark your calendar** with the dates above\n"
        prediction += "• **Start now:** Build social connections, meet people\n"
        prediction += "• **Act during windows:** Actively search, finalize proposals\n"
        prediction += "• **Don't delay:** Prime windows are limited - use them wisely\n"
        
        return prediction
    
    def _predict_marriage_timing(self, maha_lord: str, planets: dict) -> str:
        """Predict marriage timing with specific age ranges and periods"""
        marriage_planets = ['Venus', 'Jupiter', 'Moon', 'Mercury']
        
        prediction = ""
        
        if maha_lord == 'Venus':
            prediction += "⭐ **EXCELLENT PERIOD FOR MARRIAGE!**\n\n"
            prediction += "**Venus Mahadasha** is THE BEST time for marriage:\n"
            prediction += "• ✅ **Marriage highly likely within current Venus period**\n"
            prediction += "• ✅ Ideal time: **Venus-Venus, Venus-Jupiter, or Venus-Mercury antardasha**\n"
            prediction += "• ✅ Expected timeframe: **Within next 6-24 months**\n"
            prediction += "• This is THE TIME - delays unlikely\n"
            prediction += "• Partner may come through social circles, artistic events, or celebrations\n\n"
            prediction += "**Recommendation:** Actively pursue marriage proposals NOW. This period won't return for 20 years!\n"
        
        elif maha_lord == 'Jupiter':
            prediction += "⭐ **HIGHLY FAVORABLE FOR MARRIAGE!**\n\n"
            prediction += "**Jupiter Mahadasha** brings marriage blessings:\n"
            prediction += "• ✅ **Marriage very likely in current period**\n"
            prediction += "• ✅ Best antardashas: Jupiter-Venus, Jupiter-Moon, Jupiter-Mercury\n"
            prediction += "• ✅ Expected timeframe: **Within 1-3 years**\n"
            prediction += "• Spouse may be educated, religious, or from good family\n"
            prediction += "• Marriage brings prosperity and family happiness\n\n"
            prediction += "**Recommendation:** Excellent time to finalize marriage arrangements.\n"
        
        elif maha_lord == 'Moon':
            prediction += "✅ **FAVORABLE FOR MARRIAGE**\n\n"
            prediction += "**Moon Mahadasha** supports marriage:\n"
            prediction += "• Marriage possible during **Moon-Venus or Moon-Jupiter antardasha**\n"
            prediction += "• Expected: **Within 2-4 years** (depends on antardasha)\n"
            prediction += "• Emotional readiness is key - family plays important role\n"
            prediction += "• Partner may be caring, nurturing, family-oriented\n\n"
        
        elif maha_lord == 'Mercury':
            prediction += "✅ **GOOD PERIOD FOR MARRIAGE**\n\n"
            prediction += "**Mercury Mahadasha:**\n"
            prediction += "• Marriage likely during **Mercury-Venus or Mercury-Jupiter antardasha**\n"
            prediction += "• Expected: **Within 2-5 years**\n"
            prediction += "• Partner may be intelligent, communicative, business-minded\n"
            prediction += "• Meeting through professional or educational circles\n\n"
        
        elif maha_lord in ['Sun', 'Mars', 'Saturn']:
            prediction += f"⏳ **{maha_lord.upper()} MAHADASHA** - Marriage possible but with effort:\n\n"
            prediction += f"• {maha_lord} dasha not primarily for marriage\n"
            prediction += "• **BEST TIMING within this period:**\n"
            prediction += "  - **Venus antardasha** (most favorable)\n"
            prediction += "  - **Jupiter antardasha** (very good)\n"
            prediction += "  - **Mercury/Moon antardasha** (moderate)\n\n"
            prediction += "• Expected: **3-7 years** (when favorable antardasha comes)\n"
            prediction += "• Also check Jupiter transits over 7th house from Moon/Ascendant\n\n"
            prediction += "**Important:** Don't wait indefinitely - sometimes arranged proposals work better in challenging periods.\n"
        
        else:  # Rahu or Ketu
            prediction += f"⚠️ **{maha_lord.upper()} MAHADASHA** - Non-traditional timing:\n\n"
            prediction += "• Rahu/Ketu periods can bring unexpected proposals\n"
            prediction += "• Marriage may happen in **unconventional way**\n"
            prediction += "• Partner may be from different background/culture\n"
            prediction += "• Best timing: **Venus or Jupiter antardasha within this period**\n"
            prediction += "• Expected: **2-6 years**\n\n"
            prediction += "**Recommendation:** Keep mind open to non-traditional matches or circumstances.\n"
        
        return prediction
    
    def _answer_wealth_question(self, chart_data: dict = None) -> str:
        """Answer wealth-related questions with personalized predictions"""
        if not chart_data or 'planets' not in chart_data:
            return "**To answer your wealth question, please:**\n\n1. Go to **Birth Chart** section\n2. Calculate your birth chart first\n3. Then come back and ask your question\n\nI'll analyze your 2nd house (wealth), 11th house (gains), and Jupiter placement to predict financial prospects!"
        
        response = "**Wealth Analysis for Your Birth Chart:**\n\n"
        
        planets = chart_data['planets']
        jupiter = planets.get('Jupiter')
        
        jupiter_sign = self._get_planet_attr(jupiter, 'sign', 'N/A')
        jupiter_house = self._get_planet_attr(jupiter, 'house', 'N/A')
        response += f"💰 **Jupiter (Wealth Karaka):** {jupiter_sign} in {jupiter_house}th house\n\n"
        
        # Check for wealth yogas
        response += "**Financial Prospects:**\n"
        response += "• Jupiter's placement influences overall prosperity and expansion\n"
        response += "• Strong Jupiter brings opportunities for wealth accumulation\n"
        response += "• Current planetary periods affect income and financial gains\n\n"
        
        if 'dashas' in chart_data:
            dashas = chart_data['dashas']
            if dashas:
                current_dasha = dashas[0]
                maha_lord = current_dasha.get('maha_dasha_lord', '')
                antar_lord = current_dasha.get('antar_dasha_lord', '')
                
                response += f"📅 **Wealth Timing Analysis:**\n\n"
                response += self._predict_wealth_timing_with_dates(maha_lord, antar_lord, dashas)
                
                # Add timing predictions using helper
                wealth_planets = ['Jupiter', 'Venus', 'Mercury', 'Sun']
                response += "\n" + self._get_timing_predictions(chart_data, wealth_planets, "Wealth Accumulation")
        
        return response
    
    def _predict_wealth_timing_with_dates(self, maha_lord: str, antar_lord: str, dashas: list) -> str:
        """Predict wealth timing using Antardashas"""
        wealth_planets = ['Jupiter', 'Venus', 'Mercury', 'Sun']
        context = "Start investments, launch business, negotiate salary/contracts, make major purchases"
        
        return self._predict_timing_with_antardashas(
            maha_lord, antar_lord, dashas, wealth_planets, context, emoji="💰"
        ) + "\n💡 **WEALTH ACTION PLAN:**\n• **During favorable periods:** Invest, expand business, negotiate raises\n• **Prepare now:** Research investments, build skills for income growth\n• **Diversify:** Don't rely on single source - multiple income streams\n"
    
    def _predict_wealth_timing(self, maha_lord: str) -> str:
        """Predict wealth timing"""
        wealth_planets = ['Jupiter', 'Venus', 'Mercury']
        
        if maha_lord in wealth_planets:
            return f"✅ **{maha_lord} Mahadasha favors wealth accumulation**\n\n• Good time for investments, business expansion\n• Income growth likely in current period\n• Focus on saving and long-term financial planning\n"
        elif maha_lord == 'Sun':
            return "⭐ **Sun Mahadasha:** Government benefits, stable income, authority-based earnings\n"
        elif maha_lord == 'Saturn':
            return "💪 **Saturn Mahadasha:** Slow but steady wealth growth through hard work and discipline\n"
        else:
            return f"⏳ **{maha_lord} Mahadasha:** Wealth depends on effort; best gains during Jupiter/Venus/Mercury antardashas\n"
    
    def _answer_health_question(self, chart_data: dict = None) -> str:
        """Answer health-related questions"""
        response = "**Health in Vedic Astrology:**\n\n"
        response += "Health is seen through:\n"
        response += "• **1st House (Lagna)** - Overall vitality and constitution\n"
        response += "• **6th House** - Diseases, acute illnesses\n"
        response += "• **8th House** - Chronic diseases, longevity\n"
        response += "• **Sun** - Vitality, general health\n"
        response += "• **Moon** - Mental health, emotions\n\n"
        
        response += "**Planet-Disease Associations:**\n"
        response += "• **Sun** - Heart, eyes, bones, fever\n"
        response += "• **Moon** - Mind, fluids, lungs, stomach\n"
        response += "• **Mars** - Blood, accidents, inflammation, surgery\n"
        response += "• **Mercury** - Nervous system, skin, speech\n"
        response += "• **Jupiter** - Liver, obesity, blood sugar\n"
        response += "• **Venus** - Reproductive system, kidneys, diabetes\n"
        response += "• **Saturn** - Chronic diseases, bones, teeth, knees\n"
        response += "• **Rahu** - Mysterious diseases, addictions, phobias\n"
        response += "• **Ketu** - Viral infections, spiritual ailments\n\n"
        
        # Add timing predictions if chart data available
        if chart_data and 'dashas' in chart_data:
            health_planets = ['Sun', 'Moon', 'Jupiter']
            response += self._get_timing_predictions(chart_data, health_planets, "Good Health & Vitality")
        else:
            response += "*For specific health timing analysis, calculate your birth chart first.*\n\n"
        
        return response
    
    def _answer_children_question(self, chart_data: dict = None) -> str:
        """Answer children-related questions"""
        response = "**Children in Vedic Astrology:**\n\n"
        response += "Children are analyzed through:\n"
        response += "• **5th House (Putra Bhava)** - Primary house of children\n"
        response += "• **Jupiter** - Natural significator of children\n"
        response += "• **9th House** - Fortune, blessings, grandchildren\n\n"
        
        response += "**Indicators of Children:**\n"
        response += "• Benefic planets in 5th house\n"
        response += "• 5th lord well placed and strong\n"
        response += "• Jupiter well placed\n"
        response += "• Beneficial aspects on 5th house\n\n"
        
        response += "**Timing of Children:**\n"
        response += "• Usually during dasha of 5th lord or Jupiter\n"
        response += "• Jupiter transit over 5th house or its lord\n"
        response += "• Consider medical factors as well\n\n"
        
        # Add timing predictions if chart data available
        if chart_data and 'dashas' in chart_data:
            children_planets = ['Jupiter', 'Sun', 'Venus']
            response += self._get_timing_predictions(chart_data, children_planets, "Conceiving Children")
        else:
            response += "*For specific timing predictions, calculate your birth chart first.*\n\n"
        
        return response
    
    def _answer_business_question(self, chart_data: dict = None) -> str:
        """Answer business-related questions with detailed personalized analysis"""
        if not chart_data or 'planets' not in chart_data:
            return "**To answer your business question, please:**\n\n1. Go to **Birth Chart** section\n2. Calculate your birth chart first\n3. Then come back and ask your question\n\nI'll analyze your 10th house, Mercury, Mars placement for business prospects!"
        
        response = "**🏢 Business Suitability Analysis for Your Birth Chart:**\n\n"
        
        planets = chart_data['planets']
        ascendant = planets.get('Ascendant')
        asc_sign = self._get_planet_attr(ascendant, 'sign')
        
        signs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        # Calculate business houses
        if asc_sign in signs_list:
            asc_index = signs_list.index(asc_sign)
            second_house = signs_list[(asc_index + 1) % 12]
            tenth_house = signs_list[(asc_index + 9) % 12]
            eleventh_house = signs_list[(asc_index + 10) % 12]
            
            response += f"**📊 Your Business Houses:**\n"
            response += f"• **2nd House (Wealth):** {second_house}\n"
            response += f"• **10th House (Career/Business):** {tenth_house}\n"
            response += f"• **11th House (Gains):** {eleventh_house}\n\n"
            
            # Find planets in business houses
            business_planets = []
            for planet_name, planet_data in planets.items():
                if planet_name != 'Ascendant' and hasattr(planet_data, 'sign'):
                    if planet_data.sign in [second_house, tenth_house, eleventh_house]:
                        business_planets.append(f"{planet_name} in {planet_data.sign}")
            
            if business_planets:
                response += f"**✨ Planets in Business Houses:**\n"
                for p in business_planets:
                    response += f"• {p}\n"
                response += "\n**This is VERY favorable for business!** ✅\n\n"
        
        # Analyze key business planets
        mercury = planets.get('Mercury')
        mars = planets.get('Mars')
        rahu = planets.get('Rahu')
        jupiter = planets.get('Jupiter')
        
        response += "**🌟 Key Business Planet Analysis:**\n\n"
        
        if mercury:
            merc_sign = self._get_planet_attr(mercury, 'sign')
            response += f"**Mercury (Trade & Commerce):**\n"
            response += f"• Position: {merc_sign} sign\n"
            response += f"• Indicates: {self._get_business_type_mercury(merc_sign)}\n"
            response += f"• Strength: {self._analyze_planet_strength(mercury)}\n\n"
        
        if mars:
            mars_sign = self._get_planet_attr(mars, 'sign')
            response += f"**Mars (Entrepreneurship):**\n"
            response += f"• Position: {mars_sign} sign\n"
            response += f"• Indicates: {self._get_business_type_mars(mars_sign)}\n"
            response += f"• Energy Level: {self._analyze_mars_energy(mars_sign)}\n\n"
        
        if rahu:
            rahu_sign = self._get_planet_attr(rahu, 'sign')
            response += f"**Rahu (Unconventional Business):**\n"
            response += f"• Position: {rahu_sign} sign\n"
            response += f"• Indicates: Technology, foreign trade, innovative ventures\n\n"
        
        # Business suitability verdict
        response += "**🎯 Business vs Job - Recommendation:**\n\n"
        response += self._analyze_business_suitability(planets, asc_sign)
        
        # Timing analysis
        if 'dashas' in chart_data and chart_data['dashas']:
            current_dasha = chart_data['dashas'][0]
            maha_lord = current_dasha.get('maha_dasha_lord', '')
            antar_lord = current_dasha.get('antar_dasha_lord', '')
            dashas = chart_data['dashas']
            
            response += f"\n**⏰ Business Timing Analysis:**\n\n"
            response += self._analyze_business_timing_with_dates(maha_lord, antar_lord, dashas)
        
        # Recommended business types
        response += "\n**💼 Recommended Business Types for You:**\n"
        response += self._recommend_business_types(mercury, mars, rahu, jupiter)
        
        return response
    
    def _get_business_type_mercury(self, sign: str) -> str:
        """Get business type based on Mercury placement"""
        business_types = {
            'Aries': 'Fast-paced trading, sports equipment',
            'Taurus': 'Banking, luxury goods, jewelry',
            'Gemini': 'Communication, media, publishing, IT (EXCELLENT)',
            'Cancer': 'Food business, hospitality, real estate',
            'Leo': 'Entertainment, creative services, leadership training',
            'Virgo': 'Healthcare, analytics, consulting, accounting (EXCELLENT)',
            'Libra': 'Partnership business, fashion, legal services',
            'Scorpio': 'Research, investigation, occult sciences',
            'Sagittarius': 'Education, publishing, travel business',
            'Capricorn': 'Traditional business, manufacturing, construction',
            'Aquarius': 'Technology, innovation, social enterprises',
            'Pisces': 'Creative arts, healing, spirituality-based business'
        }
        return business_types.get(sign, 'General commerce')
    
    def _get_business_type_mars(self, sign: str) -> str:
        """Get business type based on Mars placement"""
        business_types = {
            'Aries': 'Start-ups, competitive ventures (STRONG)',
            'Taurus': 'Real estate, agriculture',
            'Gemini': 'Technical trading, electronics',
            'Cancer': 'Property dealing',
            'Leo': 'Manufacturing, leadership ventures',
            'Virgo': 'Technical services, machinery',
            'Libra': 'Partnership ventures, design business',
            'Scorpio': 'Investigation, research ventures (STRONG)',
            'Sagittarius': 'Adventure sports, imports',
            'Capricorn': 'Construction, heavy industry (STRONG)',
            'Aquarius': 'Technology startups, innovation',
            'Pisces': 'Charitable ventures, healing'
        }
        return business_types.get(sign, 'Entrepreneurial ventures')
    
    def _analyze_planet_strength(self, planet) -> str:
        """Analyze planet strength for business"""
        # Simplified analysis based on sign
        strong_signs = {
            'Mercury': ['Gemini', 'Virgo'],
            'Mars': ['Aries', 'Scorpio', 'Capricorn'],
            'Jupiter': ['Sagittarius', 'Pisces'],
            'Rahu': ['Gemini', 'Virgo', 'Aquarius']
        }
        
        if hasattr(planet, 'name') and hasattr(planet, 'sign'):
            if planet.sign in strong_signs.get(planet.name, []):
                return "STRONG ⭐ - Excellent for business"
        
        return "Moderate - Can succeed with effort"
    
    def _analyze_mars_energy(self, sign: str) -> str:
        """Analyze Mars energy level"""
        strong = ['Aries', 'Scorpio', 'Capricorn', 'Leo']
        if sign in strong:
            return "HIGH - Natural entrepreneur"
        return "Moderate - Can develop entrepreneurial skills"
    
    def _analyze_business_suitability(self, planets: dict, asc_sign: str) -> str:
        """Analyze if business or job is better"""
        business_score = 0
        reasons = []
        
        # Check Mercury
        mercury = planets.get('Mercury')
        if mercury:
            merc_sign = self._get_planet_attr(mercury, 'sign')
            if merc_sign in ['Gemini', 'Virgo', 'Aquarius']:
                business_score += 2
                reasons.append("Strong Mercury favors business")
        
        # Check Mars
        mars = planets.get('Mars')
        if mars:
            mars_sign = self._get_planet_attr(mars, 'sign')
            if mars_sign in ['Aries', 'Scorpio', 'Capricorn']:
                business_score += 2
                reasons.append("Strong Mars gives entrepreneurial drive")
        
        # Check Rahu
        rahu = planets.get('Rahu')
        if rahu:
            business_score += 1
            reasons.append("Rahu brings unconventional opportunities")
        
        # Verdict
        response = ""
        if business_score >= 3:
            response += "**✅ HIGHLY SUITABLE FOR BUSINESS**\n\n"
            response += "You have strong entrepreneurial potential!\n\n"
        elif business_score >= 2:
            response += "**✅ SUITABLE FOR BUSINESS**\n\n"
            response += "You can succeed in business with proper planning.\n\n"
        else:
            response += "**⚠️ MODERATE - Both Business & Job Suitable**\n\n"
            response += "Consider starting part-time business while in job.\n\n"
        
        if reasons:
            response += "**Reasons:**\n"
            for reason in reasons:
                response += f"• {reason}\n"
        
        return response
    
    def _analyze_business_timing_with_dates(self, maha_lord: str, antar_lord: str, dashas: list) -> str:
        """Analyze business timing with exact dates using Antardashas"""
        business_planets = ['Mercury', 'Mars', 'Rahu', 'Jupiter', 'Venus', 'Sun']
        context = "Launch business, sign major contracts, expand operations, fundraising"
        
        return self._predict_timing_with_antardashas(
            maha_lord, antar_lord, dashas, business_planets, context, emoji="🚀"
        ) + "\n💡 **BUSINESS ACTION PLAN:**\n• **During favorable periods:** Launch ventures, expand aggressively\n• **Prepare now:** Develop business plan, build network, arrange funding\n• **Test first:** Start small/part-time before full commitment\n"
    
    def _analyze_business_timing(self, maha_lord: str, antar_lord: str) -> str:
        """Analyze current timing for business"""
        business_favorable = ['Mercury', 'Mars', 'Rahu', 'Jupiter', 'Venus']
        
        response = ""
        if maha_lord in business_favorable:
            response += f"✅ **{maha_lord} Mahadasha is FAVORABLE for business**\n\n"
            if antar_lord in business_favorable:
                response += f"⭐ **Excellent time to start/expand business**\n"
                response += f"• Current {antar_lord} antardasha is highly supportive\n"
                response += f"• **Recommendation: START NOW or within 6-12 months**\n"
            else:
                response += f"Good period overall, wait for favorable antardasha\n"
        else:
            response += f"⏳ **{maha_lord} Mahadasha - Mixed for business**\n"
            response += f"• Better to strengthen foundation during this period\n"
            response += f"• Major expansion recommended during Mercury/Mars/Rahu dasha\n"
        
        return response
    
    def _recommend_business_types(self, mercury, mars, rahu, jupiter) -> str:
        """Recommend specific business types"""
        recommendations = []
        
        if mercury:
            merc_sign = self._get_planet_attr(mercury, 'sign')
            if merc_sign in ['Gemini', 'Virgo']:
                recommendations.append("📱 **Technology/IT Services** - Mercury strong")
                recommendations.append("💼 **Consulting/Advisory** - Communication skills")
                recommendations.append("📊 **Data Analytics/Research**")
        
        if mars:
            mars_sign = self._get_planet_attr(mars, 'sign')
            if mars_sign in ['Aries', 'Scorpio', 'Capricorn']:
                recommendations.append("🏗️ **Real Estate/Construction**")
                recommendations.append("⚙️ **Technical/Engineering Services**")
                recommendations.append("🚀 **Startup Ventures** - High energy")
        
        if rahu:
            recommendations.append("🌐 **E-commerce/Online Business**")
            recommendations.append("🌍 **Import-Export/Foreign Trade**")
            recommendations.append("💡 **Innovative/Unconventional Ventures**")
        
        if jupiter:
            recommendations.append("📚 **Education/Training Business**")
            recommendations.append("⚖️ **Legal/Financial Advisory**")
        
        if not recommendations:
            recommendations.append("• General trading and commerce")
            recommendations.append("• Service-based businesses")
        
        response = ""
        for rec in recommendations[:5]:  # Top 5 recommendations
            response += rec + "\n"
        
        return response
    
    def _answer_education_question(self, chart_data: dict = None) -> str:
        """Answer education-related questions"""
        response = "**Education in Vedic Astrology:**\n\n"
        
        response += "**Education Houses:**\n"
        response += "• **4th House** - Basic education, school education\n"
        response += "• **5th House** - Higher education, intelligence, creativity\n"
        response += "• **9th House** - Higher learning, university, research, PhD\n\n"
        
        response += "**Education Planets:**\n"
        response += "• **Mercury** - Intellect, analytical skills, communication\n"
        response += "• **Jupiter** - Wisdom, higher learning, philosophy, law\n"
        response += "• **Venus** - Arts, music, creative education\n"
        response += "• **Saturn** - Technical education, hard work, discipline\n\n"
        
        response += "**Favorable Indicators:**\n"
        response += "• Strong 4th, 5th, or 9th lords\n"
        response += "• Well-placed Mercury and Jupiter\n"
        response += "• Benefic planets in education houses\n"
        response += "• Jupiter or Mercury dasha during study years\n\n"
        
        # Add timing predictions if chart data available
        if chart_data and 'dashas' in chart_data:
            education_planets = ['Mercury', 'Jupiter', 'Venus']
            response += self._get_timing_predictions(chart_data, education_planets, "Higher Education Success")
        else:
            response += "*For specific timing predictions, calculate your birth chart first.*\n\n"
        
        return response
    
    def _answer_property_question(self, chart_data: dict = None) -> str:
        """Answer property/real estate questions with timing predictions"""
        if not chart_data or 'planets' not in chart_data:
            return "**To answer your property question with specific timing, please:**\n\n1. Go to **Birth Chart** section\n2. Calculate your birth chart first\n3. Then come back and ask your question\n\nI'll analyze your 4th house, property planets (Mars, Moon, Venus), and current dasha periods to give you specific timing predictions!"
        
        response = "**🏠 Property & Vehicle Purchase Analysis for Your Birth Chart:**\n\n"
        
        # Get planets and ascendant
        planets = chart_data['planets']
        ascendant = planets.get('Ascendant')
        asc_sign = self._get_planet_attr(ascendant, 'sign', '')
        
        # Determine 4th house (property house)
        signs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        if asc_sign and asc_sign in signs_list:
            asc_index = signs_list.index(asc_sign)
            fourth_house_index = (asc_index + 3) % 12
            fourth_house_sign = signs_list[fourth_house_index]
            
            response += f"**Your 4th House (Property House):** {fourth_house_sign}\n\n"
            
            # Find planets in 4th house
            planets_in_4th = []
            for planet_name, planet_data in planets.items():
                if planet_name != 'Ascendant':
                    planet_sign = self._get_planet_attr(planet_data, 'sign')
                    if planet_sign == fourth_house_sign:
                        planets_in_4th.append(planet_name)
            
            if planets_in_4th:
                response += f"**Planets in 4th House:** {', '.join(planets_in_4th)}\n\n"
                response += "**Property Indications:**\n"
                for planet in planets_in_4th:
                    if planet == 'Mars':
                        response += "• **Mars** - Land, real estate, construction projects. Favorable for buying property.\n"
                    elif planet == 'Moon':
                        response += "• **Moon** - Comfortable homes, mother's property. Good for home comforts.\n"
                    elif planet == 'Venus':
                        response += "• **Venus** - Luxury homes, vehicles, beautiful properties. Very favorable!\n"
                    elif planet == 'Jupiter':
                        response += "• **Jupiter** - Large properties, expansion of assets. Highly beneficial.\n"
                    elif planet == 'Saturn':
                        response += "• **Saturn** - Old properties, ancestral land. May cause delays but eventual gains.\n"
                    elif planet == 'Sun':
                        response += "• **Sun** - Authoritative property, government housing, prestige.\n"
                    elif planet == 'Mercury':
                        response += "• **Mercury** - Multiple properties, rental income, business properties.\n"
                    elif planet == 'Rahu':
                        response += "• **Rahu** - Foreign/modern properties, sudden gains, unconventional deals.\n"
                    elif planet == 'Ketu':
                        response += "• **Ketu** - Spiritual places, isolated properties, detachment from materialism.\n"
                response += "\n"
            else:
                response += "**No planets in 4th House** - Property indicated by 4th lord's placement and Mars/Venus positions\n\n"
        
        # Analyze key property planets
        response += "**Key Property Planets in Your Chart:**\n"
        
        # Check Mars (primary property planet)
        mars = planets.get('Mars')
        if mars:
            mars_sign = self._get_planet_attr(mars, 'sign')
            mars_house = self._get_planet_attr(mars, 'house')
            response += f"• **Mars** in {mars_sign} (House {mars_house}) - "
            if mars_sign in ['Aries', 'Scorpio', 'Capricorn']:  # Mars exalted/own sign
                response += "Strong! Favorable for land and property purchase\n"
            else:
                response += "Consider Mars dasha/antardasha for property\n"
        
        # Check Venus (vehicles, luxury property)
        venus = planets.get('Venus')
        if venus:
            venus_sign = self._get_planet_attr(venus, 'sign')
            venus_house = self._get_planet_attr(venus, 'house')
            response += f"• **Venus** in {venus_sign} (House {venus_house}) - "
            if venus_sign in ['Pisces', 'Taurus', 'Libra']:  # Venus exalted/own signs
                response += "Strong! Excellent for vehicles and luxury properties\n"
            else:
                response += "Venus dasha favorable for vehicle purchase\n"
        
        # Check Moon (home comforts)
        moon = planets.get('Moon')
        if moon:
            moon_sign = self._get_planet_attr(moon, 'sign')
            moon_house = self._get_planet_attr(moon, 'house')
            response += f"• **Moon** in {moon_sign} (House {moon_house}) - "
            if moon_sign in ['Taurus', 'Cancer']:  # Moon exalted/own sign
                response += "Strong! Good for comfortable homes\n"
            else:
                response += "Moon dasha for home comfort improvements\n"
        
        response += "\n**📅 TIMING PREDICTIONS - When Will You Buy Property/House:**\n\n"
        
        # Use helper method for timing predictions
        property_planets = ['Mars', 'Venus', 'Moon', 'Jupiter']
        response += self._get_timing_predictions(chart_data, property_planets, "Property/Vehicle Purchase")
        
        response += "\n**💰 Additional Recommendations:**\n"
        response += "• Check your **2nd House** (wealth) for financial capacity\n"
        response += "• Check your **11th House** (gains) for property profits\n"
        response += "• Consider purchasing during **Gudi Padwa**, **Dussehra**, or **Diwali** for auspicious timing\n"
        response += "• Avoid **Rahu Kaal** and **Yamagandam** timings for property registration\n"
        
        return response
    
    def _answer_foreign_question(self, chart_data: dict = None) -> str:
        """Answer foreign travel/settlement questions"""
        response = "**Foreign Travel & Settlement:**\n\n"
        
        response += "**Foreign Travel Houses:**\n"
        response += "• **9th House** - Long distance travel, foreign lands\n"
        response += "• **12th House** - Foreign settlement, distant places\n"
        response += "• **3rd House** - Short travels\n\n"
        
        response += "**Foreign Planets:**\n"
        response += "• **Rahu** - Foreign connections, overseas opportunities\n"
        response += "• **Moon** - Change of place, travel\n"
        response += "• **Saturn** - Foreign settlement (in 12th)\n"
        response += "• **Mercury** - Business travel\n\n"
        
        response += "**Indicators for Foreign Settlement:**\n"
        response += "• Strong Rahu in 9th or 12th house\n"
        response += "• 12th lord in 9th or 9th lord in 12th\n"
        response += "• Rahu-Moon connection\n"
        response += "• Multiple planets in 9th or 12th house\n\n"
        
        # Add timing predictions if chart data available
        if chart_data and 'dashas' in chart_data:
            foreign_planets = ['Rahu', 'Moon', 'Saturn', 'Jupiter']
            response += self._get_timing_predictions(chart_data, foreign_planets, "Foreign Travel/Settlement")
        else:
            response += "**Timing:**\n"
            response += "• Rahu dasha periods very favorable\n"
            response += "• Saturn in 12th house dasha\n"
            response += "• Jupiter transit over 9th house\n\n"
        
        return response
    
    def _answer_fortune_question(self, chart_data: dict = None) -> str:
        """Answer luck/fortune questions"""
        response = "**Luck & Fortune in Vedic Astrology:**\n\n"
        
        response += "**Fortune Houses:**\n"
        response += "• **9th House (Bhagya Bhava)** - Luck, fortune, blessings\n"
        response += "• **5th House** - Purva Punya (past life merit)\n"
        response += "• **1st House** - Overall destiny and karma\n\n"
        
        response += "**Fortune Planets:**\n"
        response += "• **Jupiter** - The great benefic, divine grace\n"
        response += "• **Venus** - Material comforts, luxuries\n"
        response += "• **Sun** - Authority, recognition, fame\n"
        response += "• **Moon** - Mental peace, public favor\n\n"
        
        response += "**Indicators of Good Fortune:**\n"
        response += "• Strong 9th house and 9th lord\n"
        response += "• Well-placed Jupiter\n"
        response += "• Benefics in Kendra (1st, 4th, 7th, 10th) and Trikona (5th, 9th)\n"
        response += "• Strong Ascendant lord\n\n"
        
        # Add timing predictions if chart data available
        if chart_data and 'dashas' in chart_data:
            fortune_planets = ['Jupiter', 'Venus', 'Sun', 'Moon']
            response += self._get_timing_predictions(chart_data, fortune_planets, "Fortune & Luck")
        else:
            response += "**To Enhance Fortune:**\n"
            response += "• Worship lord of 9th house\n"
            response += "• Strengthen Jupiter through remedies\n"
            response += "• Charity and good deeds\n"
            response += "• Respect elders and teachers\n\n"
        
        return response
    
    def _general_guidance(self) -> str:
        """General astrology guidance"""
        return """**Vedic Astrology Guidance:**

I can help you understand various aspects of Vedic astrology:

**Ask me about:**
• Planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
• Houses (1st through 12th)
• Career, job, promotion
• Business and entrepreneurship
• Marriage and relationships  
• Wealth and finances
• Health matters
• Children and family
• Education and studies
• Property and vehicles
• Foreign travel and settlement
• Luck and fortune

**Example questions:**
• "When will I get promoted in my job?"
• "Is business suitable for me?"
• "When will I get married?"
• "Will I settle abroad?"
• "What about my education?"
• "When will I buy a house?"

Or calculate your birth chart for personalized predictions based on YOUR planetary positions!"""
