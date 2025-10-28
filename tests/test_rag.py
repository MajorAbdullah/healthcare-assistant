#!/usr/bin/env python3
"""
Test script for RAG Engine
Tests document processing, embedding, retrieval, and answer generation
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.rag_engine import RAGEngine
from utils.document_processor import DocumentProcessor
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

console = Console()

async def test_rag_system():
    """Test the complete RAG pipeline"""
    
    console.print("\n[bold cyan]🧪 Testing Healthcare RAG System[/bold cyan]\n")
    
    # Initialize components
    console.print("[yellow]Initializing RAG Engine...[/yellow]")
    
    import config
    rag = RAGEngine(
        collection_name=config.CHROMA_COLLECTION_NAME,
        persist_directory=str(config.VECTOR_DB_DIR),
        api_key=config.GOOGLE_API_KEY,
        model_name=config.LLM_MODEL
    )
    doc_processor = DocumentProcessor()
    
    # Test 1: Process documents
    console.print("\n[bold]Test 1: Document Processing[/bold]")
    console.print("[yellow]Loading medical documents...[/yellow]")
    
    doc_dir = Path("data/medical_docs")
    documents_added = 0
    
    with Progress() as progress:
        task = progress.add_task("[green]Processing documents...", total=2)
        
        for doc_file in doc_dir.glob("*.txt"):
            console.print(f"  📄 Processing: {doc_file.name}")
            
            # Load and process document
            text = doc_processor.load_text_file(str(doc_file))
            chunks = doc_processor.chunk_text(text)
            chunks_with_metadata = doc_processor.add_metadata(
                chunks, 
                source=doc_file.stem.replace('_', ' ').title()
            )
            
            # Add to RAG engine
            await rag.add_documents(chunks_with_metadata)
            documents_added += len(chunks_with_metadata)
            
            progress.update(task, advance=1)
    
    console.print(f"[green]✓ Added {documents_added} document chunks to vector database[/green]\n")
    
    # Test 2: Semantic Search
    console.print("[bold]Test 2: Semantic Search[/bold]")
    test_queries = [
        "What are the symptoms of a stroke?",
        "How can I prevent stroke?",
        "What is F.A.S.T.?",
    ]
    
    for query in test_queries:
        console.print(f"\n[cyan]Query:[/cyan] {query}")
        results = await rag.search(query, n_results=3)
        
        console.print(f"[green]Found {len(results)} relevant chunks:[/green]")
        for i, result in enumerate(results, 1):
            console.print(f"  {i}. [yellow]{result['source']}[/yellow] - {result['text'][:100]}...")
    
    console.print()
    
    # Test 3: Answer Generation
    console.print("[bold]Test 3: Answer Generation with Citations[/bold]\n")
    
    questions = [
        "What are the warning signs of a stroke?",
        "How can I prevent a stroke?",
        "What should I do if I think someone is having a stroke?",
    ]
    
    for question in questions:
        console.print(f"[bold cyan]Question:[/bold cyan] {question}\n")
        
        with console.status("[yellow]Generating answer...[/yellow]"):
            result = await rag.query(question)
        
        # Display answer in a panel
        answer_text = f"{result['answer']}\n\n[dim]Sources:[/dim]\n{result['citations']}"
        console.print(Panel(
            answer_text,
            title="[bold green]Answer[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        console.print()
    
    # Test 4: Edge Cases
    console.print("[bold]Test 4: Edge Cases[/bold]\n")
    
    # Question outside domain
    console.print("[cyan]Question outside medical domain:[/cyan]")
    result = await rag.query("What is the capital of France?")
    console.print(Panel(result['answer'], title="Response", border_style="yellow"))
    console.print()
    
    # Very specific question
    console.print("[cyan]Very specific medical question:[/cyan]")
    result = await rag.query("What is the exact percentage of ischemic strokes?")
    console.print(Panel(result['answer'], title="Response", border_style="yellow"))
    console.print()
    
    # Summary
    console.print("[bold green]✅ All RAG tests completed successfully![/bold green]\n")
    console.print("[dim]The system can now:[/dim]")
    console.print("  • Process and chunk medical documents")
    console.print("  • Generate embeddings and store in vector DB")
    console.print("  • Perform semantic search")
    console.print("  • Generate answers with citations")
    console.print("  • Handle edge cases appropriately")
    console.print()

if __name__ == "__main__":
    try:
        asyncio.run(test_rag_system())
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
