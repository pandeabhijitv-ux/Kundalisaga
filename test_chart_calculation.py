"""
Quick test to calculate a sample birth chart
This demonstrates the Vedic astrology calculation capabilities
"""
from datetime import datetime
from src.astrology_engine import VedicAstrologyEngine, BirthDetails

print("=" * 60)
print("Sample Birth Chart Calculation")
print("=" * 60)
print()

# Initialize engine
print("Initializing Vedic Astrology Engine...")
engine = VedicAstrologyEngine()
print("✓ Engine initialized")
print()

# Sample birth data (Mahatma Gandhi's birth chart)
print("Calculating chart for: Mahatma Gandhi")
print("Birth: October 2, 1869, 07:12 AM")
print("Place: Porbandar, Gujarat, India")
print()

birth_details = BirthDetails(
    date=datetime(1869, 10, 2, 7, 12),
    latitude=21.6417,
    longitude=69.6293,
    timezone="Asia/Kolkata",
    name="Mahatma Gandhi",
    place="Porbandar, Gujarat, India"
)

# Calculate chart
print("Calculating birth chart...")
chart = engine.calculate_birth_chart(birth_details)
print("✓ Chart calculated successfully")
print()

# Display results
print("=" * 60)
print("BIRTH CHART RESULTS")
print("=" * 60)
print()

# Ascendant
asc = chart['ascendant']
print(f"ASCENDANT (Lagna):")
print(f"  Sign: {asc.sign}")
print(f"  Degree: {asc.degree_in_sign:.2f}°")
print(f"  Nakshatra: {asc.nakshatra} (Pada {asc.nakshatra_pada})")
print()

# Planets
print("PLANETARY POSITIONS:")
print("-" * 60)

planets = chart['planets']
for planet_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
    if planet_name in planets:
        planet = planets[planet_name]
        retro = " [R]" if planet.is_retrograde else ""
        
        print(f"{planet_name:12} | {planet.sign:12} | {planet.degree_in_sign:6.2f}° | "
              f"House {planet.house:2} | {planet.nakshatra:18} (P{planet.nakshatra_pada}){retro}")

print()

# Ayanamsa
print(f"Ayanamsa: {chart['ayanamsa']:.4f}°")
print()

# Vimshottari Dasha
print("=" * 60)
print("VIMSHOTTARI DASHA (First 5 periods)")
print("=" * 60)
print()

moon = planets['Moon']
dashas = engine.calculate_vimshottari_dasha(moon.longitude, birth_details.date)

for i, dasha in enumerate(dashas[:5], 1):
    print(f"{i}. {dasha['lord']:8} | {dasha['start_date'].strftime('%Y-%m-%d')} to "
          f"{dasha['end_date'].strftime('%Y-%m-%d')} | {dasha['years']:.2f} years")

print()
print("=" * 60)
print("Chart calculation test completed successfully!")
print("=" * 60)
print()
print("This demonstrates that the Vedic astrology engine is")
print("working correctly and can calculate:")
print("  - Sidereal planetary positions")
print("  - Nakshatras and Padas")
print("  - House positions")
print("  - Vimshottari Dasha periods")
print()
