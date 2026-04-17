"""Vedic astrology engine package with mobile-safe fallbacks."""

# Prefer lite DB engine on mobile, then skyfield, then Swiss Ephemeris.
try:
    from .vedic_calculator_lite import VedicAstrologyEngine, BirthDetails, PlanetPosition, SIGNS, NAKSHATRAS
    PLANETS = {}
except Exception:
    try:
        from .vedic_calculator_skyfield import VedicAstrologyEngine, BirthDetails, PlanetPosition, SIGNS, NAKSHATRAS
        PLANETS = {}
    except Exception:
        from .vedic_calculator import VedicAstrologyEngine, BirthDetails, PlanetPosition, PLANETS, SIGNS, NAKSHATRAS

__all__ = [
    "VedicAstrologyEngine",
    "BirthDetails",
    "PlanetPosition",
    "PLANETS",
    "SIGNS",
    "NAKSHATRAS",
]
