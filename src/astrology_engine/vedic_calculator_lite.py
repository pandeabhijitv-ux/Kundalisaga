"""
Lite Vedic Calculator for Mobile (Using Pre-computed Ephemeris Database)
Reads planetary positions from SQLite database and performs interpolation
"""
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import pytz
import math

# Zodiac Signs
SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Nakshatras
NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Vimshottari Dasha
VIMSHOTTARI_DASHA = [
    ('Ketu', 7), ('Venus', 20), ('Sun', 6), ('Moon', 10),
    ('Mars', 7), ('Rahu', 18), ('Jupiter', 16), ('Saturn', 19), ('Mercury', 17)
]

NAKSHATRA_LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 
                   'Jupiter', 'Saturn', 'Mercury'] * 3


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


class EphemerisDatabase:
    """Handler for ephemeris database"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        # Auto-detect database location
        if db_path is None:
            # Try common locations
            possible_paths = [
                "ephemeris.db",  # Current directory (Android assets)
                "mobile/android/app/src/main/assets/ephemeris.db",  # Desktop development
                "/data/data/com.kundalii.saga/files/ephemeris.db"  # Android data directory (if copied)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    db_path = path
                    break
            
            if db_path is None:
                raise FileNotFoundError("Ephemeris database not found")
        
        self.db_path = db_path
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Database connection error: {e}")
            self.conn = None
    
    def get_position(self, planet: str, date: str) -> Optional[Dict]:
        """Get position for a planet on a specific date"""
        if not self.conn:
            return None
        
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM ephemeris WHERE date=? AND planet=?",
            (date, planet)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                'longitude': row['longitude'],
                'latitude': row['latitude'],
                'distance': row['distance'],
                'speed': row['speed']
            }
        return None
    
    def interpolate_position(self, planet: str, dt: datetime) -> Optional[Dict]:
        """Interpolate position for exact datetime"""
        # Get date and time fraction
        date_floor = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        date_ceil = date_floor + timedelta(days=1)
        
        time_fraction = (dt - date_floor).total_seconds() / 86400.0
        
        # Get positions for both dates
        pos1 = self.get_position(planet, date_floor.strftime('%Y-%m-%d'))
        pos2 = self.get_position(planet, date_ceil.strftime('%Y-%m-%d'))
        
        if not pos1 or not pos2:
            return None
        
        # Handle 360° wrap-around for longitude
        lon1 = pos1['longitude']
        lon2 = pos2['longitude']
        
        # Check for wrap-around
        if abs(lon2 - lon1) > 180:
            if lon2 < lon1:
                lon2 += 360
            else:
                lon1 += 360
        
        # Linear interpolation
        longitude = lon1 + (lon2 - lon1) * time_fraction
        longitude = longitude % 360  # Normalize
        
        # Determine retrograde (if speed is negative or longitude decreased)
        is_retrograde = pos1['speed'] < 0
        
        return {
            'longitude': longitude,
            'is_retrograde': is_retrograde
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class VedicAstrologyEngine:
    """Lite Vedic Astrology Engine using pre-computed ephemeris"""
    
    def __init__(self, db_path: str = "ephemeris.db"):
        """Initialize engine"""
        self.db = EphemerisDatabase(db_path)
    
    def calculate_planetary_positions(self, birth_details: BirthDetails) -> List[PlanetPosition]:
        """Calculate positions of all planets"""
        # Convert to UTC
        tz = pytz.timezone(birth_details.timezone)
        dt_local = birth_details.date
        if dt_local.tzinfo is None:
            dt_local = tz.localize(dt_local)
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        positions = []
        
        # Get all planets
        planets_list = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        
        for planet_name in planets_list:
            pos_data = self.db.interpolate_position(planet_name, dt_utc)
            
            if pos_data:
                longitude = pos_data['longitude']
                is_retrograde = pos_data['is_retrograde']
                
                # Calculate sign
                sign_num = int(longitude / 30)
                sign = SIGNS[sign_num]
                degree_in_sign = longitude % 30
                
                # Calculate nakshatra
                nakshatra_num = int((longitude % 360) / (360/27))
                nakshatra = NAKSHATRAS[nakshatra_num]
                
                # Calculate pada
                nakshatra_progress = (longitude % 360) % (360/27)
                pada = int(nakshatra_progress / ((360/27)/4)) + 1
                
                # House (placeholder - will be calculated after Ascendant)
                house = 1
                
                positions.append(PlanetPosition(
                    name=planet_name,
                    longitude=longitude,
                    sign=sign,
                    sign_num=sign_num,
                    degree_in_sign=degree_in_sign,
                    nakshatra=nakshatra,
                    nakshatra_pada=pada,
                    house=house,
                    is_retrograde=is_retrograde
                ))
        
        return positions
    
    def calculate_ascendant(self, birth_details: BirthDetails) -> float:
        """Calculate Ascendant (simplified for mobile)"""
        # Convert to UTC
        tz = pytz.timezone(birth_details.timezone)
        dt_local = birth_details.date
        if dt_local.tzinfo is None:
            dt_local = tz.localize(dt_local)
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        # Calculate Local Sidereal Time (LST)
        # Formula: GST = 6.697374558 + 0.06570982441908 * D + 1.00273790935 * UT
        # where D is days since J2000.0
        
        j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        days_since_j2000 = (dt_utc - j2000).total_seconds() / 86400.0
        
        ut_hours = dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
        
        gst = 6.697374558 + 0.06570982441908 * days_since_j2000 + 1.00273790935 * ut_hours
        gst = (gst % 24) * 15  # Convert hours to degrees
        
        lst = gst + birth_details.longitude
        lst = lst % 360
        
        # Calculate Ascendant using obliquity of ecliptic
        obliquity = 23.4392911
        lat_rad = math.radians(birth_details.latitude)
        lst_rad = math.radians(lst)
        obl_rad = math.radians(obliquity)
        
        numerator = math.cos(lst_rad)
        denominator = (math.sin(lst_rad) * math.cos(obl_rad) - 
                      math.tan(lat_rad) * math.sin(obl_rad))
        
        asc_rad = math.atan2(numerator, denominator)
        asc_tropical = math.degrees(asc_rad) % 360
        
        # Convert to sidereal (approximate Lahiri ayanamsa for 2026)
        year = dt_utc.year
        lahiri_ayanamsa = 23.85 + (year - 2000) * 0.01397
        asc_sidereal = (asc_tropical - lahiri_ayanamsa) % 360
        
        return asc_sidereal
    
    def calculate_chart(self, birth_details: BirthDetails) -> Dict:
        """Calculate complete birth chart"""
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
            
            # Update house positions
            for planet in planets:
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
            ascendant = None
            print(f"Ascendant calculation error: {e}")
        
        return {
            'birth_details': birth_details,
            'planets': planets,
            'ascendant': ascendant
        }
    
    def calculate_vimshottari_dasha(self, birth_date: datetime, moon_longitude: float) -> List[Dict]:
        """Calculate Vimshottari Dasha periods"""
        nakshatra_num = int((moon_longitude % 360) / (360/27))
        nakshatra_lord = NAKSHATRA_LORDS[nakshatra_num]
        
        nakshatra_span = 360 / 27
        nakshatra_start = nakshatra_num * nakshatra_span
        progress_in_nakshatra = moon_longitude - nakshatra_start
        fraction_elapsed = progress_in_nakshatra / nakshatra_span
        
        dasha_index = next(i for i, (lord, _) in enumerate(VIMSHOTTARI_DASHA) 
                          if lord == nakshatra_lord)
        
        _, total_years = VIMSHOTTARI_DASHA[dasha_index]
        remaining_years = total_years * (1 - fraction_elapsed)
        
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
        years_added = remaining_years
        next_dasha_index = (dasha_index + 1) % len(VIMSHOTTARI_DASHA)
        
        while years_added < 120:
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
    
    def close(self):
        """Close database connection"""
        self.db.close()
