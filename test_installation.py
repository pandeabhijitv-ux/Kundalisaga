"""
Test script to verify the installation and core functionality
Run this after setup to ensure everything is working
"""
import sys
from pathlib import Path

print("=" * 60)
print("AstroKnowledge - Installation Verification")
print("=" * 60)
print()

# Test 1: Python version
print("✓ Testing Python version...")
assert sys.version_info >= (3, 10), "Python 3.10+ required"
print(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Test 2: Import core modules
print("✓ Testing core modules...")
try:
    from src.utils import config, logger
    print("  - Utils: OK")
    
    from src.document_processor import DocumentProcessor
    print("  - Document Processor: OK")
    
    from src.astrology_engine import VedicAstrologyEngine
    print("  - Astrology Engine: OK")
    
    from src.rag_system import RAGSystem
    print("  - RAG System: OK")
    
    from src.user_manager import UserManager
    print("  - User Manager: OK")
    
    from src.remedy_engine import RemedyEngine
    print("  - Remedy Engine: OK")
    
except ImportError as e:
    print(f"  ERROR: {e}")
    print("\n  Please run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 3: Configuration
print("✓ Testing configuration...")
try:
    llm_model = config.get('llm.model')
    print(f"  - LLM Model: {llm_model}")
    
    ayanamsa = config.get('astrology.ayanamsa')
    print(f"  - Ayanamsa: {ayanamsa}")
    
except Exception as e:
    print(f"  ERROR: {e}")
    sys.exit(1)

print()

# Test 4: Directory structure
print("✓ Testing directory structure...")
required_dirs = [
    'data/books',
    'data/vector_db',
    'data/user_data/profiles',
    'data/user_data/charts',
    'data/user_data/history',
    'logs'
]

for dir_path in required_dirs:
    path = Path(dir_path)
    if path.exists():
        print(f"  - {dir_path}: OK")
    else:
        print(f"  - {dir_path}: Creating...")
        path.mkdir(parents=True, exist_ok=True)

print()

# Test 5: Swiss Ephemeris
print("✓ Testing Swiss Ephemeris...")
try:
    import swisseph as swe
    swe.set_ephe_path(None)
    
    # Test calculation
    jd = swe.julday(2000, 1, 1, 12.0)
    result = swe.calc_ut(jd, swe.SUN)
    
    print(f"  - Swiss Ephemeris: OK")
    print(f"  - Sun position on 2000-01-01: {result[0][0]:.2f}°")
    
except Exception as e:
    print(f"  WARNING: {e}")
    print("  Swiss Ephemeris may need to download data on first use")

print()

# Test 6: Sentence Transformers
print("✓ Testing Sentence Transformers (may take a moment)...")
try:
    from sentence_transformers import SentenceTransformer
    
    model_name = config.get('embeddings.model')
    print(f"  - Loading model: {model_name}")
    
    model = SentenceTransformer(model_name)
    
    # Test embedding
    test_text = "This is a test sentence."
    embedding = model.encode([test_text])
    
    print(f"  - Embedding dimension: {len(embedding[0])}")
    print(f"  - Sentence Transformers: OK")
    
except Exception as e:
    print(f"  ERROR: {e}")
    print("  Embeddings may not work properly")

print()

# Test 7: ChromaDB
print("✓ Testing ChromaDB...")
try:
    import chromadb
    from chromadb.config import Settings
    
    # Create a test client
    client = chromadb.Client(Settings(
        anonymized_telemetry=False
    ))
    
    print(f"  - ChromaDB: OK")
    
except Exception as e:
    print(f"  ERROR: {e}")

print()

# Test 8: Ollama connection
print("✓ Testing Ollama connection...")
try:
    import requests
    
    ollama_host = config.get('llm.host', 'http://localhost:11434')
    
    response = requests.get(f"{ollama_host}/api/tags", timeout=5)
    
    if response.status_code == 200:
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        
        print(f"  - Ollama: Running")
        print(f"  - Available models: {', '.join(model_names)}")
        
        expected_model = config.get('llm.model')
        if expected_model in model_names:
            print(f"  - Required model '{expected_model}': Found ✓")
        else:
            print(f"  - Required model '{expected_model}': NOT FOUND")
            print(f"    Run: ollama pull {expected_model}")
    else:
        print(f"  - Ollama: ERROR (status {response.status_code})")
    
except Exception as e:
    print(f"  - Ollama: NOT RUNNING")
    print(f"    Make sure Ollama is installed and running")
    print(f"    Download from: https://ollama.ai")

print()

# Test 9: Streamlit
print("✓ Testing Streamlit...")
try:
    import streamlit
    print(f"  - Streamlit version: {streamlit.__version__}")
    
except ImportError:
    print(f"  ERROR: Streamlit not installed")

print()

# Summary
print("=" * 60)
print("Verification Complete!")
print("=" * 60)
print()
print("Next steps:")
print("1. Make sure Ollama is running with llama3.2 model")
print("2. Place your astrology books in: data/books/")
print("3. Run the application:")
print()
print("   streamlit run app.py")
print()
print("=" * 60)
