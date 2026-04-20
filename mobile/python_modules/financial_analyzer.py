"""Financial Analysis Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.financial_astrology.financial_analyzer import FinancialAnalyzer


def _normalize_chart(chart_data: dict) -> dict:
    if not isinstance(chart_data, dict):
        return {}

    normalized = dict(chart_data)
    planets = normalized.get('planets', {})
    if isinstance(planets, list):
        mapped = {}
        for item in planets:
            if isinstance(item, dict) and item.get('name'):
                mapped[item['name']] = item
        normalized['planets'] = mapped
    return normalized


def analyze_financial(chart_json: str) -> str:
    """Personalized financial analysis based on natal chart."""
    try:
        chart_data = _normalize_chart(json.loads(chart_json))
        analyzer = FinancialAnalyzer()

        # Personalized natal analysis using chart
        personalized = analyzer.get_personalized_analysis(chart_data)

        # Attempt general market outlook (may fail on Android without swisseph)
        market = analyzer.get_market_outlook()
        recs = (personalized or {}).get('recommendations', []) if isinstance(personalized, dict) else []

        if isinstance(personalized, dict) and not personalized.get('success', True):
            personalized = {
                'success': True,
                'recommendations': [],
                'analysis_date': None,
            }

        if not recs:
            recs = []

        if not market.get('success'):
            ranked = sorted(recs, key=lambda x: x.get('total_strength', 0), reverse=True)
            top_sectors = [
                {
                    'sector': item.get('sector', 'Sector'),
                    'rating': item.get('rating', 'Moderate'),
                    'prediction': item.get('advice', ''),
                }
                for item in ranked[:3]
            ]
            weak_sectors = [
                {
                    'sector': item.get('sector', 'Sector'),
                    'rating': item.get('rating', 'Moderate'),
                }
                for item in ranked[-2:]
            ]
            market = {
                'success': True,
                'market_sentiment': 'Live transit unavailable - using local chart-based guidance',
                'overall_strength': 50,
                'top_sectors': top_sectors,
                'weak_sectors': weak_sectors,
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
