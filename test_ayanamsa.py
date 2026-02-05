import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

print("Finding year with ayanamsa 24.4427:")
for year in range(2020, 2035):
    jd = swe.julday(year, 9, 10, 14.9)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    print(f"{year}: {ayanamsa:.4f}")
    if abs(ayanamsa - 24.4427) < 0.01:
        print(f"  ^^^ MATCH!")
