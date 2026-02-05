"""
Numerology Engine
Calculates various numerology numbers and provides interpretations
"""
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class NumerologyProfile:
    """Store numerology calculation results"""
    life_path: int
    expression: int
    soul_urge: int
    personality: int
    birthday: int
    personal_year: int
    maturity: int
    karmic_debts: List[int]
    master_numbers: List[int]


class NumerologyEngine:
    """Calculate and interpret numerology numbers"""
    
    # Letter to number mapping (Pythagorean system)
    LETTER_VALUES = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    VOWELS = {'A', 'E', 'I', 'O', 'U'}
    MASTER_NUMBERS = {11, 22, 33}
    KARMIC_DEBT_NUMBERS = {13, 14, 16, 19}
    
    def __init__(self):
        """Initialize numerology engine"""
        pass
    
    def calculate_profile(self, name: str, birth_date: datetime) -> NumerologyProfile:
        """
        Calculate complete numerology profile
        
        Args:
            name: Full name
            birth_date: Birth date
            
        Returns:
            NumerologyProfile with all calculated numbers
        """
        life_path, lp_karmic = self._calculate_life_path(birth_date)
        expression, exp_karmic = self._calculate_expression(name)
        soul_urge, su_karmic = self._calculate_soul_urge(name)
        personality, pers_karmic = self._calculate_personality(name)
        birthday = self._calculate_birthday(birth_date)
        personal_year = self._calculate_personal_year(birth_date)
        maturity = self._reduce_to_single((life_path + expression))
        
        # Collect karmic debts
        karmic_debts = []
        for debt in [lp_karmic, exp_karmic, su_karmic, pers_karmic]:
            if debt and debt in self.KARMIC_DEBT_NUMBERS:
                karmic_debts.append(debt)
        
        # Collect master numbers
        master_numbers = []
        for num in [life_path, expression, soul_urge, personality]:
            if num in self.MASTER_NUMBERS:
                master_numbers.append(num)
        
        return NumerologyProfile(
            life_path=life_path,
            expression=expression,
            soul_urge=soul_urge,
            personality=personality,
            birthday=birthday,
            personal_year=personal_year,
            maturity=maturity,
            karmic_debts=list(set(karmic_debts)),
            master_numbers=list(set(master_numbers))
        )
    
    def _calculate_life_path(self, birth_date: datetime) -> Tuple[int, int]:
        """Calculate Life Path Number from birth date"""
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        
        # Reduce each component separately to catch karmic debts
        day_sum = self._sum_digits(day)
        month_sum = self._sum_digits(month)
        year_sum = self._sum_digits(year)
        
        total = day_sum + month_sum + year_sum
        karmic_debt = total if total in self.KARMIC_DEBT_NUMBERS else None
        
        result = self._reduce_to_single(total)
        return result, karmic_debt
    
    def _calculate_expression(self, name: str) -> Tuple[int, int]:
        """Calculate Expression/Destiny Number from full name"""
        total = 0
        for char in name.upper():
            if char.isalpha():
                total += self.LETTER_VALUES.get(char, 0)
        
        karmic_debt = total if total in self.KARMIC_DEBT_NUMBERS else None
        result = self._reduce_to_single(total)
        return result, karmic_debt
    
    def _calculate_soul_urge(self, name: str) -> Tuple[int, int]:
        """Calculate Soul Urge Number from vowels in name"""
        total = 0
        for char in name.upper():
            if char in self.VOWELS:
                total += self.LETTER_VALUES.get(char, 0)
        
        karmic_debt = total if total in self.KARMIC_DEBT_NUMBERS else None
        result = self._reduce_to_single(total)
        return result, karmic_debt
    
    def _calculate_personality(self, name: str) -> Tuple[int, int]:
        """Calculate Personality Number from consonants in name"""
        total = 0
        for char in name.upper():
            if char.isalpha() and char not in self.VOWELS:
                total += self.LETTER_VALUES.get(char, 0)
        
        karmic_debt = total if total in self.KARMIC_DEBT_NUMBERS else None
        result = self._reduce_to_single(total)
        return result, karmic_debt
    
    def _calculate_birthday(self, birth_date: datetime) -> int:
        """Calculate Birthday Number"""
        return self._reduce_to_single(birth_date.day)
    
    def _calculate_personal_year(self, birth_date: datetime) -> int:
        """Calculate Personal Year Number for current year"""
        current_year = datetime.now().year
        month = birth_date.month
        day = birth_date.day
        
        total = self._sum_digits(month) + self._sum_digits(day) + self._sum_digits(current_year)
        return self._reduce_to_single(total)
    
    def _sum_digits(self, number: int) -> int:
        """Sum all digits of a number"""
        return sum(int(digit) for digit in str(number))
    
    def _reduce_to_single(self, number: int) -> int:
        """Reduce number to single digit (keeping master numbers)"""
        while number > 9:
            if number in self.MASTER_NUMBERS:
                return number
            number = self._sum_digits(number)
        return number
    
    def get_life_path_interpretation(self, number: int) -> Dict:
        """Get interpretation for Life Path Number"""
        interpretations = {
            1: {
                'title': 'The Leader',
                'traits': ['Independent', 'Ambitious', 'Pioneer', 'Confident', 'Innovative'],
                'strengths': 'Natural leader with strong will and determination. Original thinker with innovative ideas.',
                'challenges': 'Can be too dominating, aggressive, or self-centered. Learn to cooperate with others.',
                'career': ['Entrepreneur', 'CEO', 'Director', 'Self-employed', 'Innovator'],
                'lucky_days': ['Sunday', 'Monday'],
                'lucky_colors': ['Red', 'Orange', 'Gold'],
                'compatible_numbers': [1, 2, 4, 7]
            },
            2: {
                'title': 'The Mediator',
                'traits': ['Diplomatic', 'Cooperative', 'Sensitive', 'Peaceful', 'Supportive'],
                'strengths': 'Excellent mediator and peacemaker. Highly intuitive and emotionally intelligent.',
                'challenges': 'Can be overly sensitive, indecisive, or dependent. Build self-confidence.',
                'career': ['Counselor', 'Diplomat', 'Teacher', 'Artist', 'Musician'],
                'lucky_days': ['Monday', 'Friday'],
                'lucky_colors': ['White', 'Cream', 'Green'],
                'compatible_numbers': [1, 2, 6, 9]
            },
            3: {
                'title': 'The Creative',
                'traits': ['Expressive', 'Creative', 'Social', 'Optimistic', 'Artistic'],
                'strengths': 'Natural communicator with creative talents. Brings joy and inspiration to others.',
                'challenges': 'Can scatter energy, be superficial, or overly optimistic. Focus and discipline needed.',
                'career': ['Writer', 'Artist', 'Entertainer', 'Designer', 'Speaker'],
                'lucky_days': ['Thursday', 'Friday'],
                'lucky_colors': ['Yellow', 'Pink', 'Purple'],
                'compatible_numbers': [3, 6, 9]
            },
            4: {
                'title': 'The Builder',
                'traits': ['Practical', 'Disciplined', 'Hardworking', 'Reliable', 'Organized'],
                'strengths': 'Strong foundation builder with practical approach. Dependable and trustworthy.',
                'challenges': 'Can be too rigid, stubborn, or workaholic. Learn to be flexible and enjoy life.',
                'career': ['Engineer', 'Architect', 'Accountant', 'Manager', 'Builder'],
                'lucky_days': ['Saturday', 'Sunday'],
                'lucky_colors': ['Blue', 'Grey', 'Brown'],
                'compatible_numbers': [1, 4, 7, 8]
            },
            5: {
                'title': 'The Freedom Seeker',
                'traits': ['Adventurous', 'Freedom-loving', 'Versatile', 'Dynamic', 'Curious'],
                'strengths': 'Adaptable and versatile. Thrives on change and new experiences.',
                'challenges': 'Can be restless, irresponsible, or inconsistent. Need stability and commitment.',
                'career': ['Traveler', 'Sales', 'Marketing', 'Journalist', 'Consultant'],
                'lucky_days': ['Wednesday', 'Friday'],
                'lucky_colors': ['Green', 'Turquoise', 'Silver'],
                'compatible_numbers': [1, 5, 7, 9]
            },
            6: {
                'title': 'The Nurturer',
                'traits': ['Caring', 'Responsible', 'Loving', 'Harmonious', 'Service-oriented'],
                'strengths': 'Natural caregiver and family person. Creates harmony and beauty.',
                'challenges': 'Can be too sacrificing, interfering, or perfectionist. Set healthy boundaries.',
                'career': ['Teacher', 'Counselor', 'Healer', 'Chef', 'Interior Designer'],
                'lucky_days': ['Friday', 'Monday'],
                'lucky_colors': ['Blue', 'Pink', 'White'],
                'compatible_numbers': [2, 3, 6, 9]
            },
            7: {
                'title': 'The Seeker',
                'traits': ['Analytical', 'Spiritual', 'Introspective', 'Wise', 'Mysterious'],
                'strengths': 'Deep thinker and truth seeker. Highly intuitive and spiritually aware.',
                'challenges': 'Can be too isolated, skeptical, or aloof. Connect with others and trust.',
                'career': ['Researcher', 'Analyst', 'Spiritual Teacher', 'Scientist', 'Philosopher'],
                'lucky_days': ['Monday', 'Sunday'],
                'lucky_colors': ['Violet', 'Purple', 'White'],
                'compatible_numbers': [1, 4, 5, 7]
            },
            8: {
                'title': 'The Powerhouse',
                'traits': ['Ambitious', 'Authoritative', 'Material Success', 'Powerful', 'Business-minded'],
                'strengths': 'Natural executive with business acumen. Achieves material success and power.',
                'challenges': 'Can be too materialistic, controlling, or workaholic. Balance work with life.',
                'career': ['CEO', 'Banker', 'Real Estate', 'Entrepreneur', 'Judge'],
                'lucky_days': ['Saturday', 'Tuesday'],
                'lucky_colors': ['Black', 'Dark Blue', 'Purple'],
                'compatible_numbers': [2, 4, 6, 8]
            },
            9: {
                'title': 'The Humanitarian',
                'traits': ['Compassionate', 'Generous', 'Wise', 'Idealistic', 'Universal Love'],
                'strengths': 'Old soul with humanitarian values. Serves the greater good selflessly.',
                'challenges': 'Can be too idealistic, impractical, or emotionally distant. Ground yourself.',
                'career': ['Social Worker', 'Healer', 'Artist', 'Philanthropist', 'Counselor'],
                'lucky_days': ['Tuesday', 'Thursday'],
                'lucky_colors': ['Red', 'Crimson', 'Pink'],
                'compatible_numbers': [3, 6, 9]
            },
            11: {
                'title': 'The Illuminator (Master Number)',
                'traits': ['Intuitive', 'Inspirational', 'Spiritual', 'Visionary', 'Idealistic'],
                'strengths': 'Highly intuitive with spiritual gifts. Inspires and illuminates others.',
                'challenges': 'Can be overly sensitive, impractical, or nervous. Stay grounded.',
                'career': ['Spiritual Teacher', 'Counselor', 'Artist', 'Motivational Speaker', 'Healer'],
                'lucky_days': ['Monday', 'Sunday'],
                'lucky_colors': ['Silver', 'White', 'Pearl'],
                'compatible_numbers': [2, 6, 9, 11]
            },
            22: {
                'title': 'The Master Builder (Master Number)',
                'traits': ['Visionary', 'Practical', 'Master Builder', 'Powerful', 'Transformative'],
                'strengths': 'Combines vision with practical ability. Can manifest grand visions into reality.',
                'challenges': 'Can feel overwhelmed by potential. Need patience and persistence.',
                'career': ['Architect', 'Large-scale Business', 'International Work', 'Visionary Leader'],
                'lucky_days': ['Saturday', 'Sunday'],
                'lucky_colors': ['Gold', 'Coral', 'Red'],
                'compatible_numbers': [4, 8, 11, 22]
            },
            33: {
                'title': 'The Master Teacher (Master Number)',
                'traits': ['Selfless', 'Nurturing', 'Compassionate', 'Master Healer', 'Teacher'],
                'strengths': 'Master teacher and healer. Devoted to uplifting humanity.',
                'challenges': 'Can take on too much responsibility. Must learn to say no.',
                'career': ['Spiritual Leader', 'Master Healer', 'Humanitarian Work', 'Counselor'],
                'lucky_days': ['Friday', 'Monday'],
                'lucky_colors': ['Emerald Green', 'Sea Green', 'Gold'],
                'compatible_numbers': [6, 9, 11, 33]
            }
        }
        
        return interpretations.get(number, interpretations.get(1))
    
    def get_lucky_dates_for_month(self, life_path: int, year: int, month: int) -> List[int]:
        """Get lucky dates for a specific month based on life path number"""
        lucky_dates = []
        
        # Primary lucky numbers
        primary = [life_path, life_path + 9, life_path + 18]
        
        # Add numbers that reduce to life path
        for date in range(1, 32):
            try:
                # Check if date is valid for this month
                datetime(year, month, date)
                reduced = self._reduce_to_single(date)
                if reduced == life_path or date in primary:
                    lucky_dates.append(date)
            except ValueError:
                continue
        
        return sorted(lucky_dates)
    
    def get_career_paths(self, life_path: int, expression: int) -> List[Dict]:
        """Get career recommendations based on numerology"""
        interpretation = self.get_life_path_interpretation(life_path)
        careers = interpretation.get('career', [])
        
        # Add additional careers based on expression number
        expression_interp = self.get_life_path_interpretation(expression)
        additional_careers = expression_interp.get('career', [])
        
        combined_careers = list(set(careers + additional_careers))
        
        career_details = []
        for career in combined_careers[:8]:  # Limit to top 8
            career_details.append({
                'name': career,
                'suitability': 'Excellent' if career in careers else 'Very Good',
                'reason': f'Aligns with your Life Path {life_path} and Expression {expression} numbers'
            })
        
        return career_details
    
    def get_gemstone_recommendation(self, life_path: int) -> Dict:
        """Get gemstone recommendation based on numerology"""
        gemstones = {
            1: {'primary': 'Ruby', 'secondary': 'Garnet', 'planet': 'Sun'},
            2: {'primary': 'Pearl', 'secondary': 'Moonstone', 'planet': 'Moon'},
            3: {'primary': 'Yellow Sapphire', 'secondary': 'Citrine', 'planet': 'Jupiter'},
            4: {'primary': 'Hessonite', 'secondary': 'Blue Sapphire', 'planet': 'Rahu/Saturn'},
            5: {'primary': 'Emerald', 'secondary': 'Peridot', 'planet': 'Mercury'},
            6: {'primary': 'Diamond', 'secondary': 'White Sapphire', 'planet': 'Venus'},
            7: {'primary': 'Cat\'s Eye', 'secondary': 'Amethyst', 'planet': 'Ketu/Neptune'},
            8: {'primary': 'Blue Sapphire', 'secondary': 'Amethyst', 'planet': 'Saturn'},
            9: {'primary': 'Red Coral', 'secondary': 'Bloodstone', 'planet': 'Mars'},
            11: {'primary': 'Pearl', 'secondary': 'Opal', 'planet': 'Moon'},
            22: {'primary': 'Blue Sapphire', 'secondary': 'Lapis Lazuli', 'planet': 'Saturn'},
            33: {'primary': 'Diamond', 'secondary': 'Emerald', 'planet': 'Venus'}
        }
        
        return gemstones.get(life_path, gemstones.get(1))
    
    def get_karmic_debt_interpretation(self, debt_number: int) -> Dict:
        """Get interpretation for karmic debt numbers"""
        interpretations = {
            13: {
                'title': 'Karmic Debt 13',
                'meaning': 'Past life laziness or selfishness. Must work hard and stay focused.',
                'lessons': ['Hard work', 'Focus', 'Discipline', 'Orderliness', 'Service'],
                'remedy': 'Stay organized, complete tasks, help others without expecting return'
            },
            14: {
                'title': 'Karmic Debt 14',
                'meaning': 'Past life abuse of freedom. Must learn moderation and balance.',
                'lessons': ['Moderation', 'Balance', 'Commitment', 'Responsibility', 'Self-control'],
                'remedy': 'Practice moderation in all things, fulfill commitments, maintain stability'
            },
            16: {
                'title': 'Karmic Debt 16',
                'meaning': 'Past life ego and pride. Must learn humility and spiritual values.',
                'lessons': ['Humility', 'Love', 'Forgiveness', 'Spiritual growth', 'Letting go of ego'],
                'remedy': 'Practice humility, forgiveness, spiritual disciplines, serve others'
            },
            19: {
                'title': 'Karmic Debt 19',
                'meaning': 'Past life misuse of power. Must learn to serve without dominating.',
                'lessons': ['Service', 'Independence', 'Compassion', 'Balanced power', 'Humility'],
                'remedy': 'Serve others selflessly, use power wisely, practice compassion'
            }
        }
        
        return interpretations.get(debt_number, {})
    
    def calculate_name_compatibility(self, name1: str, name2: str) -> Dict:
        """Calculate compatibility between two names"""
        exp1, _ = self._calculate_expression(name1)
        exp2, _ = self._calculate_expression(name2)
        
        # Compatibility matrix
        highly_compatible = {
            (1, 1), (1, 2), (1, 4), (1, 7),
            (2, 2), (2, 6), (2, 9),
            (3, 3), (3, 6), (3, 9),
            (4, 4), (4, 7), (4, 8),
            (5, 5), (5, 7), (5, 9),
            (6, 6), (6, 9),
            (7, 7),
            (8, 8), (8, 2), (8, 6),
            (9, 9), (9, 3), (9, 6)
        }
        
        pair = (min(exp1, exp2), max(exp1, exp2))
        
        if pair in highly_compatible or (exp2, exp1) in highly_compatible:
            compatibility = 'Excellent'
            score = 90
        elif abs(exp1 - exp2) <= 2:
            compatibility = 'Good'
            score = 70
        else:
            compatibility = 'Challenging'
            score = 50
        
        return {
            'name1': name1,
            'name2': name2,
            'expression1': exp1,
            'expression2': exp2,
            'compatibility': compatibility,
            'score': score,
            'description': f'Numbers {exp1} and {exp2} show {compatibility.lower()} compatibility'
        }
