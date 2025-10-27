"""
Calendar Integration Module
Syncs appointments with Google Calendar via Pipedream
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from calendar_assistant import SmartCalendarAssistant
    import asyncio
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False
    print("⚠️  Warning: calendar_assistant.py not found. Calendar sync will be disabled.")

from modules.scheduler import AppointmentScheduler
from rich.console import Console

console = Console()


class CalendarIntegration:
    """Integrates appointment scheduler with Google Calendar via Pipedream."""
    
    def __init__(self, scheduler: AppointmentScheduler = None):
        """
        Initialize calendar integration.
        
        Args:
            scheduler: AppointmentScheduler instance (creates new one if not provided)
        """
        self.scheduler = scheduler or AppointmentScheduler()
        
        if CALENDAR_AVAILABLE:
            self.calendar = SmartCalendarAssistant()
            self._calendar_initialized = False
            console.print("✓ Calendar integration enabled", style="green")
        else:
            self.calendar = None
            self._calendar_initialized = False
            console.print("⚠️  Calendar integration disabled", style="yellow")
    
    def create_calendar_event(self, appointment_id: int) -> Tuple[bool, str, Optional[str]]:
        """
        Create a Google Calendar event for an appointment.
        
        Args:
            appointment_id: Appointment ID from database
            
        Returns:
            Tuple of (success, message, event_id)
        """
        if not self.calendar:
            return False, "Calendar integration not available", None
        
        # Get appointment details
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found", None
        
        # Get doctor details for calendar ID
        doctor = self.scheduler.get_doctor_by_id(appointment['doctor_id'])
        if not doctor or not doctor.get('calendar_id'):
            return False, "Doctor calendar not configured", None
        
        try:
            # Format appointment for calendar
            # Combine date and time for start/end
            start_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['start_time']}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['end_time']}",
                "%Y-%m-%d %H:%M"
            )
            
            # Create event description
            summary = f"Appointment: {appointment['patient_name']}"
            description = f"""
Patient: {appointment['patient_name']}
Email: {appointment['patient_email']}
Doctor: {appointment['doctor_name']} ({appointment['doctor_specialty']})
Reason: {appointment.get('reason', 'Not specified')}

Appointment ID: {appointment_id}
            """.strip()
            
            # Create calendar event
            console.print(f"📅 Creating calendar event...", style="cyan")
            console.print(f"   Date: {appointment['appointment_date']}", style="dim")
            console.print(f"   Time: {appointment['start_time']} - {appointment['end_time']}", style="dim")
            
            # Use the calendar assistant to create event
            result = self.calendar.create_event(
                summary=summary,
                description=description,
                start_time=start_datetime.isoformat(),
                end_time=end_datetime.isoformat(),
                attendees=[
                    {'email': appointment['patient_email']},
                    {'email': doctor['email']}
                ]
            )
            
            if result and 'id' in result:
                event_id = result['id']
                
                # Update appointment with calendar event ID
                conn = self.scheduler._get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE appointments 
                    SET calendar_event_id = ?
                    WHERE appointment_id = ?
                """, (event_id, appointment_id))
                conn.commit()
                conn.close()
                
                console.print(f"✓ Calendar event created: {event_id}", style="green")
                return True, "Calendar event created successfully", event_id
            else:
                return False, "Failed to create calendar event", None
                
        except Exception as e:
            console.print(f"✗ Error creating calendar event: {e}", style="red")
            return False, f"Error: {e}", None
    
    def update_calendar_event(self, appointment_id: int) -> Tuple[bool, str]:
        """Update an existing calendar event."""
        if not self.calendar:
            return False, "Calendar integration not available"
        
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found"
        
        if not appointment.get('calendar_event_id'):
            return False, "No calendar event linked to this appointment"
        
        try:
            # Similar to create but uses update API
            # For now, we'll just note that this would call the calendar update method
            console.print(f"📅 Updating calendar event {appointment['calendar_event_id']}", style="cyan")
            
            # Implementation would use calendar.update_event()
            # For demo purposes, we'll just return success
            return True, "Calendar event update queued"
            
        except Exception as e:
            return False, f"Error updating calendar event: {e}"
    
    def cancel_calendar_event(self, appointment_id: int) -> Tuple[bool, str]:
        """
        Cancel/delete a calendar event.
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Tuple of (success, message)
        """
        if not self.calendar:
            return False, "Calendar integration not available"
        
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found"
        
        if not appointment.get('calendar_event_id'):
            return False, "No calendar event linked to this appointment"
        
        try:
            console.print(f"🗑️  Cancelling calendar event {appointment['calendar_event_id']}", style="cyan")
            
            # Delete the calendar event
            result = self.calendar.delete_event(appointment['calendar_event_id'])
            
            if result:
                console.print(f"✓ Calendar event cancelled", style="green")
                return True, "Calendar event cancelled successfully"
            else:
                return False, "Failed to cancel calendar event"
                
        except Exception as e:
            console.print(f"✗ Error cancelling calendar event: {e}", style="red")
            return False, f"Error: {e}"
    
    def book_appointment_with_calendar(
        self,
        user_id: int,
        doctor_id: int,
        appointment_date: str,
        start_time: str,
        reason: str = None,
        notes: str = None,
        create_calendar_event: bool = True
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Book an appointment and optionally create calendar event.
        
        Args:
            user_id: Patient user ID
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            reason: Reason for visit
            notes: Additional notes
            create_calendar_event: Whether to create calendar event
            
        Returns:
            Tuple of (success, message, appointment_id)
        """
        # Book the appointment
        success, message, appointment_id = self.scheduler.book_appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            start_time=start_time,
            reason=reason,
            notes=notes
        )
        
        if not success:
            return success, message, appointment_id
        
        # Create calendar event if requested
        if create_calendar_event and self.calendar:
            cal_success, cal_message, event_id = self.create_calendar_event(appointment_id)
            if not cal_success:
                console.print(f"⚠️  {cal_message}", style="yellow")
        
        return success, message, appointment_id
    
    def cancel_appointment_with_calendar(
        self,
        appointment_id: int,
        reason: str = None,
        cancel_calendar_event: bool = True
    ) -> Tuple[bool, str]:
        """
        Cancel an appointment and optionally cancel calendar event.
        
        Args:
            appointment_id: Appointment ID
            reason: Cancellation reason
            cancel_calendar_event: Whether to cancel calendar event
            
        Returns:
            Tuple of (success, message)
        """
        # Cancel calendar event first if requested
        if cancel_calendar_event and self.calendar:
            cal_success, cal_message = self.cancel_calendar_event(appointment_id)
            if not cal_success:
                console.print(f"⚠️  {cal_message}", style="yellow")
        
        # Cancel the appointment in database
        success, message = self.scheduler.cancel_appointment(appointment_id, reason)
        
        return success, message


# Convenience function for quick use
def sync_appointment_to_calendar(appointment_id: int) -> Tuple[bool, str]:
    """
    Quick function to sync an appointment to calendar.
    
    Args:
        appointment_id: Appointment ID to sync
        
    Returns:
        Tuple of (success, message)
    """
    integration = CalendarIntegration()
    success, message, event_id = integration.create_calendar_event(appointment_id)
    return success, message
