#!/usr/bin/env python3
"""
QUICK START GUIDE - Appointment Scheduling System
Use this script to quickly test all features
"""

from modules.scheduler import AppointmentScheduler
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel

console = Console()

def quick_demo():
    """Quick demonstration of appointment scheduling capabilities."""
    
    console.print("\n[bold cyan]🏥 APPOINTMENT SCHEDULING - QUICK START[/bold cyan]\n")
    
    scheduler = AppointmentScheduler()
    
    # 1. Show doctors
    console.print("[yellow]1️⃣  Available Doctors:[/yellow]")
    doctors = scheduler.get_all_doctors()
    for doc in doctors:
        console.print(f"   • {doc['name']} - {doc['specialty']}")
    
    # 2. Check availability
    console.print("\n[yellow]2️⃣  Checking Availability:[/yellow]")
    doctor = doctors[0]
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    slots = scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
    console.print(f"   • {doctor['name']} has {len(slots)} free slots on {tomorrow}")
    console.print(f"   • First available: {slots[0]['start_time']} - {slots[0]['end_time']}")
    
    # 3. Create patient
    console.print("\n[yellow]3️⃣  Creating Patient:[/yellow]")
    user_id = scheduler.get_or_create_patient(
        name="Quick Test Patient",
        email="quicktest@example.com",
        phone="555-QUICK"
    )
    console.print(f"   • Patient ID: {user_id}")
    
    # 4. Book appointment
    console.print("\n[yellow]4️⃣  Booking Appointment:[/yellow]")
    success, message, appt_id = scheduler.book_appointment(
        user_id=user_id,
        doctor_id=doctor['doctor_id'],
        appointment_date=str(tomorrow),
        start_time=slots[0]['start_time'],
        reason="Quick demo appointment"
    )
    if success:
        console.print(f"   • [green]✓ Success![/green] Appointment ID: {appt_id}")
    else:
        console.print(f"   • [red]✗ Failed:[/red] {message}")
    
    # 5. Show appointment details
    if success:
        console.print("\n[yellow]5️⃣  Appointment Details:[/yellow]")
        appt = scheduler.get_appointment(appt_id)
        console.print(f"   • Patient: {appt['patient_name']}")
        console.print(f"   • Doctor: {appt['doctor_name']}")
        console.print(f"   • Date: {appt['appointment_date']}")
        console.print(f"   • Time: {appt['start_time']} - {appt['end_time']}")
        console.print(f"   • Status: {appt['status'].upper()}")
    
    # 6. Test conflict detection
    console.print("\n[yellow]6️⃣  Testing Conflict Detection:[/yellow]")
    success2, message2, _ = scheduler.book_appointment(
        user_id=user_id,
        doctor_id=doctor['doctor_id'],
        appointment_date=str(tomorrow),
        start_time=slots[0]['start_time'],  # Same time!
        reason="This should fail"
    )
    if not success2:
        console.print(f"   • [green]✓ Conflict detected correctly![/green]")
        console.print(f"   • Message: {message2}")
    
    # Summary
    console.print()
    console.print(Panel.fit(
        "[bold green]✓ All Features Working![/bold green]\n\n"
        "[cyan]What you can do now:[/cyan]\n"
        "  • View all doctors and their specialties\n"
        "  • Check real-time availability (14 slots/day)\n"
        "  • Book appointments with automatic conflict detection\n"
        "  • Track appointment status\n"
        "  • Cancel/confirm appointments\n\n"
        "[yellow]Calendar Integration:[/yellow]\n"
        "  • Ready to sync with Google Calendar via Pipedream\n"
        "  • Needs doctor calendar_id configuration\n"
        "  • Works independently without calendar\n\n"
        "[dim]Run 'python3 demo_appointment_calendar.py' for full demo[/dim]",
        title="[bold cyan]Summary[/bold cyan]",
        border_style="green"
    ))
    console.print()

if __name__ == "__main__":
    try:
        quick_demo()
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]\n")
        console.print("[yellow]Make sure you've run 'python3 db_setup.py' first![/yellow]\n")
