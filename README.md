# AstroKnowledge - Vedic Astrology AI Assistant

A privacy-focused, local-first Vedic astrology application that combines ancient wisdom from thousands of books with AI-powered insights.

## Features

- 📚 **Document Ingestion**: Process thousands of astrology books (PDF, DOCX, TXT, images)
- 🔮 **Vedic Astrology Engine**: Birth charts, Dashas, Transits, Compatibility
- 🤖 **AI-Powered Q&A**: RAG-based system with local LLM (no cloud APIs)
- 🏥 **Remedies**: Context-aware astrological remedies
- 👨‍👩‍👧‍👦 **Family Profiles**: Manage multiple family member profiles
- 🔒 **100% Private**: All data stays on your device

## Technology Stack

- **Backend**: Python 3.10+
- **Document Processing**: unstructured, pdfplumber, python-docx, pytesseract
- **Vector Database**: ChromaDB (local)
- **Embeddings**: sentence-transformers (local models)
- **LLM**: Ollama (Llama 3.2, Mistral, etc.)
- **Astrology**: pyswisseph + custom Vedic engine
- **Storage**: File-based (JSON/JSONL)
- **UI**: Streamlit (prototype), React Native (mobile - future)

## Quick Start

### Prerequisites

1. **Python 3.10+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
   ```bash
   # After installing Ollama, pull a model:
   ollama pull llama3.2
   ```

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AstroKnowledge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Vedic astrology ephemeris data (automatic on first run)
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Project Structure

```
AstroKnowledge/
├── app.py                          # Main Streamlit application
├── config/
│   └── config.yaml                 # Application configuration
├── src/
│   ├── document_processor/         # PDF/DOCX/Image processing
│   ├── astrology_engine/           # Vedic calculations
│   ├── rag_system/                 # RAG & LLM integration
│   ├── user_manager/               # Profile & history management
│   └── remedy_engine/              # Remedy suggestions
├── data/
│   ├── books/                      # Your astrology books (raw)
│   ├── vector_db/                  # ChromaDB storage
│   └── user_data/                  # User profiles & history
└── tests/                          # Unit tests
```

## Usage

### 1. Ingest Astrology Books

1. Place your books in `data/books/` folder
2. Go to "📚 Document Management" in the app
3. Click "Process All Books"

### 2. Create User Profile

1. Go to "👤 User Profile"
2. Enter birth details (date, time, place)
3. Add family members if needed

### 3. Generate Horoscope

1. Go to "🔮 Horoscope"
2. Select user/family member
3. View birth chart, dashas, transits

### 4. Ask Questions

1. Go to "💬 Ask Question"
2. Type your question
3. Get AI-powered answers based on books + chart analysis

### 5. Get Remedies

1. Based on chart analysis
2. Contextual remedies from book knowledge

## Configuration

Edit `config/config.yaml` to customize:

- LLM model selection
- Embedding model
- Chunk size for documents
- Ayanamsa (Lahiri, Raman, KP, etc.)
- Language preferences

## Data Privacy

- ✅ All data stored locally in `data/` folder
- ✅ No cloud API calls (100% local LLM)
- ✅ Easy backup: just copy the `data/` folder
- ✅ Portable across devices

## Future Enhancements

- [ ] React Native mobile app
- [ ] Electron desktop app
- [ ] More divisional charts (D-9, D-10, etc.)
- [ ] Muhurta calculations
- [ ] Prashna (Horary) astrology
- [ ] Multi-language support (Hindi, Sanskrit)

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please open an issue or PR.
