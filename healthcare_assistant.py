#!/usr/bin/env python3
"""
Healthcare Assistant - Unified CLI Application
Combines RAG Medical Q&A, Appointment Scheduling, and Memory Management
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from modules.rag_engine import RAGEngine
from modules.scheduler import AppointmentScheduler
from modules.memory_manager import MemoryManager, format_conversation_history
from modules.calendar_sync import CalendarSync
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from typing import Optional, Tuple


class HealthcareAssistant:
    """
    Main Healthcare Assistant orchestrator.
    Integrates RAG Q&A, appointment scheduling, and conversation memory.
    """
    
    def __init__(self):
        """Initialize all modules."""
        self.console = Console()
        self.rag = None  # Lazy load
        self.scheduler = AppointmentScheduler()
        self.memory = MemoryManager()
        self.calendar = CalendarSync(self.scheduler)
        
        self.current_user_id: Optional[int] = None
        self.current_user_name: Optional[str] = None
        self.current_role: Optional[str] = None  # 'patient' or 'doctor'
    
    def display_banner(self):
        """Display welcome banner."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🏥  HEALTHCARE ASSISTANT SYSTEM  🏥                ║
║                                                              ║
║     AI-Powered Medical Q&A + Appointment Scheduling          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold cyan")
        self.console.print()
    
    def login(self) -> bool:
        """
        User login/registration process.
        
        Returns:
            True if login successful
        """
        self.console.print(Panel.fit(
            "[cyan]Welcome! Let's get you started.[/cyan]",
            border_style="cyan"
        ))
        self.console.print()
        
        # Get user details
        name = Prompt.ask("[cyan]What's your name?[/cyan]")
        email = Prompt.ask("[cyan]Email address[/cyan]")
        phone = Prompt.ask("[cyan]Phone number[/cyan]", default="")
        
        # Get or create user
        self.current_user_id = self.scheduler.get_or_create_patient(
            name=name,
            email=email,
            phone=phone
        )
        
        self.current_user_name = name
        
        # Get personalized greeting
        greeting = self.memory.generate_personalized_greeting(self.current_user_id)
        
        self.console.print()
        self.console.print(Panel(
            f"[green]{greeting}[/green]",
            title="👋 Welcome",
            border_style="green"
        ))
        self.console.print()
        
        return True
    
    def main_menu(self) -> str:
        """
        Display main menu and get user choice.
        
        Returns:
            Menu choice as string
        """
        table = Table(title="🏥 Main Menu", box=box.ROUNDED, border_style="cyan")
        table.add_column("Option", style="cyan", justify="center")
        table.add_column("Description", style="white")
        
        table.add_row("1", "💬 Ask a medical question")
        table.add_row("2", "📅 Book an appointment")
        table.add_row("3", "📋 View my appointments")
        table.add_row("4", "🕐 Check doctor availability")
        table.add_row("5", "📖 View conversation history")
        table.add_row("6", "💡 Get personalized suggestions")
        table.add_row("7", "👤 View my profile")
        table.add_row("8", "🚪 Exit")
        
        self.console.print(table)
        self.console.print()
        
        choice = Prompt.ask(
            "[cyan]Select an option[/cyan]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )
        
        return choice
    
    async def handle_medical_question(self):
        """Handle medical Q&A using RAG engine."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]💬 Medical Q&A[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        # Initialize RAG if needed
        if self.rag is None:
            self.console.print("[dim]Loading medical knowledge base...[/dim]")
            try:
                self.rag = RAGEngine()
                self.console.print("[green]✓ Knowledge base loaded[/green]\n")
            except Exception as e:
                self.console.print(f"[red]Error loading knowledge base: {e}[/red]\n")
                return
        
        # Get conversation context
        history = self.memory.get_conversation_history(self.current_user_id, limit=3)
        context = format_conversation_history(history, max_chars=200) if history else ""
        
        if context:
            self.console.print("[dim]Recent conversation:[/dim]")
            self.console.print(f"[dim]{context}[/dim]\n")
        
        # Get question
        question = Prompt.ask("[cyan]Your question[/cyan]")
        
        if not question.strip():
            return
        
        # Get answer
        self.console.print("\n[dim]Searching medical knowledge base...[/dim]\n")
        
        try:
            answer = self.rag.query(question)
            
            # Display answer
            self.console.print(Panel(
                answer,
                title="🤖 Answer",
                border_style="green",
                padding=(1, 2)
            ))
            
            # Save conversation
            self.memory.save_conversation(
                user_id=self.current_user_id,
                role='user',
                message=question,
                response=answer,
                context={'topic': 'medical_qa', 'source': 'rag'}
            )
            
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
        
        self.console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_book_appointment(self):
        """Handle appointment booking workflow."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]📅 Book Appointment[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        # Step 1: Select doctor
        doctors = self.scheduler.get_all_doctors()
        
        doctor_table = Table(title="👨‍⚕️ Available Doctors", box=box.ROUNDED)
        doctor_table.add_column("ID", style="cyan", justify="center")
        doctor_table.add_column("Name", style="yellow")
        doctor_table.add_column("Specialty", style="white")
        doctor_table.add_column("Duration", style="green")
        
        for doc in doctors:
            doctor_table.add_row(
                str(doc['doctor_id']),
                doc['name'],
                doc['specialty'],
                f"{doc['consultation_duration']} min"
            )
        
        self.console.print(doctor_table)
        self.console.print()
        
        # Check for preferred doctor
        context = self.memory.get_user_context(self.current_user_id)
        pref_doctor_id = context.get('preferences', {}).get('preferred_doctor_id')
        
        if pref_doctor_id:
            pref_doctor = next((d for d in doctors if d['doctor_id'] == pref_doctor_id), None)
            if pref_doctor:
                self.console.print(f"[green]💡 You usually see {pref_doctor['name']}[/green]\n")
        
        doctor_id = int(Prompt.ask(
            "[cyan]Select doctor ID[/cyan]",
            default=str(pref_doctor_id) if pref_doctor_id else "1"
        ))
        
        selected_doctor = next((d for d in doctors if d['doctor_id'] == doctor_id), None)
        if not selected_doctor:
            self.console.print("[red]Invalid doctor ID[/red]\n")
            return
        
        # Step 2: Select date
        self.console.print()
        date_input = Prompt.ask(
            "[cyan]Appointment date (YYYY-MM-DD)[/cyan]",
            default=str((datetime.now() + __import__('datetime').timedelta(days=1)).date())
        )
        
        # Step 3: Check availability
        self.console.print("\n[dim]Checking availability...[/dim]\n")
        
        slots = self.scheduler.get_doctor_availability(doctor_id, date_input)
        
        if not slots:
            self.console.print("[red]No available slots for this date.[/red]\n")
            return
        
        # Show available slots
        slot_table = Table(title=f"🕐 Available Times - {date_input}", box=box.ROUNDED)
        slot_table.add_column("Slot", style="cyan", justify="center")
        slot_table.add_column("Time", style="yellow")
        slot_table.add_column("Duration", style="white")
        
        for i, slot in enumerate(slots[:10], 1):
            slot_table.add_row(
                str(i),
                f"{slot['start_time']} - {slot['end_time']}",
                f"{slot['duration']} min"
            )
        
        if len(slots) > 10:
            slot_table.add_row("...", f"+ {len(slots) - 10} more", "")
        
        self.console.print(slot_table)
        self.console.print()
        
        # Check for time preference
        pref_time = context.get('preferences', {}).get('preferred_time_of_day')
        if pref_time:
            self.console.print(f"[green]💡 You prefer {pref_time} appointments[/green]\n")
        
        slot_num = int(Prompt.ask("[cyan]Select slot number[/cyan]", default="1"))
        
        if slot_num < 1 or slot_num > len(slots):
            self.console.print("[red]Invalid slot number[/red]\n")
            return
        
        selected_slot = slots[slot_num - 1]
        
        # Step 4: Get reason
        reason = Prompt.ask("[cyan]Reason for appointment[/cyan]", default="Consultation")
        
        # Step 5: Confirm
        self.console.print()
        self.console.print(Panel(
            f"""[cyan]Appointment Details:[/cyan]
            
Doctor: {selected_doctor['name']} ({selected_doctor['specialty']})
Date: {date_input}
Time: {selected_slot['start_time']} - {selected_slot['end_time']}
Duration: {selected_slot['duration']} minutes
Reason: {reason}""",
            title="📋 Confirmation",
            border_style="yellow"
        ))
        self.console.print()
        
        if not Confirm.ask("[cyan]Confirm booking?[/cyan]", default=True):
            self.console.print("[yellow]Booking cancelled[/yellow]\n")
            return
        
        # Step 6: Book appointment
        self.console.print("\n[dim]Booking appointment...[/dim]\n")
        
        success, message, apt_id = self.scheduler.book_appointment(
            user_id=self.current_user_id,
            doctor_id=doctor_id,
            appointment_date=date_input,
            start_time=selected_slot['start_time'],
            reason=reason
        )
        
        if success:
            self.console.print(f"[green]✓ Appointment booked successfully! (ID: {apt_id})[/green]\n")
            
            # Sync to calendar
            if Confirm.ask("[cyan]Sync to Google Calendar?[/cyan]", default=True):
                self.console.print("[dim]Syncing to calendar...[/dim]\n")
                
                try:
                    cal_success, cal_message = asyncio.run(
                        self.calendar._sync_appointment_to_calendar(apt_id)
                    )
                    
                    if cal_success:
                        self.console.print("[green]✓ Synced to Google Calendar![/green]\n")
                    else:
                        self.console.print(f"[yellow]Calendar sync: {cal_message}[/yellow]\n")
                except Exception as e:
                    self.console.print(f"[yellow]Calendar sync failed: {e}[/yellow]\n")
            
            # Save conversation
            self.memory.save_conversation(
                user_id=self.current_user_id,
                role='user',
                message=f"Booked appointment with {selected_doctor['name']}",
                context={
                    'appointment_id': apt_id,
                    'doctor_id': doctor_id,
                    'date': date_input,
                    'time': selected_slot['start_time']
                }
            )
            
            # Update preferences
            self.memory.update_user_preferences(
                user_id=self.current_user_id,
                preferred_doctor_id=doctor_id
            )
            
        else:
            self.console.print(f"[red]✗ Booking failed: {message}[/red]\n")
        
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_view_appointments(self):
        """Display user's appointments."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]📋 My Appointments[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        appointments = self.scheduler.get_patient_appointments(
            self.current_user_id,
            future_only=False
        )
        
        if not appointments:
            self.console.print("[yellow]No appointments found.[/yellow]\n")
            Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
            return
        
        # Separate upcoming and past
        upcoming = [a for a in appointments if a['status'] == 'scheduled']
        past = [a for a in appointments if a['status'] in ['completed', 'cancelled']]
        
        # Show upcoming appointments
        if upcoming:
            upcoming_table = Table(title="📅 Upcoming Appointments", box=box.ROUNDED, border_style="green")
            upcoming_table.add_column("ID", style="cyan", justify="center")
            upcoming_table.add_column("Date", style="yellow")
            upcoming_table.add_column("Time", style="white")
            upcoming_table.add_column("Doctor", style="green")
            upcoming_table.add_column("Status", style="white")
            
            for apt in upcoming[:5]:
                upcoming_table.add_row(
                    str(apt['appointment_id']),
                    apt['appointment_date'],
                    f"{apt['start_time']} - {apt['end_time']}",
                    apt['doctor_name'],
                    apt['status'].upper()
                )
            
            self.console.print(upcoming_table)
            self.console.print()
        
        # Show past appointments
        if past:
            past_table = Table(title="📜 Past Appointments", box=box.ROUNDED, border_style="dim")
            past_table.add_column("Date", style="dim")
            past_table.add_column("Doctor", style="dim")
            past_table.add_column("Status", style="dim")
            
            for apt in past[:3]:
                past_table.add_row(
                    apt['appointment_date'],
                    apt['doctor_name'],
                    apt['status'].upper()
                )
            
            self.console.print(past_table)
            self.console.print()
        
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_check_availability(self):
        """Check doctor availability."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]🕐 Check Availability[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        doctors = self.scheduler.get_all_doctors()
        
        for doc in doctors:
            self.console.print(f"[cyan]{doc['doctor_id']}.[/cyan] {doc['name']} - {doc['specialty']}")
        
        self.console.print()
        doctor_id = int(Prompt.ask("[cyan]Select doctor ID[/cyan]", default="1"))
        
        date_input = Prompt.ask(
            "[cyan]Date (YYYY-MM-DD)[/cyan]",
            default=str((datetime.now() + __import__('datetime').timedelta(days=1)).date())
        )
        
        self.console.print("\n[dim]Checking availability...[/dim]\n")
        
        slots = self.scheduler.get_doctor_availability(doctor_id, date_input)
        
        if not slots:
            self.console.print("[red]No available slots[/red]\n")
        else:
            self.console.print(f"[green]Found {len(slots)} available slots:[/green]\n")
            
            for i, slot in enumerate(slots[:15], 1):
                self.console.print(f"  {i}. {slot['start_time']} - {slot['end_time']}")
            
            if len(slots) > 15:
                self.console.print(f"  ... and {len(slots) - 15} more\n")
        
        self.console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_conversation_history(self):
        """Display conversation history."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]📖 Conversation History[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        history = self.memory.get_conversation_history(self.current_user_id, limit=10)
        
        if not history:
            self.console.print("[yellow]No conversation history found.[/yellow]\n")
            Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
            return
        
        history_table = Table(title="💬 Recent Conversations", box=box.ROUNDED)
        history_table.add_column("Time", style="dim")
        history_table.add_column("Role", style="cyan")
        history_table.add_column("Message", style="white")
        
        for conv in history:
            timestamp = datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M')
            role_icon = "👤" if conv['role'] == 'user' else "🤖"
            
            history_table.add_row(
                timestamp,
                f"{role_icon} {conv['role']}",
                conv['message'][:60] + "..." if len(conv['message']) > 60 else conv['message']
            )
        
        self.console.print(history_table)
        self.console.print()
        
        # Show summary
        summary = self.memory.get_conversation_summary(self.current_user_id)
        self.console.print(f"[dim]Total: {summary['total_conversations']} conversations over {summary['active_days']} days[/dim]\n")
        
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_suggestions(self):
        """Show personalized suggestions."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]💡 Personalized Suggestions[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        suggestions = self.memory.get_smart_suggestions(self.current_user_id)
        
        if not suggestions:
            self.console.print("[dim]No suggestions available yet. Keep using the system![/dim]\n")
        else:
            self.console.print("[cyan]Based on your history:[/cyan]\n")
            for suggestion in suggestions:
                self.console.print(f"  {suggestion}")
            self.console.print()
        
        # Show appointment patterns
        patterns = self.memory.analyze_appointment_patterns(self.current_user_id)
        
        if patterns.get('total_appointments', 0) > 0:
            self.console.print(Panel(
                f"""[cyan]Your Appointment Patterns:[/cyan]

Total Appointments: {patterns['total_appointments']}
Preferred Time: {patterns['preferred_time'].title()}
Time Distribution: Morning: {patterns['time_distribution']['morning']}, Afternoon: {patterns['time_distribution']['afternoon']}, Evening: {patterns['time_distribution']['evening']}""",
                title="📊 Insights",
                border_style="magenta"
            ))
            self.console.print()
        
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    def handle_profile(self):
        """Display user profile."""
        self.console.print()
        self.console.print(Panel.fit("[bold cyan]👤 My Profile[/bold cyan]", border_style="cyan"))
        self.console.print()
        
        context = self.memory.get_user_context(self.current_user_id)
        
        profile_table = Table(title="User Information", show_header=False, box=box.ROUNDED)
        profile_table.add_column("Field", style="cyan")
        profile_table.add_column("Value", style="white")
        
        profile_table.add_row("Name", context['name'])
        profile_table.add_row("Email", context['email'])
        profile_table.add_row("Phone", context.get('phone', 'Not provided'))
        profile_table.add_row("Member Since", context['member_since'])
        profile_table.add_row("Total Conversations", str(context['total_conversations']))
        
        self.console.print(profile_table)
        self.console.print()
        
        # Show preferences
        prefs = context.get('preferences', {})
        if prefs:
            self.console.print("[cyan]Preferences:[/cyan]")
            if prefs.get('preferred_doctor_id'):
                self.console.print(f"  Preferred Doctor: ID {prefs['preferred_doctor_id']}")
            if prefs.get('preferred_time_of_day'):
                self.console.print(f"  Preferred Time: {prefs['preferred_time_of_day'].title()}")
            if prefs.get('health_topics'):
                topics = ', '.join(prefs['health_topics'])
                self.console.print(f"  Health Interests: {topics}")
            self.console.print()
        
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
    
    async def run(self):
        """Main application loop."""
        self.display_banner()
        
        # Login
        if not self.login():
            return
        
        # Main loop
        while True:
            try:
                choice = self.main_menu()
                
                if choice == "1":
                    await self.handle_medical_question()
                elif choice == "2":
                    self.handle_book_appointment()
                elif choice == "3":
                    self.handle_view_appointments()
                elif choice == "4":
                    self.handle_check_availability()
                elif choice == "5":
                    self.handle_conversation_history()
                elif choice == "6":
                    self.handle_suggestions()
                elif choice == "7":
                    self.handle_profile()
                elif choice == "8":
                    self.console.print("\n[green]Thank you for using Healthcare Assistant! Stay healthy! 👋[/green]\n")
                    break
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Goodbye! 👋[/yellow]\n")
                break
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/red]\n")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    assistant = HealthcareAssistant()
    asyncio.run(assistant.run())
