"""
Knowledge Search Module for Mobile
Simple search in knowledge base
"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simple_rag.simple_search import SimpleKnowledgeBase

def search(query):
    """
    Search knowledge base
    
    Args:
        query: Search query string
    
    Returns:
        JSON string with search results
    """
    try:
        kb = SimpleKnowledgeBase()
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
