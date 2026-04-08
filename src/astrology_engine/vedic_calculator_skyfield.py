"""
Vedic Astrology Calculation Engine using Skyfield
Pure Python implementation for mobile compatibility
"""
from skyfield.api import load, Topos, Star
from skyfield import almanac
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pytz
import math

try:
    from geopy.geocoders import Nominatim
    from timezonefinder import TimezoneFinder
    GEOCODING_AVAILABLE = True
except ImportError:
    GEOCODING_AVAILABLE = False


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

# Nakshatra lords for Vimshottari Dasha
NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 
    'Jupiter', 'Saturn', 'Mercury'
] * 3  # Repeat 3 times for 27 nakshatras


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
    """Vedic Astrology calculation engine using Skyfield (Pure Python)"""
    
    def __init__(self, ayanamsa_name: str = 'LAHIRI'):
        """
        Initialize Vedic Astrology Engine
        
        Args:
            ayanamsa_name: Type of ayanamsa (LAHIRI, RAMAN, KP)
        """
        self.ayanamsa_name = ayanamsa_name
        self.ts = load.timescale()
        
        # Load ephemeris (JPL DE421)
        try:
            self.eph = load('de421.bsp')
        except:
            # If ephemeris not found, Skyfield will download it automatically
            self.eph = load('de421.bsp')
        
        self.earth = self.eph['earth']
        self.planets_map = {
            'Sun': self.eph['sun'],
            'Moon': self.eph['moon'],
            'Mercury': self.eph['mercury'],
            'Venus': self.eph['venus'],
            'Mars': self.eph['mars'],
            'Jupiter': self.eph['jupiter barycenter'],
            'Saturn': self.eph['saturn barycenter']
        }
    
    def calculate_lahiri_ayanamsa(self, year: int, month: int = 1, day: int = 1) -> float:
        """
        Calculate Lahiri Ayanamsa for a given date
        
        Formula based on: 23.85° at 2000.0 + 50.2388475" per year
        
        Args:
            year: Year
            month: Month (default 1)
            day: Day (default 1)
        
        Returns:
            Ayanamsa in degrees
        """
        # Calculate decimal year
        dt = datetime(year, month, day)
        start_of_year = datetime(year, 1, 1)
        days_in_year = 366 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 365
        decimal_year = year + (dt - start_of_year).days / days_in_year
        
        # Lahiri ayanamsa formula
        # Base: 23.85° at 2000.0
        # Rate: 50.2388475" per year = 0.01395801875° per year
        base_ayanamsa = 23.85
        years_from_2000 = decimal_year - 2000.0
        rate_per_year = 50.2388475 / 3600  # Convert arcseconds to degrees
        
        ayanamsa = base_ayanamsa + (years_from_2000 * rate_per_year)
        
        return ayanamsa
    
    def get_ayanamsa(self, year: int, month: int = 1, day: int = 1) -> float:
        """
        Get ayanamsa based on selected system
        
        Args:
            year: Year
            month: Month
            day: Day
        
        Returns:
            Ayanamsa in degrees
        """
        if self.ayanamsa_name == 'RAMAN':
            # Raman ayanamsa (approximately 1° less than Lahiri)
            return self.calculate_lahiri_ayanamsa(year, month, day) - 1.0
        elif self.ayanamsa_name == 'KP':
            # KP ayanamsa (Krishnamurti - similar to Lahiri with slight variation)
            return self.calculate_lahiri_ayanamsa(year, month, day) + 0.167
        else:
            # Default: Lahiri
            return self.calculate_lahiri_ayanamsa(year, month, day)
    
    def _create_skyfield_time(self, dt_utc: datetime):
        """Create Skyfield time object from UTC datetime"""
        return self.ts.utc(dt_utc.year, dt_utc.month, dt_utc.day,
                          dt_utc.hour, dt_utc.minute, dt_utc.second)
    
    def calculate_planetary_positions(self, birth_details: BirthDetails) -> List[PlanetPosition]:
        """
        Calculate positions of all planets
        
        Args:
            birth_details: Birth details
        
        Returns:
            List of PlanetPosition objects
        """
        # Convert to UTC
        tz = pytz.timezone(birth_details.timezone)
        dt_local = birth_details.date
        if dt_local.tzinfo is None:
            dt_local = tz.localize(dt_local)
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        # Create Skyfield time
        t = self._create_skyfield_time(dt_utc)
        
        # Get ayanamsa
        ayanamsa = self.get_ayanamsa(dt_utc.year, dt_utc.month, dt_utc.day)
        
        positions = []
        
        # Calculate positions for each planet
        for planet_name, planet_body in self.planets_map.items():
            # Get geocentric position
            astrometric = self.earth.at(t).observe(planet_body)
            
            # Get ecliptic longitude
            lat_ecliptic, lon_ecliptic, distance = astrometric.ecliptic_latlon()
            tropical_long = lon_ecliptic.degrees
            
            # Convert to sidereal
            sidereal_long = (tropical_long - ayanamsa) % 360
            
            # Check for retrograde motion (compare position with day before)
            t_yesterday = self._create_skyfield_time(dt_utc - timedelta(days=1))
            astrometric_yesterday = self.earth.at(t_yesterday).observe(planet_body)
            lat_y, lon_y, _ = astrometric_yesterday.ecliptic_latlon()
            tropical_yesterday = lon_y.degrees
            sidereal_yesterday = (tropical_yesterday - ayanamsa) % 360
            
            # Retrograde if position decreased (accounting for 360° wrap)
            longitude_diff = sidereal_long - sidereal_yesterday
            if longitude_diff < -180:
                longitude_diff += 360
            elif longitude_diff > 180:
                longitude_diff -= 360
            is_retrograde = longitude_diff < 0
            
            # Calculate sign
            sign_num = int(sidereal_long / 30)
            sign = SIGNS[sign_num]
            degree_in_sign = sidereal_long % 30
            
            # Calculate nakshatra
            nakshatra_num = int((sidereal_long % 360) / (360/27))
            nakshatra = NAKSHATRAS[nakshatra_num]
            
            # Calculate pada (quarter of nakshatra)
            nakshatra_progress = (sidereal_long % 360) % (360/27)
            pada = int(nakshatra_progress / ((360/27)/4)) + 1
            
            # House calculation (placeholder - needs Ascendant)
            house = 1  # Will be calculated after Ascendant
            
            positions.append(PlanetPosition(
                name=planet_name,
                longitude=sidereal_long,
                sign=sign,
                sign_num=sign_num,
                degree_in_sign=degree_in_sign,
                nakshatra=nakshatra,
                nakshatra_pada=pada,
                house=house,
                is_retrograde=is_retrograde
            ))
        
        # Calculate Rahu (North Node) and Ketu (South Node)
        # Rahu is the ascending node of the Moon
        # For simplicity, using approximate mean node calculation
        # True node would require more complex orbital mechanics
        
        # Mean node approximation (simplified)
        # Rahu longitude (Mean Node) - approximate formula
        days_since_epoch = (dt_utc - datetime(2000, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)).total_seconds() / 86400
        mean_node_long = (125.04 - 0.05295 * days_since_epoch) % 360
        rahu_sidereal = (mean_node_long - ayanamsa) % 360
        
        # Rahu position
        rahu_sign_num = int(rahu_sidereal / 30)
        rahu_nakshatra_num = int((rahu_sidereal % 360) / (360/27))
        rahu_nakshatra_progress = (rahu_sidereal % 360) % (360/27)
        rahu_pada = int(rahu_nakshatra_progress / ((360/27)/4)) + 1
        
        positions.append(PlanetPosition(
            name='Rahu',
            longitude=rahu_sidereal,
            sign=SIGNS[rahu_sign_num],
            sign_num=rahu_sign_num,
            degree_in_sign=rahu_sidereal % 30,
            nakshatra=NAKSHATRAS[rahu_nakshatra_num],
            nakshatra_pada=rahu_pada,
            house=1,
            is_retrograde=True  # Rahu is always retrograde
        ))
        
        # Ketu is 180° opposite to Rahu
        ketu_sidereal = (rahu_sidereal + 180) % 360
        ketu_sign_num = int(ketu_sidereal / 30)
        ketu_nakshatra_num = int((ketu_sidereal % 360) / (360/27))
        ketu_nakshatra_progress = (ketu_sidereal % 360) % (360/27)
        ketu_pada = int(ketu_nakshatra_progress / ((360/27)/4)) + 1
        
        positions.append(PlanetPosition(
            name='Ketu',
            longitude=ketu_sidereal,
            sign=SIGNS[ketu_sign_num],
            sign_num=ketu_sign_num,
            degree_in_sign=ketu_sidereal % 30,
            nakshatra=NAKSHATRAS[ketu_nakshatra_num],
            nakshatra_pada=ketu_pada,
            house=1,
            is_retrograde=True  # Ketu is always retrograde
        ))
        
        return positions
    
    def calculate_ascendant(self, birth_details: BirthDetails) -> float:
        """
        Calculate Ascendant (Lagna) using sidereal time
        
        Args:
            birth_details: Birth details
        
        Returns:
            Ascendant longitude in degrees
        """
        # Convert to UTC
        tz = pytz.timezone(birth_details.timezone)
        dt_local = birth_details.date
        if dt_local.tzinfo is None:
            dt_local = tz.localize(dt_local)
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        # Create Skyfield time and location
        t = self._create_skyfield_time(dt_utc)
        location = Topos(latitude_degrees=birth_details.latitude,
                        longitude_degrees=birth_details.longitude)
        
        # Calculate Local Sidereal Time (LST)
        observer = self.earth + location
        lst_degrees = observer.at(t).lst_hours_at(birth_details.longitude) * 15
        
        # Calculate Ascendant using Obliquity of Ecliptic
        # Formula: tan(Asc) = cos(LST) / (sin(LST) * cos(obliquity) - tan(latitude) * sin(obliquity))
        
        obliquity = 23.4392911  # Mean obliquity of ecliptic (degrees)
        lat_rad = math.radians(birth_details.latitude)
        lst_rad = math.radians(lst_degrees)
        obl_rad = math.radians(obliquity)
        
        # Calculate tropical Ascendant
        numerator = math.cos(lst_rad)
        denominator = (math.sin(lst_rad) * math.cos(obl_rad) - 
                      math.tan(lat_rad) * math.sin(obl_rad))
        
        asc_rad = math.atan2(numerator, denominator)
        asc_tropical = math.degrees(asc_rad) % 360
        
        # Convert to sidereal
        ayanamsa = self.get_ayanamsa(dt_utc.year, dt_utc.month, dt_utc.day)
        asc_sidereal = (asc_tropical - ayanamsa) % 360
        
        return asc_sidereal
    
    def calculate_chart(self, birth_details: BirthDetails) -> Dict:
        """
        Calculate complete birth chart
        
        Args:
            birth_details: Birth details
        
        Returns:
            Dictionary with chart data
        """
        # Calculate planetary positions
        planets = self.calculate_planetary_positions(birth_details)
        
        # Calculate Ascendant
        try:
            ascendant_long = self.calculate_ascendant(birth_details)
            ascendant_sign_num = int(ascendant_long / 30)
            ascendant_sign = SIGNS[ascendant_sign_num]
            ascendant_degree = ascendant_long % 30
            ascendant_nakshatra_num = int((ascendant_long % 360) / (360/27))
            ascendant_nakshatra = NAKSHATRAS[ascendant_nakshatra_num]
            
            # Update house positions for planets
            for planet in planets:
                # House = (Planet sign - Ascendant sign + 1)
                house_num = ((planet.sign_num - ascendant_sign_num) % 12) + 1
                planet.house = house_num
            
            ascendant = PlanetPosition(
                name='Ascendant',
                longitude=ascendant_long,
                sign=ascendant_sign,
                sign_num=ascendant_sign_num,
                degree_in_sign=ascendant_degree,
                nakshatra=ascendant_nakshatra,
                nakshatra_pada=1,
                house=1,
                is_retrograde=False
            )
        except Exception as e:
            # If Ascendant calculation fails, create a placeholder
            ascendant = None
        
        return {
            'birth_details': birth_details,
            'planets': planets,
            'ascendant': ascendant,
            'ayanamsa': self.get_ayanamsa(birth_details.date.year, 
                                         birth_details.date.month,
                                         birth_details.date.day)
        }
    
    def calculate_vimshottari_dasha(self, birth_date: datetime, moon_longitude: float) -> List[Dict]:
        """
        Calculate Vimshottari Dasha periods
        
        Args:
            birth_date: Date of birth
            moon_longitude: Moon's sidereal longitude
        
        Returns:
            List of dasha periods
        """
        # Determine birth nakshatra
        nakshatra_num = int((moon_longitude % 360) / (360/27))
        
        # Get Nakshatra lord
        nakshatra_lord = NAKSHATRA_LORDS[nakshatra_num]
        
        # Calculate how much of the nakshatra has passed
        nakshatra_span = 360 / 27  # 13.333...°
        nakshatra_start = nakshatra_num * nakshatra_span
        progress_in_nakshatra = moon_longitude - nakshatra_start
        fraction_elapsed = progress_in_nakshatra / nakshatra_span
        
        # Find the dasha of birth nakshatra lord
        dasha_index = next(i for i, (lord, _) in enumerate(VIMSHOTTARI_DASHA) 
                          if lord == nakshatra_lord)
        
        # Calculate remaining years in birth dasha
        _, total_years = VIMSHOTTARI_DASHA[dasha_index]
        remaining_years = total_years * (1 - fraction_elapsed)
        
        # Generate dasha periods
        dashas = []
        current_date = birth_date
        
        # Add remaining period of birth dasha
        lord, years = VIMSHOTTARI_DASHA[dasha_index]
        end_date = current_date + timedelta(days=remaining_years * 365.25)
        dashas.append({
            'lord': lord,
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'years': remaining_years
        })
        current_date = end_date
        
        # Add subsequent dashas
        total_cycle_years = sum(years for _, years in VIMSHOTTARI_DASHA)  # 120 years
        years_added = remaining_years
        
        next_dasha_index = (dasha_index + 1) % len(VIMSHOTTARI_DASHA)
        
        while years_added < 120:  # Complete 120-year cycle
            lord, years = VIMSHOTTARI_DASHA[next_dasha_index]
            end_date = current_date + timedelta(days=years * 365.25)
            
            dashas.append({
                'lord': lord,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'years': years
            })
            
            current_date = end_date
            years_added += years
            next_dasha_index = (next_dasha_index + 1) % len(VIMSHOTTARI_DASHA)
        
        return dashas
    
    def get_location_info(self, place_name: str) -> Optional[Dict]:
        """
        Get latitude, longitude, and timezone for a place
        
        Args:
            place_name: Name of the place
        
        Returns:
            Dict with lat, lon, timezone or None
        """
        if not GEOCODING_AVAILABLE:
            return None
        
        try:
            geolocator = Nominatim(user_agent="kundalisaga_mobile")
            location = geolocator.geocode(place_name)
            
            if location:
                tf = TimezoneFinder()
                timezone = tf.timezone_at(lat=location.latitude, lng=location.longitude)
                
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'timezone': timezone,
                    'place': location.address
                }
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
        
        return None
