"""
Generate Pre-computed Ephemeris Database for Mobile App
Uses Swiss Ephemeris to generate accurate planetary positions
Stores in SQLite for fast mobile access
"""
import sqlite3
import swisseph as swe
from datetime import datetime, timedelta
from tqdm import tqdm
import os

# Configuration
START_YEAR = 1900
END_YEAR = 2100
DB_PATH = "mobile/android/app/src/main/assets/ephemeris.db"

# Planets to calculate
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
}

def create_database():
    """Create SQLite database with schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop existing table if any
    cursor.execute("DROP TABLE IF EXISTS ephemeris")
    
    # Create table
    cursor.execute("""
        CREATE TABLE ephemeris (
            date TEXT NOT NULL,
            planet TEXT NOT NULL,
            longitude REAL NOT NULL,
            latitude REAL NOT NULL,
            distance REAL NOT NULL,
            speed REAL NOT NULL,
            PRIMARY KEY (date, planet)
        )
    """)
    
    # Create index for fast lookups
    cursor.execute("CREATE INDEX idx_date_planet ON ephemeris(date, planet)")
    
    conn.commit()
    return conn

def calculate_positions_for_date(jd, date_str):
    """Calculate positions for all planets for a given date"""
    positions = []
    
    # Set Lahiri ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    
    for planet_name, planet_id in PLANETS.items():
        try:
            # Calculate tropical position
            calc = swe.calc_ut(jd, planet_id)
            tropical_long = calc[0][0]
            latitude = calc[0][1]
            distance = calc[0][2]
            speed = calc[0][3]
            
            # Convert to sidereal
            sidereal_long = (tropical_long - ayanamsa) % 360
            
            positions.append({
                'date': date_str,
                'planet': planet_name,
                'longitude': sidereal_long,
                'latitude': latitude,
                'distance': distance,
                'speed': speed
            })
        except Exception as e:
            print(f"Error calculating {planet_name} for {date_str}: {e}")
    
    # Calculate Ketu (180° opposite to Rahu)
    rahu_pos = next(p for p in positions if p['planet'] == 'Rahu')
    positions.append({
        'date': date_str,
        'planet': 'Ketu',
        'longitude': (rahu_pos['longitude'] + 180) % 360,
        'latitude': -rahu_pos['latitude'],
        'distance': rahu_pos['distance'],
        'speed': -rahu_pos['speed']
    })
    
    return positions

def generate_ephemeris():
    """Generate ephemeris data for the date range"""
    print(f"\n{'='*70}")
    print("🔮 GENERATING EPHEMERIS DATABASE")
    print(f"{'='*70}")
    print(f"Date Range: {START_YEAR} - {END_YEAR}")
    print(f"Output: {DB_PATH}")
    print(f"{'='*70}\n")
    
    # Create database
    conn = create_database()
    cursor = conn.cursor()
    
    # Calculate total days
    start_date = datetime(START_YEAR, 1, 1)
    end_date = datetime(END_YEAR, 12, 31)
    total_days = (end_date - start_date).days + 1
    
    print(f"Calculating positions for {total_days:,} days...")
    print(f"Total records: {total_days * len(PLANETS) + total_days:,} (including Ketu)\n")
    
    # Generate data with progress bar
    current_date = start_date
    batch = []
    batch_size = 100  # Insert in batches for speed
    
    with tqdm(total=total_days, desc="Generating ephemeris", unit="days") as pbar:
        while current_date <= end_date:
            # Calculate Julian Day (noon UTC)
            jd = swe.julday(current_date.year, current_date.month, current_date.day, 12.0)
            
            # Calculate positions
            date_str = current_date.strftime('%Y-%m-%d')
            positions = calculate_positions_for_date(jd, date_str)
            
            # Add to batch
            for pos in positions:
                batch.append((
                    pos['date'],
                    pos['planet'],
                    pos['longitude'],
                    pos['latitude'],
                    pos['distance'],
                    pos['speed']
                ))
            
            # Insert batch
            if len(batch) >= batch_size * 9:  # 9 planets per day
                cursor.executemany(
                    "INSERT INTO ephemeris VALUES (?, ?, ?, ?, ?, ?)",
                    batch
                )
                conn.commit()
                batch = []
            
            current_date += timedelta(days=1)
            pbar.update(1)
    
    # Insert remaining records
    if batch:
        cursor.executemany(
            "INSERT INTO ephemeris VALUES (?, ?, ?, ?, ?, ?)",
            batch
        )
        conn.commit()
    
    # Vacuum to optimize size
    print("\nOptimizing database size...")
    cursor.execute("VACUUM")
    conn.commit()
    
    # Get database size
    db_size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM ephemeris")
    record_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n{'='*70}")
    print("✅ DATABASE GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Location: {DB_PATH}")
    print(f"Size: {db_size_mb:.2f} MB")
    print(f"Records: {record_count:,}")
    print(f"Date Range: {START_YEAR}-01-01 to {END_YEAR}-12-31")
    print(f"{'='*70}\n")
    
    # Test query
    print("Testing database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ephemeris WHERE date='2024-01-01' AND planet='Sun'")
    test_record = cursor.fetchone()
    if test_record:
        print(f"✅ Test query successful!")
        print(f"   Sun on 2024-01-01: {test_record[2]:.2f}° (sidereal longitude)")
    conn.close()
    
    print(f"\n{'='*70}")
    print("📱 READY FOR MOBILE BUILD!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    generate_ephemeris()
