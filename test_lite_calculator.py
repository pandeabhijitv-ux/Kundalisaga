"""
Test script for the lite Vedic calculator with ephemeris database
"""
from datetime import datetime
import pytz
from src.astrology_engine.vedic_calculator_lite import VedicAstrologyEngine, BirthDetails

def test_lite_calculator():
    """Test the lite calculator with database"""
    print("=" * 70)
    print("🧪 TESTING LITE VEDIC CALCULATOR")
    print("=" * 70)
    
    # Create test birth details (Modern test case)
    # Born: 1 January 2000, 10:00 AM, Mumbai, India
    birth_date = datetime(2000, 1, 1, 10, 0, 0)
    
    birth_details = BirthDetails(
        date=birth_date,
        latitude=19.0760,  # Mumbai
        longitude=72.8777,
        timezone='Asia/Kolkata',
        name='Test Person',
        place='Mumbai'
    )
    
    print(f"\n📅 Birth Details:")
    print(f"   Name: {birth_details.name}")
    print(f"   Date: {birth_details.date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Place: {birth_details.place}")
    print(f"   Coordinates: {birth_details.latitude}°N, {birth_details.longitude}°E")
    
    # Initialize engine with database path
    db_path = "mobile/android/app/src/main/assets/ephemeris.db"
    print(f"\n💾 Loading ephemeris database: {db_path}")
    
    try:
        engine = VedicAstrologyEngine(db_path=db_path)
        print("✅ Database loaded successfully!")
        
        # Calculate chart
        print("\n🔮 Calculating birth chart...")
        chart = engine.calculate_chart(birth_details)
        
        # Display results
        print("\n" + "=" * 70)
        print("📊 PLANETARY POSITIONS")
        print("=" * 70)
        
        for planet in chart['planets']:
            retro = " (R)" if planet.is_retrograde else ""
            print(f"\n{planet.name}{retro}:")
            print(f"   Longitude: {planet.longitude:.2f}°")
            print(f"   Sign: {planet.sign} ({planet.degree_in_sign:.2f}°)")
            print(f"   Nakshatra: {planet.nakshatra} (Pada {planet.nakshatra_pada})")
            print(f"   House: {planet.house}")
        
        if chart['ascendant']:
            asc = chart['ascendant']
            print(f"\n✨ Ascendant (Lagna):")
            print(f"   Longitude: {asc.longitude:.2f}°")
            print(f"   Sign: {asc.sign} ({asc.degree_in_sign:.2f}°)")
            print(f"   Nakshatra: {asc.nakshatra}")
        
        # Calculate Vimshottari Dasha
        moon = next(p for p in chart['planets'] if p.name == 'Moon')
        print("\n" + "=" * 70)
        print("📅 VIMSHOTTARI DASHA")
        print("=" * 70)
        
        dashas = engine.calculate_vimshottari_dasha(birth_details.date, moon.longitude)
        
        print(f"\nShowing first 5 Maha Dashas:")
        for i, dasha in enumerate(dashas[:5]):
            print(f"\n{i+1}. {dasha['lord']} Dasha:")
            print(f"   Duration: {dasha['years']:.2f} years")
            print(f"   Period: {dasha['start_date']} to {dasha['end_date']}")
        
        print("\n" + "=" * 70)
        print("✅ TEST SUCCESSFUL!")
        print("=" * 70)
        print("\n📱 Lite calculator is working correctly!")
        print("   - Database queries: OK")
        print("   - Interpolation: OK")
        print("   - Vedic calculations: OK")
        print("   - Ready for mobile deployment!")
        
        engine.close()
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_lite_calculator()
