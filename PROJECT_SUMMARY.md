# AstroKnowledge - Complete Project Summary

## 🎯 Project Overview

**AstroKnowledge** is a comprehensive, privacy-focused Vedic astrology application that combines:
- Ancient astrological wisdom from thousands of books
- Precise astronomical calculations using Swiss Ephemeris
- AI-powered insights using local LLM (100% private, no cloud APIs)
- File-based storage for complete data ownership

## ✨ Key Features

### 📚 Document Management
- Process thousands of astrology books (PDF, DOCX, TXT, images)
- Automatic text extraction and OCR support
- Intelligent chunking and indexing
- Vector database for semantic search

### 🔮 Vedic Astrology Calculations
- Accurate birth chart (D1) calculations
- All 9 planets + Ascendant
- 27 Nakshatras with Pada identification
- Vimshottari Dasha periods
- House cusps (Placidus/Equal/Whole Sign)
- Multiple Ayanamsa support (Lahiri, Raman, KP)
- Retrograde detection

### 🤖 AI-Powered Q&A
- RAG (Retrieval-Augmented Generation) system
- Searches your book collection for relevant knowledge
- Combines book wisdom with chart analysis
- Local LLM (Ollama) - no data sent to cloud
- Context-aware answers

### 👨‍👩‍👧‍👦 Family Profiles
- Manage multiple user profiles
- Support for family members
- Individual chart storage
- Query history tracking

### 🏥 Remedies
- Automatic chart analysis
- Planet-specific remedies
- Mantras, gemstones, charities, fasting
- Book-based recommendations
- General spiritual guidance

### 🔒 Privacy First
- 100% local processing
- No cloud APIs for LLM
- File-based storage (JSON/JSONL)
- Easy backup and portability
- No telemetry or tracking

## 📁 Project Structure

```
AstroKnowledge/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── config/
│   └── config.yaml                     # Application configuration
├── src/
│   ├── document_processor/             # PDF/DOCX/Image processing
│   │   ├── __init__.py
│   │   └── processor.py
│   ├── astrology_engine/               # Vedic calculations
│   │   ├── __init__.py
│   │   └── vedic_calculator.py
│   ├── rag_system/                     # RAG & LLM integration
│   │   ├── __init__.py
│   │   └── rag.py
│   ├── user_manager/                   # Profile management
│   │   ├── __init__.py
│   │   └── manager.py
│   ├── remedy_engine/                  # Remedy suggestions
│   │   ├── __init__.py
│   │   └── remedies.py
│   └── utils/                          # Config & logging
│       ├── __init__.py
│       ├── config_loader.py
│       └── logger.py
├── data/
│   ├── books/                          # Your astrology books
│   ├── vector_db/                      # ChromaDB storage
│   └── user_data/                      # Profiles & history
│       ├── profiles/
│       ├── charts/
│       └── history/
├── logs/                               # Application logs
├── tests/                              # Unit tests
├── setup.ps1                           # Windows setup script
├── setup.sh                            # Linux/Mac setup script
├── test_installation.py                # Verify installation
├── test_chart_calculation.py           # Test astrology engine
├── test_rag_system.py                  # Test RAG system
├── README.md                           # Main documentation
├── QUICKSTART.md                       # Quick start guide
├── ARCHITECTURE.md                     # Technical architecture
└── LICENSE                             # MIT License
```

## 🛠️ Technology Stack

### Backend (Python 3.10+)
- **Document Processing**: unstructured, pdfplumber, python-docx, pytesseract
- **Astrology**: pyswisseph (Swiss Ephemeris)
- **Vector DB**: ChromaDB (local, persistent)
- **Embeddings**: sentence-transformers (local models)
- **LLM**: Ollama (llama3.2, mistral, etc.)
- **Storage**: JSON/JSONL (no database)
- **Location**: geopy, timezonefinder
- **Config**: PyYAML, python-dotenv

### Frontend (Prototype)
- **UI**: Streamlit (web-based)
- **Charts**: Plotly (future)
- **Interactive**: streamlit-extras

### Future (Production)
- **Mobile**: React Native (iOS/Android)
- **Desktop**: Electron (Windows/Mac/Linux)
- **API**: FastAPI (REST endpoints)

