"""Remedy calculator wrapper for mobile bridge."""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.remedy_engine import RemedyEngine


def _collect_by_type(planet_remedies):
    gemstones = []
    mantras = []
    fasting = []
    charity = []
    daily_practices = []

    for planet_name, payload in planet_remedies.items():
        for remedy in payload.get("remedies", []):
            remedy_type = remedy.get("type", "")
            normalized = {"planet": planet_name, **remedy}

            if "Gemstone" in remedy_type:
                gemstones.append(normalized)
            elif "Mantra" in remedy_type:
                mantras.append(normalized)
            elif remedy_type == "Fasting":
                fasting.append(normalized)
            elif remedy_type == "Charity":
                charity.append(normalized)
            elif remedy_type == "Practice":
                daily_practices.append(remedy.get("description", ""))

    return gemstones, mantras, fasting, charity, daily_practices


def get_remedies(chart_json):
    """Generate remedies based on chart context and return bridge-friendly JSON."""
    try:
        chart_data = json.loads(chart_json) if chart_json else {}
        engine = RemedyEngine()

        suggestions = engine.suggest_remedies(chart_data, specific_concern="general well-being")
        planet_remedies = suggestions.get("planet_remedies", {})

        gemstones, mantras, fasting, charity, daily_practices = _collect_by_type(planet_remedies)

        # Backfill from universal remedies when chart issues are sparse.
        for universal in suggestions.get("universal_remedies", []):
            if "Mantra" in universal.get("type", ""):
                mantras.append(
                    {
                        "planet": "Universal",
                        "type": universal.get("type"),
                        "mantra": universal.get("mantra") or universal.get("description", ""),
                        "benefits": universal.get("benefits", ""),
                        "frequency": universal.get("frequency", ""),
                    }
                )

        daily_practices.extend(suggestions.get("general_advice", []))

        result = {
            "identified_issues": suggestions.get("identified_issues", []),
            "gemstones": gemstones,
            "mantras": mantras,
            "fasting": fasting,
            "charity": charity,
            "daily_practices": [item for item in daily_practices if item],
        }

        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == '__main__':
    # Test
    sample_chart = json.dumps({'name': 'Test', 'planets': []})
    print(get_remedies(sample_chart))
