# AstroKnowledge - Technical Architecture

## System Overview

AstroKnowledge is a privacy-first, local-only Vedic astrology application that combines:
- Ancient astrological texts (thousands of books)
- Swiss Ephemeris for precise calculations
- Local LLM (Ollama) for AI-powered insights
- File-based storage for complete data privacy

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                          │
│  (Home | Profiles | Documents | Horoscope | Q&A | Remedies) │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                  Application Layer                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Document   │  │   Astrology  │  │     RAG      │      │
│  │  Processor   │  │    Engine    │  │    System    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │     User     │  │    Remedy    │                         │
│  │   Manager    │  │    Engine    │                         │
│  └──────────────┘  └──────────────┘                         │
└──────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                  Storage Layer                               │
│                                                              │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │  File System     │  │   ChromaDB      │                 │
│  │  (JSON/JSONL)    │  │  (Vector DB)    │                 │
│  │                  │  │                 │                 │
│  │ • User Profiles  │  │ • Embeddings    │                 │
│  │ • Charts         │  │ • Book Chunks   │                 │
│  │ • History        │  │ • Metadata      │                 │
│  └──────────────────┘  └─────────────────┘                 │
└──────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                External Services (Local)                     │
│                                                              │
│  ┌──────────────────┐  ┌─────────────────┐                 │
│  │     Ollama       │  │ Swiss Ephemeris │                 │
│  │ (Local LLM)      │  │   (Astronomy)   │                 │
│  │                  │  │                 │                 │
│  │ • llama3.2       │  │ • Planetary     │                 │
│  │ • No API calls   │  │   positions     │                 │
│  │ • 100% private   │  │ • House cusps   │                 │
│  └──────────────────┘  └─────────────────┘                 │
└──────────────────────────────────────────────────────────────┘
```

## Module Details

### 1. Document Processor (`src/document_processor/`)

**Purpose:** Extract text from various document formats

**Components:**
- `processor.py`: Main document processing logic
  - `DocumentProcessor`: Handle PDF, DOCX, TXT, images
  - `ProcessedDocument`: Data structure for processed docs
  - OCR support via Tesseract

**Key Features:**
- Multi-format support (PDF, DOCX, TXT, PNG, JPG)
- Text chunking with overlap
- File deduplication via SHA256 hashing
- Batch processing

**Technologies:**
- `pdfplumber`: PDF text extraction
- `python-docx`: Word document processing
- `pytesseract`: OCR for scanned images
- `Pillow`: Image processing

### 2. Astrology Engine (`src/astrology_engine/`)

**Purpose:** Vedic astrology calculations using Swiss Ephemeris

**Components:**
- `vedic_calculator.py`: Core calculation engine
  - `VedicAstrologyEngine`: Main calculation class
  - `BirthDetails`: Birth information data structure
  - `PlanetPosition`: Planet position data

**Key Features:**
- Sidereal calculations (Lahiri ayanamsa default)
- Birth chart (D1) calculation
- 9 planet positions + Ascendant
- Nakshatra and Pada identification
- House system (Placidus default)
- Vimshottari Dasha calculation
- Retrograde detection
- Geocoding for place → lat/lon

**Technologies:**
- `pyswisseph`: Swiss Ephemeris library
- `geopy`: Location geocoding
- `timezonefinder`: Timezone detection
- `pytz`: Timezone handling

**Supported:**
- Planets: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- Divisional charts: D1 (extensible to D9, D10, etc.)
- Dasha systems: Vimshottari (extensible to Yogini, Ashtottari)
- Ayanamsas: Lahiri, Raman, KP, Fagan-Bradley

### 3. RAG System (`src/rag_system/`)

**Purpose:** Retrieval-Augmented Generation for Q&A

**Components:**
- `rag.py`: RAG implementation
  - `RAGSystem`: Vector search + LLM generation

**Workflow:**
1. **Document Ingestion:**
   - Text → Chunks (1000 chars, 200 overlap)
   - Chunks → Embeddings (sentence-transformers)
   - Store in ChromaDB

2. **Query Processing:**
   - Query → Embedding
   - Vector search (top-k=5)
   - Retrieve relevant chunks
   - Combine with chart context (optional)

3. **Answer Generation:**
   - Build prompt with context
   - Send to Ollama (llama3.2)
   - Stream or batch response
   - Return answer + sources

**Technologies:**
- `chromadb`: Vector database (local, persistent)
- `sentence-transformers`: Embedding model (all-MiniLM-L6-v2)
- `ollama`: Local LLM API
- `langchain`: RAG framework (optional)

**Configuration:**
- Top-k: 5 results
- Min relevance: 0.5
- Temperature: 0.7
- Max tokens: 2000

### 4. User Manager (`src/user_manager/`)

**Purpose:** File-based user profile and data management

**Components:**
- `manager.py`: User and data management
  - `UserManager`: CRUD operations
  - `UserProfile`: Profile data structure

**Storage Structure:**
```
data/user_data/
├── profiles/
│   ├── john_doe.json
│   └── jane_smith.json
├── charts/
│   ├── john_doe/
│   │   ├── birth_chart_20251217_120000.json
│   │   └── transit_20251217_150000.json
│   └── jane_smith/
└── history/
    ├── queries_202512.jsonl
    └── remedies_202512.jsonl
