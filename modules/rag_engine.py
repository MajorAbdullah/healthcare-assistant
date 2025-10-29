"""
RAG Engine - Handles semantic search and answer generation for medical Q&A
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import google.generativeai as genai
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.embeddings import EmbeddingGenerator

console = Console()


class RAGEngine:
    """Retrieval-Augmented Generation engine for medical Q&A."""
    
    def __init__(self, collection_name: str, persist_directory: str, api_key: str, model_name: str, system_prompt: str = None):
        """
        Initialize the RAG engine.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the vector database
            api_key: Google API key for Gemini
            model_name: Gemini model name
            system_prompt: System prompt for answer generation (optional)
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.system_prompt = system_prompt or "You are a helpful medical education assistant."
        
        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(api_key=api_key)
        
        # Initialize ChromaDB
        console.print("🔍 Initializing vector database...", style="cyan")
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )
        
        try:
            self.collection = self.client.get_collection(name=collection_name)
            console.print(f"  ✓ Loaded existing collection: {collection_name}", style="green")
            console.print(f"  📊 Documents in collection: {self.collection.count()}", style="cyan")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Medical documents about stroke"}
            )
            console.print(f"  ✓ Created new collection: {collection_name}", style="green")
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Add document chunks to the vector database.
        
        Args:
            chunks: List of document chunks with text and metadata
        """
        if not chunks:
            print("⚠️  No chunks to add")
            return
        
        print(f"� Processing {len(chunks)} chunks...")
        
        # Extract texts and prepare data for ChromaDB
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk.get('metadata', {}) for chunk in chunks]
        ids = [f"chunk_{i}_{chunk.get('metadata', {}).get('source', 'unknown')}" 
               for i, chunk in enumerate(chunks)]
        
        # Generate embeddings using our custom embedding generator
        print("🔄 Generating embeddings...")
        embeddings = self.embedding_generator.generate_batch(texts)
        
        if not embeddings:
            print("❌ Failed to generate embeddings")
            return
        
        # Add to ChromaDB
        print("💾 Storing in vector database...")
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Successfully added {len(chunks)} chunks to vector database")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks using semantic similarity.
        
        Args:
            query: The search query
            n_results: Number of results to return
            
        Returns:
            List of relevant chunks with metadata and scores
        """
        if not query.strip():
            print("⚠️  Empty query")
            return []
        
        # Generate embedding for the query
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        if not query_embedding:
            print("❌ Failed to generate query embedding")
            return []
        
        # Search in ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            chunks = []
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    chunk = {
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'id': results['ids'][0][i] if results['ids'] else None
                    }
                    chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def format_context(self, search_results: List[Dict]) -> tuple:
        """
        Format search results into context for LLM.
        
        Args:
            search_results: Results from semantic search
            
        Returns:
            Tuple of (context_text, sources_list)
        """
        context_parts = []
        sources = []
        
        for i, result in enumerate(search_results, 1):
            text = result['text']
            metadata = result['metadata']
            source_name = metadata.get('source', 'Unknown')
            
            # Add to context
            context_parts.append(f"[Source {i}] {source_name}\n{text}\n")
            
            # Track unique sources
            source_info = {
                'id': i,
                'name': source_name,
                'type': metadata.get('doc_type', 'Document'),
                'author': metadata.get('author', ''),
                'url': metadata.get('url', '')
            }
            sources.append(source_info)
        
        context_text = "\n\n".join(context_parts)
        return context_text, sources
    
    def generate_answer(self, query: str, context: str, sources: List[Dict]) -> Dict:
        """
        Generate answer using Gemini with retrieved context.
        
        Args:
            query: User's question
            context: Retrieved context from vector search
            sources: List of source documents
            
        Returns:
            Dictionary with answer and citations
        """
        # Build prompt
        prompt = f"""You are an intelligent and friendly medical assistant named HealthBot. You help patients with medical questions, appointment scheduling, and general health information.

YOUR CAPABILITIES:
- Answer medical questions using verified medical sources
- Provide health education and wellness tips
- Help with symptom understanding (not diagnosis)
- Guide users on when to seek medical care
- Be conversational, empathetic, and helpful
- Remember this is a healthcare appointment system

CONVERSATION GUIDELINES:
1. For greetings ("hi", "hello"): Respond warmly and ask how you can help with their health concerns
2. For general help requests: Explain what you can do (answer medical questions, help book appointments, provide health info)
3. For medical questions: Use the provided sources and cite them with [1], [2] format
4. For personal medical concerns: Always recommend consulting their doctor
5. For emergencies: Immediately tell them to call emergency services (911)
6. Be conversational and natural - don't just say "I don't have information"

IMPORTANT SAFETY RULES:
⚠️ Never diagnose conditions or prescribe medications
⚠️ Always encourage professional medical consultation for serious concerns
⚠️ For emergencies, tell them to call 911 immediately
⚠️ Be clear about the difference between general information and medical advice

MEDICAL KNOWLEDGE BASE:
{context}

USER MESSAGE: {query}

YOUR RESPONSE (be natural, helpful, and conversational): """
        
        try:
            # Generate response with slightly higher temperature for natural conversation
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,  # Increased from 0.1 for more natural, conversational responses
                    'max_output_tokens': 1024,
                }
            )
            
            answer_text = response.text
            
            # Format sources for citation
            citations = []
            for source in sources:
                citation = f"[{source['id']}] {source['name']}"
                if source['author']:
                    citation += f" by {source['author']}"
                if source['type']:
                    citation += f" ({source['type']})"
                citations.append(citation)
            
            return {
                'answer': answer_text,
                'citations': citations,
                'sources': sources
            }
            
        except Exception as e:
            Console().print(f"✗ Error generating answer: {e}", style="red")
            return {
                'answer': "I apologize, but I encountered an error generating the answer. Please try again.",
                'citations': [],
                'sources': []
            }
    
    def query(self, question: str, n_results: int = 5, verbose: bool = False) -> Dict:
        """
        Complete RAG pipeline: Search + Generate answer.
        
        Args:
            question: User's question
            n_results: Number of chunks to retrieve
            verbose: Whether to print detailed info
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        console = Console()
        
        if verbose:
            console.print(f"\n❓ Question: {question}", style="bold cyan")
            console.print("🔍 Searching medical documents...", style="cyan")
        
        # 1. Semantic search
        search_results = self.search(question, n_results)
        
        if not search_results:
            return {
                'answer': "I don't have any medical documents to answer this question. Please add medical documents first.",
                'citations': [],
                'sources': [],
                'search_results': []
            }
        
        if verbose:
            console.print(f"  ✓ Found {len(search_results)} relevant passages", style="green")
        
        # 2. Format context
        context, sources = self.format_context(search_results)
        
        if verbose:
            console.print("🤖 Generating answer with AI...", style="cyan")
        
        # 3. Generate answer
        result = self.generate_answer(question, context, sources)
        result['search_results'] = search_results
        
        return result
    
    def display_answer(self, result: Dict) -> None:
        """
        Display answer in a beautiful format.
        
        Args:
            result: Result dictionary from query()
        """
        console = Console()
        
        # Display answer
        answer_panel = Panel(
            result['answer'],
            title="💡 Answer",
            border_style="green",
            padding=(1, 2)
        )
        console.print(answer_panel)
        
        # Display citations
        if result['citations']:
            console.print("\n📚 Sources:", style="bold cyan")
            for citation in result['citations']:
                console.print(f"  {citation}", style="dim")
    
    def clear_collection(self) -> None:
        """Delete all documents from the collection."""
        console = Console()
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Medical documents about stroke"}
            )
            console.print("✓ Collection cleared", style="green")
        except Exception as e:
            console.print(f"✗ Error clearing collection: {e}", style="red")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector database."""
        return {
            'collection_name': self.collection_name,
            'total_documents': self.collection.count(),
            'persist_directory': str(self.persist_directory)
        }


