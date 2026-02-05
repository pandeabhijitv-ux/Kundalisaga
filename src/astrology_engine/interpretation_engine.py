"""
Vedic Astrology Interpretation Engine
Built-in knowledge base for planetary interpretations
Based on classical Vedic astrology principles
"""

from typing import Dict, List, Any


class VedicInterpretationEngine:
    """Generates interpretations based on classical Vedic astrology principles"""
    
    def __init__(self):
        self.planet_house_effects = self._init_planet_house_effects()
        self.dasha_effects = self._init_dasha_effects()
        self.planetary_yogas = self._init_yogas()
        self.house_significations = self._init_house_significations()
    
    def _init_house_significations(self) -> Dict:
        """Core significations of each house"""
        return {
            1: {"name": "Ascendant/Lagna", "areas": ["Self", "Personality", "Physical body", "Overall vitality", "Life path"]},
            2: {"name": "Dhana Bhava", "areas": ["Wealth", "Family", "Speech", "Food", "Accumulated resources", "Face", "Right eye"]},
            3: {"name": "Sahaja Bhava", "areas": ["Courage", "Siblings", "Short journeys", "Communication", "Skills", "Efforts", "Right ear"]},
            4: {"name": "Sukha Bhava", "areas": ["Mother", "Home", "Comfort", "Education", "Vehicles", "Property", "Inner peace", "Heart"]},
            5: {"name": "Putra Bhava", "areas": ["Children", "Intelligence", "Creativity", "Romance", "Speculation", "Past karma", "Mantras"]},
            6: {"name": "Ripu Bhava", "areas": ["Enemies", "Diseases", "Debts", "Service", "Daily work", "Obstacles", "Maternal uncle"]},
            7: {"name": "Kalatra Bhava", "areas": ["Spouse", "Marriage", "Partnerships", "Business relations", "Public image", "Travel"]},
            8: {"name": "Ayur Bhava", "areas": ["Longevity", "Transformation", "Occult", "Inheritance", "Sudden events", "Research", "Mysteries"]},
            9: {"name": "Dharma Bhava", "areas": ["Father", "Guru", "Fortune", "Higher learning", "Religion", "Long journeys", "Philosophy"]},
            10: {"name": "Karma Bhava", "areas": ["Career", "Status", "Reputation", "Authority", "Government", "Achievements", "Knees"]},
            11: {"name": "Labha Bhava", "areas": ["Gains", "Income", "Friends", "Aspirations", "Elder siblings", "Fulfillment", "Left ear"]},
            12: {"name": "Vyaya Bhava", "areas": ["Losses", "Expenses", "Isolation", "Foreign lands", "Liberation", "Sleep", "Left eye", "Charity"]}
        }
    
    def _init_planet_house_effects(self) -> Dict:
        """Detailed effects of each planet in each house"""
        return {
            "Sun": {
                1: "Strong personality, leadership qualities, good health, authoritative nature, dignified appearance. Natural confidence and self-assurance.",
                2: "Wealth through government or father, strong family values, authoritative speech. May face ego issues in family matters.",
                3: "Courage, leadership among siblings, success through own efforts. Strong willpower and determination.",
                4: "Happiness through property and education, respect in society, comfort from mother. Leadership in educational field.",
                5: "Intelligent children, creative expression, success in speculation. Strong wisdom and good judgment.",
                6: "Victory over enemies, success in competitive fields, good health after initial challenges. Service in authoritative positions.",
                7: "Strong partner but may face ego clashes in marriage. Success in partnerships and public dealings.",
                8: "Interest in occult, inheritance from father, transformation through challenges. Research abilities.",
                9: "Blessed by father, spiritual inclination, good fortune, higher education. Strong moral values.",
                10: "Excellent for career, high position, government favor, professional success. Authority and recognition.",
                11: "Good income, influential friends, fulfillment of desires. Success in elder siblings.",
                12: "Expenses on spiritual pursuits, foreign travels, expenditure for father. Liberation-oriented."
            },
            "Moon": {
                1: "Attractive personality, emotional nature, changeable moods, popular among masses. Good imagination and intuition.",
                2: "Wealth fluctuations, emotional family bonds, pleasant speech. Income through public dealings.",
                3: "Brave, good relationship with siblings, frequent short travels. Quick decision making.",
                4: "Very strong placement - happiness, property, vehicle comforts, devoted mother. Emotional fulfillment and peace.",
                5: "Intelligent, creative mind, good children, romantic nature. Emotional intelligence.",
                6: "Digestive issues, mental stress from enemies. Service-oriented work, helpful nature.",
                7: "Beautiful spouse, emotional marriage, public popularity. Partner may be moody or nurturing.",
                8: "Emotional ups and downs, intuitive abilities, interest in occult. Inheritance from mother. Psychological depth.",
                9: "Religious mind, devoted to mother, fortunate, spiritual travels. Emotional connection to dharma.",
                10: "Career involving public, changeable career paths, fame among masses. Emotional investment in work.",
                11: "Multiple income sources, large network of friends, emotional fulfillment. Gains through women.",
                12: "Expenses on comforts, foreign settlement possible, spiritual inclination. Emotional isolation at times."
            },
            "Mars": {
                1: "Energetic, aggressive, courageous, athletic build, quick temper. Leadership and initiative.",
                2: "Wealth through land/property, harsh speech, family disputes. Income through courage and effort.",
                3: "Very strong - courageous, successful through own efforts, good siblings. Competitive spirit.",
                4: "Property disputes, anger issues at home, engineering skills. Technical education.",
                5: "Intelligent but aggressive children, speculation gains, sports abilities. Sharp intelligence.",
                6: "Excellent placement - victory over enemies, good vitality, success in competition. Service in police/military.",
                7: "Aggressive spouse, conflicts in marriage, business partnerships need care. Sexual vitality.",
                8: "Interest in occult, sudden gains, accidents possible, inheritance disputes. Transformation through challenges.",
                9: "Disputes with father/guru, foreign travel, success through courage. Religious warrior spirit.",
                10: "Success in technical/engineering career, property dealings, authoritative position. Dynamic professional life.",
                11: "Excellent for gains, success in competitive fields, wealthy friends. Elder brother's support.",
                12: "Expenses on siblings, foreign settlement, hidden enemies. Sexual expenditure."
            },
            "Mercury": {
                1: "Intelligent, good communication, analytical mind, youthful appearance. Quick wit and adaptability.",
                2: "Good wealth through business/communication, pleasant speech, educated family. Multiple income sources.",
                3: "Very strong - excellent communication, writing abilities, good siblings, business skills. Clever and witty.",
                4: "Intelligent mother, education, property through business, comfortable home. Academic excellence.",
                5: "Highly intelligent children, creative writing, speculation through intelligence. Sharp analytical ability.",
                6: "Success through analytical work, victory through intelligence, service in communication fields. Problem-solving skills.",
                7: "Intelligent spouse, business partnerships, communicative marriage. Young-looking partner.",
                8: "Research abilities, inheritance through intelligence, interest in astrology/occult. Analytical depth.",
                9: "Higher education, intelligent father, teaching abilities, spiritual wisdom. Philosophical communication.",
                10: "Success in business/communication careers, intellectual work, writing/speaking professions. Versatile career.",
                11: "Multiple income sources, intelligent friends, gains through networking. Business circles.",
                12: "Foreign business, expenses on education, charitable communication. Spiritual studies."
            },
            "Jupiter": {
                1: "Wisdom, optimistic nature, good health, respected personality, spiritual inclination. Natural teacher and guide.",
                2: "Good family wealth, wise speech, sound financial judgment, educated family. Wealth accumulation.",
                3: "Wise siblings, good communication, success through guidance. Teaching siblings.",
                4: "Excellent education, happiness from mother, property, vehicles, spiritual comfort. Wisdom at home.",
                5: "Blessed with children, high intelligence, good speculation judgment, spiritual creativity. Divine grace.",
                6: "Victory over enemies through wisdom, good health, service in education/law. Healing abilities.",
                7: "Wise and religious spouse, good marriage, beneficial partnerships. Dharmic relationships.",
                8: "Long life, inheritance, interest in spirituality/astrology, research in philosophy. Transformative wisdom.",
                9: "Very strong - blessed by father, higher education, spiritual inclination, good fortune, foreign travels. Dharma path.",
                10: "Excellent career in teaching/law/religion, high position, respected profession. Ethical authority.",
                11: "Very good income, wise friends, fulfillment of desires, financial prosperity. Elder's blessings.",
                12: "Charitable nature, spiritual expenses, foreign residence, moksha-oriented. Divine grace for liberation."
            },
            "Venus": {
                1: "Attractive appearance, artistic nature, luxury loving, charming personality. Refined aesthetics.",
                2: "Good wealth, beautiful family, sweet speech, artistic expression. Luxurious lifestyle.",
                3: "Artistic siblings, creative communication, love for arts and music. Beautiful expression.",
                4: "Comfortable home, luxury vehicles, artistic mother, beautiful property. Aesthetic comforts.",
                5: "Creative children, romantic nature, artistic talents, speculation in arts. Love affairs.",
                6: "Diseases from overindulgence, secret relationships, service in luxury fields. Sexual health issues.",
                7: "Very strong - beautiful spouse, happy marriage, artistic partnerships. Harmonious relationships.",
                8: "Sudden gains through partner, interest in tantric practices, inheritance. Hidden pleasures.",
                9: "Fortunate marriage, artistic father, spiritual arts, travel for pleasure. Devotional nature.",
                10: "Career in arts/fashion/luxury, creativity in profession, public appeal. Diplomatic career.",
                11: "Good income from arts, beautiful friends, luxury gains, romantic friendships. Material fulfillment.",
                12: "Expenses on luxuries, foreign travel for pleasure, spiritual love. Bedroom comforts."
            },
            "Saturn": {
                1: "Serious personality, disciplined, delays in life, lean body, hardworking nature. Maturity and responsibility.",
                2: "Slow wealth accumulation, harsh speech, family responsibilities, frugal nature. Delayed financial gains.",
                3: "Difficulties with siblings, success through persistent efforts, obstacles initially. Hard-earned courage.",
                4: "Challenges from mother, property delays, limited comforts early in life. Discipline in education.",
                5: "Delays in childbirth, serious intelligence, speculation losses, conservative creativity. Disciplined wisdom.",
                6: "Excellent placement - victory over enemies through persistence, chronic health issues manageable, service work. Endurance.",
                7: "Delayed or older spouse, serious marriage, business partnerships face obstacles. Mature relationships.",
                8: "Long life, interest in occult/astrology, inheritance delays, chronic diseases. Deep transformation.",
                9: "Difficulties from father, spiritual discipline, foreign settlement, philosophical maturity. Hard-earned dharma.",
                10: "Slow but steady career growth, government service, persistent professional efforts. Authority through time.",
                11: "Delayed but stable income, older friends, gains through hard work. Patient achievement.",
                12: "Expenses controlled, foreign lands, spiritual discipline, isolation brings peace. Moksha through renunciation."
            },
            "Rahu": {
                1: "Unconventional personality, foreign influences, sudden changes, innovative thinking. Obsessive nature.",
                2: "Wealth through unusual means, foreign food habits, speech issues. Unconventional family.",
                3: "Unusual siblings, courage in foreign lands, innovative communication. Obsessive efforts.",
                4: "Foreign education, unconventional mother, property in foreign lands. Unusual comforts.",
                5: "Issues with children, unconventional creativity, speculation through foreign means. Obsessive intelligence.",
                6: "Victory through unconventional means, foreign diseases, service abroad. Hidden enemies.",
                7: "Foreign spouse, unconventional marriage, partnerships with foreigners. Obsessive relationships.",
                8: "Sudden transformations, inheritance disputes, occult interests, accidents. Foreign inheritance.",
                9: "Foreign higher education, unconventional beliefs, pilgrimage abroad. Foreign father/guru.",
                10: "Career in foreign lands, unconventional profession, sudden rise and falls. Innovative work.",
                11: "Gains from foreign sources, unusual friends, fulfillment through foreign connections. Foreign network.",
                12: "Foreign settlement, unusual expenses, spiritual seeking abroad. Liberation through foreign."
            },
            "Ketu": {
                1: "Spiritual personality, detached nature, thin body, mystical inclinations. Self-realization focus.",
                2: "Detachment from family, spiritual speech, minimal material focus. Past life resources.",
                3: "Spiritual siblings, minimal communication, detached efforts. Inner courage.",
                4: "Detachment from mother, spiritual education, minimal property focus. Inner peace.",
                5: "Spiritual children, intuitive intelligence, detachment from romance. Past life intelligence.",
                6: "Excellent for spiritual service, healing abilities, victory through detachment. Minimal enemies.",
                7: "Spiritual partner, detachment in marriage, minimal partnership focus. Moksha-oriented relationships.",
                8: "Very strong - deep spiritual transformation, occult mastery, inheritance detachment. Moksha path.",
                9: "Spiritual father/guru, strong spiritual inclination, past life dharma. Natural wisdom.",
                10: "Spiritual career, detachment from status, service-oriented work. Renunciation in profession.",
                11: "Detachment from material gains, spiritual friends, minimal desire fulfillment. Past life connections.",
                12: "Very strong - moksha, foreign spiritual residence, enlightenment. Liberation oriented."
            }
        }
    
    def _init_dasha_effects(self) -> Dict:
        """General effects during different planetary dashas"""
        return {
            "Sun": "Period of authority, government dealings, father's influence, leadership opportunities, self-confidence boost, recognition. Good for career advancement.",
            "Moon": "Emotional period, public dealings, changes and fluctuations, mother's influence, property matters, mental peace or anxiety depending on Moon's strength.",
            "Mars": "Active period requiring courage, property dealings, conflicts possible, energy boost, competitive scenarios, technical work, sibling matters.",
            "Mercury": "Intellectual pursuits, business opportunities, communication focus, education, writing, analytical work, networking, versatile activities.",
            "Jupiter": "Auspicious period, wisdom growth, spiritual inclination, children's matters, higher education, teaching opportunities, expansion in life, good fortune.",
            "Venus": "Romantic period, marriage prospects, artistic pursuits, luxury gains, vehicle purchase, comforts increase, creative expression, partnership opportunities.",
            "Saturn": "Period of discipline, hard work, delays and obstacles, karmic lessons, slow but steady progress, service work, health issues need attention.",
            "Rahu": "Sudden changes, foreign opportunities, unconventional paths, material desires increase, obsessive pursuits, innovation, unexpected events.",
            "Ketu": "Spiritual awakening, detachment, minimal material focus, occult interests, past life karma resolution, health issues possible, moksha orientation."
        }
    
    def _init_yogas(self) -> Dict:
        """Common planetary combinations (yogas)"""
        return {
            "raj_yogas": [
                "9th lord in 10th house creates Dharma-Karma Adhipati Yoga - brings fame, success, and righteous career.",
                "10th lord in 9th house creates Dharma-Karma Adhipati Yoga - fortune through career and father's blessings.",
                "1st and 9th lords together create Maha Lakshmi Yoga - great wealth and prosperity.",
                "1st and 10th lords together create Raja Yoga - authority, power, and high position.",
                "Benefics in kendras (1,4,7,10) and trikonas (1,5,9) create strong Raja Yogas."
            ],
            "dhana_yogas": [
                "2nd and 11th lords together create strong Dhana Yoga - wealth accumulation.",
                "Venus and Jupiter together create prosperity and luxury.",
                "2nd lord in 11th or 11th lord in 2nd creates income and wealth.",
                "5th lord in 9th creates fortune through intelligence and speculation."
            ]
        }
    
    def interpret_planet_in_house(self, planet: str, house: int, is_retrograde: bool = False) -> str:
        """Get interpretation for a planet in a specific house"""
        if planet in self.planet_house_effects and house in self.planet_house_effects[planet]:
            interpretation = self.planet_house_effects[planet][house]
            
            # Add retrograde effect if applicable
            if is_retrograde and planet in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
                interpretation += f" **{planet} is retrograde** - this intensifies the effects and brings delays or internal focus to these matters."
            
            return interpretation
        return f"{planet} in {house}th house influences the {self.house_significations.get(house, {}).get('name', 'house')}."
    
    def interpret_dasha(self, planet: str, subdasha: str = None) -> str:
        """Get interpretation for a dasha period"""
        main = self.dasha_effects.get(planet, f"Period of {planet}'s influence.")
        
        if subdasha and subdasha in self.dasha_effects:
            sub = self.dasha_effects[subdasha]
            return f"**{planet} Mahadasha - {subdasha} Antardasha:** {main}\n\nThe {subdasha} sub-period brings: {sub}"
        
        return f"**{planet} Mahadasha:** {main}"
    
    def get_house_analysis(self, house_num: int, planets: List[str], house_lord: str, lord_position: int) -> str:
        """Comprehensive analysis of a specific house"""
        house_info = self.house_significations.get(house_num, {})
        house_name = house_info.get("name", f"{house_num}th house")
        areas = ", ".join(house_info.get("areas", []))
        
        analysis = f"**{house_name} (House {house_num})** governs: {areas}\n\n"
        
        # Planets in this house
        if planets:
            analysis += f"**Planets present:** {', '.join(planets)}\n"
            for planet in planets:
                effect = self.interpret_planet_in_house(planet, house_num)
                analysis += f"• **{planet}:** {effect}\n"
        else:
            analysis += "**No planets in this house** - Results depend on the house lord's position.\n"
        
        # House lord analysis
        analysis += f"\n**House Lord {house_lord} is in {lord_position}th house:**\n"
        lord_effect = self.interpret_planet_in_house(house_lord, lord_position)
        analysis += f"The {house_num}th house results will manifest through {lord_position}th house matters. {lord_effect}\n"
        
        return analysis
    
    def generate_life_area_prediction(self, area: str, chart_data: Dict) -> List[str]:
        """Generate predictions for specific life areas"""
        predictions = []
        
        if area == "career":
            # 10th house, 10th lord, planets in 10th
            predictions = self._analyze_career(chart_data)
        elif area == "marriage":
            # 7th house, 7th lord, Venus, planets in 7th
            predictions = self._analyze_marriage(chart_data)
        elif area == "wealth":
            # 2nd house, 11th house, 2nd lord, 11th lord, Jupiter
            predictions = self._analyze_wealth(chart_data)
        elif area == "health":
            # 1st house, 6th house, 8th house, ascendant lord
            predictions = self._analyze_health(chart_data)
        elif area == "education":
            # 4th house, 5th house, Mercury, Jupiter
            predictions = self._analyze_education(chart_data)
        elif area == "family":
            # 4th house, 2nd house, Moon
            predictions = self._analyze_family(chart_data)
        
        return predictions
    
    def _analyze_career(self, chart_data: Dict) -> List[str]:
        """Analyze career prospects"""
        predictions = []
        planets = chart_data.get('planets', {})
        houses = chart_data.get('houses', {})
        
        # Find planets in 10th house
        tenth_house_planets = [p for p, data in planets.items() if data.get('house') == 10]
        
        if tenth_house_planets:
            for planet in tenth_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 10)
                predictions.append(f"**{planet} in 10th house (Career):** {interpretation}")
        else:
            predictions.append("**10th House Analysis:** No planets in the house of career. Results depend on the 10th house lord's position and strength.")
        
        # Add general career guidance
        predictions.append("The 10th house represents your profession, status, and public image. Strengthen your 10th house through dedication to your work and maintaining ethical standards.")
        
        return predictions
    
    def _analyze_marriage(self, chart_data: Dict) -> List[str]:
        """Analyze marriage and relationships"""
        predictions = []
        planets = chart_data.get('planets', {})
        
        # Find planets in 7th house
        seventh_house_planets = [p for p, data in planets.items() if data.get('house') == 7]
        
        if seventh_house_planets:
            for planet in seventh_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 7)
                predictions.append(f"**{planet} in 7th house (Marriage):** {interpretation}")
        
        # Venus analysis
        if 'Venus' in planets:
            venus_house = planets['Venus'].get('house')
            venus_interp = self.interpret_planet_in_house('Venus', venus_house)
            predictions.append(f"**Venus (Marriage significator) in {venus_house}th house:** {venus_interp}")
        
        if not predictions:
            predictions.append("**Marriage Analysis:** The 7th house governs marriage and partnerships. Consult the 7th house lord's position for detailed timing and nature of marriage.")
        
        return predictions
    
    def _analyze_wealth(self, chart_data: Dict) -> List[str]:
        """Analyze wealth and finances"""
        predictions = []
        planets = chart_data.get('planets', {})
        
        # 2nd house analysis
        second_house_planets = [p for p, data in planets.items() if data.get('house') == 2]
        if second_house_planets:
            for planet in second_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 2)
                predictions.append(f"**{planet} in 2nd house (Wealth):** {interpretation}")
        
        # 11th house analysis
        eleventh_house_planets = [p for p, data in planets.items() if data.get('house') == 11]
        if eleventh_house_planets:
            for planet in eleventh_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 11)
                predictions.append(f"**{planet} in 11th house (Gains):** {interpretation}")
        
        # Jupiter analysis
        if 'Jupiter' in planets:
            jupiter_house = planets['Jupiter'].get('house')
            jupiter_interp = self.interpret_planet_in_house('Jupiter', jupiter_house)
            predictions.append(f"**Jupiter (Wealth significator) in {jupiter_house}th house:** {jupiter_interp}")
        
        return predictions if predictions else ["**Wealth Analysis:** Examine 2nd house (accumulated wealth), 11th house (gains), and Jupiter's position for financial prospects."]
    
    def _analyze_health(self, chart_data: Dict) -> List[str]:
        """Analyze health prospects"""
        predictions = []
        planets = chart_data.get('planets', {})
        
        # 1st house (ascendant) analysis
        first_house_planets = [p for p, data in planets.items() if data.get('house') == 1]
        if first_house_planets:
            for planet in first_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 1)
                predictions.append(f"**{planet} in Ascendant (Health):** {interpretation}")
        
        # 6th house (diseases)
        sixth_house_planets = [p for p, data in planets.items() if data.get('house') == 6]
        if sixth_house_planets:
            for planet in sixth_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 6)
                predictions.append(f"**{planet} in 6th house (Health challenges):** {interpretation}")
        
        predictions.append("**Health Tip:** Regular exercise, proper diet, and spiritual practices strengthen the ascendant and overall vitality.")
        
        return predictions
    
    def _analyze_education(self, chart_data: Dict) -> List[str]:
        """Analyze education prospects"""
        predictions = []
        planets = chart_data.get('planets', {})
        
        # 4th house (basic education)
        fourth_house_planets = [p for p, data in planets.items() if data.get('house') == 4]
        if fourth_house_planets:
            for planet in fourth_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 4)
                predictions.append(f"**{planet} in 4th house (Education):** {interpretation}")
        
        # 5th house (intelligence)
        fifth_house_planets = [p for p, data in planets.items() if data.get('house') == 5]
        if fifth_house_planets:
            for planet in fifth_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 5)
                predictions.append(f"**{planet} in 5th house (Intelligence):** {interpretation}")
        
        # Mercury analysis
        if 'Mercury' in planets:
            mercury_house = planets['Mercury'].get('house')
            mercury_interp = self.interpret_planet_in_house('Mercury', mercury_house)
            predictions.append(f"**Mercury (Education significator) in {mercury_house}th house:** {mercury_interp}")
        
        return predictions if predictions else ["**Education Analysis:** The 4th house (basic education), 5th house (intelligence), and Mercury's position indicate educational prospects."]
    
    def _analyze_family(self, chart_data: Dict) -> List[str]:
        """Analyze family life"""
        predictions = []
        planets = chart_data.get('planets', {})
        
        # 4th house (mother, home)
        fourth_house_planets = [p for p, data in planets.items() if data.get('house') == 4]
        if fourth_house_planets:
            for planet in fourth_house_planets:
                interpretation = self.interpret_planet_in_house(planet, 4)
                predictions.append(f"**{planet} in 4th house (Family & Home):** {interpretation}")
        
        # Moon analysis (mother)
        if 'Moon' in planets:
            moon_house = planets['Moon'].get('house')
            moon_interp = self.interpret_planet_in_house('Moon', moon_house)
            predictions.append(f"**Moon (Mother & emotions) in {moon_house}th house:** {moon_interp}")
        
        return predictions if predictions else ["**Family Analysis:** The 4th house and Moon's position indicate family life, mother's influence, and domestic happiness."]
