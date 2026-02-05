"""
Test the RAG system with a sample query
This requires Ollama to be running
"""
import sys
from src.rag_system import RAGSystem
from src.utils import logger

print("=" * 60)
print("RAG System Test")
print("=" * 60)
print()

# Initialize RAG system
print("Initializing RAG system...")
try:
    rag = RAGSystem()
    print("✓ RAG system initialized")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print()

# Check Ollama status
print("Checking Ollama status...")
ollama_ok = rag.check_ollama_status()

if not ollama_ok:
    print("✗ Ollama is not running or model not found")
    print()
    print("Please:")
    print("1. Install Ollama from https://ollama.ai")
    print("2. Run: ollama pull llama3.2")
    print("3. Make sure Ollama is running")
    sys.exit(1)

print("✓ Ollama is running and model is available")
print()

# Check vector DB
stats = rag.get_collection_stats()
print(f"Vector DB status:")
print(f"  - Total documents: {stats['total_documents']}")
print(f"  - Collection: {stats['collection_name']}")
print()

if stats['total_documents'] == 0:
    print("Note: No documents in vector database yet.")
    print("You can still test the LLM, but search results will be empty.")
    print()
    
    # Add a sample document for testing
    print("Adding a sample document for testing...")
    
    sample_text = """
    Mars is the planet of energy, action, and desire. In Vedic astrology, Mars (Mangal) 
    is considered a natural malefic but can bestow courage, strength, and determination 
    when well-placed. Mars rules Aries and Scorpio and is exalted in Capricorn. 
    When Mars is in the 7th house, it can create Mangal Dosha (Kuja Dosha), which 
    traditionally affects marriage. However, this placement also gives a passionate 
    and energetic approach to relationships.
    """
    
    rag.add_documents(
        texts=[sample_text],
        metadatas=[{'source': 'test_document', 'type': 'sample'}],
        ids=['test_001']
    )
    
    print("✓ Sample document added")
    print()

# Test query
test_query = "What does Mars in the 7th house signify?"
print(f"Test Query: {test_query}")
print()

print("Processing query...")
print("(This may take 10-30 seconds depending on your hardware)")
print()

try:
    result = rag.ask(test_query)
    
    print("=" * 60)
    print("QUERY RESULT")
    print("=" * 60)
    print()
    
    print(f"Query: {result['query']}")
    print()
    
    print("Answer:")
    print("-" * 60)
    print(result['answer'])
    print("-" * 60)
    print()
    
    print(f"Sources used: {result['num_sources']}")
    
    if result['sources']:
        print()
        print("Source snippets:")
        for i, source in enumerate(result['sources'][:2], 1):
            print(f"\n{i}. From: {source['metadata'].get('source', 'Unknown')}")
            print(f"   {source['text'][:150]}...")
    
    print()
    print("=" * 60)
    print("✓ RAG system test completed successfully!")
    print("=" * 60)
    print()
    print("The RAG system is working correctly and can:")
    print("  - Search for relevant context in the knowledge base")
    print("  - Generate answers using the local LLM (Ollama)")
    print("  - Combine multiple sources for comprehensive answers")
    print()

except Exception as e:
    print(f"✗ Error during query: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
