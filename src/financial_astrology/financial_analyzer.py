"""
Financial Analyzer - Main Interface
Combines transit tracking and sector predictions for comprehensive analysis
"""

from typing import Dict
from .transit_tracker import TransitTracker
from .sector_predictor import SectorPredictor


class FinancialAnalyzer:
    """Main interface for financial astrology analysis"""
    
    def __init__(self):
        """Initialize financial analyzer"""
        self.transit_tracker = TransitTracker()
        self.sector_predictor = SectorPredictor()
    
    def get_market_outlook(self) -> Dict:
        """Get overall market outlook based on current transits"""
        try:
            # Get current transits
            transits = self.transit_tracker.get_current_transits()
            
            if not transits['success']:
                return transits
            
            # Get sector predictions
            sector_predictions = self.sector_predictor.get_all_sector_predictions(transits)
            
            # Get upcoming events
            upcoming_events = self.transit_tracker.get_upcoming_events(days=30)
            
            # Calculate overall market sentiment
            avg_strength = sum(p['strength'] for p in sector_predictions) / len(sector_predictions)
            market_sentiment = self._get_market_sentiment(avg_strength)
            
            return {
                'success': True,
                'date': transits['date'],
                'market_sentiment': market_sentiment,
                'overall_strength': round(avg_strength, 1),
                'top_sectors': sector_predictions[:3],
                'weak_sectors': sector_predictions[-3:],
                'upcoming_events': upcoming_events[:5],
                'current_transits': transits['transits']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_sector(self, sector: str) -> Dict:
        """Analyze a specific sector in detail"""
        try:
            transits = self.transit_tracker.get_current_transits()
            
            if not transits['success']:
                return transits
            
            analysis = self.sector_predictor.analyze_sector_transit(transits, sector)
            
            if analysis['success']:
                # Add timing recommendation
                analysis['timing'] = self._get_timing_recommendation(analysis['strength'])
            
            return analysis
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_personalized_analysis(self, birth_chart: Dict) -> Dict:
        """Get personalized investment recommendations"""
        try:
            transits = self.transit_tracker.get_current_transits()
            
            if not transits['success']:
                return transits
            
            recommendations = self.sector_predictor.get_personalized_recommendations(
                transits, birth_chart
            )
            
            return recommendations
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_market_sentiment(self, avg_strength: float) -> str:
        """Determine overall market sentiment"""
        if avg_strength >= 60:
            return "🟢 Bullish - Favorable for growth"
        elif avg_strength >= 30:
            return "🟡 Neutral - Selective opportunities"
        else:
            return "🔴 Bearish - Exercise caution"
    
    def _get_timing_recommendation(self, strength: int) -> str:
        """Get timing recommendation for investment"""
        if strength >= 60:
            return "Now is a good time to invest"
        elif strength >= 30:
            return "Wait for stronger alignment or invest conservatively"
        else:
            return "Avoid new positions, consider booking profits"