## 📦 Installation Summary

### Prerequisites
1. **Python 3.10+**
2. **Ollama** (from https://ollama.ai)
3. **Git** (optional)

### Quick Setup (Windows)
```powershell
# Clone or download the project
cd C:\AstroKnowledge

# Run setup script
.\setup.ps1

# This will:
# - Create virtual environment
# - Install dependencies
# - Download Ollama model (llama3.2)
# - Setup directories
```

### Quick Setup (Linux/Mac)
```bash
# Clone or download the project
cd /path/to/AstroKnowledge

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Verify Installation
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Run verification
python test_installation.py

# Test astrology calculations
python test_chart_calculation.py

# Test RAG system (requires Ollama)
python test_rag_system.py
```

### Run Application
```bash
streamlit run app.py
```

Visit http://localhost:8501

## 🚀 Quick Start Workflow

### 1. First Time Setup (5 minutes)
1. Run setup script
2. Start Ollama: `ollama pull llama3.2`
3. Run `streamlit run app.py`

### 2. Create Your Profile (2 minutes)
1. Go to "👤 User Profiles"
2. Click "Create New Profile"
3. Enter birth details (date, time, place)
4. System auto-detects lat/lon/timezone

### 3. Add Books (10-30 minutes)
1. Place PDFs in `data/books/` folder
2. Go to "📚 Document Management"
3. Click "Process Books from data/books/ folder"
4. Wait for indexing to complete

### 4. Generate Horoscope (1 minute)
1. Go to "🔮 Horoscope"
2. Select your profile
3. Click "Calculate Birth Chart"
4. View detailed planetary positions

### 5. Ask Questions (30 seconds each)
1. Go to "💬 Ask Question"
2. Check "Include my birth chart"
3. Type question (e.g., "What does my Moon in Cancer mean?")
4. Get AI-powered answer with sources

### 6. Get Remedies (1 minute)
1. Go to "🏥 Remedies"
2. Select profile
3. Enter specific concern (optional)
4. Receive personalized remedies

## 📊 File Formats & Storage

### User Data (JSON)
```json
// data/user_data/profiles/john_doe.json
{
  "user_id": "john_doe",
  "name": "John Doe",
  "birth_date": "1990-01-15",
  "birth_time": "14:30",
  "birth_place": "New Delhi, India",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata",
  "relationship": "Self"
}
```

### Chart Data (JSON)
```json
// data/user_data/charts/john_doe/birth_chart_20251217.json
{
  "birth_details": {...},
  "ascendant": {...},
  "planets": {
    "Sun": {"sign": "Capricorn", "house": 10, ...},
    ...
  },
  "saved_at": "2025-12-17T10:30:00"
}
```

### Query History (JSONL)
```jsonl
// data/user_data/history/queries_202512.jsonl
{"timestamp": "2025-12-17T10:00:00", "user_id": "john_doe", "query": "...", "answer": "..."}
{"timestamp": "2025-12-17T11:00:00", "user_id": "jane_smith", "query": "...", "answer": "..."}
```

## 🎨 UI Features

### Home Page
- Quick start guide
- System status (Ollama, documents indexed)
- Recent activity

### User Profiles
- Create/view/select profiles
- Support for family members
- Birth detail management

### Document Management
- Upload books via UI
- Process from folder
- View indexing status

### Horoscope
- Select profile
- Calculate birth chart
- View planetary positions
- Nakshatra details
- Vimshottari Dasha periods

### Ask Question
- Text input for questions
- Optional chart context
- AI-powered answers
- Source citations
- Query history

### Remedies
- Automatic chart analysis
- Planet-specific remedies
- Book-based suggestions
- General spiritual advice

### Settings
- View configuration
- LLM model info
- Ayanamsa settings
- Data directories

## 🔧 Configuration Options

Edit `config/config.yaml`:

```yaml
# Change LLM model
llm:
  model: "llama3.2"  # or "mistral", "llama2", etc.
  temperature: 0.7

# Change ayanamsa
astrology:
  ayanamsa: "LAHIRI"  # or "RAMAN", "KP"
  house_system: "PLACIDUS"

# Adjust RAG settings
rag:
  top_k: 5  # Number of search results
  min_relevance_score: 0.5

# Document processing
documents:
  chunk_size: 1000
  chunk_overlap: 200
```

## 📈 Performance

### Typical Performance (CPU-based)
- **Document processing**: 10-50 pages/minute
- **Embedding generation**: 100-500 sentences/second
- **Vector search**: <100ms per query
- **Chart calculation**: <10ms per chart
- **LLM generation**: 10-50 tokens/second (llama3.2 3B)

### Recommended Hardware
- **Minimum**: 8GB RAM, modern CPU
- **Recommended**: 16GB RAM, multi-core CPU
- **Optimal**: 32GB RAM, GPU (CUDA), SSD

### Scalability
- **Books**: Handles thousands
- **Users**: Unlimited (file-based)
- **Queries**: ChromaDB efficient up to 1M documents

## 🔐 Security & Privacy

### What's Local
✅ All user data (profiles, charts, history)
✅ LLM processing (Ollama)
✅ Vector search (ChromaDB)
✅ Embeddings generation
✅ Astrology calculations

### What Needs Internet
⚠️ Initial Ollama model download (~2GB, one-time)
⚠️ Geocoding for birth place (first time only, cached)
⚠️ Swiss Ephemeris data (first time only, cached)
⚠️ Python package installation (setup only)

### After Setup
✅ Can run 100% offline
✅ No telemetry
✅ No tracking
✅ No cloud APIs

## 🚧 Future Development

### Short Term
- [ ] Chart visualization (graphical)
- [ ] PDF report export
- [ ] More divisional charts (D9, D10)
- [ ] Transit analysis

### Medium Term
- [ ] FastAPI backend
- [ ] REST API
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)

