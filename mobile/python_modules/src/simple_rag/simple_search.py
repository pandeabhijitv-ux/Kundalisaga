"""
Simple text-based search system (no ChromaDB dependency)
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
import re
from datetime import datetime


class SimpleKnowledgeBase:
    """Simple text-based knowledge base for astrology books"""
    
    def __init__(self, storage_path: str = "data/knowledge_base"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_path / "index.json"
        self.chunks_dir = self.storage_path / "chunks"
        self.chunks_dir.mkdir(exist_ok=True)
        
    def add_document(self, text: str, metadata: Dict) -> bool:
        """Add a document to the knowledge base"""
        try:
            # Split into chunks
            chunks = self._chunk_text(text, chunk_size=1000, overlap=200)
            
            # Create document ID
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save chunks
            doc_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                chunk_data = {
                    'id': chunk_id,
                    'text': chunk,
                    'metadata': metadata,
                    'chunk_index': i
                }
                doc_chunks.append(chunk_data)
                
                # Save chunk to file
                chunk_file = self.chunks_dir / f"{chunk_id}.json"
                with open(chunk_file, 'w', encoding='utf-8') as f:
                    json.dump(chunk_data, f, ensure_ascii=False, indent=2)
            
            # Update index
            self._update_index(doc_id, metadata, len(chunks))
            
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant chunks using keyword matching"""
        try:
            # Get all chunk files
            chunk_files = list(self.chunks_dir.glob("*.json"))
            
            # Score each chunk
            results = []
            query_terms = query.lower().split()
            
            for chunk_file in chunk_files:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunk_data = json.load(f)
                
                # Calculate simple relevance score
                text_lower = chunk_data['text'].lower()
                score = sum(text_lower.count(term) for term in query_terms)
                
                if score > 0:
                    results.append({
                        'text': chunk_data['text'],
                        'metadata': chunk_data['metadata'],
                        'score': score
                    })
            
            # Sort by score and return top_k
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:top_k]
            
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
                return {
                    'total_documents': len(index.get('documents', [])),
                    'total_chunks': sum(d.get('num_chunks', 0) for d in index.get('documents', []))
                }
            return {'total_documents': 0, 'total_chunks': 0}
        except:
            return {'total_documents': 0, 'total_chunks': 0}
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < text_length:
                # Look for sentence end
                chunk_text = text[start:end]
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:  # Only break if we're past halfway
                    end = start + break_point + 1
            
            chunks.append(text[start:end].strip())
            start = end - overlap
        
        return chunks
    
    def _update_index(self, doc_id: str, metadata: Dict, num_chunks: int):
        """Update the document index"""
        try:
            # Load existing index
            if self.index_file.exists():
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            else:
                index = {'documents': []}
            
            # Add new document
            index['documents'].append({
                'id': doc_id,
                'metadata': metadata,
                'num_chunks': num_chunks,
                'added_at': datetime.now().isoformat()
            })
            
            # Save index
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error updating index: {e}")


def generate_answer(query: str, context_chunks: List[Dict]) -> str:
    """Generate interpretive predictions from classical texts"""
    if not context_chunks:
        return "I couldn't find relevant information in the knowledge base to answer your question."
    
    # Check if the text is garbled/corrupted
    def is_garbled(text: str) -> bool:
        """Check if text contains too many special characters (corrupted encoding)"""
        import re
        if not text or len(text) < 20:
            return True
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = len(text.replace('\n', '').replace(' ', ''))
        return total_chars > 0 and (english_chars / total_chars) < 0.4
    
    # Filter out garbled chunks
    clean_chunks = [c for c in context_chunks if not is_garbled(c['text'])]
    
    if not clean_chunks:
        return """⚠️ **Text Encoding Issue Detected**

The astrology books in the knowledge base contain text encoding issues (likely Hindi/Sanskrit text that wasn't properly converted).

**Recommendations:**
1. Upload English language astrology books (e.g., "Light on Life" by Hart de Fouw, "Astrology of the Seers" by David Frawley)
2. Or provide properly encoded/OCR'd PDFs of classical texts
3. Currently, the built-in interpretations are available through the chart predictions

For now, please use the **Chart Interpretation** feature which has 108 built-in planetary combinations programmed from classical Vedic principles."""
    
    # Try to find actual prediction/interpretation sentences (not just combinations)
    predictions = []
    
    for chunk in clean_chunks[:5]:  # Check top 5 chunks
        text = chunk['text']
        
        # Look for sentences that contain interpretive keywords
        interpretive_keywords = [
            'indicates', 'suggests', 'brings', 'causes', 'gives', 'makes',
            'will', 'may', 'should', 'can', 'native', 'person', 'individual',
            'success', 'failure', 'gain', 'loss', 'good', 'bad', 'fortune',
            'wealth', 'health', 'career', 'marriage', 'happiness', 'sorrow',
            'prosperity', 'difficulty', 'challenge', 'opportunity', 'blessed',
            'suffers', 'enjoys', 'experiences', 'achieves', 'attains'
        ]
        
        # Split into sentences
        sentences = re.split(r'[.;!?\n]+', text)
        
        for sent in sentences:
            sent = sent.strip()
            
            # Must be substantial length
            if len(sent) < 30:
                continue
            
            # Check if it's an actual interpretation (not just a combination)
            if any(keyword in sent.lower() for keyword in interpretive_keywords):
                # This looks like a real prediction!
                sent_clean = sent[0].upper() + sent[1:] if sent else sent
                if not sent_clean.endswith(('.', '!', '?')):
                    sent_clean += '.'
                predictions.append(sent_clean)
                
                if len(predictions) >= 3:
                    break
        
        if len(predictions) >= 3:
            break
    
    # If we found good predictions, return them
    if predictions:
        answer = ""
        for i, pred in enumerate(predictions[:3]):
            if i == 0:
                answer += f"{pred}\n\n"
            else:
                answer += f"• {pred}\n\n"
        return answer.strip()
    
    # Fallback: No real predictions found, just show reference text
    # This means the books are giving combinations, not interpretations
    return "📚 **Classical Reference Found:**\n\nThe classical texts describe this planetary combination but don't provide a direct interpretation. The combination mentioned is:\n\n" + clean_chunks[0]['text'][:200] + "...\n\n*Note: These are technical references from classical texts. For detailed predictions, consider consulting with an astrologer who can interpret these combinations in context of your full chart.*"
    
    # Fallback: Create a generic interpretation
    # Look for planet and house mentions
    planets_found = []
    houses_found = []
    
    for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
        if planet in cleaned_text:
            planets_found.append(planet)
    
    for i in range(1, 13):
        if f" {i} " in cleaned_text or f"house {i}" in cleaned_text:
            houses_found.append(str(i))
    
    if planets_found and houses_found:
        answer = f"According to the classical texts, the placement of {', '.join(planets_found[:3])} "
        answer += f"in houses {', '.join(houses_found[:3])} has significant astrological implications. "
        answer += "This combination influences the native's life in various ways according to Vedic astrology principles."
        return answer
    
    # Last resort: return cleaned excerpt
    excerpt = cleaned_text[:400].strip()
    if excerpt:
        return excerpt + "..."
    
    return "The astrological texts indicate specific planetary combinations for this placement. Consult the source texts for detailed interpretation."

