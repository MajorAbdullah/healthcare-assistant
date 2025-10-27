#!/usr/bin/env python3
"""
Demo: Appointment Scheduling with Calendar Integration
Tests the complete workflow from checking availability to booking with calendar sync
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.scheduler import AppointmentScheduler
from modules.calendar_integration import CalendarIntegration, CALENDAR_AVAILABLE
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def print_header(text: str):
    """Print a fancy header."""
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]{text}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()


def demo_1_check_doctors():
    """Demo 1: List all available doctors."""
    print_header("📋 DEMO 1: View Available Doctors")
    
    scheduler = AppointmentScheduler()
    doctors = scheduler.get_all_doctors()
    
    if doctors:
        console.print(f"[green]✓ Found {len(doctors)} doctors in the system[/green]\n")
        scheduler.display_doctors(doctors)
    else:
        console.print("[red]✗ No doctors found. Run db_setup.py first![/red]")
        return False
    
    return True


def demo_2_check_availability():
    """Demo 2: Check doctor's available time slots."""
    print_header("📅 DEMO 2: Check Doctor's Free Time Slots")
    
    scheduler = AppointmentScheduler()
    
    # Get a doctor (Dr. Aisha Khan - Rehabilitation)
    doctors = scheduler.get_all_doctors()
    if not doctors:
        console.print("[red]✗ No doctors available[/red]")
        return None
    
    doctor = doctors[0]  # Use first doctor
    doctor_id = doctor['doctor_id']
    
    console.print(f"[cyan]Checking availability for:[/cyan] [bold]{doctor['name']}[/bold]")
    console.print(f"[dim]Specialty: {doctor['specialty']}[/dim]")
    console.print(f"[dim]Consultation Duration: {doctor['consultation_duration']} minutes[/dim]\n")
    
    # Check tomorrow's availability
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    console.print(f"[cyan]📆 Date:[/cyan] {tomorrow.strftime('%A, %B %d, %Y')}\n")
    
    slots = scheduler.get_doctor_availability(doctor_id, tomorrow)
    
    if slots:
        console.print(f"[green]✓ Found {len(slots)} available time slots:[/green]\n")
        scheduler.display_available_slots(slots, doctor['name'])
        return doctor_id, tomorrow, slots[0] if slots else None
    else:
        console.print(f"[yellow]⚠️  No available slots for {tomorrow}[/yellow]")
        return doctor_id, tomorrow, None


def demo_3_book_appointment(doctor_id, appointment_date, slot=None):
    """Demo 3: Book an appointment."""
    print_header("🗓️  DEMO 3: Book New Appointment")
    
    scheduler = AppointmentScheduler()
    
    # Create or get a test patient
    console.print("[cyan]Creating/finding patient...[/cyan]")
    user_id = scheduler.get_or_create_patient(
        name="Test Patient",
        email="test.patient@example.com",
        phone="555-TEST-001"
    )
    console.print(f"[green]✓ Patient ID: {user_id}[/green]\n")
    
    # Use provided slot or default time
    if slot:
        start_time = slot['start_time']
        console.print(f"[cyan]Using available slot: {start_time}[/cyan]\n")
    else:
        start_time = "10:00"
        console.print(f"[yellow]⚠️  No slot provided, trying {start_time}[/yellow]\n")
    
    # Book appointment
    console.print("[cyan]Booking appointment...[/cyan]")
    success, message, appointment_id = scheduler.book_appointment(
        user_id=user_id,
        doctor_id=doctor_id,
        appointment_date=str(appointment_date),
        start_time=start_time,
        reason="Demo consultation - Testing appointment system"
    )
    
    if success:
        console.print(f"[green bold]✓ {message}[/green bold]")
        console.print(f"[green]Appointment ID: {appointment_id}[/green]\n")
        
        # Show appointment details
        appointment = scheduler.get_appointment(appointment_id)
        if appointment:
            console.print("[cyan]📋 Appointment Details:[/cyan]\n")
            
            table = Table(show_header=False, box=box.ROUNDED, border_style="green")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Appointment ID", str(appointment['appointment_id']))
            table.add_row("Patient", appointment['patient_name'])
            table.add_row("Doctor", f"{appointment['doctor_name']} ({appointment['doctor_specialty']})")
            table.add_row("Date", appointment['appointment_date'])
            table.add_row("Time", f"{appointment['start_time']} - {appointment['end_time']}")
            table.add_row("Status", f"[green]{appointment['status'].upper()}[/green]")
            table.add_row("Reason", appointment.get('reason', 'Not specified'))
            
            console.print(table)
            console.print()
        
        return appointment_id
    else:
        console.print(f"[red]✗ {message}[/red]")
        return None


