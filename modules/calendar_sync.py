#!/usr/bin/env python3
"""
Calendar Sync Module
Properly integrates appointment scheduler with Google Calendar using calendar_assistant.py
Uses the working Pipedream MCP integration via natural language commands
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.scheduler import AppointmentScheduler
from calendar_assistant import SmartCalendarAssistant
from rich.console import Console

console = Console()


class CalendarSync:
    """
    Syncs appointments to Google Calendar using the SmartCalendarAssistant.
    
    This uses the working calendar_assistant.py which handles:
    - Pipedream authentication
    - MCP (Model Context Protocol) integration
    - Google Calendar API calls via Gemini AI
    - Natural language event creation
    """
    
    def __init__(self, scheduler: AppointmentScheduler = None):
        """Initialize calendar sync."""
        self.scheduler = scheduler or AppointmentScheduler()
        self.assistant = None
        self.initialized = False
    
    async def _initialize_assistant(self):
        """Initialize the calendar assistant asynchronously."""
        if self.initialized:
            return True
        
        try:
            self.assistant = SmartCalendarAssistant()
            await self.assistant.initialize()
            self.initialized = True
            console.print("[green]✓ Calendar assistant initialized[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize calendar: {e}[/red]")
            return False
    
    async def _sync_appointment_to_calendar(self, appointment_id: int) -> Tuple[bool, str]:
        """
        Sync an appointment to Google Calendar using natural language.
        
        Args:
            appointment_id: The appointment ID to sync
            
        Returns:
            Tuple of (success, message)
        """
        # Ensure assistant is initialized
        if not self.initialized:
            success = await self._initialize_assistant()
            if not success:
                return False, "Failed to initialize calendar assistant"
        
        # Get appointment details
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, f"Appointment {appointment_id} not found"
        
        try:
            # Format the appointment for natural language
            start_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['start_time']}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['end_time']}",
                "%Y-%m-%d %H:%M"
            )
            
            # Format date and times nicely
            date_str = start_datetime.strftime("%A, %B %d, %Y")
            start_time_str = start_datetime.strftime("%I:%M %p")
            end_time_str = end_datetime.strftime("%I:%M %p")
            
            # Create event title
            event_title = f"Appointment: {appointment['patient_name']} with {appointment['doctor_name']}"
            
            # Create event description
            event_description = f"""
Patient: {appointment['patient_name']}
Email: {appointment['patient_email']}
Doctor: {appointment['doctor_name']} ({appointment['doctor_specialty']})
Reason: {appointment.get('reason', 'Not specified')}

Appointment ID: {appointment_id}
"""
            
            # Build natural language command for calendar assistant
            calendar_command = f"""Schedule an event titled "{event_title}" on {date_str} from {start_time_str} to {end_time_str}.

Description: {event_description.strip()}

