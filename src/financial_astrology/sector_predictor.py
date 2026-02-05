"""
Sector Predictor
Maps planetary influences to stock market sectors
"""

from typing import Dict, List
from datetime import datetime


class SectorPredictor:
    """Predicts favorable/unfavorable periods for stock market sectors"""
    
    # Sector to Planet correlations
    SECTOR_PLANETS = {
        'Technology & IT': {
            'primary': ['Mercury', 'Rahu'],
            'secondary': ['Uranus'],
            'favorable_signs': ['Gemini', 'Virgo', 'Aquarius'],
            'companies': 'TCS, Infosys, Wipro, Tech Mahindra'
        },
        'Banking & Finance': {
            'primary': ['Jupiter', 'Venus'],
            'secondary': ['Mercury'],
            'favorable_signs': ['Taurus', 'Libra', 'Sagittarius', 'Pisces'],
            'companies': 'HDFC Bank, ICICI Bank, SBI, Kotak'
        },
        'Pharmaceuticals': {
            'primary': ['Moon', 'Jupiter'],
            'secondary': ['Neptune'],
            'favorable_signs': ['Cancer', 'Pisces', 'Sagittarius'],
            'companies': 'Sun Pharma, Dr Reddy, Cipla, Lupin'
        },
        'Real Estate': {
            'primary': ['Mars', 'Saturn'],
            'secondary': [],
            'favorable_signs': ['Aries', 'Taurus', 'Capricorn'],
            'companies': 'DLF, Godrej Properties, Prestige, Oberoi'
        },
        'Oil & Energy': {
            'primary': ['Sun', 'Mars'],
            'secondary': ['Pluto'],
            'favorable_signs': ['Leo', 'Aries', 'Scorpio'],
            'companies': 'Reliance, ONGC, BPCL, IOC'
        },
        'FMCG & Consumer': {
            'primary': ['Venus', 'Moon'],
            'secondary': [],
            'favorable_signs': ['Taurus', 'Cancer', 'Libra'],
            'companies': 'HUL, ITC, Nestle, Britannia'
        },
        'Automobiles': {
            'primary': ['Mars', 'Mercury'],
            'secondary': [],
            'favorable_signs': ['Aries', 'Gemini', 'Scorpio'],
            'companies': 'Maruti, Tata Motors, M&M, Bajaj Auto'
        },
        'Metals & Mining': {
            'primary': ['Saturn', 'Mars'],
            'secondary': [],
            'favorable_signs': ['Capricorn', 'Aquarius', 'Scorpio'],
            'companies': 'Tata Steel, JSW Steel, Hindalco, Vedanta'
        },
        'Infrastructure': {
            'primary': ['Saturn', 'Mars'],
            'secondary': [],
            'favorable_signs': ['Capricorn', 'Aries'],
            'companies': 'L&T, Adani Ports, GMR, IRB Infra'
        },
        'Media & Entertainment': {
            'primary': ['Venus', 'Mercury'],
            'secondary': [],
            'favorable_signs': ['Taurus', 'Libra', 'Gemini'],
            'companies': 'Zee, PVR, Sun TV, Dish TV'
        }
    }
    
    def analyze_sector_transit(self, transits: Dict, sector: str) -> Dict:
        """Analyze how current transits affect a specific sector"""
        if sector not in self.SECTOR_PLANETS:
            return {'success': False, 'error': 'Unknown sector'}
        
        sector_info = self.SECTOR_PLANETS[sector]
        transit_data = transits.get('transits', {})
        
        strength = 0
        favorable_factors = []
        unfavorable_factors = []
        
        # Check primary planets
        for planet in sector_info['primary']:
            if planet in transit_data:
                planet_data = transit_data[planet]
                sign = planet_data.get('sign', '')
                
                # Favorable sign
                if sign in sector_info['favorable_signs']:
                    strength += 30
                    favorable_factors.append(f"{planet} in {sign} (favorable)")
                
                # Retrograde
                if planet_data.get('retrograde', False):
                    strength -= 20
                    unfavorable_factors.append(f"{planet} retrograde (delays)")
        
        # Moon phase impact
        moon_phase = transit_data.get('moon_phase', '')
        if 'Full Moon' in moon_phase or 'New Moon' in moon_phase:
            favorable_factors.append(f"{moon_phase} (turning point)")
        
        # Generate prediction
        prediction = self._generate_prediction(strength, favorable_factors, unfavorable_factors)
        
        return {
            'success': True,
            'sector': sector,
            'strength': strength,
            'rating': self._get_rating(strength),
            'prediction': prediction,
            'favorable_factors': favorable_factors,
            'unfavorable_factors': unfavorable_factors,
            'major_companies': sector_info['companies']
        }
    
    def get_all_sector_predictions(self, transits: Dict) -> List[Dict]:
        """Get predictions for all sectors"""
        predictions = []
        
        for sector in self.SECTOR_PLANETS.keys():
            result = self.analyze_sector_transit(transits, sector)
            if result['success']:
                predictions.append(result)
        
        # Sort by strength
        predictions.sort(key=lambda x: x['strength'], reverse=True)
        return predictions
    
    def get_personalized_recommendations(self, transits: Dict, birth_chart: Dict) -> Dict:
        """Get personalized investment recommendations based on birth chart and transits"""
        try:
            # Analyze natal chart
            natal_planets = birth_chart.get('planets', {})
            
            # Find strong planets in natal chart
            strong_sectors = []
            
            for sector, info in self.SECTOR_PLANETS.items():
                sector_strength = 0
                
                for planet in info['primary']:
                    if planet in natal_planets and planet != 'Ascendant':
                        # Check if planet is strong in natal chart
                        planet_data = natal_planets[planet]
                        
                        # Handle both object and dict formats
                        if hasattr(planet_data, 'sign'):
                            # Planet object - check strength
                            sector_strength += 30
                            # Bonus for exaltation/own sign
                            if self._is_planet_strong(planet, planet_data.sign):
                                sector_strength += 20
                        elif isinstance(planet_data, dict):
                            # Dict format
                            sector_strength += 30
                            if 'sign' in planet_data and self._is_planet_strong(planet, planet_data['sign']):
                                sector_strength += 20
                
                if sector_strength > 0:
                    strong_sectors.append({
                        'sector': sector,
                        'natal_strength': sector_strength
                    })
            
            # Combine with current transits
            transit_predictions = self.get_all_sector_predictions(transits)
            
            # Merge recommendations
            recommendations = []
            for sector in strong_sectors:
                # Find transit prediction for this sector
                transit_pred = next(
                    (p for p in transit_predictions if p['sector'] == sector['sector']),
                    None
                )
                
                if transit_pred:
                    combined_strength = sector['natal_strength'] + transit_pred['strength']
                    recommendations.append({
                        'sector': sector['sector'],
                        'natal_strength': sector['natal_strength'],
                        'transit_strength': transit_pred['strength'],
                        'total_strength': combined_strength,
                        'rating': self._get_rating(combined_strength),
                        'advice': self._get_investment_advice(combined_strength),
                        'stocks': self._get_stock_recommendations(sector['sector'])
                    })
            
            recommendations.sort(key=lambda x: x['total_strength'], reverse=True)
            
            return {
                'success': True,
                'recommendations': recommendations[:5],  # Top 5
                'analysis_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_rating(self, strength: int) -> str:
        """Get rating based on strength"""
        if strength >= 80:
            return "⭐⭐⭐⭐⭐ Excellent"
        elif strength >= 60:
            return "⭐⭐⭐⭐ Very Good"
        elif strength >= 40:
            return "⭐⭐⭐ Good"
        elif strength >= 20:
            return "⭐⭐ Fair"
        else:
            return "⭐ Caution"
    
    def _generate_prediction(self, strength: int, favorable: List, unfavorable: List) -> str:
        """Generate prediction text"""
        if strength >= 60:
            return "Strong positive alignment. Favorable period for investment and growth."
        elif strength >= 30:
            return "Moderately favorable. Good for selective investments with research."
        elif strength >= 0:
            return "Neutral period. Focus on stable, blue-chip stocks."
        else:
            return "Challenging period. Exercise caution and wait for better alignment."
    
    def _is_planet_strong(self, planet: str, sign: str) -> bool:
        """Check if planet is strong in given sign"""
        # Exaltation signs
        exaltation = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mercury': 'Virgo',
            'Venus': 'Pisces', 'Mars': 'Capricorn', 'Jupiter': 'Cancer',
            'Saturn': 'Libra'
        }
        
        # Own signs
        own_signs = {
            'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
            'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
            'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius']
        }
        
        return sign == exaltation.get(planet) or sign in own_signs.get(planet, [])
    
    def _get_investment_advice(self, strength: int) -> str:
        """Get investment advice based on combined strength"""
        if strength >= 100:
            return "Excellent time for investment. Your chart strongly supports this sector."
        elif strength >= 60:
            return "Good investment opportunity. Consider accumulating positions."
        elif strength >= 30:
            return "Moderate potential. Invest only in fundamentally strong companies."
        else:
            return "Wait for better alignment. Focus on other sectors currently."
    
    def _get_stock_recommendations(self, sector: str) -> List[str]:
        """Get stock recommendations for each sector"""
        stock_recommendations = {
            'Technology': [
                'TCS (Tata Consultancy Services)',
                'Infosys',
                'Wipro',
                'HCL Technologies',
                'Tech Mahindra'
            ],
            'Banking': [
                'HDFC Bank',
                'ICICI Bank',
                'State Bank of India (SBI)',
                'Kotak Mahindra Bank',
                'Axis Bank'
            ],
            'Pharmaceuticals': [
                'Sun Pharmaceutical',
                'Dr. Reddy\'s Laboratories',
                'Cipla',
                'Divi\'s Laboratories',
                'Lupin'
            ],
            'Real Estate': [
                'DLF Limited',
                'Godrej Properties',
                'Oberoi Realty',
                'Prestige Estates',
                'Brigade Enterprises'
            ],
            'Metals & Mining': [
                'Tata Steel',
                'Hindalco',
                'JSW Steel',
                'Coal India',
                'NMDC'
            ],
            'Infrastructure': [
                'Larsen & Toubro (L&T)',
                'IRB Infrastructure',
                'GMR Infrastructure',
                'Adani Ports',
                'Power Grid'
            ],
            'FMCG': [
                'Hindustan Unilever',
                'ITC',
                'Nestle India',
                'Britannia',
                'Dabur'
            ],
            'Automobile': [
                'Maruti Suzuki',
                'Tata Motors',
                'Mahindra & Mahindra',
                'Bajaj Auto',
                'Hero MotoCorp'
            ],
            'Energy': [
                'Reliance Industries',
                'ONGC',
                'Indian Oil',
                'NTPC',
                'Power Grid'
            ]
        }
        
        return stock_recommendations.get(sector, [])
