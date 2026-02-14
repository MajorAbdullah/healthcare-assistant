"""
Embedding Generator - Handles text to vector conversion using Google Gemini API
"""

import google.generativeai as genai
from typing import List, Optional
import time
from rich.console import Console

console = Console()


class EmbeddingGenerator:
    """Generate embeddings using Google Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "models/gemini-embedding-001"):
        """
        Initialize the embedding generator.
        
        Args:
            api_key: Google API key for Gemini
            model_name: Name of the embedding model to use
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.embedding_model = genai
        
    def generate_embedding(self, text: str, retry_count: int = 3) -> Optional[List[float]]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            retry_count: Number of retries on failure
            
        Returns:
            Embedding vector as list of floats, or None on failure
        """
        if not text or not text.strip():
            console.print("⚠️  Empty text provided for embedding", style="yellow")
            return None
        
        for attempt in range(retry_count):
            try:
                result = genai.embed_content(
                    model=self.model_name,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
                
            except Exception as e:
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    console.print(
                        f"⚠️  Embedding attempt {attempt + 1} failed, retrying in {wait_time}s...",
                        style="yellow"
                    )
                    time.sleep(wait_time)
                else:
                    console.print(f"❌ Failed to generate embedding: {e}", style="red")
                    return None
        
        return None
    
    def generate_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with batching.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process at once
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            console.print("⚠️  No texts provided for embedding", style="yellow")
            return []
        
        embeddings = []
        total_texts = len(texts)
        
        # Process in batches
        for i in range(0, total_texts, batch_size):
            batch = texts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_texts + batch_size - 1) // batch_size
            
            console.print(
                f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} texts)...",
                style="cyan"
            )
            
            # Generate embeddings for this batch
            for j, text in enumerate(batch):
                embedding = self.generate_embedding(text)
                
                if embedding:
                    embeddings.append(embedding)
                else:
                    # Add a zero vector as fallback to maintain alignment
                    console.print(
                        f"⚠️  Using zero vector for text {i+j+1} due to embedding failure",
                        style="yellow"
                    )
                    # Use a default dimension size (768 for Gemini)
                    embeddings.append([0.0] * 3072)
                
                # Rate limiting: small delay between requests
                if j < len(batch) - 1:  # Don't sleep after last item
                    time.sleep(0.1)
            
            # Delay between batches
            if i + batch_size < total_texts:
                time.sleep(1)
        
        console.print(
            f"✅ Generated {len(embeddings)}/{total_texts} embeddings",
            style="green"
        )
        
        return embeddings
    
    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Embedding vector or None on failure
        """
        if not query or not query.strip():
            console.print("⚠️  Empty query provided", style="yellow")
            return None
        
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"  # Different task type for queries
            )
            return result['embedding']
            
        except Exception as e:
            console.print(f"❌ Failed to generate query embedding: {e}", style="red")
            return None


# Convenience function for quick embedding generation
def embed_text(text: str, api_key: str) -> Optional[List[float]]:
    """
    Quick function to embed a single text.
    
    Args:
        text: Text to embed
        api_key: Google API key
        
    Returns:
        Embedding vector or None
    """
    generator = EmbeddingGenerator(api_key)
    return generator.generate_embedding(text)


def embed_texts(texts: List[str], api_key: str, batch_size: int = 100) -> List[List[float]]:
    """
    Quick function to embed multiple texts.
    
    Args:
        texts: List of texts to embed
        api_key: Google API key
        batch_size: Batch processing size
        
    Returns:
        List of embedding vectors
    """
    generator = EmbeddingGenerator(api_key)
    return generator.generate_batch(texts, batch_size)