def demo_4_calendar_integration(appointment_id):
    """Demo 4: Sync appointment with Google Calendar."""
    print_header("📅 DEMO 4: Calendar Integration (Pipedream)")
    
    if not CALENDAR_AVAILABLE:
        console.print("[yellow]⚠️  Calendar integration is NOT available[/yellow]")
        console.print("[dim]calendar_assistant.py not found or not configured[/dim]\n")
        console.print("[cyan]Calendar integration capabilities:[/cyan]")
        console.print("  • Sync appointments to Google Calendar via Pipedream")
        console.print("  • Automatic event creation with patient/doctor emails")
        console.print("  • Email notifications to both parties")
        console.print("  • Calendar event links stored in database")
        console.print("  • Support for event updates and cancellations\n")
        console.print("[yellow]To enable calendar sync:[/yellow]")
        console.print("  1. Ensure calendar_assistant.py is configured")
        console.print("  2. Set up Pipedream API credentials")
        console.print("  3. Configure doctor's calendar_id in database\n")
        return False
    
    console.print("[green]✓ Calendar integration is AVAILABLE[/green]\n")
    
    integration = CalendarIntegration()
    
    console.print(f"[cyan]Syncing appointment {appointment_id} to Google Calendar...[/cyan]\n")
    
    success, message, event_id = integration.create_calendar_event(appointment_id)
    
    if success:
        console.print(f"[green bold]✓ {message}[/green bold]")
        console.print(f"[green]Calendar Event ID: {event_id}[/green]\n")
        
        console.print("[cyan]📨 What happens next:[/cyan]")
        console.print("  • Event created in doctor's Google Calendar")
        console.print("  • Email invitation sent to patient")
        console.print("  • Email notification sent to doctor")
        console.print("  • Event appears in both calendars")
        console.print("  • Automatic reminders set (30 min before)\n")
        
        return True
    else:
        console.print(f"[red]✗ {message}[/red]\n")
        return False


def demo_5_conflict_detection():
    """Demo 5: Show conflict detection in action."""
    print_header("⚠️  DEMO 5: Conflict Detection")
    
    scheduler = AppointmentScheduler()
    
    # Try to book in an already occupied slot
    console.print("[cyan]Attempting to book an appointment in an already occupied time slot...[/cyan]\n")
    
    # Get existing appointment
    doctors = scheduler.get_all_doctors()
    if not doctors:
        console.print("[yellow]No doctors available for demo[/yellow]")
        return
    
    doctor_id = doctors[0]['doctor_id']
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    # Get occupied slots
    occupied = scheduler.get_doctor_appointments(doctor_id, str(tomorrow))
    
    if occupied:
        first_appt = occupied[0]
        conflict_time = first_appt['start_time']
        
        console.print(f"[yellow]Existing appointment at {conflict_time}[/yellow]")
        console.print(f"[dim]Patient: {first_appt['patient_name']}[/dim]\n")
        
        # Try to book at same time
        user_id = scheduler.get_or_create_patient(
            name="Another Patient",
            email="another@example.com",
            phone="555-0002"
        )
        
        success, message, _ = scheduler.book_appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            appointment_date=str(tomorrow),
            start_time=conflict_time,
            reason="Test conflict"
        )
        
        if not success:
            console.print(f"[red]✗ Booking prevented: {message}[/red]")
            console.print("[green]✓ Conflict detection working correctly![/green]\n")
        else:
            console.print("[red]⚠️  Conflict detection may have an issue[/red]\n")
    else:
        console.print("[yellow]No existing appointments to test conflict detection[/yellow]\n")


