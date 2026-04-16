"""Numerology calculator wrapper for mobile bridge."""

import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.numerology import NumerologyEngine


def calculate_numerology(name, date_of_birth):
    """Calculate numerology profile and return bridge-friendly JSON."""
    try:
        engine = NumerologyEngine()
        birth_dt = datetime.strptime(date_of_birth, "%Y-%m-%d")
        profile = engine.calculate_profile(name, birth_dt)

        life_path_info = engine.get_life_path_interpretation(profile.life_path)
        destiny_info = engine.get_life_path_interpretation(profile.expression)

        result = {
            "name": name,
            "date_of_birth": date_of_birth,
            "life_path_number": profile.life_path,
            "destiny_number": profile.expression,
            "soul_number": profile.soul_urge,
            "personality_number": profile.personality,
            "birthday_number": profile.birthday,
            "personal_year_number": profile.personal_year,
            "maturity_number": profile.maturity,
            "karmic_debts": profile.karmic_debts,
            "master_numbers": profile.master_numbers,
            "interpretation": {
                "life_path": life_path_info.get("strengths", ""),
                "destiny": destiny_info.get("strengths", ""),
                "title": life_path_info.get("title", ""),
                "traits": life_path_info.get("traits", []),
                "challenges": life_path_info.get("challenges", ""),
            },
        }

        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == '__main__':
    print(calculate_numerology('John Doe', '1990-01-01'))
