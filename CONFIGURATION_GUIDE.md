# AstroKnowledge - Configuration Guide
## Complete Configuration Reference

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Configuration File](#configuration-file)
3. [Application Settings](#application-settings)
4. [Astrology Settings](#astrology-settings)
5. [Document Processing](#document-processing)
6. [Email Configuration](#email-configuration)
7. [AI/LLM Settings](#aillm-settings)
8. [Payment Configuration](#payment-configuration)
9. [RAG System](#rag-system)
10. [Storage Settings](#storage-settings)
11. [Advanced Configuration](#advanced-configuration)

---

## 🌟 Overview

The main configuration file is located at: `config/config.yaml`

This YAML file controls all aspects of the AstroKnowledge application, from astrology calculations to payment processing.

### Configuration Hierarchy
```
config/
├── config.yaml          # Main configuration file
└── (optional) .env      # Environment variables for sensitive data
```

---

## 📄 Configuration File

**Location**: `config/config.yaml`

### File Structure
The configuration is organized into logical sections:
- `app` - Application metadata
- `astrology` - Vedic astrology calculation settings
- `documents` - Document processing parameters
- `email` - Email service configuration
- `embeddings` - AI embeddings model settings
- `llm` - Language model configuration
- `logging` - Logging preferences
- `payment` - Payment and credits system
- `rag` - Retrieval Augmented Generation settings
- `storage` - Data storage configuration
- `vector_db` - Vector database settings

---

## 🎯 Application Settings

```yaml
app:
  language: en              # Application language (en, hi, etc.)
  name: KundaliSaga         # Application display name
  theme: light              # UI theme (light/dark)
  version: 1.0.0            # Application version
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | string | `en` | Interface language. Currently supports English (`en`) |
| `name` | string | `KundaliSaga` | Brand name displayed in the application |
| `theme` | string | `light` | UI color theme. Options: `light`, `dark` |
| `version` | string | `1.0.0` | Application version number |

### Usage
- Change `name` to customize branding
- Set `theme: dark` for dark mode interface
- Update `version` when releasing new features

---

## 🔮 Astrology Settings

```yaml
astrology:
  ayanamsa: LAHIRI                    # Ayanamsa system
  dasha_systems:                      # Dasha calculation methods
    - VIMSHOTTARI
    - YOGINI
    - ASHTOTTARI
  default_location:                   # Default birth location
    latitude: 28.6139                 # Delhi coordinates
    longitude: 77.209
    timezone: Asia/Kolkata
  divisional_charts:                  # Supported divisional charts
    - D1                              # Birth Chart
    - D9                              # Navamsa
    - D10                             # Dasamsa (Career)
    - D12                             # Dwadasamsa
    - D30                             # Trimshamsha
  house_system: WHOLE_SIGN            # House calculation system
```

### Parameters Explained

#### `ayanamsa`
**Type**: string  
**Default**: `LAHIRI`  
**Options**: `LAHIRI`, `RAMAN`, `KRISHNAMURTI`, `YUKTESHWAR`

The Ayanamsa defines the zodiacal starting point. Lahiri (Chitrapaksha) is most commonly used in Indian Vedic astrology.

- **LAHIRI**: Most popular in India, officially adopted
- **RAMAN**: Used by B.V. Raman school
- **KRISHNAMURTI**: KP system ayanamsa
- **YUKTESHWAR**: Sri Yukteshwar's calculation

#### `dasha_systems`
**Type**: list  
**Default**: `[VIMSHOTTARI, YOGINI, ASHTOTTARI]`

Dasha systems predict planetary periods and timing of events:
- **VIMSHOTTARI**: 120-year cycle, most widely used
- **YOGINI**: 36-year cycle, used for women's charts
- **ASHTOTTARI**: 108-year cycle, alternative system

#### `default_location`
**Type**: object  
Default location for charts when user doesn't specify:
- `latitude`: Decimal degrees (-90 to 90)
- `longitude`: Decimal degrees (-180 to 180)
- `timezone`: IANA timezone identifier

**Example**:
```yaml
default_location:
  latitude: 19.0760    # Mumbai
  longitude: 72.8777
  timezone: Asia/Kolkata
```

#### `divisional_charts`
**Type**: list  
Divisional charts (Vargas) for detailed analysis:

| Chart | Name | Focus Area |
|-------|------|------------|
| D1 | Rasi | Main birth chart |
| D9 | Navamsa | Marriage, spirituality |
| D10 | Dasamsa | Career, profession |
| D12 | Dwadasamsa | Parents, family |
| D30 | Trimshamsha | Misfortunes, evils |
| D7 | Saptamsa | Children |
| D2 | Hora | Wealth |
| D3 | Drekkana | Siblings |
| D4 | Chaturthamsa | Assets, property |
| D16 | Shodasamsa | Vehicles, comforts |
| D20 | Vimsamsa | Spiritual progress |
| D24 | Chaturvimsamsa | Education |
| D27 | Bhamsa | Strengths/weaknesses |
| D40 | Khavedamsa | Auspicious/inauspicious |
| D45 | Akshavedamsa | General character |
| D60 | Shashtiamsa | Karmic influences |

Add or remove from the list as needed.

#### `house_system`
**Type**: string  
**Default**: `WHOLE_SIGN`  
**Options**: `WHOLE_SIGN`, `PLACIDUS`, `KOCH`, `EQUAL`, `PORPHYRY`

Determines how houses are calculated:
- **WHOLE_SIGN**: Traditional Vedic method (30° per house)
- **PLACIDUS**: Most common Western system
- **EQUAL**: Equal 30° houses from Ascendant
- **KOCH**: Birthplace system
- **PORPHYRY**: Divides quadrants equally

---

## 📚 Document Processing

```yaml
documents:
  batch_size: 10                      # Documents per batch
  chunk_overlap: 200                  # Overlap between chunks (chars)
  chunk_size: 1000                    # Size of each chunk (chars)
  supported_formats:                  # Accepted file formats
    - .pdf
    - .docx
    - .doc
    - .txt
    - .png
    - .jpg
    - .jpeg
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `batch_size` | integer | 10 | Number of documents processed simultaneously |
| `chunk_overlap` | integer | 200 | Character overlap between consecutive chunks |
| `chunk_size` | integer | 1000 | Characters per document chunk |
| `supported_formats` | list | [various] | Accepted file extensions for upload |

### Performance Tuning

**For faster processing** (more RAM required):
```yaml
batch_size: 20
chunk_size: 1500
```

**For lower memory systems**:
```yaml
batch_size: 5
chunk_size: 500
```

**For better context** (AI responses):
```yaml
chunk_size: 1500
chunk_overlap: 300
```

---

## 📧 Email Configuration

```yaml
email:
  enabled: false                      # Enable/disable email service
  sender_email: ''                    # Sender email address
  sender_password: ''                 # App-specific password
  smtp_port: 587                      # SMTP port
  smtp_server: smtp.gmail.com         # SMTP server address
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | false | Master switch for email functionality |
| `sender_email` | string | '' | Email address to send from |
| `sender_password` | string | '' | App password (not regular password) |
| `smtp_port` | integer | 587 | SMTP server port (587 for TLS, 465 for SSL) |
| `smtp_server` | string | smtp.gmail.com | SMTP server hostname |

### Setup Instructions

#### Gmail Configuration
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update configuration:

```yaml
email:
  enabled: true
  sender_email: 'your-email@gmail.com'
  sender_password: 'your-app-password'  # 16-character app password
  smtp_port: 587
  smtp_server: smtp.gmail.com
```

#### Other Email Providers

**Outlook/Office365**:
```yaml
smtp_server: smtp.office365.com
smtp_port: 587
```

**Yahoo**:
```yaml
smtp_server: smtp.mail.yahoo.com
smtp_port: 587
```

**Custom Domain**:
```yaml
smtp_server: mail.yourdomain.com
smtp_port: 587
sender_email: 'noreply@yourdomain.com'
```

### Security Best Practice
Store credentials in environment variables instead:

**config.yaml**:
```yaml
email:
  enabled: true
  sender_email: ${SMTP_EMAIL}
  sender_password: ${SMTP_PASSWORD}
```

**.env file**:
```
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 🤖 AI/LLM Settings

```yaml
llm:
  context_window: 8192                # Token context window
  max_tokens: 2000                    # Max response tokens
  model: llama3.2                     # Model name
  provider: ollama                    # LLM provider
  temperature: 0.7                    # Response creativity (0-1)

embeddings:
  device: cpu                         # Processing device
  model: sentence-transformers/all-MiniLM-L6-v2
```

### LLM Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | string | ollama | LLM provider (ollama, openai, anthropic) |
| `model` | string | llama3.2 | Specific model to use |
| `context_window` | integer | 8192 | Maximum context size in tokens |
| `max_tokens` | integer | 2000 | Maximum response length |
| `temperature` | float | 0.7 | Randomness (0=deterministic, 1=creative) |

### Provider-Specific Configuration

#### Ollama (Local)
```yaml
llm:
  provider: ollama
  model: llama3.2                     # or mistral, codellama, etc.
  context_window: 8192
  max_tokens: 2000
  temperature: 0.7
```

**Available Ollama Models**:
- `llama3.2` - Latest Llama 3.2
- `mistral` - Mistral 7B
- `codellama` - Code-specialized
- `gemma` - Google's Gemma
- `phi3` - Microsoft Phi-3

**Install Ollama Models**:
```bash
ollama pull llama3.2
ollama pull mistral
```

#### OpenAI (Cloud)
```yaml
llm:
  provider: openai
  model: gpt-4-turbo-preview         # or gpt-3.5-turbo
  context_window: 128000
  max_tokens: 4096
  temperature: 0.7
  api_key: ${OPENAI_API_KEY}         # Use environment variable
```

#### Anthropic Claude (Cloud)
```yaml
llm:
  provider: anthropic
  model: claude-3-opus-20240229      # or claude-3-sonnet
  context_window: 200000
  max_tokens: 4096
  temperature: 0.7
  api_key: ${ANTHROPIC_API_KEY}      # Use environment variable
```

### Embeddings Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `device` | string | cpu | Processing device (cpu, cuda, mps) |
| `model` | string | all-MiniLM-L6-v2 | Sentence transformer model |

**Device Options**:
- `cpu` - Run on CPU (slower, works everywhere)
- `cuda` - Use NVIDIA GPU (faster, requires CUDA)
- `mps` - Use Apple Silicon GPU (Mac M1/M2)

**Alternative Models**:
```yaml
embeddings:
  # Faster but less accurate
  model: sentence-transformers/all-MiniLM-L12-v2
  
  # More accurate but slower
  model: sentence-transformers/all-mpnet-base-v2
  
  # Multilingual support
  model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Temperature Guidelines

| Value | Behavior | Best For |
|-------|----------|----------|
| 0.0-0.3 | Very focused, deterministic | Facts, calculations |
| 0.4-0.6 | Balanced | General Q&A |
| 0.7-0.8 | Creative | Interpretations, advice |
| 0.9-1.0 | Very creative | Story-telling, brainstorming |

---

## 💰 Payment Configuration

```yaml
payment:
  currency: INR                       # Currency code
  enabled: false                      # Enable payment system
  pricing:
    bulk_packs:                       # Credit packages
      - price: 40
        questions: 5
      - price: 80
        questions: 10
      - price: 120
        questions: 15
    career_guidance: 20               # Cost per career analysis
    financial_astrology:              # Financial features
      enabled: true
      per_query: 50
      personalized_report: 50
      premium_packs:
        - price: 200
          queries: 5
        - price: 350
          queries: 10
        - price: 600
          queries: 20
      sector_analysis: 50
    remedy_consultation: 10           # Cost per remedy
    single_question: 10               # Cost per question
  upi_id: abhi1009.pande-1@okaxis     # UPI payment ID
  upi_name: KundaliSaga               # UPI display name
```

### Parameters Explained

#### Master Controls

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | false | Enable/disable entire payment system |
| `currency` | string | INR | Currency code (INR, USD, EUR, etc.) |
| `upi_id` | string | - | UPI ID for payments (India) |
| `upi_name` | string | - | Display name for UPI |

#### Pricing Structure

**Single Services**:
```yaml
single_question: 10          # ₹10 per astrology question
career_guidance: 20          # ₹20 per career analysis
remedy_consultation: 10      # ₹10 per remedy consultation
```

**Bulk Credit Packs**:
```yaml
bulk_packs:
  - price: 40                # ₹40 for 5 questions (₹8 each)
    questions: 5
  - price: 80                # ₹80 for 10 questions (₹8 each)
    questions: 10
  - price: 120               # ₹120 for 15 questions (₹8 each)
    questions: 15
```

**Financial Astrology Premium**:
```yaml
financial_astrology:
  enabled: true
  per_query: 50              # ₹50 per financial query
  personalized_report: 50    # ₹50 for personalized report
  sector_analysis: 50        # ₹50 per sector analysis
  premium_packs:
    - price: 200             # ₹200 for 5 queries (₹40 each)
      queries: 5
    - price: 350             # ₹350 for 10 queries (₹35 each)
      queries: 10
    - price: 600             # ₹600 for 20 queries (₹30 each)
      queries: 20
```

### Customization Examples

#### Free Tier Model
```yaml
payment:
  enabled: false             # Disable payments entirely
```

#### International Setup (USD)
```yaml
payment:
  enabled: true
  currency: USD
  pricing:
    single_question: 1       # $1 per question
    career_guidance: 3       # $3 per analysis
    bulk_packs:
      - price: 5
        questions: 5
      - price: 10
        questions: 12
```

#### Premium Model
```yaml
payment:
  enabled: true
  currency: INR
  pricing:
    single_question: 25      # Higher per-query rate
    career_guidance: 50
    financial_astrology:
      enabled: true
      per_query: 100         # Premium pricing
      personalized_report: 150
```

### Payment Flow
1. User purchases credits (via UPI/other method)
2. Credits added to user account
3. Each query deducts credits
4. Transactions logged in `data/payments/transactions.json`
5. Balance stored in `data/payments/user_credits.json`

---

## 🔍 RAG System

```yaml
rag:
  combine_chart_context: true         # Include birth chart in context
  min_relevance_score: 0.5            # Minimum similarity threshold
  top_k: 5                            # Number of relevant chunks
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `combine_chart_context` | boolean | true | Include user's chart data in AI responses |
| `min_relevance_score` | float | 0.5 | Minimum cosine similarity (0-1) |
| `top_k` | integer | 5 | Number of document chunks to retrieve |

### RAG Quality Tuning

**For more accurate responses** (retrieves more context):
```yaml
rag:
  top_k: 8
  min_relevance_score: 0.4
  combine_chart_context: true
```

**For faster responses** (less context):
```yaml
rag:
  top_k: 3
  min_relevance_score: 0.6
  combine_chart_context: false
```

**Relevance Score Guidelines**:
- `0.8-1.0`: Very relevant (strict)
- `0.6-0.8`: Relevant (balanced)
- `0.4-0.6`: Somewhat relevant (more results)
- `0.0-0.4`: Loose matching (may include noise)

---

## 💾 Storage Settings

```yaml
storage:
  backup_enabled: true                # Enable automatic backups
  backup_interval_days: 7             # Backup frequency
  base_path: ./data/user_data         # User data directory
  charts_dir: charts                  # Chart storage subdirectory
  history_dir: history                # Query history subdirectory
  profiles_dir: profiles              # User profiles subdirectory
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backup_enabled` | boolean | true | Enable automatic backups |
| `backup_interval_days` | integer | 7 | Days between automatic backups |
| `base_path` | string | ./data/user_data | Root path for user data |
| `charts_dir` | string | charts | Subdirectory for chart files |
| `history_dir` | string | history | Subdirectory for query history |
| `profiles_dir` | string | profiles | Subdirectory for user profiles |

### Storage Structure
```
data/
├── user_data/
│   ├── charts/          # User birth charts
│   ├── history/         # Query history
│   └── profiles/        # User profiles
├── payments/
│   ├── transactions.json
│   └── user_credits.json
├── users/
│   ├── users.json
│   ├── sessions.json
│   └── otp_codes.json
├── knowledge_base/      # Document chunks
│   ├── index.json
│   └── chunks/
└── vector_db/           # Vector embeddings
```

---

## 🗄️ Vector Database

```yaml
vector_db:
  collection_name: astrology_books    # Collection name
  persist_directory: ./data/vector_db # Database directory
  type: chromadb                      # Database type
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | string | chromadb | Vector DB type (chromadb, faiss, pinecone) |
| `collection_name` | string | astrology_books | Collection identifier |
| `persist_directory` | string | ./data/vector_db | Storage location |

### Advanced Vector DB Configuration

#### ChromaDB (Default - Local)
```yaml
vector_db:
  type: chromadb
  collection_name: astrology_books
  persist_directory: ./data/vector_db
```

#### Pinecone (Cloud - Scalable)
```yaml
vector_db:
  type: pinecone
  api_key: ${PINECONE_API_KEY}
  environment: us-east-1-aws
  index_name: astrology-index
  dimension: 384                      # Must match embedding model
```

---

## 📊 Logging

```yaml
logging:
  file: ./logs/app.log                # Log file location
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  level: INFO                         # Logging level
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | string | INFO | Minimum log level to record |
| `file` | string | ./logs/app.log | Log file path |
| `format` | string | (standard) | Log message format |

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| `DEBUG` | Development, troubleshooting | Variable values, function calls |
| `INFO` | Normal operations | User login, chart calculations |
| `WARNING` | Potential issues | Deprecated features, slow queries |
| `ERROR` | Errors that don't crash app | Failed calculations, API errors |
| `CRITICAL` | Severe errors | Database corruption, system failure |

**For Production**:
```yaml
logging:
  level: WARNING               # Less verbose
  file: ./logs/app.log
```

**For Development**:
```yaml
logging:
  level: DEBUG                 # Very verbose
  file: ./logs/debug.log
```

---

## 🔧 Advanced Configuration

### Environment-Specific Configs

Create separate config files:
- `config.yaml` - Default/Production
- `config.dev.yaml` - Development
- `config.test.yaml` - Testing

Load based on environment:
```python
import os
config_file = os.getenv('CONFIG_FILE', 'config.yaml')
```

### Performance Optimization

**High-Performance Setup** (16GB+ RAM):
```yaml
documents:
  batch_size: 20
  chunk_size: 2000
  
llm:
  context_window: 16384
  max_tokens: 4096
  
rag:
  top_k: 10
  
embeddings:
  device: cuda                 # Use GPU
```

**Low-Resource Setup** (4GB RAM):
```yaml
documents:
  batch_size: 3
  chunk_size: 500
  
llm:
  context_window: 4096
  max_tokens: 1000
  
rag:
  top_k: 3
  
embeddings:
  device: cpu
  model: sentence-transformers/all-MiniLM-L6-v2  # Smaller model
```

---

## 🔐 Security Considerations

### Sensitive Data
Never store these in config.yaml:
- Email passwords
- API keys
- Payment credentials
- User passwords

### Use Environment Variables
**.env file**:
```env
SMTP_PASSWORD=your-app-password
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
UPI_ID=your-upi@bank
```

**config.yaml**:
```yaml
email:
  sender_password: ${SMTP_PASSWORD}
  
llm:
  api_key: ${OPENAI_API_KEY}
```

---

## 📝 Configuration Validation

### Check Configuration
```python
# Validate configuration
python -c "
from src.utils.config_loader import load_config
config = load_config()
print('Configuration loaded successfully!')
print('Payment enabled:', config.get('payment', {}).get('enabled'))
print('LLM Provider:', config.get('llm', {}).get('provider'))
"
```

### Common Issues

**Issue**: "Configuration file not found"
```bash
# Ensure config file exists
ls -l config/config.yaml
```

**Issue**: "Invalid YAML syntax"
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

---

## 📚 Configuration Templates

### Minimal Configuration
```yaml
app:
  name: MyAstroApp
  version: 1.0.0

astrology:
  ayanamsa: LAHIRI
  house_system: WHOLE_SIGN

llm:
  provider: ollama
  model: llama3.2

payment:
  enabled: false
```

### Full Production Configuration
```yaml
# Complete production-ready configuration
app:
  language: en
  name: AstroKnowledge Pro
  theme: light
  version: 2.0.0

astrology:
  ayanamsa: LAHIRI
  dasha_systems: [VIMSHOTTARI, YOGINI]
  house_system: WHOLE_SIGN
  divisional_charts: [D1, D9, D10]
  default_location:
    latitude: 28.6139
    longitude: 77.209
    timezone: Asia/Kolkata

email:
  enabled: true
  sender_email: ${SMTP_EMAIL}
  sender_password: ${SMTP_PASSWORD}
  smtp_server: smtp.gmail.com
  smtp_port: 587

llm:
  provider: openai
  model: gpt-4-turbo-preview
  context_window: 128000
  max_tokens: 4096
  temperature: 0.7
  api_key: ${OPENAI_API_KEY}

payment:
  enabled: true
  currency: INR
  upi_id: ${UPI_ID}
  upi_name: AstroKnowledge
  pricing:
    single_question: 15
    career_guidance: 25
    
logging:
  level: WARNING
  file: ./logs/production.log
```

---

## 🔄 Configuration Changes

### Applying Changes
Most configuration changes require application restart:

```powershell
# Stop application (Ctrl+C)
# Edit config/config.yaml
# Restart application
streamlit run app.py
```

### Hot-Reloadable Settings
These can be changed without restart (Streamlit auto-reloads):
- UI theme
- Display names
- Pricing (new sessions only)

### Non-Reloadable Settings
These require full restart:
- Database connections
- LLM provider
- Email configuration
- Storage paths

---

**Last Updated**: December 21, 2025  
**Version**: 1.0.0  
**Configuration Schema Version**: 1.0
