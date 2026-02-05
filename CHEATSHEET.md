# AstroKnowledge - Command Cheatsheet

Quick reference for common operations and commands.

## Setup & Installation

### Initial Setup
```bash
# Windows
.\setup.ps1

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install Ollama model
ollama pull llama3.2
```

## Running the Application

### Start Application
```bash
# Activate virtual environment first!
streamlit run app.py

# With custom port
streamlit run app.py --server.port 8502

# With debug logging
streamlit run app.py --logger.level=debug
```

### Stop Application
- Press `Ctrl+C` in terminal
- Close browser tab
- Deactivate environment: `deactivate`

## Testing

### Verify Installation
```bash
python test_installation.py
```

### Test Astrology Engine
```bash
python test_chart_calculation.py
```

### Test RAG System
```bash
python test_rag_system.py
```

### Run All Tests
```bash
pytest tests/
```

## Ollama Commands

### Check Status
```bash
ollama --version
ollama list
```

### Manage Models
```bash
# Pull model
ollama pull llama3.2

# Alternative models
ollama pull mistral
ollama pull llama2

# Remove model
ollama rm llama3.2

# Show model info
ollama show llama3.2
```

### Test Ollama Directly
```bash
# Interactive chat
ollama run llama3.2

# Single query
ollama run llama3.2 "What is Vedic astrology?"
```

## File Operations

### Backup User Data
```bash
# Windows
tar -czf backup_%date:~10,4%%date:~4,2%%date:~7,2%.tar.gz data\user_data

# Linux/Mac
tar -czf backup_$(date +%Y%m%d).tar.gz data/user_data

# Just profiles
tar -czf profiles_backup.tar.gz data/user_data/profiles
```

### Restore User Data
```bash
tar -xzf backup_YYYYMMDD.tar.gz
```

### Clear Vector Database (reset books)
```bash
# Windows
rmdir /s data\vector_db
mkdir data\vector_db

# Linux/Mac
rm -rf data/vector_db
mkdir -p data/vector_db
```

### Clear User Data (fresh start)
```bash
# Backup first!
rm -rf data/user_data/*
mkdir -p data/user_data/{profiles,charts,history}
```

## Configuration

### Edit Config
```bash
# Windows
notepad config\config.yaml

# Linux/Mac
nano config/config.yaml
vim config/config.yaml
```

### Common Config Changes

**Change LLM Model:**
```yaml
llm:
  model: "mistral"  # Change from llama3.2
```

**Change Ayanamsa:**
```yaml
astrology:
  ayanamsa: "RAMAN"  # Change from LAHIRI
```

**Increase Search Results:**
```yaml
rag:
  top_k: 10  # Increase from 5
```

**Adjust Chunk Size:**
```yaml
documents:
  chunk_size: 1500  # Increase from 1000
  chunk_overlap: 300  # Increase from 200
```

## Environment Variables

### Create .env File
```bash
# Copy example
cp .env.example .env

# Edit
notepad .env      # Windows
nano .env         # Linux/Mac
```

### Common Variables
```bash
# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Tesseract (for OCR)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows
TESSERACT_CMD=/usr/bin/tesseract  # Linux/Mac

# Data directories (optional)
DATA_DIR=./data
BOOKS_DIR=./data/books
```

## Document Management

### Add Books via Folder
```bash
# Copy books to directory
cp ~/Documents/astrology_books/*.pdf data/books/

# Then in app: Document Management → Process Books from folder
```

### Supported File Types
```
.pdf    - PDF documents
.docx   - Word documents
.txt    - Text files
.png    - Images (OCR)
.jpg    - Images (OCR)
.jpeg   - Images (OCR)
```

### Organize Books
```bash
# Recommended structure
data/books/
├── classics/
│   ├── brihat_parashara_hora.pdf
│   └── jataka_parijata.pdf
├── modern/
│   ├── planets_in_houses.pdf
│   └── nakshatra_guide.pdf
└── reference/
    └── ephemeris_tables.pdf
```

## User Management

### Manual Profile Creation (JSON)
```json
// data/user_data/profiles/example.json
{
  "user_id": "example",
  "name": "Example User",
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

### View Query History
```bash
# View recent queries
cat data/user_data/history/queries_202512.jsonl | tail -10

# Search for specific query
grep "Mars" data/user_data/history/queries_202512.jsonl
```

## Python Package Management

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Add New Package
```bash
# Install
pip install package-name

