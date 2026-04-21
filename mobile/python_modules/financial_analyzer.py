"""Financial Analysis Entry Point for Chaquopy - Dasha + Sector based"""
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ── Planet → Sector mappings ──────────────────────────────────────────────────
PLANET_SECTORS = {
    'Sun': {
        'sectors': ['Government & PSU', 'Energy & Power', 'Gold & Precious Metals', 'Healthcare & Pharma'],
        'stocks': 'ONGC, NTPC, Coal India, BHEL, GAIL',
        'character': 'authority, government, leadership, stability',
    },
    'Moon': {
        'sectors': ['FMCG & Consumer Goods', 'Agriculture & Food', 'Real Estate', 'Water & Beverages'],
        'stocks': 'HUL, ITC, Britannia, Nestle, Dabur',
        'character': 'mass market, public sentiment, liquidity',
    },
    'Mars': {
        'sectors': ['Real Estate & Construction', 'Defense & Arms', 'Steel & Metals', 'Automobiles'],
        'stocks': 'DLF, L&T, Tata Steel, JSW Steel, M&M',
        'character': 'aggression, speed, short-term gains, action',
    },
    'Mercury': {
        'sectors': ['Technology & IT', 'Banking & Finance', 'Media & Publishing', 'Telecom'],
        'stocks': 'TCS, Infosys, HDFC Bank, Bharti Airtel, HCL Tech',
        'character': 'intelligence, communication, trade, quick returns',
    },
    'Jupiter': {
        'sectors': ['Banking & Finance', 'Education & Research', 'Insurance', 'Pharmaceuticals'],
        'stocks': 'Kotak Bank, SBI, Bajaj Finance, LIC, Dr Reddys',
        'character': 'expansion, wealth creation, long-term growth, wisdom',
    },
    'Venus': {
        'sectors': ['Luxury & Lifestyle', 'FMCG & Cosmetics', 'Hospitality & Tourism', 'Entertainment & Media'],
        'stocks': 'Titan, Tata Consumer, Indian Hotels, Zomato, PVR Inox',
        'character': 'comfort, beauty, accumulation, enjoyment, creative industries',
    },
    'Saturn': {
        'sectors': ['Oil & Gas', 'Mining & Metals', 'Infrastructure & Utilities', 'Cement & Construction'],
        'stocks': 'Reliance, BPCL, Vedanta, Ultratech Cement, Adani Ports',
        'character': 'discipline, long-term, hard work, slow but steady gains',
    },
    'Rahu': {
        'sectors': ['Technology & Innovation', 'Chemicals & Plastics', 'Aviation & Aerospace', 'Foreign Stocks'],
        'stocks': 'Adani Enterprises, PI Industries, IndiGo, Naukri, Zomato',
        'character': 'disruption, speculation, foreign exposure, high risk/reward',
    },
    'Ketu': {
        'sectors': ['Gold & Precious Metals', 'Ayurveda & Spirituality', 'Research & Niche', 'Alternative Investments'],
        'stocks': 'Patanjali, Gold ETFs, Emami, Bajaj Consumer',
        'character': 'detachment, unconventional, spiritual earnings, gold as hedge',
    },
}

