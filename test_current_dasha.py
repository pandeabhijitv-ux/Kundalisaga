from datetime import datetime
import pytz
from src.astrology_engine.vedic_calculator import VedicCalculator

calc = VedicCalculator()
birth_date = datetime(1978, 9, 10, 14, 55)
tz = pytz.timezone('Asia/Kolkata')
birth_dt = tz.localize(birth_date)

# Moon at 97.3899° (from chart data)
dashas = calc.calculate_vimshottari_dasha(97.3899, birth_dt)

today = datetime.now()
print(f'Birth: {birth_dt.date()}')
print(f'Today: {today.date()}')
print(f'\nSearching for current dasha...\n')

for i, d in enumerate(dashas[:30]):
    start = d['start_date']
    end = d['end_date']
    if start <= today <= end:
        print(f'>>> CURRENT DASHA FOUND <<<')
        print(f'Mahadasha: {d["lord"]}')
        print(f'Antardasha: {d.get("antar_lord", d["lord"])}')
        print(f'Period: {start.date()} to {end.date()}')
        print(f'Index in list: {i}')
        break
else:
    print('First 3 dashas:')
    for i in range(min(3, len(dashas))):
        d = dashas[i]
        print(f'{i+1}. {d["lord"]}-{d.get("antar_lord", d["lord"])} ({d["start_date"].date()} to {d["end_date"].date()})')
