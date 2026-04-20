"""Remedy calculator wrapper for mobile bridge."""

import json
import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from src.remedy_engine import RemedyEngine


def _safe_engine_lookup(engine, method_name, planet):
    method = getattr(engine, method_name, None)
    if callable(method):
        try:
            return method(planet)
        except Exception:
            return []
    return []


def _collect_by_type(planet_remedies):
    gemstones = []
    mantras = []
    fasting = []
    charity = []
    daily_practices = []

    if not isinstance(planet_remedies, dict):
        return gemstones, mantras, fasting, charity, daily_practices

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


def _build_from_general(engine, focus_planets):
    """Build remedy buckets from general planet remedies when issue-based data is sparse."""
    planet_remedies = {}
    for planet in focus_planets:
        remedies = engine.get_general_remedies(planet)
        if remedies:
            planet_remedies[planet] = {"remedies": remedies}
    return _collect_by_type(planet_remedies)


def _extract_focus_planets(chart_data, suggestions):
    ordered = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    from_suggestions = []
    if isinstance(suggestions, dict):
        planet_remedies = suggestions.get("planet_remedies", {})
        if isinstance(planet_remedies, dict):
            from_suggestions = list(planet_remedies.keys())

    if from_suggestions:
        return [p for p in ordered if p in from_suggestions]

    planets = chart_data.get("planets", {})
    if isinstance(planets, dict):
        from_chart = [p for p in ordered if p in planets]
        if from_chart:
            return from_chart

    return ["Sun", "Moon", "Jupiter", "Venus", "Saturn"]


def _group_by_planet(items):
    grouped = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        planet = item.get("planet") or "General"
        grouped.setdefault(planet, []).append(item)
    return grouped


def _normalize_chart(chart_data):
    """Normalize chart payload from mobile format into remedy-engine format."""
    if not isinstance(chart_data, dict):
        return {}

    normalized = dict(chart_data)
    planets = normalized.get("planets", {})

    if isinstance(planets, list):
        planets_map = {}
        for item in planets:
            if isinstance(item, dict) and item.get("name"):
                planets_map[item["name"]] = item
        normalized["planets"] = planets_map

    return normalized


def get_remedies(chart_json):
    """Generate remedies based on chart context and return bridge-friendly JSON."""
    try:
        chart_data = json.loads(chart_json) if chart_json else {}
        chart_data = _normalize_chart(chart_data)
        engine = RemedyEngine()

        suggestions = engine.suggest_remedies(chart_data, specific_concern="general well-being")
        planet_remedies = suggestions.get("planet_remedies", {})
        focus_planets = _extract_focus_planets(chart_data, suggestions)

        gemstones, mantras, fasting, charity, daily_practices = _collect_by_type(planet_remedies)

        if not gemstones and not mantras:
            (gemstones, mantras, fasting, charity, daily_practices) = _build_from_general(engine, focus_planets)

        ayurvedic = {}
        yoga = {}
        color = {}
        muhurat = {}
        for planet in focus_planets:
            # Some mobile remedy-engine builds expose only core methods.
            ayurvedic[planet] = _safe_engine_lookup(engine, "get_ayurvedic_remedies", planet)
            yoga[planet] = _safe_engine_lookup(engine, "get_yoga_remedies", planet)
            color[planet] = _safe_engine_lookup(engine, "get_color_therapy_remedies", planet)
            muhurat[planet] = _safe_engine_lookup(engine, "get_muhurat_recommendations", planet)

        dasha = chart_data.get("dasha") if isinstance(chart_data, dict) else None
        lal_kitab_list = engine.get_lal_kitab_remedies(
            chart_data,
            current_dasha=dasha if isinstance(dasha, dict) else None,
            goal="general",
        )
        lal_kitab = _group_by_planet(lal_kitab_list)

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
            "ayurvedic": ayurvedic,
            "yoga": yoga,
            "muhurat": muhurat,
            "color": color,
            "lal_kitab": lal_kitab,
        }

        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == '__main__':
    # Test
    sample_chart = json.dumps({'name': 'Test', 'planets': []})
    print(get_remedies(sample_chart))
