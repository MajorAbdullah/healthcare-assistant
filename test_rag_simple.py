#!/usr/bin/env python3
"""
Simple RAG test using local embeddings (sentence-transformers)
This avoids API rate limits and is faster for testing
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.document_processor import DocumentProcessor
from rich.console import Console
from rich.panel import Panel
import chromadb
from sentence_transformers import SentenceTransformer

console = Console()

def test_simple_rag():
    """Test basic RAG functionality with local embeddings"""
    
    console.print("\n[bold cyan]🧪 Simple RAG Test (Local Embeddings)[/bold cyan]\n")
    
    # Initialize
    console.print("[yellow]Loading embedding model (this may take a moment)...[/yellow]")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast model
    console.print("[green]✓ Model loaded[/green]\n")
    
    # Initialize ChromaDB
    console.print("[yellow]Initializing vector database...[/yellow]")
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(
        name="test_medical_docs",
        metadata={"description": "Test medical documents"}
    )
    console.print("[green]✓ Vector DB ready[/green]\n")
    
    # Process documents
    console.print("[bold]Processing Medical Documents[/bold]")
    doc_processor = DocumentProcessor(chunk_size=300, chunk_overlap=30)
    doc_dir = Path("data/medical_docs")
    
    all_chunks = []
    for doc_file in doc_dir.glob("*.txt"):
        console.print(f"  📄 {doc_file.name}")
        text = doc_processor.load_text_file(str(doc_file))
        chunks = doc_processor.chunk_text(text, source_name=doc_file.stem)
        chunks_with_metadata = doc_processor.add_metadata(
            chunks,
            source=doc_file.stem.replace('_', ' ').title()
        )
        all_chunks.extend(chunks_with_metadata)
    
    console.print(f"\n[green]✓ Created {len(all_chunks)} chunks[/green]\n")
    
    # Generate embeddings and add to ChromaDB
    console.print("[yellow]Generating embeddings...[/yellow]")
    texts = [chunk['text'] for chunk in all_chunks]
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    
    # Add to collection
    collection.add(
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{
            'source': chunk['source'],
            'chunk_id': str(i)
        } for i, chunk in enumerate(all_chunks)],
        ids=[f"chunk_{i}" for i in range(len(all_chunks))]
    )
    
    console.print(f"[green]✓ Added {len(all_chunks)} chunks to vector database[/green]\n")
    
    # Test queries
    console.print("[bold]Testing Semantic Search[/bold]\n")
    
    test_questions = [
        "What are the symptoms of a stroke?",
        "How can I prevent stroke?",
        "What does F.A.S.T. stand for?",
        "What are the risk factors for stroke?",
    ]
    
    for question in test_questions:
        console.print(f"[cyan]Q:[/cyan] {question}")
        
        # Embed question
        question_embedding = embedding_model.encode([question])[0]
        
        # Search
        results = collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=3
        )
        
        # Display results
        console.print("[green]Top 3 relevant chunks:[/green]")
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
            source = metadata['source']
            preview = doc[:150] + "..." if len(doc) > 150 else doc
            console.print(f"  {i}. [yellow]{source}[/yellow]")
            console.print(f"     {preview}\n")
    
    # Summary
    console.print(Panel(
        "[bold green]✅ RAG System Working![/bold green]\n\n"
        "The system successfully:\n"
        "  • Loaded medical documents\n"
        "  • Chunked text appropriately\n"
        "  • Generated embeddings\n"
        "  • Stored in vector database\n"
        "  • Performed semantic search\n\n"
        "[dim]Next step: Integrate with Gemini for answer generation[/dim]",
        title="Test Summary",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        test_simple_rag()
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
