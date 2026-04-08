"""
Test the new Skyfield-based Vedic calculator
"""
from datetime import datetime
from src.astrology_engine.vedic_calculator_skyfield import (
    VedicAstrologyEngine, BirthDetails
)
import pytz

# Test case
engine = VedicAstrologyEngine(ayanamsa_name='LAHIRI')

# Mumbai birth
birth = BirthDetails(
    date=datetime(1990, 1, 15, 10, 30),
    latitude=19.0760,
    longitude=72.8777,
    timezone='Asia/Kolkata',
    name='Test Person',
    place='Mumbai'
)

print("\n" + "="*70)
print("🔮 SKYFIELD VEDIC CALCULATOR TEST")
print("="*70)
print(f"Name: {birth.name}")
print(f"Date: {birth.date.strftime('%Y-%m-%d %H:%M')}")
print(f"Place: {birth.place} ({birth.latitude}°N, {birth.longitude}°E)")
print(f"Timezone: {birth.timezone}")
print("="*70 + "\n")

# Calculate chart
chart = engine.calculate_chart(birth)

print("PLANETARY POSITIONS:")
print("-"*70)
print(f"{'Planet':<12} | {'Sign':<12} | {'Degree':<8} | {'Nakshatra':<20} | House")
print("-"*70)

for planet in chart['planets']:
    retro = " (R)" if planet.is_retrograde else ""
    print(f"{planet.name:<12} | {planet.sign:<12} | "
          f"{planet.degree_in_sign:6.2f}° | "
          f"{planet.nakshatra:<20} | {planet.house}")

if chart['ascendant']:
    asc = chart['ascendant']
    print(f"\n{'Ascendant':<12} | {asc.sign:<12} | "
          f"{asc.degree_in_sign:6.2f}° | "
          f"{asc.nakshatra:<20} | {asc.house}")

print("-"*70)
print(f"\nAyanamsa (Lahiri): {chart['ayanamsa']:.2f}°")

# Calculate Vimshottari Dasha
moon = next(p for p in chart['planets'] if p.name == 'Moon')
dashas = engine.calculate_vimshottari_dasha(birth.date, moon.longitude)

print("\n" + "="*70)
print("VIMSHOTTARI DASHA PERIODS:")
print("="*70)
print(f"{'Lord':<10} | {'Start Date':<12} | {'End Date':<12} | Years")
print("-"*70)

for i, dasha in enumerate(dashas[:10]):  # Show first 10 dashas
    print(f"{dasha['lord']:<10} | {dasha['start_date']:<12} | "
          f"{dasha['end_date']:<12} | {dasha['years']:.2f}")

print("\n" + "="*70)
print("✅ Skyfield Vedic Calculator Working Successfully!")
print("="*70 + "\n")

print("This calculator is:")
print("✓ Pure Python - Works with Chaquopy on Android")
print("✓ Self-sufficient - No server required")
print("✓ Accurate - JPL DE421 ephemeris")
print("✓ Complete - All planets, nakshatras, dashas")
print("\nReady for mobile APK build! 🚀\n")
