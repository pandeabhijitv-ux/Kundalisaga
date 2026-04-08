# AstroKnowledge - AI Coding Agent Instructions

## Project Overview
**KundaliSaga** (formerly AstroKnowledge) is a privacy-first Vedic astrology application with dual interfaces: a Streamlit web app (`app.py`) and React Native mobile app (`mobile/`). The system integrates ancient astrological calculations (Swiss Ephemeris) with modern AI (local Ollama LLM) for interpretations.

**Core Principle**: 100% local-first, no cloud APIs. All data stays on device (file-based storage, ChromaDB vectors, Ollama LLM).

## Architecture

### Component Boundaries
- **Frontend Layer**: Streamlit UI (`app.py`, 7800+ lines) handles all user interactions, routing, and state management via `st.session_state`
- **Calculation Layer**: `src/astrology_engine/vedic_calculator.py` wraps Swiss Ephemeris for Vedic calculations (sidereal zodiac, Lahiri ayanamsa)
- **Knowledge Layer**: Dual RAG system - `src/simple_rag/` (text search fallback) and `src/rag_system/` (ChromaDB + sentence-transformers)
- **Storage Layer**: JSON files for all persistent data (`data/users/`, `data/payments/`, `data/user_data/`)
- **Mobile Bridge**: React Native app uses Chaquopy to call Python modules directly (`mobile/python_modules/`)

### Critical Data Flows
1. **Birth Chart Generation**: `app.py` → `VedicAstrologyEngine` → Swiss Ephemeris → returns `PlanetPosition` dataclasses → saved to `data/user_data/charts/{user_id}.json`
2. **Q&A System**: User query → `SimpleKnowledgeBase.search()` (keyword matching) → `generate_answer()` (Ollama) → logged to `data/user_data/history/{user_id}_queries.jsonl`
3. **Authentication**: Email OTP stored in `data/users/otp_codes.json`, sessions in `sessions.json`, bcrypt-hashed passwords in `users.json`
4. **Payment Credits**: File-based ledger in `data/payments/user_credits.json`, transactions in `transactions.json`

## Development Workflows

### Running the Application
```powershell
# Activate virtual environment (ALWAYS required)
.\.venv\Scripts\Activate.ps1

# Start Streamlit (default: http://localhost:8501)
streamlit run app.py
```

### Building Mobile APK
```powershell
# Use the build script (handles Gradle wrapper, JDK setup)
.\build_apk.ps1

# Output: mobile/android/app/build/outputs/apk/release/app-release.apk
```

### Testing Key Components
```powershell
# Test calculations (no external services needed)
python test_chart_calculation.py

# Test RAG system (requires Ollama running)
python test_rag_system.py

# Test current Dasha calculations
python test_current_dasha.py
```

### Configuration
All config in `config/config.yaml`:
- Astrology: ayanamsa (LAHIRI), house system (WHOLE_SIGN), dasha systems
- LLM: model (llama3.2), provider (ollama), temperature (0.7)
- Payment: pricing per feature (all 10 INR), UPI details, coupon codes
- Email: SMTP settings (disabled by default)

## Project-Specific Conventions

### Dataclasses Over Dicts
Use typed dataclasses for structured data:
```python
from dataclasses import dataclass, asdict

@dataclass
class BirthDetails:
    date: datetime
    latitude: float
    longitude: float
    timezone: str
    name: str = ""
```

### File-Based Storage Pattern
All managers follow this pattern (no database):
```python
class Manager:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_file = self.data_dir / "data.json"
        
    def _load_data(self) -> Dict:
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
```

### Streamlit Session State Keys
Critical session keys in `app.py`:
- `st.session_state.authenticated`: bool for login status
- `st.session_state.user_email`: current user email
- `st.session_state.selected_profile`: active user profile
- `st.session_state.credits`: credit balance (refreshed per page)