# Dasha financial profile
DASHA_FINANCIAL_PROFILE = {
    'Sun': {
        'sentiment': 'Stable & Government-Favored',
        'outlook': 'Positive for PSU stocks, gold, and energy sector. Suitable for long-term, stable holdings. Avoid speculation.',
        'strength': 65,
        'favorable': ['Government & PSU', 'Energy & Power', 'Gold & Precious Metals'],
        'caution': 'Avoid highly speculative or volatile plays. Authority and stability are themes.',
        'tip': 'This is a period of authority and visibility. Invest in stable, blue-chip government-linked companies.',
    },
    'Moon': {
        'sentiment': 'Consumer & Market-Driven',
        'outlook': 'FMCG, food, real estate, and mass-consumption stocks do well. Markets reflect public mood — emotional swings possible.',
        'strength': 60,
        'favorable': ['FMCG & Consumer Goods', 'Agriculture & Food', 'Real Estate'],
        'caution': 'Emotional volatility — do not trade impulsively. Liquidity fluctuates.',
        'tip': 'Invest in everyday consumer needs and real estate. Avoid leverage during full/new moon periods.',
    },
    'Mars': {
        'sentiment': 'Aggressive & Action-Oriented',
        'outlook': 'Real estate, defense, steel, and construction sectors are active. Short-term trading opportunities abound. Energy is high.',
        'strength': 70,
        'favorable': ['Real Estate & Construction', 'Defense & Arms', 'Steel & Metals'],
        'caution': 'Impulsive decisions can lead to losses. Control aggression in trading.',
        'tip': 'Short-term trading and decisive action pay off. Real estate and metals are strong choices.',
    },
    'Mercury': {
        'sentiment': 'Tech & Trade Favorable',
        'outlook': 'IT, banking, media, and telecom sectors are highlighted. Quick trading cycles. Intelligence and analysis pay off.',
        'strength': 75,
        'favorable': ['Technology & IT', 'Banking & Finance', 'Telecom'],
        'caution': 'Mercury retrograde periods can disrupt trades. Double-check all financial decisions.',
        'tip': 'Invest in technology and banking. Day trading and short-term positions suit this period.',
    },
    'Jupiter': {
        'sentiment': 'Expansion & Wealth Growth',
        'outlook': 'BEST dasha for wealth creation. Banking, finance, gold, and education thrive. Long-term investments compound beautifully.',
        'strength': 90,
        'favorable': ['Banking & Finance', 'Insurance', 'Pharmaceuticals', 'Gold & Precious Metals'],
        'caution': 'Overconfidence and over-expansion can occur. Stay grounded.',
        'tip': 'Jupiter Mahadasha is considered the most auspicious for financial growth. Invest broadly in quality stocks and gold.',
    },
    'Venus': {
        'sentiment': 'Luxury & Accumulation Phase',
        'outlook': 'Luxury goods, FMCG, entertainment, hospitality, and cosmetics sectors thrive. Wealth accumulation is strong and steady.',
        'strength': 85,
        'favorable': ['Luxury & Lifestyle', 'FMCG & Cosmetics', 'Hospitality & Tourism', 'Entertainment & Media'],
        'caution': 'Overspending tendency — manage expenses as well as investments.',
        'tip': 'This is an excellent dasha for accumulating wealth. Consumer discretionary and luxury sectors outperform.',
    },
    'Saturn': {
        'sentiment': 'Disciplined & Long-Term',
        'outlook': 'Oil & gas, mining, infrastructure, and cement sectors are highlighted. Slow but steady returns. Discipline is rewarded.',
        'strength': 65,
        'favorable': ['Oil & Gas', 'Mining & Metals', 'Infrastructure & Utilities', 'Cement & Construction'],
        'caution': 'Saturn periods can bring delays and setbacks. Avoid get-rich-quick schemes.',
        'tip': 'SIP investments and infrastructure stocks suit this period. Patience is key — compounding works in your favor.',
    },
    'Rahu': {
        'sentiment': 'Speculative & High Risk/Reward',
        'outlook': 'New-age tech, chemicals, aviation, and foreign stocks can give extraordinary gains but with high risk. Unconventional opportunities.',
        'strength': 55,
        'favorable': ['Technology & Innovation', 'Chemicals & Plastics', 'Aviation & Aerospace'],
        'caution': 'Rahu brings illusion and sudden reversals. Speculative positions can collapse. Diversify.',
        'tip': 'Innovative sectors can boom, but have strict stop-losses. Diversify into multiple assets.',
    },
    'Ketu': {
        'sentiment': 'Detachment — Gold & Alternatives',
        'outlook': 'Worldly financial gains are muted. Gold, alternative investments, and spiritual/herbal sectors are safe. Consider gold ETFs.',
        'strength': 40,
        'favorable': ['Gold & Precious Metals', 'Ayurveda & Spirituality', 'Alternative Investments'],
        'caution': 'Ketu dasha is not recommended for aggressive equity investments. Focus on preservation.',
        'tip': 'Increase gold allocation. Preserve capital. Use this period to study markets and plan for next dasha.',
    },
}


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


def _get_planet_sign(planets: dict, planet_name: str) -> str:
    p = planets.get(planet_name, {})
    if isinstance(p, dict):
        return p.get('sign', '')
    return getattr(p, 'sign', '')


def _get_planet_house(planets: dict, planet_name: str) -> int:
    p = planets.get(planet_name, {})
    if isinstance(p, dict):
        return int(p.get('house', 0))
    return int(getattr(p, 'house', 0))


def _get_planet_retrograde(planets: dict, planet_name: str) -> bool:
    p = planets.get(planet_name, {})
    if isinstance(p, dict):
        return bool(p.get('is_retrograde', False))
    return bool(getattr(p, 'is_retrograde', False))


