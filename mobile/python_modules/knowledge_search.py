"""
Knowledge Search Module for Mobile
Simple search in knowledge base
"""

import json
import sys
import os
from pathlib import Path

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from src.simple_rag.simple_search import SimpleKnowledgeBase


def _resolve_storage_path() -> Path:
    """Resolve a writable/readable knowledge-base path for mobile and local dev."""
    module_path = Path(MODULE_DIR)
    candidates = [
        module_path / "data" / "knowledge_base",  # Bundled mobile path
        module_path.parent / "data" / "knowledge_base",  # Local workspace fallback
    ]

    for path in candidates:
        if (path / "index.json").exists() or path.exists():
            return path

    # Default to bundled location.
    return candidates[0]

def search(query):
    """
    Search knowledge base
    
    Args:
        query: Search query string
    
    Returns:
        JSON string with search results
    """
    try:
        kb = SimpleKnowledgeBase(str(_resolve_storage_path()))
        results = kb.search(query, top_k=5)
        
        formatted_results = {
            'query': query,
            'results': []
        }
        
        for result in results:
            formatted_results['results'].append({
                'text': result.get('text', ''),
                'score': result.get('score', 0),
                'source': result.get('source', 'Unknown')
            })
        
        return json.dumps(formatted_results)
        
    except Exception as e:
        return json.dumps({'error': str(e), 'results': []})


if __name__ == '__main__':
    print(search('What is ascendant?'))