### Long Term
- [ ] Fine-tuned astrology LLM
- [ ] Multi-language (Hindi, Sanskrit)
- [ ] Voice interface
- [ ] Compatibility analysis
- [ ] Muhurta calculations

## 📝 Notes for Development

### Adding New Features
1. **New chart types**: Extend `VedicAstrologyEngine`
2. **New remedies**: Update `RemedyEngine.get_general_remedies()`
3. **New UI pages**: Add tabs in `app.py`
4. **New storage**: Add methods in `UserManager`

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test
python test_chart_calculation.py

# Test with coverage
pytest --cov=src tests/
```

### Debugging
- Check `logs/` folder for detailed errors
- Enable DEBUG level in config
- Use `streamlit run app.py --logger.level=debug`

## 📚 Documentation Files

1. **README.md** - Main project overview
2. **QUICKSTART.md** - Installation and first steps
3. **ARCHITECTURE.md** - Technical details and design
4. **LICENSE** - MIT License
5. **This file** - Complete summary

## 🤝 Contributing

Contributions welcome! Areas:
- Astrological calculations
- Remedy databases
- UI/UX improvements
- Documentation
- Testing
- Performance optimization

## 📧 Support

For issues:
1. Check `QUICKSTART.md` troubleshooting
2. Review `logs/` files
3. Check `ARCHITECTURE.md` for technical details
4. Run verification scripts

## 🎓 Learning Resources

### Vedic Astrology
- Use the app to query your own books
- Classical texts: Brihat Parashara Hora, Jataka Parijata
- Modern: Books by K.N. Rao, B.V. Raman

### Technical
- Swiss Ephemeris: https://www.astro.com/swisseph/
- Ollama: https://ollama.ai
- ChromaDB: https://docs.trychroma.com/
- Streamlit: https://docs.streamlit.io/

## 🌟 Acknowledgments

- Swiss Ephemeris for astronomical calculations
- Ollama team for local LLM infrastructure
- ChromaDB for vector database
- Sentence Transformers for embeddings
- Streamlit for rapid UI development

---

## ⚡ Getting Started Right Now

```bash
# 1. Setup (one time)
.\setup.ps1  # Windows
# or
./setup.sh   # Linux/Mac

# 2. Run
streamlit run app.py

# 3. Create profile → Add books → Ask questions!
```

**That's it! You now have a complete, privacy-focused Vedic astrology AI assistant running locally on your machine.**

---

**Built with ❤️ for the Vedic Astrology community**
