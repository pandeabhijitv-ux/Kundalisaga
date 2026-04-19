"""Career Analysis Entry Point for Chaquopy"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.career_guidance.career_analyzer import CareerAnalyzer


def analyze_career(chart_json: str) -> str:
    try:
        chart_data = json.loads(chart_json)
        analyzer = CareerAnalyzer()
        result = analyzer.analyze_career_sectors(chart_data)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e), 'recommendations': []})
