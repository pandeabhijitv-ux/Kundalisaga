"""
RAG (Retrieval-Augmented Generation) System
Combines vector search with local LLM for Q&A
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import requests
import json

from src.utils import logger, config


class RAGSystem:
    """RAG system for astrology knowledge Q&A"""
    
    def __init__(self):
        self.logger = logger
        
        # Initialize embedding model
        embedding_model_name = config.get('embeddings.model')
        self.logger.info(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Initialize ChromaDB
        persist_dir = config.get('vector_db.persist_directory')
        self.logger.info(f"Initializing ChromaDB at: {persist_dir}")
        
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
        
        collection_name = config.get('vector_db.collection_name', 'astrology_books')
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name
            )
            self.logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"description": "Astrology books knowledge base"}
            )
            self.logger.info(f"Created new collection: {collection_name}")
        
        # Ollama configuration
        self.ollama_host = config.get('llm.host', 'http://localhost:11434')
        self.ollama_model = config.get('llm.model', 'llama3.2')
        self.temperature = config.get('llm.temperature', 0.7)
        self.max_tokens = config.get('llm.max_tokens', 2000)
    
    def add_documents(self, texts: List[str], metadatas: List[Dict],
                     ids: List[str]) -> None:
        """
        Add documents to vector database
        
        Args:
            texts: List of text chunks
            metadatas: List of metadata dicts
            ids: List of unique IDs
        """
        self.logger.info(f"Adding {len(texts)} documents to vector DB")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Add to ChromaDB in batches
        batch_size = config.get('documents.batch_size', 10)
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            self.collection.add(
                documents=batch_texts,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        
        self.logger.info("Documents added successfully")
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant documents with metadata
        """
        if top_k is None:
            top_k = config.get('rag.top_k', 5)
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        documents = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                documents.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return documents
    
    def generate_answer(self, query: str, context: str, 
                       chart_context: Optional[str] = None) -> str:
        """
        Generate answer using Ollama LLM
        
        Args:
            query: User's question
            context: Retrieved context from documents
            chart_context: Optional birth chart context
        
        Returns:
            Generated answer
        """
        # Build prompt
        system_prompt = """You are an expert Vedic astrologer with deep knowledge of ancient texts and modern interpretations. 
Your role is to provide accurate, insightful answers based on the provided astrological texts and chart information.

Guidelines:
- Base your answers on the provided context from astrology books
- If chart information is provided, integrate it into your interpretation
- Provide practical, actionable insights
- Mention relevant Sanskrit terms when appropriate
- Be respectful of the ancient wisdom while being accessible
- If you don't have enough information, acknowledge it honestly
"""
        
        user_prompt = f"""Context from Astrology Books:
{context}

"""
        
        if chart_context:
            user_prompt += f"""Birth Chart Information:
{chart_context}

"""
        
        user_prompt += f"""Question: {query}

Please provide a comprehensive answer based on the above context and chart information (if provided)."""
        
        # Call Ollama API
        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return "Error: Unable to generate response from LLM"
        
        except Exception as e:
            self.logger.error(f"Error calling Ollama: {str(e)}")
            return f"Error: {str(e)}"
    
    def ask(self, query: str, chart_context: Optional[str] = None) -> Dict:
        """
        Complete RAG pipeline: search + generate
        
        Args:
            query: User's question
            chart_context: Optional birth chart information
        
        Returns:
            Dict with answer and sources
        """
        self.logger.info(f"Processing query: {query}")
        
        # Search for relevant context
        relevant_docs = self.search(query)
        
        # Combine context
        context = "\n\n---\n\n".join([doc['text'] for doc in relevant_docs])
        
        # Generate answer
        answer = self.generate_answer(query, context, chart_context)
        
        return {
            'query': query,
            'answer': answer,
            'sources': relevant_docs,
            'num_sources': len(relevant_docs)
        }
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }
    
    def check_ollama_status(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.ollama_model in model_names:
                    self.logger.info(f"Ollama is running with model: {self.ollama_model}")
                    return True
                else:
                    self.logger.warning(f"Model {self.ollama_model} not found. Available: {model_names}")
                    return False
            
            return False
        
        except Exception as e:
            self.logger.error(f"Ollama not accessible: {str(e)}")
            return False
