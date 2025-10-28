#!/usr/bin/env python3
"""
Quick start script for Healthcare Assistant
Provides easy access to all features
"""

import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box


def main():
    console = Console()
    
    console.print()
    console.print("=" * 80)
    console.print("[bold cyan]🏥 HEALTHCARE ASSISTANT - QUICK START[/bold cyan]")
    console.print("=" * 80)
    console.print()
    
    table = Table(title="🚀 Available Options", box=box.ROUNDED, border_style="cyan")
    table.add_column("Option", style="cyan", justify="center", width=8)
    table.add_column("Description", style="white", width=50)
    table.add_column("File", style="dim", width=30)
    
    table.add_row("1", "🏥 Patient Portal (MAIN APP)", "healthcare_assistant.py")
    table.add_row("2", "👨‍⚕️ Doctor Portal (NEW!)", "doctor_portal.py")
    table.add_row("3", "💬 Medical Q&A Demo", "tests/demo_qa.py")
    table.add_row("4", "📅 Calendar Integration Demo", "tests/final_demo.py")
    table.add_row("5", "🧠 Memory Manager Test", "tests/test_memory_manager.py")
    table.add_row("6", "📆 Interactive Calendar", "calendar_assistant.py")
    table.add_row("7", "🔍 Test RAG System", "tests/test_rag_complete.py")
    table.add_row("8", "⚙️  Test Scheduler", "tests/test_scheduler.py")
    table.add_row("9", "📊 View Database Stats", "(query database)")
    table.add_row("10", "ℹ️  Show Documentation", "(list docs)")
    table.add_row("0", "🚪 Exit", "")
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask(
        "[cyan]Select an option[/cyan]",
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        default="1"
    )
    
    console.print()
    
    if choice == "1":
        console.print("[green]Launching Patient Portal...[/green]\n")
        subprocess.run([sys.executable, "healthcare_assistant.py"])
    
    elif choice == "2":
        console.print("[green]Launching Doctor Portal...[/green]\n")
        subprocess.run([sys.executable, "doctor_portal.py"])
    
    elif choice == "3":
        console.print("[green]Starting Medical Q&A Demo...[/green]\n")
        subprocess.run([sys.executable, "tests/demo_qa.py"])
    
    elif choice == "4":
        console.print("[green]Running Calendar Integration Demo...[/green]\n")
        subprocess.run([sys.executable, "tests/final_demo.py"])
    
    elif choice == "5":
        console.print("[green]Testing Memory Manager...[/green]\n")
        subprocess.run([sys.executable, "tests/test_memory_manager.py"])
    
    elif choice == "6":
        console.print("[green]Launching Interactive Calendar...[/green]\n")
        subprocess.run([sys.executable, "calendar_assistant.py"])
    
    elif choice == "7":
        console.print("[green]Testing RAG System...[/green]\n")
        subprocess.run([sys.executable, "tests/test_rag_complete.py"])
    
    elif choice == "8":
        console.print("[green]Testing Scheduler...[/green]\n")
        subprocess.run([sys.executable, "tests/test_scheduler.py"])
    
    elif choice == "9":
        console.print("[cyan]Database Statistics:[/cyan]\n")
        subprocess.run([
            "sqlite3", "data/healthcare.db",
            """
            SELECT 'Users: ' || COUNT(*) FROM users
            UNION ALL SELECT 'Doctors: ' || COUNT(*) FROM doctors
            UNION ALL SELECT 'Appointments: ' || COUNT(*) FROM appointments
            UNION ALL SELECT 'Conversations: ' || COUNT(*) FROM conversations
            UNION ALL SELECT 'User Preferences: ' || COUNT(*) FROM user_preferences;
            """
        ])
        console.print()
    
    elif choice == "10":
        console.print("[cyan]📚 Documentation Files:[/cyan]\n")
        docs = [
            "docs/COMPLETE.md - Final summary",
            "docs/HEALTHCARE_README.md - Main documentation",
            "docs/HEALTHCARE_PROJECT_PLAN.md - Complete plan",
            "docs/IMPLEMENTATION_ROADMAP.md - Development guide",
            "docs/PROJECT_SUMMARY.md - Executive summary",
            "docs/PHASE1_COMPLETE.md - RAG system",
            "docs/PHASE3_COMPLETE.md - Memory system",
            "docs/API_ENDPOINTS.md - Backend API reference",
            "docs/FRONTEND_PROMPTS.md - Frontend specifications",
            "CHANGELOG.md - Change history"
        ]
        for doc in docs:
            console.print(f"  • {doc}")
        console.print()
    
    elif choice == "0":
        console.print("[green]Goodbye! 👋[/green]\n")
        return
    
    console.print("[dim]Press Enter to return to menu...[/dim]")
    input()
    main()  # Loop back to menu


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋\n")
    except Exception as e:
        print(f"\nError: {e}\n")
