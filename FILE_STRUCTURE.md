# AstroKnowledge - Complete File Structure

## Project Root
```
AstroKnowledge/
│
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # Quick start installation guide  
├── ARCHITECTURE.md                    # Technical architecture details
├── PROJECT_SUMMARY.md                 # Complete project summary
├── LICENSE                            # MIT License
│
├── app.py                             # Main Streamlit application (entry point)
├── requirements.txt                   # Python dependencies
│
├── setup.ps1                          # Windows PowerShell setup script
├── setup.sh                           # Linux/Mac bash setup script
│
├── test_installation.py               # Verify installation and dependencies
├── test_chart_calculation.py          # Test Vedic astrology engine
├── test_rag_system.py                 # Test RAG and LLM integration
│
├── .env.example                       # Example environment variables
├── .gitignore                         # Git ignore rules
│
├── config/
│   └── config.yaml                    # Application configuration (YAML)
│
├── src/                               # Source code modules
│   ├── __init__.py
│   │
│   ├── utils/                         # Utilities (config, logging)
│   │   ├── __init__.py
│   │   ├── config_loader.py           # YAML config loader with singleton
│   │   └── logger.py                  # Logging setup and configuration
│   │
│   ├── document_processor/            # Document processing module
│   │   ├── __init__.py
│   │   └── processor.py               # PDF/DOCX/Image text extraction
│   │                                  # - DocumentProcessor class
│   │                                  # - ProcessedDocument dataclass
│   │                                  # - OCR support via Tesseract
│   │                                  # - Text chunking with overlap
│   │
│   ├── astrology_engine/              # Vedic astrology calculations
│   │   ├── __init__.py
│   │   └── vedic_calculator.py        # Swiss Ephemeris integration
│   │                                  # - VedicAstrologyEngine class
│   │                                  # - BirthDetails dataclass
│   │                                  # - PlanetPosition dataclass
│   │                                  # - Birth chart calculations
│   │                                  # - Nakshatra identification
│   │                                  # - Vimshottari Dasha
│   │                                  # - Geocoding support
│   │
│   ├── rag_system/                    # RAG (Retrieval-Augmented Generation)
│   │   ├── __init__.py
│   │   └── rag.py                     # Vector search + LLM generation
│   │                                  # - RAGSystem class
│   │                                  # - ChromaDB integration
│   │                                  # - Sentence Transformers embeddings
│   │                                  # - Ollama LLM integration
│   │                                  # - Document indexing
│   │                                  # - Semantic search
│   │
│   ├── user_manager/                  # User profile management
│   │   ├── __init__.py
│   │   └── manager.py                 # File-based user storage
│   │                                  # - UserManager class
│   │                                  # - UserProfile dataclass
│   │                                  # - JSON profile storage
│   │                                  # - Chart storage
│   │                                  # - Query/remedy logging (JSONL)
│   │                                  # - Family member support
│   │
│   └── remedy_engine/                 # Astrological remedy suggestions
│       ├── __init__.py
│       └── remedies.py                # Remedy analysis and database
│                                      # - RemedyEngine class
│                                      # - Chart analysis for issues
│                                      # - Planet-specific remedies
│                                      # - Mantra/gemstone/charity suggestions
│                                      # - RAG integration for book remedies
│
├── data/                              # All application data (local)
│   ├── books/                         # User's astrology books
│   │   └── .gitkeep                   # Placeholder (git tracking)
│   │                                  # Structure:
│   │                                  # books/
│   │                                  # ├── vedic_astrology_101.pdf
│   │                                  # ├── classics/
│   │                                  # │   ├── brihat_parashara.pdf
│   │                                  # │   └── jataka_parijata.docx
│   │                                  # └── modern/
│   │                                  #     └── planets_in_houses.pdf
│   │
│   ├── vector_db/                     # ChromaDB vector database
│   │   └── .gitkeep                   # (Created automatically by ChromaDB)
│   │                                  # Contains:
│   │                                  # - Document embeddings
│   │                                  # - Vector indices
│   │                                  # - Metadata
│   │
│   └── user_data/                     # User profiles and data
│       ├── .gitkeep
│       ├── profiles/                  # User profiles (JSON)
│       │                              # Example: john_doe.json
│       │                              # {
│       │                              #   "user_id": "john_doe",
│       │                              #   "name": "John Doe",
│       │                              #   "birth_date": "1990-01-15",
│       │                              #   "birth_time": "14:30",
│       │                              #   "latitude": 28.6139,
│       │                              #   ...
│       │                              # }
│       │
│       ├── charts/                    # Calculated charts (JSON)
│       │   └── {user_id}/             # One folder per user
│       │       ├── birth_chart_YYYYMMDD_HHMMSS.json
│       │       └── transit_YYYYMMDD_HHMMSS.json
│       │
│       └── history/                   # Query and remedy logs (JSONL)
│           ├── queries_YYYYMM.jsonl   # Append-only query logs
│           └── remedies_YYYYMM.jsonl  # Append-only remedy logs
│
├── logs/                              # Application logs
│   └── app_YYYYMMDD.log               # Daily rotating logs
│
└── tests/                             # Unit tests (future)
    ├── __init__.py
    ├── test_document_processor.py
    ├── test_astrology_engine.py
    ├── test_rag_system.py
    ├── test_user_manager.py
    └── test_remedy_engine.py
```

