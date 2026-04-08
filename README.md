# KundaliSaga - Vedic Astrology AI Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy Policy](https://img.shields.io/badge/Privacy-Local%20First-green)](PRIVACY_POLICY.md)
[![Google Play](https://img.shields.io/badge/Google%20Play-Coming%20Soon-blue)]()

A privacy-focused, local-first Vedic astrology application that combines ancient wisdom with AI-powered insights. Available as **web app** (Streamlit) and **mobile app** (Android).

## 🌟 Why KundaliSaga?

- **🔒 100% Private**: All data stays on YOUR device - no cloud APIs, no tracking
- **📱 Cross-Platform**: Web app + Native Android mobile app
- **🤖 AI-Powered**: Local LLM (Ollama) for intelligent interpretations
- **📚 Knowledge-Rich**: RAG system with astrology knowledge base
- **🔮 Complete Vedic System**: Swiss Ephemeris for accurate calculations
- **💰 Affordable**: One-time payment, no subscriptions

## ✨ Features

### Core Astrology
- 📊 **Birth Chart Analysis**: Complete Vedic horoscope (D-1, D-9, and more)
- 🌙 **Dasha Systems**: Vimshottari, Yogini, Ashtottari with predictions
- 🌍 **Transit Analysis**: Current planetary positions and effects
- 💑 **Compatibility**: Relationship compatibility analysis
- 🔢 **Numerology**: Life path, destiny, and lucky numbers

### AI & Knowledge
- 💬 **Ask Questions**: AI-powered Q&A about your chart
- 🏥 **Remedies**: Personalized mantras, gemstones, and rituals
- 📖 **Knowledge Base**: Searchable astrology knowledge database
- 🧠 **Context-Aware**: Answers based on YOUR birth chart

### User Management
- 👨‍👩‍👧‍👦 **Family Profiles**: Manage multiple family member charts
- 📜 **History**: Track all your queries and insights
- 💳 **Credits System**: Simple credit-based payment (UPI)
- 🌐 **Multi-Language**: English, Hindi, Marathi support

## 🛠 Technology Stack

### Backend
- **Python 3.10+**: Core application logic
- **pyswisseph**: Swiss Ephemeris for Vedic calculations
- **Ollama**: Local LLM (Llama 3.2, Mistral)
- **ChromaDB**: Local vector database
- **sentence-transformers**: Local embeddings

### Frontend
- **Streamlit**: Web application UI
- **React Native**: Mobile app (Android)
- **Chaquopy**: Python-Java bridge for mobile

### Storage
- **File-based**: JSON/JSONL (no external database needed)
- **Local Vector DB**: ChromaDB for semantic search
- **Portable**: Easy backup - just copy the data folder!

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2. **Ollama**: [Install Ollama](https://ollama.ai)
   ```bash
   # After installing Ollama, pull a model:
   ollama pull llama3.2
   ```

### Installation (Web App)

```bash
# Clone the repository
git clone https://github.com/pandeabhijitv-ux/kundalisaga.git
cd kundalisaga

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Web App

```bash
# Make sure Ollama is running (in another terminal):
ollama serve

# A📁 Project Structure

```
KundaliSaga/
├── app.py                          # Main Streamlit application (7800+ lines)
├── config/
│   └── config.yaml                 # Application configuration
├── src/
│   ├── astrology_engine/           # Vedic calculations (Swiss Ephemeris wrapper)
│   ├── rag_system/                 # RAG & LLM integration (ChromaDB)
│   ├── simple_rag/                 # Fallback text search
│   ├── user_manager/               # Profile & history management
│   ├── auth/                       # Email OTP, password authentication
│   ├── payment/                    # Credit system, UPI payments
│   ├── remedy_engine/              # Remedy suggestions
│   ├── numerology/                 # Numerology calculations
│   ├── career_guidance/            # Career analysis
│   └── financial_astrology/        # Financial predictions
├── data/
│   ├── users/                      # User accounts (JSON)
│  📱 Usage

### 1. Create Account
- Email + Password OR Email OTP authentication
- Secure bcrypt password hashing
- Session management

### 2. Create Profile
1. Go to "👤 Manage Profiles"
2. Add your birth details (date, time, place)
3. Add family members if needed

### 3. Generate Birth Chart
1. Go to "📊 Birth Chart"
2. Select profile
3. View planetary positions, houses, aspects

### 4. Check Dasha Periods
1. Go to "🌙 Dasha Analysis"
2. See current and upcoming planetary periods
3. Get predictions for each period

### 5. Ask AI Questions
1. Go to "💬 Ask Me Anything"
2. Type your question (e.g., "When will I get married?")
3. Get AI-powered answers based on your chart

### 6. Get Remedies
1. Go to "🏥 Remedies"
2. Select weak/afflicted planet
3. Get mantras, gemstones, rituals, and donation suggestions
⚙️ Configuration

Edit `config/config.yaml` to customize:

### Astrology Settings
- **Ayanamsa**: Lahiri (default), Raman, KP, etc.
- **House System**: Whole Sign (default), Placidus, Equal
- **Dasha Systems**: Vimshottari, Yogini, Ashtottari

### LLM Settings
- **Model**: llama3.2, mistral, etc.
- **Provider**: ollama (local)
- **Temperature**: 0.7 (default)

### Payment Settings
- **Pricing**: 10 INR per feature
- **UPI ID**: Configure your payment details
- **Coupon Codes**: Add promotional codes

### Language
- English (default)
- Hindi (हिंदी)
- Marathi (मराठी)

## 🔒 Privacy & Security

**KundaliSaga is built with privacy at its core.**

- ✅ **No Cloud APIs**: All processing happens locally
- ✅ **No Tracking**: Zero analytics or telemetry
- ✅ **No Data Sharing**: Your data never leaves your device
- ✅ **Open Source**: Verify our privacy claims in code
- ✅ **Encrypted Passwords**: bcrypt hashing with salt
- ✅ **Session Security**: Secure token-based sessions

📄 **Full Privacy Policy**: [PRIVACY_POLICY.md](PRIVACY_POLICY.md)

## 📊 Data Storage

All🎯 Roadmap

### Completed ✅
- [x] Web app (Streamlit)
- [x] Android mobile app (React Native + Chaquopy)
- [x] Birth chart calculations (Swiss Ephemeris)
- [x] Dasha analysis (Vimshottari, Yogini, Ashtottari)
- [x] AI-powered Q&A (RAG + Ollama)
- [x] Remedies system
- [x] Numerology integration
- [x] User authentication (Email OTP + Password)
- [x] Credit-based payment system (UPI)
- [x] Multi-language support (EN/HI/MR)

### In Progress 🚧
- [ ] Google Play Store submission
- [ ] iOS app (React Native)

### Planned 📅
- [ ] More divisional charts (D-2, D-3, D-4, etc.)
- [ ] Muhurta (auspicious timing) calculations
- [ ] Prashna (Horary) astrology
- [ ] Advanced transit predictions
- [ ] Varshaphal (annual predictions)
- [ ] Match-making with more algorithms
- [ ] AI-powered chart interpretation improvements
- [ ] Offline LLM models bundled in mobile app

## 📜 License

MIT License - See [LICENSE](LICENSE) file

Copyright © 2026 Krittika Apps

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact & Support

- **GitHub**: [pandeabhijitv-ux/kundalisaga](https://github.com/pandeabhijitv-ux/kundalisaga)
- **Issues**: [Report bugs or request features](https://github.com/pandeabhijitv-ux/kundalisaga/issues)
- **Email**: support@kundalisaga.com

## 🙏 Acknowledgments

- **Swiss Ephemeris**: High-precision astronomical calculations
- **Ollama**: Making local LLM accessible
- **ChromaDB**: Excellent local vector database
- **Streamlit**: Rapid prototyping framework
- **React Native**: Cross-platform mobile development
- **Chaquopy**: Python-Android integration

---

**Made with ❤️ by Krittika Apps**  
*Sharp. Supreme. Protective.*

[![Star on GitHub](https://img.shields.io/github/stars/pandeabhijitv-ux/kundalisaga?style=social)](https://github.com/pandeabhijitv-ux/kundalisaga)

**Backup**: Simply copy the entire `data/` folder to backup all user data."

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