Please confirm after creating the event."""
            
            console.print(f"\n[cyan]Syncing to Google Calendar...[/cyan]")
            console.print(f"[dim]Title:[/dim] {event_title}")
            console.print(f"[dim]Date:[/dim] {date_str}")
            console.print(f"[dim]Time:[/dim] {start_time_str} - {end_time_str}\n")
            
            # Send to calendar assistant within MCP context
            async with self.assistant.mcp_client:
                # Create chat session if needed
                if not self.assistant.chat:
                    await self.assistant.create_chat_session()
                
                # Send the command
                response = await self.assistant.send_message(calendar_command)
                
                console.print("[yellow]📅 Calendar Response:[/yellow]")
                console.print(f"[dim]{response}[/dim]\n")
                
                # If asking for confirmation, automatically confirm
                if "confirm?" in response.lower():
                    console.print("[cyan]Auto-confirming calendar event...[/cyan]\n")
                    response = await self.assistant.send_message("Yes, please confirm and create the event.")
                    console.print("[yellow]📅 Confirmation Response:[/yellow]")
                    console.print(f"[dim]{response}[/dim]\n")
                
                # Check if successful
                if any(keyword in response.lower() for keyword in ['successfully', 'created', 'scheduled', 'added']):
                    # Update database with calendar sync flag
                    import sqlite3
                    conn = sqlite3.connect('data/healthcare.db')
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        UPDATE appointments 
                        SET calendar_event_id = 'synced_via_assistant',
                            notes = COALESCE(notes, '') || '\n[Calendar synced to pinkpantherking20@gmail.com]'
                        WHERE appointment_id = ?
                    """, (appointment_id,))
                    
                    conn.commit()
                    conn.close()
                    
                    console.print("[green bold]✓ Appointment synced to Google Calendar![/green bold]\n")
                    return True, "Calendar event created successfully"
                else:
                    return False, f"Calendar response unclear: {response}"
                    
        except Exception as e:
            console.print(f"[red]✗ Error syncing to calendar: {e}[/red]\n")
            return False, f"Error: {str(e)}"
    
    def sync_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        """
        Synchronous wrapper to sync an appointment to calendar.
        
        Args:
            appointment_id: The appointment ID to sync
            
        Returns:
            Tuple of (success, message)
        """
        return asyncio.run(self._sync_appointment_to_calendar(appointment_id))
    
    async def _book_and_sync(
        self,
        user_id: int,
        doctor_id: int,
        appointment_date: str,
        start_time: str,
        reason: str = None
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Book an appointment and sync to calendar in one operation.
        
        Args:
            user_id: Patient ID
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD format
            start_time: Time in HH:MM format
            reason: Reason for appointment
            
        Returns:
            Tuple of (success, message, appointment_id)
        """
        # First, book the appointment in database
        success, message, appointment_id = self.scheduler.book_appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            start_time=start_time,
            reason=reason
        )
        
        if not success:
            return False, message, None
        
        console.print(f"[green]✓ Appointment booked in database (ID: {appointment_id})[/green]\n")
        
        # Now sync to calendar
        cal_success, cal_message = await self._sync_appointment_to_calendar(appointment_id)
        
        if not cal_success:
            console.print(f"[yellow]⚠️  Calendar sync failed: {cal_message}[/yellow]")
            console.print("[yellow]Appointment is saved in database but not synced to calendar[/yellow]\n")
        
        return success, message, appointment_id
    
    def book_with_calendar(
        self,
        user_id: int,
        doctor_id: int,
        appointment_date: str,
        start_time: str,
        reason: str = None
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Synchronous wrapper to book and sync appointment.
        
        Args:
            user_id: Patient ID
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD format
            start_time: Time in HH:MM format
            reason: Reason for appointment
            
        Returns:
            Tuple of (success, message, appointment_id)
        """
        return asyncio.run(self._book_and_sync(
            user_id, doctor_id, appointment_date, start_time, reason
        ))


async def test_calendar_sync():
    """Test the calendar sync functionality."""
    from datetime import timedelta
    
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]TESTING CALENDAR SYNC MODULE[/bold cyan]")
    console.print("=" * 70 + "\n")
    
    # Initialize
    sync = CalendarSync()
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    # Get scheduler
    scheduler = sync.scheduler
    
    # Get first doctor
    doctors = scheduler.get_all_doctors()
    if not doctors:
        console.print("[red]No doctors available[/red]")
        return
    
    doctor = doctors[0]
    console.print(f"[cyan]Doctor:[/cyan] {doctor['name']} ({doctor['specialty']})")
    console.print(f"[cyan]Calendar:[/cyan] {doctor['calendar_id']}\n")
    
    # Check availability
    slots = scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
    if not slots:
        console.print("[red]No available slots[/red]")
        return
    
    console.print(f"[green]✓ Found {len(slots)} available slots for {tomorrow}[/green]\n")
    
    # Create test patient
    user_id = scheduler.get_or_create_patient(
        name="Calendar Sync Test Patient",
        email="calendar.test@example.com",
        phone="555-SYNC"
    )
    
    console.print(f"[green]✓ Patient created (ID: {user_id})[/green]\n")
    
    # Book and sync
    console.print("[cyan]Booking appointment and syncing to calendar...[/cyan]\n")
    
    success, message, appointment_id = await sync._book_and_sync(
        user_id=user_id,
        doctor_id=doctor['doctor_id'],
        appointment_date=str(tomorrow),
        start_time=slots[3]['start_time'],  # Use 4th slot
        reason="Testing calendar sync integration"
    )
    
    if success:
        console.print(f"\n[green bold]✅ SUCCESS![/green bold]")
        console.print(f"[green]Appointment ID: {appointment_id}[/green]")
        console.print(f"[green]Message: {message}[/green]\n")
        
        console.print("[cyan]Check your Google Calendar at pinkpantherking20@gmail.com[/cyan]")
        console.print("[cyan]You should see the appointment event![/cyan]\n")
    else:
        console.print(f"\n[red]✗ Failed: {message}[/red]\n")
    
    console.print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_calendar_sync())
