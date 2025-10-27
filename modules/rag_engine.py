"""
RAG Engine - Handles semantic search and answer generation for medical Q&A
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import google.generativeai as genai

console = Console()


class RAGEngine:
    """Retrieval-Augmented Generation engine for medical Q&A."""
    
    def __init__(self, collection_name: str, persist_directory: str, api_key: str, model_name: str):
        """
        Initialize the RAG engine.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the vector database
            api_key: Google API key for Gemini
            model_name: Gemini model name
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
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
    
    def add_documents(self, chunks: List[Dict]) -> None:
        """
        Add document chunks to the vector database.
        
        Args:
            chunks: List of document chunks with text and metadata
        """
        if not chunks:
            console.print("⚠️  No chunks to add", style="yellow")
            return
        
        console.print(f"\n📥 Adding {len(chunks)} chunks to vector database...", style="cyan")
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for chunk in chunks:
            ids.append(chunk['id'])
            documents.append(chunk['text'])
            metadatas.append(chunk.get('metadata', {}))
        
        # Add to collection in batches (ChromaDB has size limits)
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i+batch_size]
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            
            self.collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_meta
            )
        
        console.print(f"  ✓ Added {len(chunks)} chunks successfully", style="green")
        console.print(f"  📊 Total documents in collection: {self.collection.count()}", style="cyan")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Perform semantic search on the vector database.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of relevant document chunks with metadata
        """
        if self.collection.count() == 0:
            console.print("⚠️  No documents in vector database. Please add documents first.", style="yellow")
            return []
        
        # Query the collection
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return formatted_results
    
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
        prompt = f"""You are a medical education assistant specializing in stroke awareness.

Answer the following question using ONLY the information from the provided medical documents.

IMPORTANT RULES:
1. Use ONLY information from the provided sources
2. Cite sources using [1], [2], etc. format inline
3. Be clear, accurate, and compassionate
4. If the information is not in the sources, say "I don't have information about this in the provided documents"
5. Never provide medical diagnosis or treatment advice
6. Encourage consulting healthcare professionals for personal medical concerns

SOURCES:
{context}

QUESTION: {query}

ANSWER: """
        
        try:
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,
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
            console.print(f"✗ Error generating answer: {e}", style="red")
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
