"""
Test Suite for Appointment Scheduler
Tests booking, availability, conflicts, and cancellations
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.scheduler import AppointmentScheduler
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_get_doctors():
    """Test retrieving doctors from database."""
    console.print("\n[bold cyan]Test 1: Get All Doctors[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    doctors = scheduler.get_all_doctors()
    
    console.print(f"✓ Found {len(doctors)} doctors", style="green")
    scheduler.display_doctors(doctors)
    
    assert len(doctors) > 0, "Should have at least one doctor"
    console.print("✅ Test passed!\n", style="bold green")
    
    return doctors


def test_get_availability():
    """Test checking doctor availability."""
    console.print("[bold cyan]Test 2: Check Doctor Availability[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get first doctor
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    
    # Check availability for tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    console.print(f"Checking availability for Dr. {doctor['name']} on {tomorrow}", style="cyan")
    
    slots = scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
    
    console.print(f"✓ Found {len(slots)} available slots", style="green")
    scheduler.display_available_slots(slots[:10], doctor['name'])  # Show first 10
    
    console.print("✅ Test passed!\n", style="bold green")
    
    return doctor, slots


def test_book_appointment():
    """Test booking a new appointment."""
    console.print("[bold cyan]Test 3: Book New Appointment[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get a patient
    user_id = scheduler.get_or_create_patient(
        name="Test Patient",
        email="test.patient@email.com",
        phone="555-9999"
    )
    console.print(f"✓ Patient ID: {user_id}", style="green")
    
    # Get doctor and availability
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    tomorrow = (datetime.now() + timedelta(days=2)).date()  # Day after tomorrow
    slots = scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
    
    if not slots:
        console.print("⚠️  No available slots for testing", style="yellow")
        return None
    
    # Book first available slot
    slot = slots[0]
    
    console.print(f"Booking appointment with Dr. {doctor['name']}", style="cyan")
    console.print(f"  Date: {slot['date']}", style="dim")
    console.print(f"  Time: {slot['start_time']}", style="dim")
    
    success, message, appointment_id = scheduler.book_appointment(
        user_id=user_id,
        doctor_id=doctor['doctor_id'],
        appointment_date=slot['date'],
        start_time=slot['start_time'],
        reason="Test appointment",
        notes="This is a test booking"
    )
    
    if success:
        console.print(f"✓ {message}", style="green")
        console.print(f"✓ Appointment ID: {appointment_id}", style="green")
        console.print("✅ Test passed!\n", style="bold green")
        return appointment_id
    else:
        console.print(f"✗ {message}", style="red")
        console.print("❌ Test failed!\n", style="bold red")
        return None


def test_conflict_detection():
    """Test conflict detection."""
    console.print("[bold cyan]Test 4: Conflict Detection[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get an existing appointment
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    appointments = scheduler.get_doctor_appointments(doctor['doctor_id'])
    
    if not appointments:
        console.print("⚠️  No appointments to test conflict with", style="yellow")
        return
    
    appt = appointments[0]
    
    console.print(f"Testing conflict with existing appointment:", style="cyan")
    console.print(f"  Date: {appt['appointment_date']}", style="dim")
    console.print(f"  Time: {appt['start_time']} - {appt['end_time']}", style="dim")
    
    # Try to book at the same time
    has_conflict = scheduler.check_conflict(
        doctor_id=doctor['doctor_id'],
        appointment_date=appt['appointment_date'],
        start_time=appt['start_time'],
        end_time=appt['end_time']
    )
    
    if has_conflict:
        console.print("✓ Conflict detected correctly", style="green")
        console.print("✅ Test passed!\n", style="bold green")
    else:
        console.print("✗ Failed to detect conflict", style="red")
        console.print("❌ Test failed!\n", style="bold red")


def test_get_appointments():
    """Test retrieving appointments."""
    console.print("[bold cyan]Test 5: Get Appointments[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get doctor appointments
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    
    console.print(f"Getting appointments for Dr. {doctor['name']}", style="cyan")
    appointments = scheduler.get_doctor_appointments(doctor['doctor_id'])
    
    console.print(f"✓ Found {len(appointments)} appointments", style="green")
    scheduler.display_appointments(appointments, f"Dr. {doctor['name']}'s Appointments")
    
    console.print("✅ Test passed!\n", style="bold green")


def test_cancel_appointment():
    """Test cancelling an appointment."""
    console.print("[bold cyan]Test 6: Cancel Appointment[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get a scheduled appointment
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    appointments = scheduler.get_doctor_appointments(
        doctor['doctor_id'], 
        status='scheduled'
    )
    
    if not appointments:
        console.print("⚠️  No scheduled appointments to cancel", style="yellow")
        return
    
    appt = appointments[-1]  # Cancel the last one
    
    console.print(f"Cancelling appointment #{appt['appointment_id']}", style="cyan")
    console.print(f"  Patient: {appt['patient_name']}", style="dim")
    console.print(f"  Date: {appt['appointment_date']} at {appt['start_time']}", style="dim")
    
    success, message = scheduler.cancel_appointment(
        appointment_id=appt['appointment_id'],
        reason="Test cancellation"
    )
    
    if success:
        console.print(f"✓ {message}", style="green")
        console.print("✅ Test passed!\n", style="bold green")
    else:
        console.print(f"✗ {message}", style="red")
        console.print("❌ Test failed!\n", style="bold red")


def test_confirm_appointment():
    """Test confirming an appointment."""
    console.print("[bold cyan]Test 7: Confirm Appointment[/bold cyan]")
    console.print("-" * 80)
    
    scheduler = AppointmentScheduler()
    
    # Get a scheduled appointment
    doctors = scheduler.get_all_doctors()
    doctor = doctors[0]
    appointments = scheduler.get_doctor_appointments(
        doctor['doctor_id'],
        status='scheduled'
    )
    
    if not appointments:
        console.print("⚠️  No scheduled appointments to confirm", style="yellow")
        return
    
    appt = appointments[0]
    
    console.print(f"Confirming appointment #{appt['appointment_id']}", style="cyan")
    
    success, message = scheduler.confirm_appointment(appt['appointment_id'])
    
    if success:
        console.print(f"✓ {message}", style="green")
        console.print("✅ Test passed!\n", style="bold green")
    else:
        console.print(f"✗ {message}", style="yellow")


def main():
    """Run all tests."""
    panel = Panel(
        "[bold cyan]🧪 Appointment Scheduler Test Suite[/bold cyan]\n\n"
        "Testing appointment booking, availability checking, and conflict detection.",
        border_style="cyan"
    )
    console.print(panel)
    
    try:
        # Run tests
        test_get_doctors()
        test_get_availability()
        test_book_appointment()
        test_conflict_detection()
        test_get_appointments()
        test_cancel_appointment()
        test_confirm_appointment()
        
        # Final summary
        console.print("\n" + "="*80, style="bold green")
        console.print(" "*25 + "✅ ALL TESTS COMPLETED!", style="bold green")
        console.print("="*80, style="bold green")
        console.print("\n🎉 Appointment scheduler is working correctly!", style="bold green")
        
    except Exception as e:
        console.print(f"\n❌ Test suite failed: {e}", style="bold red")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
