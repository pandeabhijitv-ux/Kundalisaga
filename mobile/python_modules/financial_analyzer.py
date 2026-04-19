"""Financial Analysis Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.financial_astrology.financial_analyzer import FinancialAnalyzer


def analyze_financial(chart_json: str) -> str:
    """Personalized financial analysis based on natal chart."""
    try:
        chart_data = json.loads(chart_json)
        analyzer = FinancialAnalyzer()

        # Personalized natal analysis using chart
        personalized = analyzer.get_personalized_analysis(chart_data)

        # Attempt general market outlook (may fail on Android without swisseph)
        market = analyzer.get_market_outlook()
        if not market.get('success'):
            market = {
                'success': True,
                'market_sentiment': '🌐 Connect to internet for live analysis',
                'overall_strength': 50,
                'top_sectors': [],
                'weak_sectors': [],
                'upcoming_events': [],
            }

        result = {
            'success': True,
            'personalized': personalized,
            'market': market,
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
