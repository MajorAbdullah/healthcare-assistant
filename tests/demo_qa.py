#!/usr/bin/env python3
"""
Interactive Medical Q&A Demo
Ask questions about stroke and get AI-powered answers from medical documents!
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    VECTOR_DB_DIR,
    GOOGLE_API_KEY,
    CHROMA_COLLECTION_NAME,
    RAG_SYSTEM_PROMPT
)
from modules.rag_engine import RAGEngine
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

console = Console()


def print_welcome():
    """Display welcome message."""
    welcome_text = """
[bold cyan]🏥 Healthcare Assistant - Medical Q&A Demo[/bold cyan]

[white]This demo uses RAG (Retrieval-Augmented Generation) to answer questions about stroke
based on medical documents in our knowledge base.[/white]

[dim]📚 Knowledge Base: Stroke overview, prevention, symptoms, treatment
🤖 Powered by: Google Gemini + ChromaDB Vector Search
🎯 Accuracy: Answers backed by medical document citations[/dim]

[yellow]Type your question or 'quit' to exit.[/yellow]
    """
    
    panel = Panel(
        welcome_text,
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(panel)


def main():
    """Run the interactive Q&A demo."""
    
    print_welcome()
    
    # Initialize RAG engine
    console.print("\n🔄 Initializing RAG system...", style="cyan")
    
    try:
        rag_engine = RAGEngine(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=VECTOR_DB_DIR,
            api_key=GOOGLE_API_KEY,
            model_name="gemini-2.0-flash-exp",
            system_prompt=RAG_SYSTEM_PROMPT
        )
        
        # Check if we have documents
        stats = rag_engine.get_stats()
        if stats['total_documents'] == 0:
            console.print(
                "\n⚠️  [yellow]No documents in vector database![/yellow]\n"
                "   Run [cyan]python3 test_rag_complete.py[/cyan] first to load medical documents.",
                style="yellow"
            )
            return
        
        console.print(f"✅ Ready! ({stats['total_documents']} chunks loaded)\n", style="green")
        
    except Exception as e:
        console.print(f"\n❌ Failed to initialize: {e}", style="red")
        return
    
    # Example questions
    console.print("💡 [bold cyan]Example questions:[/bold cyan]")
    examples = [
        "What are the warning signs of a stroke?",
        "How can I prevent a stroke?",
        "What is the F.A.S.T. method?",
        "What are the risk factors for stroke?",
        "What should I do if someone has a stroke?",
        "How is stroke treated?"
    ]
    for i, example in enumerate(examples, 1):
        console.print(f"   {i}. [dim]{example}[/dim]")
    
    console.print()
    
    # Interactive loop
    while True:
        try:
            # Get question from user
            question = Prompt.ask("\n[bold cyan]Your question[/bold cyan]")
            
            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'q', 'bye']:
                console.print("\n👋 Thank you for using the Healthcare Assistant!", style="bold green")
                console.print("💡 Remember: Always consult healthcare professionals for medical advice.\n", style="dim")
                break
            
            # Skip empty questions
            if not question.strip():
                continue
            
            # Get answer from RAG system
            result = rag_engine.query(question, n_results=5, verbose=False)
            
            # Display answer
            rag_engine.display_answer(result)
            
            # Show search info
            if result.get('search_results'):
                num_chunks = len(result['search_results'])
                console.print(
                    f"\n[dim]ℹ️  Retrieved {num_chunks} relevant passages from medical documents[/dim]"
                )
            
        except KeyboardInterrupt:
            console.print("\n\n👋 Goodbye!", style="bold green")
            break
        
        except Exception as e:
            console.print(f"\n❌ Error: {e}", style="red")
            console.print("Please try rephrasing your question.\n", style="yellow")


if __name__ == "__main__":
    main()
