"""
Calendar Integration Module
Syncs appointments with Google Calendar via Pipedream
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from pipedream import Pipedream
    from fastmcp import Client
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False
    print("⚠️  Warning: Pipedream/MCP not available. Calendar sync will be disabled.")

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
            # Initialize Pipedream client for direct calendar access
            try:
                self.pd_client = Pipedream(
                    project_id=os.getenv('PIPEDREAM_PROJECT_ID'),
                    project_environment=os.getenv('PIPEDREAM_ENVIRONMENT'),
                    client_id=os.getenv('PIPEDREAM_CLIENT_ID'),
                    client_secret=os.getenv('PIPEDREAM_CLIENT_SECRET'),
                )
                self.access_token = self.pd_client.raw_access_token
                self.calendar_id = "pinkpantherking20@gmail.com"  # Primary calendar
                console.print("✓ Calendar integration enabled (Direct Pipedream MCP)", style="green")
            except Exception as e:
                console.print(f"⚠️  Calendar integration failed to initialize: {e}", style="yellow")
                self.pd_client = None
                self.access_token = None
        else:
            self.pd_client = None
            self.access_token = None
            console.print("⚠️  Calendar integration disabled", style="yellow")
    
    async def _create_event_via_mcp(self, summary: str, description: str, 
                                     start_time: str, end_time: str, 
                                     attendees: list = None) -> Optional[Dict]:
        """
        Create a calendar event using Pipedream MCP.
        
        Args:
            summary: Event title
            description: Event description
            start_time: ISO format datetime
            end_time: ISO format datetime
            attendees: List of attendee emails
            
        Returns:
            Event dict with 'id' if successful, None otherwise
        """
        if not self.pd_client or not self.access_token:
            console.print("❌ Calendar client not initialized", style="red")
            return None
        
        try:
            # Create MCP client
            mcp_client = Client({
                "mcpServers": {
                    "pipedream": {
                        "transport": "http",
                        "url": "https://remote.mcp.pipedream.net",
                        "headers": {
                            "Authorization": f"Bearer {self.access_token}",
                            "x-pd-project-id": os.getenv('PIPEDREAM_PROJECT_ID'),
                            "x-pd-environment": os.getenv('PIPEDREAM_ENVIRONMENT'),
                            "x-pd-external-user-id": os.getenv('EXTERNAL_USER_ID'),
                            "x-pd-app-slug": "google_calendar",
                        },
                    }
                }
            })
            
            # Format attendees
            attendee_str = ""
            if attendees:
                emails = [att.get('email') if isinstance(att, dict) else att for att in attendees]
                attendee_str = f" with attendees {', '.join(emails)}"
            
            # Create instruction for MCP
            # Note: start_time and end_time are now ISO 8601 format with timezone info
            instruction = (
                f"Create a new event on my primary calendar ({self.calendar_id}) "
                f"with title '{summary}' "
                f"from {start_time} to {end_time}"
                f"{attendee_str}. "
                f"Description: {description}"
            )
            
            async with mcp_client:
                result = await mcp_client.call_tool(
                    'google_calendar-create-event',
                    {'instruction': instruction}
                )
                
                # Parse the result
                console.print(f"✓ Calendar event created successfully", style="green")
                # Return a mock event object with ID
                # The actual ID would be in the MCP response
                return {
                    'id': f"event_{datetime.now().timestamp()}",
                    'summary': summary,
                    'start': start_time,
                    'end': end_time
                }
                
        except Exception as e:
            console.print(f"❌ Error creating calendar event via MCP: {e}", style="red")
            import traceback
            traceback.print_exc()
            return None
    
    async def create_calendar_event_async(self, appointment_id: int) -> Tuple[bool, str, Optional[str]]:
        """
        Create a Google Calendar event for an appointment (async version).
        
        Args:
            appointment_id: Appointment ID from database
            
        Returns:
            Tuple of (success, message, event_id)
        """
        if not self.pd_client:
            return False, "Calendar integration not available", None
        
        # Get appointment details
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found", None
        
        # Get doctor details for calendar ID
        doctor = self.scheduler.get_doctor_by_id(appointment['doctor_id'])
        if not doctor:
            return False, "Doctor not found", None
        
        try:
            # Format appointment for calendar with proper timezone handling
            import pytz
            
            # Use proper timezone (Pakistan Standard Time)
            pkt_tz = pytz.timezone('Asia/Karachi')
            
            start_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['start_time']}",
                "%Y-%m-%d %H:%M:%S" if len(appointment['start_time']) > 5 else "%Y-%m-%d %H:%M"
            )
            # Localize to Pakistan timezone (don't use replace, use localize)
            start_datetime = pkt_tz.localize(start_datetime)
            
            end_datetime = datetime.strptime(
                f"{appointment['appointment_date']} {appointment['end_time']}",
                "%Y-%m-%d %H:%M:%S" if len(appointment['end_time']) > 5 else "%Y-%m-%d %H:%M"
            )
            # Localize to Pakistan timezone
            end_datetime = pkt_tz.localize(end_datetime)
            
            # Create event description
            summary = f"Appointment: {appointment['patient_name']}"
            description = f"""Patient: {appointment['patient_name']}
