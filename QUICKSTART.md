# AstroKnowledge - Quick Start Guide

## Installation

### Windows

1. **Open PowerShell** (Run as Administrator if needed)

2. **Navigate to the project folder:**
   ```powershell
   cd C:\AstroKnowledge
   ```

3. **Run the setup script:**
   ```powershell
   .\setup.ps1
   ```

   If you get an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Linux/Mac

1. **Open Terminal**

2. **Navigate to the project folder:**
   ```bash
   cd /path/to/AstroKnowledge
   ```

3. **Make setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

4. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

## Manual Installation (if scripts fail)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama:**
   - Download from https://ollama.ai
   - Install and run: `ollama pull llama3.2`

## Running the Application

1. **Make sure Ollama is running**

2. **Activate virtual environment** (if not already activated):
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Start the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to http://localhost:8501

## First Steps

### 1. Create Your Profile

1. Go to **"👤 User Profiles"** → **"Create New Profile"**
2. Fill in your birth details:
   - Name
   - Birth date and time
   - Birth place (city, country)
3. Click **"Create Profile"**

### 2. Add Astrology Books

**Option A: Upload through UI**
1. Go to **"📚 Document Management"**
2. Upload your PDF/DOCX books
3. Click **"Process Uploaded Files"**

**Option B: Place in folder**
1. Copy your books to `data/books/` folder
2. Go to **"📚 Document Management"**
3. Click **"Process Books from data/books/ folder"**

This will take some time depending on the number and size of books.

### 3. Generate Your Horoscope

1. Go to **"🔮 Horoscope"**
2. Select your profile
3. Click **"Calculate Birth Chart"**
4. View your detailed Vedic chart with planetary positions, nakshatras, and dashas

### 4. Ask Questions

1. Go to **"💬 Ask Question"**
2. Optionally check **"Include my birth chart in analysis"**
3. Type your question (e.g., "What does Mars in 7th house signify?")
4. Click **"Get Answer"**

The AI will search your book collection and provide an answer based on Vedic astrology texts.

### 5. Get Remedies

1. Go to **"🏥 Remedies"**
2. Select your profile
3. Optionally specify a concern (e.g., "career", "health")
4. Click **"Get Remedies"**
5. View personalized remedies including mantras, gemstones, charities, and practices

## Adding Family Members

1. Go to **"👤 User Profiles"** → **"Create New Profile"**
2. Select relationship (Spouse, Child, Parent, etc.)
3. Enter their birth details
4. You can now calculate charts and get answers for any family member

## Troubleshooting

### Ollama Not Detected

**Issue:** "❌ Ollama not detected" in sidebar

**Solution:**
1. Make sure Ollama is installed: https://ollama.ai
2. Start Ollama (it should run automatically)
3. Pull the model: `ollama pull llama3.2`
4. Refresh the Streamlit app

### Location Not Found

**Issue:** "Could not find location" when creating profile

**Solution:**
- Try different formats:
  - "New Delhi, India"
  - "Mumbai, Maharashtra, India"
  - "Los Angeles, California, USA"
- Be specific with city and country

### Documents Not Processing

**Issue:** Books upload but don't get indexed

**Solution:**
1. Check file format is supported (PDF, DOCX, TXT, images)
2. For scanned PDFs, make sure Tesseract OCR is installed
3. Check logs in `logs/` folder for errors

### Swiss Ephemeris Data

**Issue:** Astrology calculations fail

**Solution:**
- The first time you calculate a chart, Swiss Ephemeris will download required data
- This is automatic and only happens once
- Make sure you have internet connection for first chart calculation

## Configuration

Edit `config/config.yaml` to customize:

- **LLM Model:** Change `llm.model` to use different Ollama models
- **Ayanamsa:** Change `astrology.ayanamsa` (LAHIRI, RAMAN, KP)
- **Chunk Size:** Adjust `documents.chunk_size` for better/worse context
- **Top K Results:** Change `rag.top_k` for more/fewer search results

## Data Backup

All your data is in the `data/` folder:

- **User profiles:** `data/user_data/profiles/`
- **Charts:** `data/user_data/charts/`
- **Query history:** `data/user_data/history/`
- **Book embeddings:** `data/vector_db/`

To backup: Simply copy the entire `data/` folder

## Tips for Best Results

1. **Book Quality:** Use high-quality scanned PDFs or text-based PDFs
2. **Specific Questions:** Ask specific questions for better answers
3. **Include Charts:** When asking questions, include your chart for personalized insights
4. **Multiple Books:** More books = better knowledge base = better answers
5. **Accurate Birth Time:** Precise birth time is crucial for accurate charts

## Support

- Check `logs/` folder for detailed error messages
- Review `README.md` for full documentation
- Make sure all dependencies are installed correctly

## What's Next?

The current Streamlit app is a **prototype**. Future development includes:

- [ ] React Native mobile app (iOS/Android)
- [ ] Electron desktop app
- [ ] More divisional charts (D9, D10, etc.)
- [ ] Transit predictions
- [ ] Compatibility analysis
- [ ] Muhurta (electional astrology)
- [ ] Multi-language support (Hindi, Sanskrit)

---

Enjoy exploring Vedic astrology with AI! 🔮✨
