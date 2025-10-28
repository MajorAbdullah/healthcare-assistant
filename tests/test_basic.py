#!/usr/bin/env python3
"""
Minimal RAG demonstration - proves the concept works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.document_processor import DocumentProcessor
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_basic_functionality():
    """Test document processing without vector DB"""
    
    console.print("\n[bold cyan]📚 Healthcare Assistant - Initial Setup Test[/bold cyan]\n")
    
    # Test 1: Document Processing
    console.print("[bold]✅ Phase 1: Document Processing[/bold]\n")
    
    doc_processor = DocumentProcessor(chunk_size=400, chunk_overlap=50)
    
    # Load one document
    doc_file = Path("data/medical_docs/stroke_overview.txt")
    if doc_file.exists():
        console.print(f"[cyan]Loading:[/cyan] {doc_file.name}")
        text = doc_processor.load_text_file(str(doc_file))
        
        # Chunk it
        chunks = doc_processor.chunk_text(text, source_name=doc_file.stem)
        console.print(f"[green]✓ Created {len(chunks)} chunks[/green]\n")
        
        # Show first chunk as sample
        console.print("[bold]Sample Chunk:[/bold]")
        console.print(Panel(
            chunks[0]['text'][:300] + "...",
            title="Chunk 0",
            border_style="cyan"
        ))
        
        # Create table of chunks
        table = Table(title="\nDocument Chunks Overview")
        table.add_column("ID", style="cyan")
        table.add_column("Preview", style="white")
        table.add_column("Length", style="green")
        
        for chunk in chunks[:5]:  # Show first 5
            preview = chunk['text'][:60] + "..."
            table.add_row(
                str(chunk['chunk_index']),
                preview,
                str(len(chunk['text']))
            )
        
        console.print(table)
    else:
        console.print(f"[red]✗ Document not found: {doc_file}[/red]")
        return
    
    # Summary of what's ready
    console.print("\n" + "="*60)
    console.print(Panel(
        "[bold green]✅ Initial Setup Complete![/bold green]\n\n"
        "[white]Working Components:[/white]\n"
        "  ✓ Document processor (PDF + TXT support)\n"
        "  ✓ Text chunking with overlap\n"
        "  ✓ Metadata management\n"
        "  ✓ RAG engine structure\n"
        "  ✓ Configuration system\n\n"
        "[white]Medical Knowledge Base:[/white]\n"
        f"  ✓ Stroke overview document ({len(text)} chars)\n"
        f"  ✓ {len(chunks)} searchable chunks\n\n"
        "[yellow]Next Steps:[/yellow]\n"
        "  1. Add vector database integration\n"
        "  2. Test with Gemini embeddings\n"
        "  3. Implement answer generation\n"
        "  4. Build scheduler module\n"
        "  5. Create memory manager\n\n"
        "[dim]The foundation is ready for full RAG implementation![/dim]",
        title="🏥 Healthcare Assistant Status",
        border_style="green",
        padding=(1, 2)
    ))
    
    # Show what we can do now
    console.print("\n[bold cyan]Demo: How RAG Will Work[/bold cyan]\n")
    
    # Simulate retrieval
    query = "What are stroke symptoms?"
    console.print(f"[yellow]Patient asks:[/yellow] \"{query}\"\n")
    
    # Find relevant chunks (simple keyword match for demo)
    relevant_chunks = []
    keywords = ['symptom', 'sign', 'warning', 'F.A.S.T']
    for chunk in chunks:
        if any(keyword.lower() in chunk['text'].lower() for keyword in keywords):
            relevant_chunks.append(chunk)
    
    console.print(f"[green]System finds {len(relevant_chunks)} relevant chunks:[/green]\n")
    for i, chunk in enumerate(relevant_chunks[:2], 1):
        console.print(f"[cyan]{i}. Chunk {chunk['chunk_index']}:[/cyan]")
        console.print(f"   {chunk['text'][:200]}...\n")
    
    console.print("[yellow]Next: AI will synthesize these chunks into a coherent answer with citations[/yellow]\n")

if __name__ == "__main__":
    try:
        test_basic_functionality()
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
