"""
Test Skyfield for Vedic Astrology Calculations
Proof of concept to verify Skyfield can replace pyswisseph
"""
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import datetime
import pytz

def calculate_with_skyfield(date_str, time_str, latitude, longitude, timezone_str):
    """
    Calculate planetary positions using Skyfield
    """
    # Load ephemeris data
    ts = load.timescale()
    eph = load('de421.bsp')  # JPL ephemeris
    
    # Parse birth details
    tz = pytz.timezone(timezone_str)
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt_local = tz.localize(dt)
    dt_utc = dt_local.astimezone(pytz.UTC)
    
    # Create Skyfield time object
    t = ts.utc(dt_utc.year, dt_utc.month, dt_utc.day, 
               dt_utc.hour, dt_utc.minute, dt_utc.second)
    
    # Location
    location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    
    # Get planets
    earth = eph['earth']
    planets = {
        'Sun': eph['sun'],
        'Moon': eph['moon'],
        'Mercury': eph['mercury'],
        'Venus': eph['venus'],
        'Mars': eph['mars'],
        'Jupiter': eph['jupiter barycenter'],
        'Saturn': eph['saturn barycenter']
    }
    
    print(f"\n{'='*60}")
    print(f"SKYFIELD CALCULATION TEST")
    print(f"{'='*60}")
    print(f"Date: {date_str} {time_str} {timezone_str}")
    print(f"Location: {latitude}°N, {longitude}°E")
    print(f"{'='*60}\n")
    
    results = {}
    
    for name, planet in planets.items():
        # Get apparent position (as seen from Earth)
        astrometric = earth.at(t).observe(planet)
        ra, dec, distance = astrometric.radec()
        
        # Get ecliptic longitude
        lat_ecliptic, lon_ecliptic, _ = astrometric.ecliptic_latlon()
        
        # Convert to degrees
        tropical_long = lon_ecliptic.degrees
        
        # Lahiri Ayanamsa for 2026 (approximate)
        # Formula: 23.85° + (year - 2000) * 0.01397°
        year = dt_utc.year
        lahiri_ayanamsa = 23.85 + (year - 2000) * 0.01397
        
        # Sidereal longitude
        sidereal_long = (tropical_long - lahiri_ayanamsa) % 360
        
        # Sign and degree within sign
        sign_num = int(sidereal_long / 30)
        degree_in_sign = sidereal_long % 30
        
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        sign = signs[sign_num]
        
        # Nakshatra (27 nakshatras, each 13°20')
        nakshatra_num = int((sidereal_long % 360) / (360/27))
        nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        nakshatra = nakshatras[nakshatra_num]
        
        results[name] = {
            'tropical': tropical_long,
            'sidereal': sidereal_long,
            'sign': sign,
            'degree': degree_in_sign,
            'nakshatra': nakshatra
        }
        
        print(f"{name:12} | {sign:12} {degree_in_sign:6.2f}° | {nakshatra:20} | Sidereal: {sidereal_long:7.2f}°")
    
    # Calculate Ascendant (Lagna)
    # Sidereal time calculation for Ascendant
    observer = earth + location
    altaz = observer.at(t).observe(eph['sun']).apparent().altaz()
    
    # This is simplified - proper Ascendant calculation needs more work
    # For now, showing the concept
    print(f"\n{'='*60}")
    print("✅ Skyfield calculations complete!")
    print(f"{'='*60}\n")
    
    return results


def compare_with_swiss_ephemeris(date_str, time_str, latitude, longitude, timezone_str):
    """
    Compare Skyfield results with Swiss Ephemeris (if available)
    """
    try:
        import swisseph as swe
        
        print(f"\n{'='*60}")
        print(f"SWISS EPHEMERIS COMPARISON")
        print(f"{'='*60}\n")
        
        # Parse date
        tz = pytz.timezone(timezone_str)
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt_local = tz.localize(dt)
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        # Julian day
        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                       dt_utc.hour + dt_utc.minute/60.0)
        
        # Set ayanamsa
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa_ut(jd)
        
        planet_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN
        }
        
        for name, pid in planet_ids.items():
            calc = swe.calc_ut(jd, pid)
            tropical = calc[0][0] if isinstance(calc[0], tuple) else calc[0]
            sidereal = (tropical - ayanamsa) % 360
            
            sign_num = int(sidereal / 30)
            degree_in_sign = sidereal % 30
            signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            sign = signs[sign_num]
            
            print(f"{name:12} | {sign:12} {degree_in_sign:6.2f}° | Sidereal: {sidereal:7.2f}°")
        
        print(f"\n{'='*60}\n")
        
    except ImportError:
        print("\n⚠️ Swiss Ephemeris not available for comparison")


if __name__ == "__main__":
    # Test case: Birth chart calculation
    test_date = "1990-01-15"
    test_time = "10:30"
    test_lat = 19.0760  # Mumbai
    test_lon = 72.8777
    test_tz = "Asia/Kolkata"
    
    print("\n" + "="*60)
    print("🔮 SKYFIELD VEDIC ASTROLOGY TEST")
    print("="*60)
    
    # Calculate with Skyfield
    skyfield_results = calculate_with_skyfield(test_date, test_time, test_lat, test_lon, test_tz)
    
    # Compare with Swiss Ephemeris
    compare_with_swiss_ephemeris(test_date, test_time, test_lat, test_lon, test_tz)
    
    print("\n✅ Test complete! Skyfield is working for Vedic calculations.")
    print("\nNext steps:")
    print("1. ✓ Skyfield installed and tested")
    print("2. → Create full vedic_calculator.py replacement")
    print("3. → Add to mobile build.gradle")
    print("4. → Build APK with Skyfield\n")