```

**Key Features:**
- JSON for profiles and charts
- JSONL for append-only logs
- Auto-generated user IDs
- Family member support
- Query history tracking
- Chart versioning

**No Database Required:**
- Pure file system
- Human-readable JSON
- Easy backup (copy folder)
- Portable across devices

### 5. Remedy Engine (`src/remedy_engine/`)

**Purpose:** Suggest astrological remedies

**Components:**
- `remedies.py`: Remedy suggestion logic
  - `RemedyEngine`: Analysis and suggestions

**Analysis:**
1. Chart analysis:
   - Debilitated planets
   - Retrograde planets
   - Malefics in key houses
   
2. Remedy database:
   - Mantras for each planet
   - Gemstone recommendations
   - Charitable activities
   - Fasting schedules
   - Lifestyle practices

3. Book integration:
   - Query RAG for remedies
   - Combine classical + AI insights

**Remedy Types:**
- **Mantra**: Specific chants (108 repetitions)
- **Gemstone**: Weight, metal, finger, day
- **Charity**: Items to donate, timing
- **Fasting**: Days and methods
- **Practices**: Lifestyle changes

### 6. Utils (`src/utils/`)

**Components:**
- `config_loader.py`: YAML configuration management
- `logger.py`: Logging setup

**Configuration:**
- YAML-based (`config/config.yaml`)
- Environment variable overrides
- Singleton pattern
- Dot notation access

**Logging:**
- Console + file logging
- Daily log rotation
- Configurable levels
- Detailed error tracking

## Data Flow Examples

### Example 1: Creating a Profile

```
User Input (UI)
  ├→ Name, Birth Date/Time, Place
  ↓
UserManager.create_profile()
  ├→ Geocode place (geopy)
  ├→ Get timezone (timezonefinder)
  ├→ Generate user_id
  ├→ Save to JSON file
  ↓
Profile Created
```

### Example 2: Calculating Birth Chart

```
User Selects Profile
  ↓
VedicAstrologyEngine.calculate_birth_chart()
  ├→ Convert local time → UTC → Julian Day
  ├→ Calculate house cusps (Swiss Ephemeris)
  ├→ Calculate Ascendant
  ├→ For each planet:
  │   ├→ Get tropical position
  │   ├→ Apply ayanamsa (sidereal)
  │   ├→ Determine sign & degree
  │   ├→ Find nakshatra & pada
  │   ├→ Determine house placement
  │   └→ Check retrograde
  ├→ Calculate Vimshottari Dasha
  ↓
UserManager.save_chart()
  ├→ Create JSON file
  ├→ Save in charts/user_id/
  ↓
Chart Displayed
```

### Example 3: Asking a Question

```
User Query + Optional Chart Context
  ↓
RAGSystem.ask()
  ├→ Generate query embedding (sentence-transformers)
  ├→ Search ChromaDB (vector similarity)
  ├→ Retrieve top-k documents
  ├→ Format chart context (if provided)
  ├→ Build prompt with system instructions
  ↓
Ollama API
  ├→ Send prompt to local LLM
  ├→ Generate answer (stream/batch)
  ↓
RAGSystem returns
  ├→ Answer text
  ├→ Source documents
  ├→ Metadata
  ↓
UserManager.log_query()
  ├→ Append to JSONL log
  ↓
Display Answer + Sources
```

### Example 4: Document Ingestion

```
User Uploads PDFs
  ↓
DocumentProcessor.process_file()
  ├→ Extract text (pdfplumber/pytesseract)
  ├→ Calculate file hash (SHA256)
  ├→ Chunk text (1000 chars, 200 overlap)
  ↓
RAGSystem.add_documents()
  ├→ Generate embeddings (sentence-transformers)
  ├→ Store in ChromaDB with metadata
  ├→ Persist to disk
  ↓