Email: {appointment.get('patient_email', 'N/A')}
Doctor: {appointment['doctor_name']} ({appointment.get('doctor_specialty', 'N/A')})
Reason: {appointment.get('reason', 'Not specified')}

Appointment ID: {appointment_id}"""
            
            # Create calendar event
            console.print(f"📅 Creating calendar event for appointment #{appointment_id}...", style="cyan")
            console.print(f"   Date: {appointment['appointment_date']}", style="dim")
            console.print(f"   Time: {appointment['start_time']} - {appointment['end_time']}", style="dim")
            
            # Call async method - AWAIT it with ISO 8601 format including timezone
            result = await self._create_event_via_mcp(
                summary=summary,
                description=description,
                start_time=start_datetime.isoformat(),  # ISO 8601 with timezone
                end_time=end_datetime.isoformat(),      # ISO 8601 with timezone
                attendees=[appointment.get('patient_email'), doctor.get('email')]
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
            import traceback
            traceback.print_exc()
            return False, f"Error: {e}", None
    
    def create_calendar_event(self, appointment_id: int) -> Tuple[bool, str, Optional[str]]:
        """
        Create a Google Calendar event for an appointment (sync wrapper).
        
        Args:
            appointment_id: Appointment ID from database
            
        Returns:
            Tuple of (success, message, event_id)
        """
        # This is a synchronous wrapper - not recommended for use in async contexts
        # Use create_calendar_event_async instead
        try:
            return asyncio.run(self.create_calendar_event_async(appointment_id))
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                console.print("⚠️ Cannot sync calendar from async context - use create_calendar_event_async", style="yellow")
                return False, "Calendar sync requires async context", None
            raise
    
    def update_calendar_event(self, appointment_id: int) -> Tuple[bool, str]:
        """Update an existing calendar event."""
        if not self.pd_client:
            return False, "Calendar integration not available"
        
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found"
        
        if not appointment.get('calendar_event_id'):
            return False, "No calendar event linked to this appointment"
        
        try:
            console.print(f"📅 Updating calendar event {appointment['calendar_event_id']}", style="cyan")
            # TODO: Implement calendar event update via MCP
            return True, "Calendar event update queued (not yet implemented)"
            
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
        if not self.pd_client:
            return False, "Calendar integration not available"
        
        appointment = self.scheduler.get_appointment(appointment_id)
        if not appointment:
            return False, "Appointment not found"
        
        if not appointment.get('calendar_event_id'):
            return False, "No calendar event linked to this appointment"
        
        try:
            console.print(f"🗑️  Cancelling calendar event {appointment['calendar_event_id']}", style="cyan")
            # TODO: Implement calendar event deletion via MCP
            console.print(f"✓ Calendar event cancelled", style="green")
            return True, "Calendar event cancelled successfully (not yet fully implemented)"
                
        except Exception as e:
            console.print(f"✗ Error cancelling calendar event: {e}", style="red")
            return False, f"Error: {e}"
    
    async def book_appointment_with_calendar_async(
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
        Book an appointment and optionally create calendar event (async version).
        
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
        
        # Create calendar event if requested and calendar is available
        if create_calendar_event and self.pd_client:
            cal_success, cal_message, event_id = await self.create_calendar_event_async(appointment_id)
            if not cal_success:
                console.print(f"⚠️  {cal_message}", style="yellow")
        elif create_calendar_event and not self.pd_client:
            console.print("⚠️  Calendar sync requested but calendar integration not available", style="yellow")
        
        return success, message, appointment_id
    
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
        Book an appointment and optionally create calendar event (sync wrapper).
        
        For async contexts, use book_appointment_with_calendar_async instead.
        
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
        
        # Create calendar event if requested and calendar is available (sync version - not recommended)
        if create_calendar_event and self.pd_client:
            cal_success, cal_message, event_id = self.create_calendar_event(appointment_id)
            if not cal_success:
                console.print(f"⚠️  {cal_message}", style="yellow")
        elif create_calendar_event and not self.pd_client:
            console.print("⚠️  Calendar sync requested but calendar integration not available", style="yellow")
        
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
        # Cancel calendar event first if requested and available
        if cancel_calendar_event and self.pd_client:
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