# Exaltation / own sign strength
EXALTATION = {'Sun': 'Aries', 'Moon': 'Taurus', 'Mercury': 'Virgo',
               'Venus': 'Pisces', 'Mars': 'Capricorn', 'Jupiter': 'Cancer', 'Saturn': 'Libra'}
OWN_SIGNS = {
    'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mercury': ['Gemini', 'Virgo'],
    'Venus': ['Taurus', 'Libra'], 'Mars': ['Aries', 'Scorpio'],
    'Jupiter': ['Sagittarius', 'Pisces'], 'Saturn': ['Capricorn', 'Aquarius'],
    'Rahu': ['Gemini', 'Virgo'], 'Ketu': ['Sagittarius', 'Pisces'],
}
DEBILITATION = {'Sun': 'Libra', 'Moon': 'Scorpio', 'Mercury': 'Pisces',
                'Venus': 'Virgo', 'Mars': 'Cancer', 'Jupiter': 'Capricorn', 'Saturn': 'Aries'}


def _planet_strength_score(planet_name: str, sign: str, house: int, is_retro: bool) -> int:
    """Return 0-100 strength score for a planet in a natal chart."""
    score = 50
    if sign == EXALTATION.get(planet_name):
        score += 30
    elif sign in OWN_SIGNS.get(planet_name, []):
        score += 20
    elif sign == DEBILITATION.get(planet_name):
        score -= 25
    if house in [1, 4, 7, 10]:  # Kendra houses — strong
        score += 15
    elif house in [5, 9]:  # Trikona — very auspicious
        score += 20
    elif house in [6, 8, 12]:  # Dusthana — weak
        score -= 20
    if is_retro:
        score -= 10
    return max(10, min(100, score))


def _build_market_overview(chart: dict) -> dict:
    """Dasha-based market overview."""
    dasha_info = chart.get('dasha', {})
    mahadasha = dasha_info.get('mahadasha', '')
    end_date = dasha_info.get('end_date', '')

    profile = DASHA_FINANCIAL_PROFILE.get(mahadasha, {
        'sentiment': 'Neutral',
        'outlook': 'Analyze your current Mahadasha lord for deeper insight.',
        'strength': 50,
        'favorable': [],
        'caution': 'Keep a balanced portfolio.',
        'tip': 'Consult your chart for current dasha details.',
    })

    # Compute years remaining in dasha
    years_remaining = ''
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            remaining_days = (end_dt - datetime.now()).days
            if remaining_days > 0:
                yrs = remaining_days / 365.25
                if yrs >= 1:
                    years_remaining = f'{yrs:.1f} years'
                else:
                    years_remaining = f'{int(remaining_days)} days'
        except Exception:
            pass

    return {
        'success': True,
        'mahadasha': mahadasha or 'Unknown',
        'dasha_end': end_date,
        'years_remaining': years_remaining,
        'sentiment': profile['sentiment'],
        'outlook': profile['outlook'],
        'strength': profile['strength'],
        'favorable_sectors': profile['favorable'],
        'caution': profile['caution'],
        'investment_tip': profile['tip'],
        'dasha_sectors': [
            PLANET_SECTORS.get(mahadasha, {}).get('sectors', []),
        ],
    }


def _build_sector_analysis(chart: dict) -> list:
    """Sector rankings based on natal planet strengths."""
    planets = chart.get('planets', {})
    sectors_scored = {}

    for planet_name, sector_info in PLANET_SECTORS.items():
        sign = _get_planet_sign(planets, planet_name)
        house = _get_planet_house(planets, planet_name)
        is_retro = _get_planet_retrograde(planets, planet_name)

        if not sign:
            continue

        strength = _planet_strength_score(planet_name, sign, house, is_retro)

        for sector in sector_info['sectors']:
            if sector not in sectors_scored or sectors_scored[sector]['strength'] < strength:
                sectors_scored[sector] = {
                    'sector': sector,
                    'ruling_planet': planet_name,
                    'planet_sign': sign,
                    'planet_house': house,
                    'strength': strength,
                    'stocks': sector_info['stocks'],
                    'planet_character': sector_info['character'],
                    'is_retro': is_retro,
                }

    # Sort by strength
    ranked = sorted(sectors_scored.values(), key=lambda x: x['strength'], reverse=True)

    def _rating(s):
        if s >= 80:
            return 'Excellent'
        elif s >= 65:
            return 'Very Good'
        elif s >= 50:
            return 'Good'
        elif s >= 35:
            return 'Moderate'
        else:
            return 'Caution'

    result = []
    for item in ranked:
        result.append({
            'sector': item['sector'],
            'ruling_planet': item['ruling_planet'],
            'planet_sign': item['planet_sign'],
            'planet_house': item['planet_house'],
            'strength': item['strength'],
            'rating': _rating(item['strength']),
            'stocks': item['stocks'],
            'reason': (
                f"{item['ruling_planet']} in {item['planet_sign']} "
                f"(House {item['planet_house']}) — "
                f"{'retrograde, use caution / ' if item['is_retro'] else ''}"
                f"{item['planet_character']}"
            ),
        })
    return result