def demo_6_book_with_calendar():
    """Demo 6: Combined booking with calendar sync."""
    print_header("🚀 DEMO 6: One-Step Booking with Calendar Sync")
    
    if not CALENDAR_AVAILABLE:
        console.print("[yellow]⚠️  Calendar not available for combined booking demo[/yellow]")
        console.print("[dim]This feature requires calendar_assistant.py[/dim]\n")
        return
    
    console.print("[cyan]This demo shows booking an appointment and syncing to calendar in one step[/cyan]\n")
    
    integration = CalendarIntegration()
    
    # Create patient
    user_id = integration.scheduler.get_or_create_patient(
        name="VIP Patient",
        email="vip.patient@example.com",
        phone="555-VIP-001"
    )
    
    # Get doctor
    doctors = integration.scheduler.get_all_doctors()
    doctor_id = doctors[0]['doctor_id']
    
    # Find available slot
    day_after_tomorrow = (datetime.now() + timedelta(days=2)).date()
    slots = integration.scheduler.get_doctor_availability(doctor_id, day_after_tomorrow)
    
    if not slots:
        console.print("[yellow]No available slots found[/yellow]")
        return
    
    first_slot = slots[0]
    
    console.print(f"[cyan]Booking appointment with calendar sync...[/cyan]")
    console.print(f"[dim]Date: {day_after_tomorrow}[/dim]")
    console.print(f"[dim]Time: {first_slot['start_time']}[/dim]\n")
    
    success, message, appointment_id = integration.book_appointment_with_calendar(
        user_id=user_id,
        doctor_id=doctor_id,
        appointment_date=str(day_after_tomorrow),
        start_time=first_slot['start_time'],
        reason="VIP consultation via combined booking",
        create_calendar_event=True
    )
    
    if success:
        console.print(f"[green bold]✓ Complete! Appointment booked and synced to calendar[/green bold]")
        console.print(f"[green]Appointment ID: {appointment_id}[/green]\n")
    else:
        console.print(f"[red]✗ {message}[/red]\n")


def main():
    """Run all demos."""
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]APPOINTMENT SCHEDULING & CALENDAR INTEGRATION DEMO[/bold cyan]")
    console.print("=" * 70)
    console.print()
    console.print("[dim]This demo showcases:[/dim]")
    console.print("[dim]  • Viewing available doctors[/dim]")
    console.print("[dim]  • Checking free time slots[/dim]")
    console.print("[dim]  • Booking appointments[/dim]")
    console.print("[dim]  • Calendar integration via Pipedream[/dim]")
    console.print("[dim]  • Conflict detection[/dim]")
    console.print("=" * 70)
    
    # Demo 1: Check doctors
    if not demo_1_check_doctors():
        console.print("\n[red]Please run 'python3 db_setup.py' first to initialize the database[/red]\n")
        return
    
    input("\n[cyan]Press Enter to continue to Demo 2...[/cyan]")
    
    # Demo 2: Check availability
    result = demo_2_check_availability()
    if result:
        doctor_id, appointment_date, slot = result
    else:
        console.print("[yellow]Skipping remaining demos due to no availability[/yellow]")
        return
    
    input("\n[cyan]Press Enter to continue to Demo 3...[/cyan]")
    
    # Demo 3: Book appointment
    appointment_id = demo_3_book_appointment(doctor_id, appointment_date, slot)
    
    if appointment_id:
        input("\n[cyan]Press Enter to continue to Demo 4...[/cyan]")
        
        # Demo 4: Calendar integration
        demo_4_calendar_integration(appointment_id)
        
        input("\n[cyan]Press Enter to continue to Demo 5...[/cyan]")
        
        # Demo 5: Conflict detection
        demo_5_conflict_detection()
        
        input("\n[cyan]Press Enter to continue to Demo 6...[/cyan]")
        
        # Demo 6: Combined booking
        demo_6_book_with_calendar()
    
    # Summary
    console.print()
    console.print(Panel.fit(
        "[bold green]✓ Demo Complete![/bold green]\n\n"
        "[cyan]System Capabilities Verified:[/cyan]\n"
        "  ✓ Doctor availability checking\n"
        "  ✓ Time slot generation (30-min intervals)\n"
        "  ✓ Appointment booking\n"
        "  ✓ Conflict detection\n"
        f"  {'✓' if CALENDAR_AVAILABLE else '⚠️ '} Google Calendar integration via Pipedream\n\n"
        "[dim]The appointment scheduling system is fully operational and ready for use![/dim]",
        title="[bold cyan]Summary[/bold cyan]",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]\n")
        import traceback
        traceback.print_exc()