# Add to requirements
pip freeze > requirements.txt
```

### Check Installed Packages
```bash
pip list
pip show streamlit
```

## Logs

### View Logs
```bash
# View latest log
cat logs/app_$(date +%Y%m%d).log

# Tail logs (live)
tail -f logs/app_$(date +%Y%m%d).log

# Search logs
grep "ERROR" logs/*.log
```

### Clear Logs
```bash
rm logs/*.log
```

## Troubleshooting

### Ollama Issues
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart Ollama (Windows)
# Close Ollama from system tray → Restart

# Restart Ollama (Linux)
systemctl restart ollama
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502

# Find process using port 8501 (Windows)
netstat -ano | findstr :8501

# Kill process (Windows)
taskkill /PID <PID> /F

# Find process (Linux/Mac)
lsof -i :8501

# Kill process (Linux/Mac)
kill -9 <PID>
```

### Virtual Environment Issues
```bash
# Deactivate
deactivate

# Remove venv
rm -rf venv

# Recreate
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Package Installation Fails
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose
pip install -r requirements.txt -v

# Install individually
pip install streamlit
pip install pyswisseph
# etc.
```

## Performance Optimization

### Speed Up LLM
```bash
# Use smaller model
ollama pull llama3.2:3b  # Smaller, faster

# GPU acceleration (if available)
# Ollama automatically uses GPU if CUDA available
```

### Reduce Memory Usage
```yaml
# In config.yaml
documents:
  batch_size: 5  # Reduce from 10
  chunk_size: 500  # Reduce from 1000

embeddings:
  device: "cpu"  # Ensure CPU mode
```

### Speed Up Search
```yaml
rag:
  top_k: 3  # Reduce from 5
```

## Development

### Enable Debug Mode
```python
# In config.yaml
logging:
  level: "DEBUG"
```

### Watch for Changes
```bash
# Streamlit auto-reloads on file changes
# Just edit and save - browser refreshes automatically
```

### Create New Module
```bash
# Create directory
mkdir src/new_module

# Create files
touch src/new_module/__init__.py
touch src/new_module/main.py
```

## Git Operations (if using Git)

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit"
```

### Daily Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# View history
git log --oneline
```

### Branching
```bash
# Create feature branch
git checkout -b feature/new-feature

# Switch back to main
git checkout main

# Merge feature
git merge feature/new-feature
```

## Export & Import

### Export Profile
```bash
# Copy profile
cp data/user_data/profiles/john_doe.json ~/backup/

# Export with charts
cp -r data/user_data/charts/john_doe ~/backup/
```

### Import Profile
```bash
# Copy profile
cp ~/backup/john_doe.json data/user_data/profiles/

# Copy charts
cp -r ~/backup/john_doe data/user_data/charts/
```

## System Information

### Check Python Version
```bash
python --version
python -c "import sys; print(sys.version)"
```

### Check Package Versions
```bash
pip show streamlit
pip show pyswisseph
pip show chromadb
```

### System Resources
```bash
# Windows
wmic cpu get loadpercentage
wmic OS get FreePhysicalMemory

# Linux/Mac
top
htop
free -h
```

## Quick Reference

### Project Structure
```
AstroKnowledge/
├── app.py              # Run this
├── config/             # Configuration
├── src/                # Source code
├── data/               # All data
│   ├── books/          # Your books
│   ├── vector_db/      # Indexed books
│   └── user_data/      # Profiles & charts
└── logs/               # Application logs
```

### Important URLs
- **App**: http://localhost:8501
- **Ollama API**: http://localhost:11434
- **Ollama Website**: https://ollama.ai
- **Swiss Ephemeris**: https://www.astro.com/swisseph/

### Important Commands
```bash
# Start app
streamlit run app.py

# Test installation
python test_installation.py

# Pull LLM model
ollama pull llama3.2

# Backup data
tar -czf backup.tar.gz data/user_data

# View logs
tail -f logs/app_*.log
```

## Getting Help

1. **Check logs**: `logs/app_YYYYMMDD.log`
2. **Run tests**: `python test_installation.py`
3. **Read docs**: `README.md`, `QUICKSTART.md`
4. **Check config**: `config/config.yaml`
5. **Verify Ollama**: `ollama list`

---

**💡 Tip**: Bookmark this file for quick reference!