### Swiss Ephemeris Integration
Always set ayanamsa mode before calculations:
```python
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri ayanamsa
swe.set_ephe_path(None)  # Use default ephemeris path

# Calculate planets (tropical first, then subtract ayanamsa)
ayanamsa = swe.get_ayanamsa_ut(julian_day)
tropical_long = swe.calc_ut(julian_day, planet_id)[0]
sidereal_long = (tropical_long - ayanamsa) % 360
```

### Mobile-Python Bridge
React Native calls Python via Chaquopy:
```typescript
// TypeScript side (mobile/src/services/PythonBridge.ts)
import { NativeModules } from 'react-native';
const { PythonBridge } = NativeModules;

const result = await PythonBridge.calculateChart(birthData);
```

```python
# Python side (mobile/python_modules/vedic_calculator.py)
def calculate_chart_json(birth_data_json: str) -> str:
    birth_data = json.loads(birth_data_json)
    engine = VedicAstrologyEngine()
    chart = engine.calculate_chart(BirthDetails(**birth_data))
    return json.dumps(asdict(chart))
```

## Common Pitfalls

### ChromaDB Dependency Issues
If ChromaDB breaks (common on Windows), app falls back to `src/simple_rag/simple_search.py`. Check imports:
```python
try:
    from src.rag_system import RAGSystem
except:
    from src.simple_rag.simple_search import SimpleKnowledgeBase
```

### Timezone Handling
Always use `pytz` for timezone-aware datetimes:
```python
import pytz
tz = pytz.timezone(user_timezone)
birth_dt = tz.localize(datetime(year, month, day, hour, minute))
utc_dt = birth_dt.astimezone(pytz.UTC)
```

### Ollama Connection
Check Ollama is running before RAG operations:
```python
import requests
try:
    requests.get("http://localhost:11434", timeout=2)
except:
    st.error("Ollama not running. Start with: ollama serve")
```

### Credit Deduction
Always wrap paid features with credit checks:
```python
credits = payment_manager.get_user_credits(user_email)
if credits < cost:
    st.error(f"Insufficient credits. Need {cost}, have {credits}")
    return

success, msg = payment_manager.deduct_credits(user_email, cost, reason)
if not success:
    st.error(msg)
    return
```

## Key Files Reference

- **Entry Point**: `app.py` - Entire Streamlit UI (7800 lines)
- **Calculations**: `src/astrology_engine/vedic_calculator.py` - Swiss Ephemeris wrapper
- **RAG System**: `src/simple_rag/simple_search.py` - Keyword-based search + Ollama
- **User Profiles**: `src/user_manager/manager.py` - File-based profile/chart storage
- **Auth**: `src/auth/auth_manager.py` - Email OTP, bcrypt passwords, sessions
- **Payment**: `src/payment/payment_manager.py` - Credit ledger, UPI QR generation
- **Config**: `config/config.yaml` - Single source of truth for all settings
- **Mobile Entry**: `mobile/App.tsx` - React Native navigation setup
- **Build Scripts**: `build_apk.ps1` - Android build with Gradle wrapper handling

## External Dependencies

### Required Services
- **Ollama** (localhost:11434): Local LLM for Q&A generation
- **Swiss Ephemeris**: Planetary calculations (bundled with pyswisseph)

### Python Packages (requirements.txt)
- `streamlit==1.29.0`: Web UI framework
- `pyswisseph==2.10.3.2`: Vedic astrology calculations
- `chromadb==0.4.22`: Vector database (fallback: simple_rag)
- `sentence-transformers==2.2.2`: Local embeddings
- `ollama==0.1.6`: LLM client
- `bcrypt==4.1.2`: Password hashing
- `qrcode[pil]==7.4.2`: UPI QR code generation

### Mobile Dependencies (mobile/package.json)
- `react-native==0.74.*`: Mobile framework
- `@react-navigation/native`: Navigation
- Chaquopy (Android Gradle plugin): Python-Java bridge
