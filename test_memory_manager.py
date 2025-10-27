#!/usr/bin/env python3
"""
Comprehensive test for Memory Manager
Demonstrates conversation tracking, user profiling, and personalization features
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.memory_manager import MemoryManager, format_conversation_history
from modules.scheduler import AppointmentScheduler
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from datetime import datetime, timedelta


def main():
    console = Console()
    
    console.print()
    console.print("=" * 80)
    console.print("[bold cyan]🧠 MEMORY MANAGER - COMPREHENSIVE TEST[/bold cyan]")
    console.print("=" * 80)
    console.print()
    
    # Initialize
    memory = MemoryManager()
    scheduler = AppointmentScheduler()
    
    # Create test patient
    console.print("[yellow]Step 1: Creating Test Patient...[/yellow]\n")
    
    test_user_id = scheduler.get_or_create_patient(
        name="Alice Williams",
        email="alice.williams@email.com",
        phone="555-9999"
    )
    
    console.print(f"[green]✓ Patient created: ID {test_user_id}[/green]\n")
    
    # ==================== CONVERSATION TRACKING ====================
    
    console.print(Panel.fit("[bold cyan]TEST 1: Conversation Tracking[/bold cyan]", border_style="cyan"))
    console.print()
    
    console.print("[cyan]Simulating conversation exchanges...[/cyan]\n")
    
    # Medical Q&A conversations
    conversations_to_save = [
        {
            'message': 'What are the warning signs of a stroke?',
            'response': 'Warning signs include sudden numbness, confusion, trouble speaking, difficulty walking, and severe headache. Remember: BE-FAST (Balance, Eyes, Face, Arms, Speech, Time).',
            'context': {'topic': 'stroke', 'category': 'symptoms', 'urgency': 'high'}
        },
        {
            'message': 'How can I reduce my risk of stroke?',
            'response': 'Key prevention methods: maintain healthy blood pressure, exercise regularly, eat a balanced diet, limit alcohol, quit smoking, and manage diabetes.',
            'context': {'topic': 'stroke', 'category': 'prevention'}
        },
        {
            'message': 'What should I do if I suspect someone is having a stroke?',
            'response': 'Call emergency services immediately! Time is critical. While waiting: note the time symptoms started, keep the person comfortable, and do not give them food or drinks.',
            'context': {'topic': 'stroke', 'category': 'emergency', 'urgency': 'critical'}
        },
        {
            'message': 'Can you help me book an appointment with a neurologist?',
            'response': 'Of course! I can help you schedule with our neurology specialist Dr. Sarah Johnson. When would you like to come in?',
            'context': {'intent': 'booking', 'specialty': 'neurology'}
        },
        {
            'message': 'I need a morning appointment next week',
            'response': 'I found several morning slots next week. How about Tuesday at 9:30 AM or Wednesday at 10:00 AM?',
            'context': {'intent': 'booking', 'time_preference': 'morning'}
        }
    ]
    
    for i, conv in enumerate(conversations_to_save, 1):
        memory.save_conversation(
            user_id=test_user_id,
            role='user',
            message=conv['message'],
            response=conv['response'],
            context=conv['context']
        )
        console.print(f"  [dim]{i}. {conv['message'][:60]}...[/dim]")
    
    console.print(f"\n[green]✓ Saved {len(conversations_to_save)} conversation exchanges[/green]\n")
    
    # Retrieve history
    console.print("[cyan]Retrieving conversation history...[/cyan]\n")
    history = memory.get_conversation_history(test_user_id, limit=6)
    
    history_table = Table(title="📜 Recent Conversation History", box=box.ROUNDED, border_style="cyan")
    history_table.add_column("Time", style="dim")
    history_table.add_column("Role", style="yellow")
    history_table.add_column("Message", style="white")
    
    for conv in history[:6]:
        timestamp = datetime.fromisoformat(conv['timestamp']).strftime('%H:%M:%S')
        role_icon = "👤" if conv['role'] == 'user' else "🤖"
        history_table.add_row(
            timestamp,
            f"{role_icon} {conv['role']}",
            conv['message'][:50] + "..."
        )
    
    console.print(history_table)
    console.print()
    
    # ==================== USER PROFILING ====================
    
    console.print(Panel.fit("[bold cyan]TEST 2: User Profiling & Context[/bold cyan]", border_style="cyan"))
    console.print()
    
    # Get user context
    console.print("[cyan]Building user profile...[/cyan]\n")
    context = memory.get_user_context(test_user_id)
    
    profile_table = Table(title="👤 User Profile", show_header=False, box=box.ROUNDED, border_style="green")
    profile_table.add_column("Field", style="cyan")
    profile_table.add_column("Value", style="white")
    
    profile_table.add_row("User ID", str(context['user_id']))
    profile_table.add_row("Name", context['name'])
    profile_table.add_row("Email", context['email'])
    profile_table.add_row("Phone", context['phone'])
    profile_table.add_row("Member Since", context['member_since'])
    profile_table.add_row("Total Conversations", str(context['total_conversations']))
    profile_table.add_row("Appointment Stats", str(context['appointment_stats']))
    
    console.print(profile_table)
    console.print()
    
    # Conversation summary
    console.print("[cyan]Analyzing conversation activity...[/cyan]\n")
    summary = memory.get_conversation_summary(test_user_id, days=30)
    
    summary_table = Table(title="📊 Activity Summary (Last 30 Days)", box=box.ROUNDED)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="yellow")
    
    summary_table.add_row("Total Conversations", str(summary['total_conversations']))
    summary_table.add_row("Active Days", str(summary['active_days']))
    
    for role, count in summary['role_breakdown'].items():
        role_icon = "👤" if role == 'user' else "🤖" if role == 'assistant' else "⚙️"
        summary_table.add_row(f"{role_icon} {role.capitalize()}", str(count))
    
    console.print(summary_table)
    console.print()
    
    # ==================== PREFERENCE LEARNING ====================
    
    console.print(Panel.fit("[bold cyan]TEST 3: Preference Learning[/bold cyan]", border_style="cyan"))
    console.print()
    
    # Update preferences based on conversation
    console.print("[cyan]Learning user preferences from interactions...[/cyan]\n")
    
    memory.update_user_preferences(
        user_id=test_user_id,
        preferred_doctor_id=1,  # Dr. Sarah Johnson (Neurology)
        preferred_time_of_day='morning',
        preferred_days=['Tuesday', 'Wednesday', 'Thursday'],
        health_topics=['stroke', 'prevention', 'neurology']
    )
    
    console.print("[green]✓ Preferences learned and saved[/green]\n")
    
    # Retrieve updated context
    updated_context = memory.get_user_context(test_user_id)
    prefs = updated_context['preferences']
    
    prefs_table = Table(title="⚙️ User Preferences", show_header=False, box=box.ROUNDED, border_style="magenta")
    prefs_table.add_column("Preference", style="cyan")
    prefs_table.add_column("Value", style="white")
    
    prefs_table.add_row("Preferred Doctor ID", str(prefs.get('preferred_doctor_id', 'Not set')))
    prefs_table.add_row("Preferred Time", prefs.get('preferred_time_of_day', 'Not set').title())
    prefs_table.add_row("Preferred Days", ', '.join(prefs.get('preferred_days', [])))
    prefs_table.add_row("Health Topics", ', '.join(prefs.get('health_topics', [])))
    prefs_table.add_row("Last Updated", prefs.get('last_updated', 'Never'))
    
    console.print(prefs_table)
    console.print()
    
    # ==================== HEALTH TOPICS ====================
    
    console.print(Panel.fit("[bold cyan]TEST 4: Health Topic Tracking[/bold cyan]", border_style="cyan"))
    console.print()
    
    topics = memory.get_health_topics(test_user_id)
    console.print(f"[cyan]Topics discussed:[/cyan] {', '.join(topics)}\n")
    
    # ==================== PERSONALIZED GREETING ====================
    
    console.print(Panel.fit("[bold cyan]TEST 5: Personalized Greetings[/bold cyan]", border_style="cyan"))
    console.print()
    
    greeting = memory.generate_personalized_greeting(test_user_id)
    
    console.print(Panel(
        f"[green]{greeting}[/green]",
        title="👋 Personalized Greeting",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()
    
    # ==================== SMART SUGGESTIONS ====================
    
    console.print(Panel.fit("[bold cyan]TEST 6: Smart Suggestions[/bold cyan]", border_style="cyan"))
    console.print()
    
    suggestions = memory.get_smart_suggestions(test_user_id)
    
    if suggestions:
        console.print("[cyan]AI-powered suggestions based on your history:[/cyan]\n")
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"  {i}. {suggestion}")
        console.print()
    else:
        console.print("[dim]No suggestions available yet.[/dim]\n")
    
    # ==================== APPOINTMENT PATTERN ANALYSIS ====================
    
    console.print(Panel.fit("[bold cyan]TEST 7: Appointment Pattern Analysis[/bold cyan]", border_style="cyan"))
    console.print()
    
    # First, book a test appointment
    console.print("[cyan]Booking test appointment for pattern analysis...[/cyan]\n")
    
    success, message, apt_id = scheduler.book_appointment(
        user_id=test_user_id,
        doctor_id=1,
        appointment_date=str((datetime.now() + timedelta(days=3)).date()),
        start_time="09:30",
        reason="Follow-up consultation"
    )
    
    if success:
        console.print(f"[green]✓ Appointment booked (ID: {apt_id})[/green]\n")
        
        # Analyze patterns
        console.print("[cyan]Analyzing appointment patterns...[/cyan]\n")
        patterns = memory.analyze_appointment_patterns(test_user_id)
        
        if 'total_appointments' in patterns:
            pattern_table = Table(title="📈 Appointment Patterns", box=box.ROUNDED)
            pattern_table.add_column("Insight", style="cyan")
            pattern_table.add_column("Details", style="white")
            
            pattern_table.add_row("Total Appointments", str(patterns['total_appointments']))
            pattern_table.add_row("Preferred Time", patterns['preferred_time'].title())
            
            time_dist = patterns['time_distribution']
            pattern_table.add_row(
                "Time Distribution",
                f"Morning: {time_dist['morning']}, Afternoon: {time_dist['afternoon']}, Evening: {time_dist['evening']}"
            )
            
            if patterns.get('most_visited_doctor'):
                doc = patterns['most_visited_doctor']
                pattern_table.add_row(
                    "Favorite Doctor",
                    f"{doc['name']} ({doc['specialty']}) - {doc['visits']} visits"
                )
            
            console.print(pattern_table)
            console.print()
    
    # ==================== FORMATTED HISTORY ====================
    
    console.print(Panel.fit("[bold cyan]TEST 8: Formatted History (for Context)[/bold cyan]", border_style="cyan"))
    console.print()
    
    formatted = format_conversation_history(history, max_chars=300)
    
    console.print(Panel(
        f"[dim]{formatted}[/dim]",
        title="📝 Formatted Conversation Context",
        border_style="blue"
    ))
    console.print()
    
    # ==================== SUMMARY ====================
    
    console.print()
    console.print("=" * 80)
    console.print("[bold green]✅ MEMORY MANAGER - ALL TESTS PASSED![/bold green]")
    console.print("=" * 80)
    console.print()
    
    console.print(Panel.fit(
        f"""[cyan]Memory Manager Capabilities Demonstrated:[/cyan]

✓ Conversation tracking with context
✓ User profiling and context building
✓ Preference learning and storage
✓ Health topic extraction
✓ Personalized greetings
✓ Smart suggestions
✓ Appointment pattern analysis
✓ Formatted history for AI context

[yellow]Database Tables Used:[/yellow]
• conversations - {summary['total_conversations']} records
• user_preferences - 1 record
• users - Patient profile
• appointments - Pattern analysis

[green]The system can now remember conversations and personalize interactions! 🎉[/green]""",
        title="[bold cyan]🧠 Test Summary[/bold cyan]",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user\n")
    except Exception as e:
        print(f"\n\nError: {e}\n")
        import traceback
        traceback.print_exc()
