"""
Transit Tracker
Tracks current planetary positions and transits for market analysis
"""

try:
    import swisseph as swe
    HAS_SWE = True
except ImportError:
    HAS_SWE = False
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class TransitTracker:
    """Tracks and analyzes planetary transits for financial predictions"""
    
    PLANET_IDS = {
        'Sun': 0, 'Moon': 1, 'Mercury': 2, 'Venus': 3,
        'Mars': 4, 'Jupiter': 5, 'Saturn': 6,
        'Rahu': 10, 'Ketu': 11
    }
    
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self):
        """Initialize transit tracker"""
        if HAS_SWE:
            swe.set_ephe_path('/usr/share/ephe')
    
    def get_current_transits(self) -> Dict:
        """Get current planetary positions"""
        try:
            if not HAS_SWE:
                return {'success': False, 'error': 'Ephemeris not available on this platform', 'transits': {}}
            now = datetime.now()
            jd = self._datetime_to_jd(now)
            
            transits = {}
            for planet_name, planet_id in self.PLANET_IDS.items():
                try:
                    pos, _ = swe.calc_ut(jd, planet_id)
                    longitude = pos[0]
                    
                    transits[planet_name] = {
                        'longitude': longitude,
                        'sign': self._get_sign(longitude),
                        'degree': longitude % 30,
                        'retrograde': pos[3] < 0 if len(pos) > 3 else False
                    }
                except Exception:
                    continue
            
            # Add current Moon phase
            transits['moon_phase'] = self._get_moon_phase(transits.get('Moon', {}).get('longitude', 0),
                                                          transits.get('Sun', {}).get('longitude', 0))
            
            return {
                'success': True,
                'date': now.strftime('%Y-%m-%d %H:%M'),
                'transits': transits
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'transits': {}
            }
    
    def get_upcoming_events(self, days: int = 30) -> List[Dict]:
        """Get upcoming astrological events (retrograde, eclipses, etc.)"""
        events = []
        
        try:
            now = datetime.now()
            
            # Check for retrogrades
            for planet_name in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                retrograde_periods = self._check_retrograde(planet_name, now, days)
                events.extend(retrograde_periods)
            
            # Check for eclipses
            eclipse_dates = self._check_eclipses(now, days)
            events.extend(eclipse_dates)
            
            # Sort by date
            events.sort(key=lambda x: x['date'])
            
            return events
            
        except Exception:
            return []
    
    def _datetime_to_jd(self, dt: datetime) -> float:
        """Convert datetime to Julian Day"""
        if HAS_SWE:
            return swe.julday(dt.year, dt.month, dt.day,
                             dt.hour + dt.minute/60.0 + dt.second/3600.0)
        import calendar
        epoch = datetime(1970, 1, 1)
        delta = dt - epoch
        return 2440587.5 + delta.total_seconds() / 86400.0
    
    def _get_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude"""
        sign_num = int(longitude / 30)
        return self.SIGNS[sign_num % 12]
    
    def _get_moon_phase(self, moon_long: float, sun_long: float) -> str:
        """Calculate current Moon phase"""
        diff = (moon_long - sun_long) % 360
        
        if diff < 45:
            return "New Moon"
        elif diff < 90:
            return "Waxing Crescent"
        elif diff < 135:
            return "First Quarter"
        elif diff < 180:
            return "Waxing Gibbous"
        elif diff < 225:
            return "Full Moon"
        elif diff < 270:
            return "Waning Gibbous"
        elif diff < 315:
            return "Last Quarter"
        else:
            return "Waning Crescent"
    
    def _check_retrograde(self, planet_name: str, start_date: datetime, days: int) -> List[Dict]:
        """Check for retrograde periods"""
        events = []
        planet_id = self.PLANET_IDS.get(planet_name)
        if not planet_id:
            return events
        
        # Sample check (simplified)
        jd = self._datetime_to_jd(start_date)
        try:
            pos, _ = swe.calc_ut(jd, planet_id)
            if len(pos) > 3 and pos[3] < 0:
                events.append({
                    'type': 'retrograde',
                    'planet': planet_name,
                    'date': start_date,
                    'impact': 'high',
                    'description': f"{planet_name} is retrograde - delays and revisions likely"
                })
        except Exception:
            pass
        
        return events
    
    def _check_eclipses(self, start_date: datetime, days: int) -> List[Dict]:
        """Check for eclipse dates (simplified)"""
        # Note: Full eclipse calculation requires complex logic
        # This is a placeholder
        return []
    
    def analyze_transit_strength(self, transits: Dict, sector: str) -> Dict:
        """Analyze how current transits affect a specific sector"""
        from .sector_predictor import SectorPredictor
        
        predictor = SectorPredictor()
        return predictor.analyze_sector_transit(transits, sector)
