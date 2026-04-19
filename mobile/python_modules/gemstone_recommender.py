"""Gemstone Recommendation Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.remedy_engine.gemstone_recommender import GemstoneRecommender


def get_gemstone_recommendations(chart_json: str, question: str = '') -> str:
    try:
        chart_data = json.loads(chart_json)
        recommender = GemstoneRecommender()
        result = recommender.get_recommendations(
            question=question or 'general',
            d1_chart=chart_data,
            d2_chart=None,
            d9_chart=None,
        )
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
