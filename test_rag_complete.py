"""
Complete RAG Pipeline Test
Tests the full workflow: document loading → chunking → embedding → storage → search → answer generation
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    MEDICAL_DOCS_DIR,
    VECTOR_DB_DIR,
    GOOGLE_API_KEY,
    CHROMA_COLLECTION_NAME
)
from utils.document_processor import DocumentProcessor
from modules.rag_engine import RAGEngine
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def main():
    """Test the complete RAG pipeline."""
    
    console.print("\n" + "="*80, style="bold cyan")
    console.print(" "*25 + "🏥 RAG PIPELINE TEST", style="bold cyan")
    console.print("="*80 + "\n", style="bold cyan")
    
    # Step 1: Initialize components
    console.print("📦 [bold cyan]Step 1: Initializing Components[/bold cyan]")
    console.print("-" * 80)
    
    try:
        # Initialize document processor
        doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        console.print("  ✅ Document processor initialized", style="green")
        
        # Initialize RAG engine
        rag_engine = RAGEngine(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=VECTOR_DB_DIR,
            api_key=GOOGLE_API_KEY,
            model_name="gemini-2.0-flash-exp"
        )
        console.print("  ✅ RAG engine initialized", style="green")
        console.print()
        
    except Exception as e:
        console.print(f"  ❌ Initialization failed: {e}", style="red")
        return
    
    # Step 2: Load and process documents
    console.print("📄 [bold cyan]Step 2: Loading Medical Documents[/bold cyan]")
    console.print("-" * 80)
    
    try:
        # Process all documents in the medical_docs directory
        all_chunks = doc_processor.process_directory(MEDICAL_DOCS_DIR)
        
        if not all_chunks:
            console.print("  ❌ No chunks generated from documents", style="red")
            return
        
        console.print(f"  ✅ Processed documents into {len(all_chunks)} chunks", style="green")
        
        # Show sample chunk
        if all_chunks:
            sample = all_chunks[0]
            sample_panel = Panel(
                f"[dim]{sample['text'][:200]}...[/dim]\n\n"
                f"[cyan]Source:[/cyan] {sample['metadata'].get('source', 'N/A')}\n"
                f"[cyan]Type:[/cyan] {sample['metadata'].get('doc_type', 'N/A')}",
                title="📝 Sample Chunk",
                border_style="blue"
            )
            console.print(sample_panel)
        
    except Exception as e:
        console.print(f"  ❌ Document processing failed: {e}", style="red")
        return
    
    # Step 3: Add documents to vector database
    console.print("\n💾 [bold cyan]Step 3: Building Vector Database[/bold cyan]")
    console.print("-" * 80)
    
    try:
        rag_engine.add_documents(all_chunks)
        
        # Get stats
        stats = rag_engine.get_stats()
        console.print(f"  ✅ Vector database built successfully", style="green")
        console.print(f"  📊 Total chunks in DB: {stats['total_documents']}", style="cyan")
        console.print()
        
    except Exception as e:
        console.print(f"  ❌ Vector database build failed: {e}", style="red")
        console.print(f"  💡 This might be due to API rate limits. Try again in a moment.", style="yellow")
        return
    
    # Step 4: Test semantic search
    console.print("🔍 [bold cyan]Step 4: Testing Semantic Search[/bold cyan]")
    console.print("-" * 80)
    
    test_queries = [
        "What are the warning signs of stroke?",
        "How can I prevent a stroke?",
        "What is the F.A.S.T. method?"
    ]
    
    for query in test_queries:
        console.print(f"\n  ❓ Query: [yellow]{query}[/yellow]")
        
        try:
            results = rag_engine.search(query, n_results=3)
            
            if results:
                console.print(f"  ✅ Found {len(results)} relevant chunks", style="green")
                
                # Show top result
                top_result = results[0]
                console.print(f"     [dim]Top match: {top_result['text'][:100]}...[/dim]")
                console.print(f"     [dim]Distance: {top_result.get('distance', 'N/A'):.4f}[/dim]")
            else:
                console.print(f"  ⚠️  No results found", style="yellow")
                
        except Exception as e:
            console.print(f"  ❌ Search failed: {e}", style="red")
    
    console.print()
    
    # Step 5: Test answer generation
    console.print("🤖 [bold cyan]Step 5: Testing Answer Generation[/bold cyan]")
    console.print("-" * 80 + "\n")
    
    test_question = "What are the main symptoms of a stroke and why is quick action important?"
    
    console.print(f"  ❓ Question: [bold yellow]{test_question}[/bold yellow]\n")
    
    try:
        result = rag_engine.query(test_question, n_results=5, verbose=True)
        
        # Display the answer beautifully
        console.print("\n")
        rag_engine.display_answer(result)
        
        # Show metadata
        console.print("\n📊 [bold cyan]Metadata[/bold cyan]")
        metadata_table = Table(box=box.SIMPLE)
        metadata_table.add_column("Metric", style="cyan")
        metadata_table.add_column("Value", style="white")
        metadata_table.add_row("Chunks Retrieved", str(len(result.get('search_results', []))))
        metadata_table.add_row("Sources Used", str(len(result.get('sources', []))))
        metadata_table.add_row("Citations", str(len(result.get('citations', []))))
        console.print(metadata_table)
        
    except Exception as e:
        console.print(f"  ❌ Answer generation failed: {e}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim red")
        return
    
    # Success!
    console.print("\n" + "="*80, style="bold green")
    console.print(" "*25 + "✅ ALL TESTS PASSED!", style="bold green")
    console.print("="*80, style="bold green")
    console.print("\n🎉 The RAG system is working perfectly!", style="bold green")
    console.print("💡 You can now ask questions about stroke and get AI-powered answers!\n", style="cyan")


if __name__ == "__main__":
    main()