## File Descriptions

### Configuration Files

| File | Purpose | Format |
|------|---------|--------|
| `config/config.yaml` | Main configuration | YAML |
| `.env` | Environment variables (local) | KEY=VALUE |
| `.env.example` | Example env variables | KEY=VALUE |

### Python Modules

| Module | Lines | Purpose |
|--------|-------|---------|
| `app.py` | ~800 | Streamlit web application |
| `src/utils/config_loader.py` | ~100 | Config management |
| `src/utils/logger.py` | ~60 | Logging setup |
| `src/document_processor/processor.py` | ~250 | Document processing |
| `src/astrology_engine/vedic_calculator.py` | ~400 | Astrology calculations |
| `src/rag_system/rag.py` | ~250 | RAG system |
| `src/user_manager/manager.py` | ~300 | User management |
| `src/remedy_engine/remedies.py` | ~350 | Remedy suggestions |

### Setup & Testing

| File | Purpose | Platform |
|------|---------|----------|
| `setup.ps1` | Automated setup | Windows |
| `setup.sh` | Automated setup | Linux/Mac |
| `test_installation.py` | Verify setup | All |
| `test_chart_calculation.py` | Test astrology | All |
| `test_rag_system.py` | Test AI/RAG | All |

### Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Overview & features | All users |
| `QUICKSTART.md` | Installation guide | New users |
| `ARCHITECTURE.md` | Technical details | Developers |
| `PROJECT_SUMMARY.md` | Complete summary | All |
| `LICENSE` | MIT license | Legal |

## Data Storage Structure

### User Profile (JSON)
```
data/user_data/profiles/john_doe.json
```
```json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "birth_date": "1990-01-15",
  "birth_time": "14:30",
  "birth_place": "New Delhi, India",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata",
  "relationship": "Self",
  "gender": "Male",
  "notes": "",
  "created_at": "2025-12-17T10:00:00",
  "updated_at": "2025-12-17T10:00:00"
}
```

### Birth Chart (JSON)
```
data/user_data/charts/john_doe/birth_chart_20251217_100000.json
```
```json
{
  "birth_details": {...},
  "julian_day": 2460660.9583333335,
  "ascendant": {
    "name": "Ascendant",
    "longitude": 285.34,
    "sign": "Capricorn",
    "sign_num": 9,
    "degree_in_sign": 15.34,
    "nakshatra": "Uttara Ashadha",
    "nakshatra_pada": 2,
    "house": 1
  },
  "planets": {
    "Sun": {...},
    "Moon": {...},
    ...
  },
  "house_cusps": [285.34, 315.67, ...],
  "ayanamsa": 24.1234,
  "saved_at": "2025-12-17T10:00:00",
  "chart_type": "birth_chart"
}
```

