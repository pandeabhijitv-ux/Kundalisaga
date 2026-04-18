"""
Vedic Astrology Calculation Engine
"""
import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from src.utils import logger, config


# Planet IDs in Swiss Ephemeris
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,  # North Node
    'Ketu': -1,  # Calculated as 180° from Rahu
    'Ascendant': -2  # Special calculation
}

# Zodiac Signs (Rashi)
SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Nakshatras (27 lunar mansions)
NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Vimshottari Dasha Lords and Years
VIMSHOTTARI_DASHA = [
    ('Ketu', 7),
    ('Venus', 20),
    ('Sun', 6),
    ('Moon', 10),
    ('Mars', 7),
    ('Rahu', 18),
    ('Jupiter', 16),
    ('Saturn', 19),
    ('Mercury', 17)
]


@dataclass
class BirthDetails:
    """Birth details for chart calculation"""
    date: datetime
    latitude: float
    longitude: float
    timezone: str
    name: str = ""
    place: str = ""


@dataclass
class PlanetPosition:
    """Planet position data"""
    name: str
    longitude: float
    sign: str
    sign_num: int
    degree_in_sign: float
    nakshatra: str
    nakshatra_pada: int
    house: int
    is_retrograde: bool = False


class VedicAstrologyEngine:
    """Vedic Astrology calculation engine using Swiss Ephemeris"""
    
    def __init__(self):
        self.logger = logger
        self.ayanamsa_mode = self._get_ayanamsa_mode()
        
        # Set ayanamsa
        swe.set_sid_mode(self.ayanamsa_mode)
        
        # Set ephemeris path (will download if needed)
        swe.set_ephe_path(None)  # Use default path
    
    def _get_ayanamsa_mode(self) -> int:
        """Get ayanamsa mode from config"""
        ayanamsa_name = config.get('astrology.ayanamsa', 'LAHIRI')
        
        ayanamsa_map = {
            'LAHIRI': swe.SIDM_LAHIRI,  # Traditional Lahiri (most widely used)
            'TRUE_CHITRAPAKSHA': swe.SIDM_TRUE_CITRA,  # True Chitrapaksha
            'RAMAN': swe.SIDM_RAMAN,
            'KP': swe.SIDM_KRISHNAMURTI,
            'FAGAN_BRADLEY': swe.SIDM_FAGAN_BRADLEY,
            'YUKTESHWAR': swe.SIDM_YUKTESHWAR,
            'JN_BHASIN': swe.SIDM_JN_BHASIN
        }
        
        return ayanamsa_map.get(ayanamsa_name, swe.SIDM_LAHIRI)
    
    def set_ayanamsa(self, ayanamsa_name: str):
        """Dynamically set ayanamsa mode"""
        ayanamsa_map = {
            'LAHIRI': swe.SIDM_LAHIRI,
            'TRUE_CHITRAPAKSHA': swe.SIDM_TRUE_CITRA,
            'RAMAN': swe.SIDM_RAMAN,
            'KP': swe.SIDM_KRISHNAMURTI,
            'FAGAN_BRADLEY': swe.SIDM_FAGAN_BRADLEY,
            'YUKTESHWAR': swe.SIDM_YUKTESHWAR,
            'JN_BHASIN': swe.SIDM_JN_BHASIN
        }
        self.ayanamsa_mode = ayanamsa_map.get(ayanamsa_name, swe.SIDM_LAHIRI)
        swe.set_sid_mode(self.ayanamsa_mode)
        self.logger.info(f"Ayanamsa changed to {ayanamsa_name}")

    def _compose_place_label(self, location) -> str:
        """Build a compact human-readable place label with locality + district context."""
        raw_address = getattr(location, "raw", {}).get("address", {})
        if not raw_address:
            return location.address

        locality = (
            raw_address.get("city")
            or raw_address.get("town")
            or raw_address.get("village")
            or raw_address.get("hamlet")
            or raw_address.get("municipality")
            or raw_address.get("suburb")
        )
        subdistrict = raw_address.get("subdistrict") or raw_address.get("county")
        district = raw_address.get("state_district") or raw_address.get("district")
        state = raw_address.get("state")
        country = raw_address.get("country")

        parts = [locality, subdistrict, district, state, country]
        cleaned_parts = []
        seen = set()
        for part in parts:
            if not part:
                continue
            lowered = part.strip().lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            cleaned_parts.append(part.strip())

        return ", ".join(cleaned_parts) if cleaned_parts else location.address

    def _location_to_dict(self, location, tf: TimezoneFinder) -> Dict:
        timezone = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        if not timezone:
            timezone = tf.closest_timezone_at(lat=location.latitude, lng=location.longitude)

        return {
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'timezone': timezone or 'UTC',
            'place': self._compose_place_label(location)
        }
    
    def get_location_info(self, place_name: str) -> Optional[Dict]:
        """
        Get latitude, longitude, and timezone for a place
        
        Args:
            place_name: Name of the place
        
        Returns:
            Dict with lat, lon, timezone or None
        """
        try:
            geolocator = Nominatim(user_agent="astro_knowledge")
            location = geolocator.geocode(
                place_name,
                country_codes="in",
                addressdetails=True,
                language="en",
                exactly_one=True,
            )

            # Fallback for non-India locations.
            if not location:
                location = geolocator.geocode(
                    place_name,
                    addressdetails=True,
                    language="en",
                    exactly_one=True,
                )
            
            if location:
                tf = TimezoneFinder()
                return self._location_to_dict(location, tf)
        except Exception as e:
            self.logger.error(f"Error getting location info: {str(e)}")
        
        return None
    
    def get_multiple_locations(self, place_name: str, limit: int = 5) -> List[Dict]:
        """
        Get multiple possible locations for a place name
        
        Args:
            place_name: Name of the place
            limit: Maximum number of results
        
        Returns:
            List of location dictionaries
        """
        try:
            geolocator = Nominatim(user_agent="astro_knowledge")
            locations = geolocator.geocode(
                place_name,
                exactly_one=False,
                limit=limit,
                country_codes="in",
                addressdetails=True,
                language="en",
            )

            # Fallback for non-India locations.
            if not locations:
                locations = geolocator.geocode(
                    place_name,
                    exactly_one=False,
                    limit=limit,
                    addressdetails=True,
                    language="en",
                )
            
            if locations:
                results = []
                tf = TimezoneFinder()
                
                for loc in locations:
                    results.append(self._location_to_dict(loc, tf))
                
                return results
        except Exception as e:
            self.logger.error(f"Error getting multiple locations: {str(e)}")
        
        return []
    
    def calculate_julian_day(self, birth_details: BirthDetails) -> float:
        """Calculate Julian Day for the birth time"""
        dt = birth_details.date
        
        # Convert to UTC
        local_tz = pytz.timezone(birth_details.timezone)
        local_dt = local_tz.localize(dt)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        # Calculate Julian Day
        jd = swe.julday(
            utc_dt.year, utc_dt.month, utc_dt.day,
            utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
        )
        
        self.logger.info(f"Birth date: {dt}, UTC: {utc_dt}, JD: {jd}")
        
        return jd
    
    def get_planet_position(self, planet_id: int, jd: float) -> Tuple[float, bool]:
        """
        Get planet position and convert to sidereal
        
        Returns:
            (sidereal_longitude, is_retrograde)
        """
        # Get tropical position
        result = swe.calc_ut(jd, planet_id)
        tropical_lon = result[0][0]
        speed = result[0][3]
        
        is_retrograde = speed < 0
        
        # Convert to sidereal manually (FLG_SIDEREAL doesn't work reliably)
        sidereal_lon = self.tropical_to_sidereal(tropical_lon, jd)
        
        return sidereal_lon, is_retrograde
    
    def tropical_to_sidereal(self, tropical_lon: float, jd: float) -> float:
        """Convert tropical to sidereal longitude"""
        # Re-set ayanamsa mode to ensure it's active
        swe.set_sid_mode(self.ayanamsa_mode)
        
        self.logger.info(f"BEFORE get_ayanamsa_ut: JD={jd}, type={type(jd)}, mode={self.ayanamsa_mode}")
        ayanamsa = swe.get_ayanamsa_ut(jd)
        sidereal_lon = (tropical_lon - ayanamsa) % 360
        # Debug logging
        self.logger.info(f"Tropical: {tropical_lon:.4f}, JD: {jd:.6f}, Ayanamsa: {ayanamsa:.4f}, Sidereal: {sidereal_lon:.4f}")
        return sidereal_lon
    
    def get_sign_and_degree(self, longitude: float) -> Tuple[int, str, float]:
        """
        Get sign number, name, and degree within sign
        
        Returns:
            (sign_num, sign_name, degree_in_sign)
        """
        sign_num = int(longitude / 30)
        degree_in_sign = longitude % 30
        sign_name = SIGNS[sign_num]
        
        return sign_num, sign_name, degree_in_sign
    
    def get_nakshatra(self, longitude: float) -> Tuple[str, int]:
        """
        Get nakshatra and pada from longitude
        
        Returns:
            (nakshatra_name, pada)
        """
        # Each nakshatra is 13°20' (13.333...)
        nakshatra_length = 360 / 27
        nakshatra_num = int(longitude / nakshatra_length)
        
        # Each pada is 3°20' (1/4 of nakshatra)
        pada_num = int((longitude % nakshatra_length) / (nakshatra_length / 4)) + 1
        
        return NAKSHATRAS[nakshatra_num], pada_num
    
    def calculate_ascendant(self, jd: float, latitude: float, 
                           longitude: float) -> float:
        """
        Calculate Ascendant (Lagna) using sidereal calculation
        
        Jagannath Hora uses the sidereal zodiac position of the ecliptic
        point rising on the eastern horizon at birth time.
        """
        # Get tropical ascendant
        result = swe.houses_ex(jd, latitude, longitude, b'W')
        ascendant_tropical = result[1][0]
        
        # Convert to sidereal
        ascendant_sidereal = self.tropical_to_sidereal(ascendant_tropical, jd)
        
        return ascendant_sidereal
    
    def calculate_houses(self, jd: float, latitude: float, 
                        longitude: float) -> List[float]:
        """
        Calculate 12 house cusps using Whole Sign system
        
        For Vedic astrology (Jagannath Hora compatibility), we use
        Whole Sign houses where each house spans exactly 30 degrees
        starting from the ascendant sign.
        """
        try:
            # Get tropical house cusps
            result = swe.houses_ex(jd, latitude, longitude, b'W')
            house_cusps = list(result[0][1:13])  # Get exactly 12 houses
            
            # Ensure we have 12 houses
            if len(house_cusps) < 12:
                self.logger.error(f"Only got {len(house_cusps)} house cusps, expected 12")
                # Pad with calculated values if needed
                while len(house_cusps) < 12:
                    house_cusps.append(0.0)
            
            # Convert to sidereal
            sidereal_cusps = [
                self.tropical_to_sidereal(cusp, jd) for cusp in house_cusps[:12]
            ]
            
            return sidereal_cusps
        except Exception as e:
            self.logger.error(f"Error calculating houses: {e}")
            # Return default houses starting from 0° with 30° intervals
            return [i * 30.0 for i in range(12)]
    
    def get_planet_house_whole_sign(self, planet_lon: float, ascendant_lon: float) -> int:
        """
        Determine which house a planet is in using Whole Sign House system
        This is the traditional Vedic method where each sign = one house
        """
        # Get sign numbers (0-11)
        planet_sign = int(planet_lon / 30)
        asc_sign = int(ascendant_lon / 30)
        
        # Calculate house: how many signs from ascendant sign?
        house = ((planet_sign - asc_sign) % 12) + 1
        
        return house
    
    def get_planet_house(self, planet_lon: float, house_cusps: List[float]) -> int:
        """Determine which house a planet is in using Placidus cusps"""
        # Ensure we have 12 houses
        if len(house_cusps) < 12:
            self.logger.warning(f"House cusps has only {len(house_cusps)} elements, expected 12")
            return 1
        
        for i in range(12):
            cusp_start = house_cusps[i]
            cusp_end = house_cusps[(i + 1) % 12]
            
            if cusp_start < cusp_end:
                if cusp_start <= planet_lon < cusp_end:
                    return i + 1
            else:  # Handle wrap around at 360°
                if planet_lon >= cusp_start or planet_lon < cusp_end:
                    return i + 1
        
        return 1  # Default to first house
    
    def calculate_divisional_chart(self, planet_longitude: float, division: int) -> float:
        """
        Calculate divisional chart (Varga) position
        
        Args:
            planet_longitude: Planet's longitude in D1
            division: Division number (2 for D2/Hora, 9 for D9/Navamsa, etc.)
        
        Returns:
            Divisional chart longitude
        """
        # Get sign and degree within sign
        sign_num = int(planet_longitude / 30)
        degree_in_sign = planet_longitude % 30
        
        # Calculate portion within division
        portion_size = 30.0 / division
        portion_num = int(degree_in_sign / portion_size)
        
        # Calculate divisional sign based on rules
        if division == 2:  # D2 - Hora (Wealth)
            # Odd signs start from Leo (4), Even signs start from Cancer (3)
            if sign_num % 2 == 0:  # Even signs (Taurus, Cancer, Virgo, etc.)
                div_sign = 3 if portion_num == 0 else 4
            else:  # Odd signs (Aries, Gemini, Leo, etc.)
                div_sign = 4 if portion_num == 0 else 3
        
        elif division == 9:  # D9 - Navamsa (Marriage/Dharma)
            # Count from the sign itself for movable, fixed from 9th, dual from 5th
            if sign_num in [0, 3, 6, 9]:  # Movable signs (Aries, Cancer, Libra, Capricorn)
                div_sign = (sign_num + portion_num) % 12
            elif sign_num in [1, 4, 7, 10]:  # Fixed signs (Taurus, Leo, Scorpio, Aquarius)
                div_sign = (sign_num + 8 + portion_num) % 12
            else:  # Dual signs (Gemini, Virgo, Sagittarius, Pisces)
                div_sign = (sign_num + 4 + portion_num) % 12
        
        elif division == 10:  # D10 - Dasamsa (Career/Profession)
            # Odd signs count from same sign, even signs from 9th
            if sign_num % 2 == 0:  # Even signs
                div_sign = (sign_num + 8 + portion_num) % 12
            else:  # Odd signs
                div_sign = (sign_num + portion_num) % 12
        
        elif division == 7:  # D7 - Saptamsa (Children)
            # Count from the sign itself for odd, from 7th for even
            if sign_num % 2 == 0:  # Even signs
                div_sign = (sign_num + 6 + portion_num) % 12
            else:  # Odd signs
                div_sign = (sign_num + portion_num) % 12
        
        elif division == 12:  # D12 - Dwadasamsa (Parents)
            div_sign = (sign_num + portion_num) % 12
        
        elif division == 30:  # D30 - Trimsamsa (Evils/Misfortunes)
            div_sign = (sign_num + portion_num) % 12
        
        else:  # Default calculation for other divisions
            div_sign = (sign_num * division + portion_num) % 12
        
        # Convert back to longitude (middle of the division)
        div_longitude = (div_sign * 30) + (portion_size / 2)
        
        return div_longitude
    
    def calculate_birth_chart(self, birth_details: BirthDetails, 
                              include_divisional: bool = True) -> Dict:
        """
        Calculate complete birth chart with divisional charts
        
        Args:
            birth_details: Birth details
            include_divisional: Whether to calculate divisional charts
        
        Returns:
            Dict with planets, houses, ascendant, divisional charts, etc.
        """
        self.logger.info(f"Calculating birth chart for {birth_details.name}")
        
        jd = self.calculate_julian_day(birth_details)
        
        # Calculate houses
        house_cusps = self.calculate_houses(
            jd, birth_details.latitude, birth_details.longitude
        )
        
        # Calculate Ascendant
        ascendant_lon = self.calculate_ascendant(
            jd, birth_details.latitude, birth_details.longitude
        )
        
        # Calculate all planets for D1 (Rasi chart)
        planets = {}
        
        for planet_name, planet_id in PLANETS.items():
            if planet_name == 'Ascendant':
                longitude = ascendant_lon
                is_retrograde = False
            elif planet_name == 'Ketu':
                # Ketu is 180° from Rahu
                rahu_lon = planets['Rahu'].longitude
                longitude = (rahu_lon + 180) % 360
                is_retrograde = False
            else:
                # get_planet_position now returns sidereal coordinates directly
                longitude, is_retrograde = self.get_planet_position(planet_id, jd)
            
            sign_num, sign_name, degree_in_sign = self.get_sign_and_degree(longitude)
            nakshatra, pada = self.get_nakshatra(longitude)
            # Use Whole Sign Houses for traditional Vedic astrology (D1 Lagna chart)
            house = self.get_planet_house_whole_sign(longitude, ascendant_lon)
            
            planets[planet_name] = PlanetPosition(
                name=planet_name,
                longitude=longitude,
                sign=sign_name,
                sign_num=sign_num,
                degree_in_sign=degree_in_sign,
                nakshatra=nakshatra,
                nakshatra_pada=pada,
                house=house,
                is_retrograde=is_retrograde
            )
        
        chart_data = {
            'birth_details': birth_details,
            'julian_day': jd,
            'ascendant': planets['Ascendant'],
            'planets': planets,
            'house_cusps': house_cusps,
            'ayanamsa': swe.get_ayanamsa_ut(jd)
        }
        
        # Calculate divisional charts
        if include_divisional:
            divisional_charts = {}
            
            # D2 - Hora (Wealth)
            divisional_charts['D2'] = self._create_divisional_chart(planets, ascendant_lon, 2)
            
            # D9 - Navamsa (Marriage, Dharma, Strength)
            divisional_charts['D9'] = self._create_divisional_chart(planets, ascendant_lon, 9)
            
            # D10 - Dasamsa (Career, Profession)
            divisional_charts['D10'] = self._create_divisional_chart(planets, ascendant_lon, 10)
            
            # D7 - Saptamsa (Children, Progeny)
            divisional_charts['D7'] = self._create_divisional_chart(planets, ascendant_lon, 7)
            
            # D12 - Dwadasamsa (Parents)
            divisional_charts['D12'] = self._create_divisional_chart(planets, ascendant_lon, 12)
            
            chart_data['divisional_charts'] = divisional_charts
        
        # Calculate Vimshottari Dasha
        moon_longitude = planets['Moon'].longitude
        dasha_periods = self.calculate_vimshottari_dasha(moon_longitude, birth_details.date)
        
        # Find current Mahadasha and Antardasha
        from datetime import datetime as dt
        today = dt.now()
        current_mahadasha = 'Unknown'
        current_antardasha = 'Unknown'
        
        for dasha in dasha_periods:
            if dasha['start_date'] <= today <= dasha['end_date']:
                current_mahadasha = dasha['lord']
                # Calculate antardashas for this period
                antardashas = self.calculate_antardashas(
                    dasha['lord'], 
                    dasha['start_date'], 
                    dasha['end_date']
                )
                # Find current antardasha
                for antar in antardashas:
                    if antar['start_date'] <= today <= antar['end_date']:
                        current_antardasha = antar['antar_dasha_lord']
                        break
                break
        
        chart_data['dasha'] = {
            'all_periods': dasha_periods,
            'current_mahadasha': current_mahadasha,
            'current_antardasha': current_antardasha
        }
        
        return chart_data
    
    def _create_divisional_chart(self, d1_planets: Dict[str, PlanetPosition], 
                                 d1_ascendant_lon: float, division: int) -> Dict:
        """Create a divisional chart from D1 positions"""
        div_planets = {}
        
        # Calculate divisional ascendant
        div_asc_lon = self.calculate_divisional_chart(d1_ascendant_lon, division)
        
        for planet_name, planet_d1 in d1_planets.items():
            if planet_name == 'Ascendant':
                div_lon = div_asc_lon
            else:
                div_lon = self.calculate_divisional_chart(planet_d1.longitude, division)
            
            sign_num, sign_name, degree_in_sign = self.get_sign_and_degree(div_lon)
            house = self.get_planet_house_whole_sign(div_lon, div_asc_lon)
            
            div_planets[planet_name] = {
                'sign': sign_name,
                'sign_num': sign_num,
                'house': house,
                'degree_in_sign': degree_in_sign,
                'is_retrograde': planet_d1.is_retrograde
            }
        
        return {
            'division': division,
            'ascendant_sign': SIGNS[int(div_asc_lon / 30)],
            'planets': div_planets
        }
    
    def calculate_vimshottari_dasha(self, moon_longitude: float, 
                                    birth_date: datetime) -> List[Dict]:
        """
        Calculate Vimshottari Dasha periods for 120 years
        
        Args:
            moon_longitude: Sidereal longitude of Moon
            birth_date: Date of birth
        
        Returns:
            List of dasha periods
        """
        # Determine starting dasha lord based on Moon's nakshatra
        nakshatra, _ = self.get_nakshatra(moon_longitude)
        nakshatra_num = NAKSHATRAS.index(nakshatra)
        
        # Starting dasha lord (cycles through 9 lords)
        start_index = nakshatra_num % 9
        
        # Calculate proportion of current nakshatra completed
        nakshatra_length = 360 / 27
        nakshatra_start = (nakshatra_num * nakshatra_length)
        completed_portion = (moon_longitude - nakshatra_start) / nakshatra_length
        
        # Calculate dashas for 120 years (full Vimshottari cycle)
        dashas = []
        current_date = birth_date
        total_years_covered = 0
        cycle_count = 0
        
        while total_years_covered < 120:
            for i in range(9):
                if total_years_covered >= 120:
                    break
                    
                lord_index = (start_index + i) % 9
                lord_name, total_years = VIMSHOTTARI_DASHA[lord_index]
                
                # First dasha is proportional
                if i == 0 and cycle_count == 0:
                    years_remaining = total_years * (1 - completed_portion)
                else:
                    years_remaining = total_years
                
                # Convert years to days
                days = int(years_remaining * 365.25)
                end_date = current_date + pd.Timedelta(days=days)
                
                dashas.append({
                    'lord': lord_name,
                    'start_date': current_date,
                    'end_date': end_date,
                    'years': years_remaining,
                    'maha_dasha_lord': lord_name,
                    'maha_dasha_start': current_date.strftime('%Y-%m-%d'),
                    'maha_dasha_end': end_date.strftime('%Y-%m-%d')
                })
                
                current_date = end_date
                total_years_covered += years_remaining
            
            cycle_count += 1
        
        return dashas
    
    def calculate_antardashas(self, maha_lord: str, maha_start: datetime, 
                             maha_end: datetime) -> List[Dict]:
        """
        Calculate Antardasha (sub-periods) within a Mahadasha
        
        Args:
            maha_lord: Lord of Mahadasha
            maha_start: Start date of Mahadasha
            maha_end: End date of Mahadasha
        
        Returns:
            List of antardasha periods
        """
        # Get mahadasha duration
        maha_duration_years = None
        for lord, years in VIMSHOTTARI_DASHA:
            if lord == maha_lord:
                maha_duration_years = years
                break
        
        if not maha_duration_years:
            return []
        
        # Total days in mahadasha
        total_days = (maha_end - maha_start).days
        
        # Find index of maha lord
        maha_index = None
        for idx, (lord, _) in enumerate(VIMSHOTTARI_DASHA):
            if lord == maha_lord:
                maha_index = idx
                break
        
        antardashas = []
        current_date = maha_start
        
        # Calculate antardashas in sequence starting from maha lord
        for i in range(9):
            antar_index = (maha_index + i) % 9
            antar_lord, antar_years = VIMSHOTTARI_DASHA[antar_index]
            
            # Antardasha proportion = (antar_years / total_maha_years) * total_maha_years
            antar_proportion = antar_years / 120.0  # Proportion in 120-year cycle
            antar_duration_years = antar_proportion * maha_duration_years
            antar_days = int(antar_duration_years * 365.25)
            
            end_date = current_date + pd.Timedelta(days=antar_days)
            
            # Don't exceed mahadasha end
            if end_date > maha_end:
                end_date = maha_end
            
            antardashas.append({
                'maha_dasha_lord': maha_lord,
                'antar_dasha_lord': antar_lord,
                'antar_dasha_start': current_date.strftime('%Y-%m-%d'),
                'antar_dasha_end': end_date.strftime('%Y-%m-%d'),
                'antar_duration_years': antar_duration_years,
                'lord': f"{maha_lord}-{antar_lord}",
                'start_date': current_date,
                'end_date': end_date
            })
            
            current_date = end_date
            
            if current_date >= maha_end:
                break
        
        return antardashas


# Initialize pandas for date calculations
import pandas as pd