def build_index_from_docs(docs_directory: str, rag_engine: RAGEngine) -> None:
    """
    Helper function to build the vector index from a directory of documents.
    
    Args:
        docs_directory: Path to directory containing medical documents
        rag_engine: RAG engine instance
    """
    from utils.document_processor import DocumentProcessor
    
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    chunks = processor.process_directory(docs_directory)
    
    if chunks:
        rag_engine.add_documents(chunks)
        console.print("\n✓ Vector index built successfully!", style="bold green")
    else:
        console.print("\n⚠️  No documents found to index", style="yellow")


if __name__ == "__main__":
    # Test the RAG engine
    from config import (
        CHROMA_COLLECTION_NAME,
        VECTOR_DB_DIR,
        GOOGLE_API_KEY,
        LLM_MODEL,
        MEDICAL_DOCS_DIR
    )
    
    # Initialize RAG engine
    rag = RAGEngine(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=str(VECTOR_DB_DIR),
        api_key=GOOGLE_API_KEY,
        model_name=LLM_MODEL
    )
    
    # Check if we need to build the index
    stats = rag.get_stats()
    console.print(f"\n📊 Vector Database Stats:", style="bold")
    console.print(f"  Collection: {stats['collection_name']}")
    console.print(f"  Documents: {stats['total_documents']}")
    console.print(f"  Location: {stats['persist_directory']}")
    
    if stats['total_documents'] == 0:
        console.print("\n⚠️  No documents in database. Building index...", style="yellow")
        build_index_from_docs(str(MEDICAL_DOCS_DIR), rag)
    
    # Test query
    if rag.collection.count() > 0:
        console.print("\n" + "="*70, style="bold")
        console.print("🧪 Testing RAG System", style="bold cyan")
        console.print("="*70 + "\n", style="bold")
        
        test_question = "What is a stroke?"
        result = rag.query(test_question, verbose=True)
        console.print()
        rag.display_answer(result)
    else:
        console.print("\n⚠️  Add medical documents to data/medical_docs/ to test", style="yellow")