### Query Log (JSONL)
```
data/user_data/history/queries_202512.jsonl
```
```jsonl
{"timestamp":"2025-12-17T10:00:00","user_id":"john_doe","query":"What does Moon in Cancer mean?","answer":"The Moon is...","num_sources":5}
{"timestamp":"2025-12-17T11:00:00","user_id":"jane_smith","query":"Mars in 7th house effects?","answer":"Mars in the 7th...","num_sources":3}
```

## Module Dependencies

```
app.py
├── src.utils (config, logger)
├── src.document_processor
│   └── src.utils
├── src.astrology_engine
│   └── src.utils
├── src.rag_system
│   └── src.utils
├── src.user_manager
│   └── src.utils
└── src.remedy_engine
    ├── src.utils
    └── src.rag_system (optional)
```

## External Dependencies

### Core Libraries
- `python 3.10+`
- `streamlit` - Web UI
- `pyyaml` - Config parsing
- `python-dotenv` - Environment variables

### Document Processing
- `unstructured` - Universal document parser
- `pdfplumber` - PDF text extraction
- `python-docx` - Word documents
- `pytesseract` - OCR
- `Pillow` - Image processing

### Astrology
- `pyswisseph` - Swiss Ephemeris
- `pytz` - Timezone handling
- `geopy` - Geocoding
- `timezonefinder` - Timezone lookup

### AI/ML
- `chromadb` - Vector database
- `sentence-transformers` - Embeddings
- `ollama` - Local LLM API
- `langchain` - RAG framework

### Data & Utils
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `requests` - HTTP client
- `jsonlines` - JSONL format
- `tqdm` - Progress bars

## File Sizes (Approximate)

| Component | Size |
|-----------|------|
| Source code | ~15 KB (pure Python) |
| Config files | ~5 KB |
| Documentation | ~100 KB |
| Virtual environment | ~500 MB |
| Ollama model (llama3.2) | ~2 GB |
| Embedding model | ~100 MB |
| Swiss Ephemeris data | ~10 MB |
| Sample books (user data) | Variable |
| Vector DB (per 1000 books) | ~500 MB |

## Backup Strategy

### Essential Files (always backup)
```
data/user_data/         # User profiles, charts, history
config/config.yaml      # Your configuration
.env                    # Environment settings (if modified)
```

### Optional (can regenerate)
```
data/vector_db/         # Can rebuild from books
data/books/             # Backup original books separately
logs/                   # Log files (usually not needed)
```

### Backup Command
```bash
# Windows
tar -czf astroknowledge_backup_YYYYMMDD.tar.gz data/user_data config .env

# Linux/Mac
tar -czf astroknowledge_backup_$(date +%Y%m%d).tar.gz data/user_data config .env
```

## Development Workflow

### Adding a New Feature

1. **Create branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Modify source**
   - Add to appropriate module in `src/`
   - Update `config.yaml` if needed

3. **Update tests**
   - Add test in `tests/`

4. **Update docs**
   - Update `README.md` or `ARCHITECTURE.md`

5. **Test**
   ```bash
   python test_installation.py
   pytest tests/
   ```

6. **Commit**
   ```bash
   git add .
   git commit -m "Add: new feature description"
   ```

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production (Future)
```bash
# Build FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Build mobile app
cd mobile && npm run build

# Build desktop app
cd desktop && npm run build
```

---

**This file structure supports:**
- ✅ Scalability (add more modules easily)
- ✅ Maintainability (clear separation of concerns)
- ✅ Privacy (all data local)
- ✅ Portability (easy backup/restore)
- ✅ Extensibility (modular design)