Documents Indexed
```

## Performance Considerations

### Document Processing
- **Batch size**: 10 documents at a time
- **Chunk size**: 1000 characters (configurable)
- **OCR**: Slower for scanned PDFs (use Tesseract)
- **Expected speed**: ~10-50 pages/minute

### Embedding Generation
- **Model**: all-MiniLM-L6-v2 (fast, 384 dimensions)
- **Speed**: ~100-500 sentences/second (CPU)
- **Alternative**: all-mpnet-base-v2 (slower, better quality)

### Vector Search
- **ChromaDB**: Efficient for <1M documents
- **Search speed**: <100ms for typical queries
- **Scalability**: Suitable for thousands of books

### LLM Generation
- **Ollama**: Depends on hardware
- **llama3.2 (3B)**: ~10-50 tokens/second (CPU)
- **Recommended**: 16GB RAM, modern CPU
- **GPU**: Significantly faster (CUDA support)

### Astrology Calculations
- **Swiss Ephemeris**: Very fast (<10ms per chart)
- **Bottleneck**: Geocoding (first time only)
- **Cached**: Location data reused

## Security & Privacy

### Data Privacy
✅ **100% Local**: No cloud services
✅ **No API Calls**: LLM runs locally (Ollama)
✅ **File-Based**: All data in user-controlled files
✅ **Portable**: Easy to backup and transfer
✅ **Transparent**: JSON files are human-readable

### Potential Concerns
⚠️ **Local Storage**: Data not encrypted at rest
⚠️ **Ollama Models**: Downloaded from internet (once)
⚠️ **Geocoding**: Requires internet (geopy)

### Recommendations
- Keep `data/` folder secure
- Regular backups
- Use disk encryption if needed
- Firewall rules for Ollama (optional)

## Extensibility

### Adding New Features

**1. More Divisional Charts (D9, D10, etc.)**
```python
# In vedic_calculator.py
def calculate_divisional_chart(self, birth_chart, division):
    # D9 = longitude * 9 % 360
    # D10 = longitude * 10 % 360
    pass
```

**2. Transit Predictions**
```python
def calculate_transits(self, birth_chart, transit_date):
    # Calculate current planet positions
    # Compare with natal positions
    # Generate predictions
    pass
```

**3. Compatibility Analysis**
```python
def calculate_compatibility(self, chart1, chart2):
    # Gun Milan (Ashtakoot)
    # Kuja Dosha check
    # Dasha compatibility
    pass
```

**4. Additional LLM Providers**
```python
# In rag.py
class RAGSystem:
    def generate_answer_gpt4all(self, ...):
        # Alternative to Ollama
        pass
```

**5. Mobile App**
- React Native frontend
- Connect to FastAPI backend
- Same Python core modules
- REST API endpoints

## Troubleshooting Guide

### Common Issues

**1. Ollama Not Detected**
- Check: `ollama --version`
- Fix: Install from https://ollama.ai
- Pull model: `ollama pull llama3.2`

**2. Swiss Ephemeris Errors**
- First run downloads ephemeris data
- Requires internet connection
- Data cached for future use

**3. OCR Failures**
- Install Tesseract: https://github.com/tesseract-ocr/tesseract
- Set TESSERACT_CMD in .env
- Use text-based PDFs when possible

**4. Out of Memory**
- Reduce batch_size in config
- Use smaller embedding model
- Close other applications
- Use smaller LLM model

**5. Slow Performance**
- GPU acceleration for Ollama
- Smaller chunk_size for documents
- Reduce top_k in RAG config
- Use faster embedding model

## Future Roadmap

### Phase 1: Core Functionality (Current)
✅ Document ingestion
✅ Vedic chart calculations
✅ RAG-based Q&A
✅ User profiles
✅ Remedies
✅ Streamlit UI

### Phase 2: Enhanced Features
- [ ] More divisional charts (D9, D10, D12, D30)
- [ ] Transit analysis and predictions
- [ ] Compatibility (synastry) analysis
- [ ] Muhurta (electional astrology)
- [ ] Prashna (horary) astrology

### Phase 3: UI Improvements
- [ ] Chart visualization (graphical)
- [ ] Interactive ephemeris
- [ ] Dasha timeline visualization
- [ ] PDF report generation
- [ ] Export/import profiles

### Phase 4: Mobile & Desktop
- [ ] React Native mobile app (iOS/Android)
- [ ] Electron desktop app (Windows/Mac/Linux)
- [ ] FastAPI backend server
- [ ] REST API documentation

### Phase 5: Advanced AI
- [ ] Fine-tuned models on astrology texts
- [ ] Multi-language support (Hindi, Sanskrit)
- [ ] Voice input/output
- [ ] Personalized learning from user feedback

## Contributing

Contributions welcome! Areas of interest:
- More astrological calculations
- Additional remedy databases
- UI/UX improvements
- Performance optimizations
- Documentation
- Testing

## License

MIT License - See LICENSE file

---

**Built with ❤️ for Vedic Astrology enthusiasts**
