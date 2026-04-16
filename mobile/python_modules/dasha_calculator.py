"""Dasha calculator wrapper for mobile bridge."""

import json
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _to_date(date_text: str) -> datetime:
    return datetime.strptime(date_text, "%Y-%m-%d")


def get_current_dasha(date_of_birth):
    """Calculate current Mahadasha and Antardasha from DOB."""
    try:
        birth_dt = _to_date(date_of_birth)
        now = datetime.now()

        # Simplified Vimshottari sequence for stable mobile runtime (no native ephemeris dependency).
        sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        maha_years_lookup = {
            "Ketu": 7,
            "Venus": 20,
            "Sun": 6,
            "Moon": 10,
            "Mars": 7,
            "Rahu": 18,
            "Jupiter": 16,
            "Saturn": 19,
            "Mercury": 17,
        }

        # Use a repeatable seed from birth date so dasha is stable for each user.
        start_idx = (birth_dt.day + birth_dt.month + birth_dt.year) % len(sequence)

        dashas = []
        cursor = birth_dt
        for i in range(12):
            lord = sequence[(start_idx + i) % len(sequence)]
            years = maha_years_lookup[lord]
            end_date = cursor + timedelta(days=int(years * 365.25))
            dashas.append(
                {
                    "lord": lord,
                    "start_date": cursor.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "years": years,
                }
            )
            cursor = end_date

        current_maha = None
        for dasha in dashas:
            start = _to_date(dasha["start_date"])
            end = _to_date(dasha["end_date"])
            if start <= now <= end:
                current_maha = dasha
                break

        if current_maha is None and dashas:
            current_maha = dashas[0]

        if current_maha is None:
            return json.dumps({"error": "Unable to determine current dasha"})

        maha_lord = current_maha["lord"]
        maha_start = _to_date(current_maha["start_date"])
        maha_end = _to_date(current_maha["end_date"])
        maha_total_days = max((maha_end - maha_start).days, 1)

        start_idx = sequence.index(maha_lord) if maha_lord in sequence else 0
        antar_periods = []
        cursor = maha_start
        for i in range(9):
            antar_lord = sequence[(start_idx + i) % 9]
            antar_days = int(maha_total_days * (maha_years_lookup[antar_lord] / 120.0))
            antar_days = max(antar_days, 1)
            antar_end = min(cursor + timedelta(days=antar_days), maha_end)
            antar_periods.append(
                {
                    "planet": antar_lord,
                    "start_date": cursor.strftime("%Y-%m-%d"),
                    "end_date": antar_end.strftime("%Y-%m-%d"),
                }
            )
            cursor = antar_end
            if cursor >= maha_end:
                break

        current_antar = next(
            (
                antar
                for antar in antar_periods
                if _to_date(antar["start_date"]) <= now <= _to_date(antar["end_date"])
            ),
            antar_periods[0] if antar_periods else None,
        )

        result = {
            "mahadasha": {
                "planet": maha_lord,
                "start_date": current_maha["start_date"],
                "end_date": current_maha["end_date"],
                "duration_years": round(current_maha.get("years", 0), 2),
            },
            "antardasha": current_antar
            or {"planet": "Unknown", "start_date": "-", "end_date": "-"},
            "mahadasha_name": maha_lord,
            "antardasha_name": (current_antar or {}).get("planet", "Unknown"),
            "interpretation": (
                f"{maha_lord} Mahadasha with {(current_antar or {}).get('planet', 'Unknown')} "
                "Antardasha is currently active."
            ),
        }

        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == '__main__':
    print(get_current_dasha('1990-01-01'))