def _build_personalized(chart: dict) -> dict:
    """Deep personalized analysis — natal + dasha combined."""
    planets = chart.get('planets', {})
    dasha_info = chart.get('dasha', {})
    mahadasha = dasha_info.get('mahadasha', '')
    asc = chart.get('ascendant', {})
    asc_sign = asc.get('sign', '') if isinstance(asc, dict) else ''

    # 2nd house = wealth, 11th house = gains, 9th house = luck, 5th = speculation
    wealth_houses = {2: 'Wealth', 5: 'Speculation', 9: 'Fortune', 11: 'Gains'}
    wealth_analysis = []
    for planet_name, planet_data in planets.items():
        if planet_name == 'Ascendant':
            continue
        h = _get_planet_house(planets, planet_name)
        if h in wealth_houses:
            sign = _get_planet_sign(planets, planet_name)
            is_retro = _get_planet_retrograde(planets, planet_name)
            strength = _planet_strength_score(planet_name, sign, h, is_retro)
            wealth_analysis.append({
                'planet': planet_name,
                'house': h,
                'house_name': wealth_houses[h],
                'sign': sign,
                'strength': strength,
                'retro': is_retro,
            })

    # Build sector recommendations combining natal strength + dasha
    sector_list = _build_sector_analysis(chart)
    dasha_profile = DASHA_FINANCIAL_PROFILE.get(mahadasha, {})
    dasha_favored = dasha_profile.get('favorable', [])

    personal_recs = []
    for item in sector_list[:8]:
        is_dasha_favored = any(item['sector'].lower() in d.lower() or d.lower() in item['sector'].lower()
                               for d in dasha_favored)
        combined_strength = item['strength'] + (20 if is_dasha_favored else 0)
        combined_strength = min(100, combined_strength)

        def _rating(s):
            if s >= 85:
                return 'Excellent'
            elif s >= 70:
                return 'Very Good'
            elif s >= 55:
                return 'Good'
            elif s >= 40:
                return 'Moderate'
            else:
                return 'Caution'

        personal_recs.append({
            'sector': item['sector'],
            'natal_strength': item['strength'],
            'dasha_boost': 20 if is_dasha_favored else 0,
            'combined_strength': combined_strength,
            'rating': _rating(combined_strength),
            'ruling_planet': item['ruling_planet'],
            'planet_sign': item['planet_sign'],
            'planet_house': item['planet_house'],
            'stocks': item['stocks'],
            'advice': (
                ('✅ Dasha + Natal aligned — strong opportunity. ' if is_dasha_favored else '') +
                item['reason']
            ),
        })

    personal_recs.sort(key=lambda x: x['combined_strength'], reverse=True)

    return {
        'success': True,
        'ascendant': asc_sign,
        'mahadasha': mahadasha,
        'wealth_house_analysis': sorted(wealth_analysis, key=lambda x: x['strength'], reverse=True),
        'recommendations': personal_recs[:6],
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'summary': (
            f"Your {asc_sign} ascendant with {mahadasha} Mahadasha indicates: "
            f"{dasha_profile.get('outlook', 'Focus on your natal strengths.')}"
        ),
    }


def analyze_financial(chart_json: str) -> str:
    """Three-tab financial analysis: market (dasha), sector (natal), personalized (combined)."""
    try:
        chart_data = _normalize_chart(json.loads(chart_json))

        market_overview = _build_market_overview(chart_data)
        sector_analysis = _build_sector_analysis(chart_data)
        personalized = _build_personalized(chart_data)

        return json.dumps({
            'success': True,
            'market': market_overview,
            'sector': sector_analysis,
            'personalized': personalized,
        })
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})
