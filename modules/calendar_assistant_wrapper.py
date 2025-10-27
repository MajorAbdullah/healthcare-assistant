"""
Calendar Assistant Wrapper for Appointment Scheduler
Properly integrates the async calendar_assistant with the scheduler
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from calendar_assistant import SmartCalendarAssistant
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False


class CalendarAssistantWrapper:
    """Synchronous wrapper for the async SmartCalendarAssistant."""
    
    def __init__(self):
        """Initialize the calendar assistant wrapper."""
        self.assistant = None
        self.initialized = False
        
        if not CALENDAR_AVAILABLE:
            print("⚠️  Warning: calendar_assistant not available")
            return
        
        try:
            # Initialize the assistant
            self.assistant = SmartCalendarAssistant()
            self.initialized = True
        except Exception as e:
            print(f"⚠️  Failed to initialize calendar assistant: {e}")
            self.initialized = False
    
    async def _initialize_async(self):
        """Initialize the assistant asynchronously."""
        if not self.initialized:
            return False
        
        try:
            await self.assistant.initialize()
            await self.assistant.create_chat_session()
            return True
        except Exception as e:
            print(f"⚠️  Failed to initialize calendar: {e}")
            return False
    
    async def _create_event_async(self, summary: str, description: str, 
                                  start_datetime: str, end_datetime: str,
                                  attendee_email: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Create a calendar event asynchronously.
        
        Args:
            summary: Event title
            description: Event description
            start_datetime: Start time in ISO format
            end_datetime: End time in ISO format
            attendee_email: Optional attendee email
            
        Returns:
            Tuple of (success, message, event_id)
        """
        if not self.initialized:
            return False, "Calendar not initialized", None
        
        try:
            async with self.assistant.mcp_client:
                await self.assistant.create_chat_session()
                
                # Format the date nicely
                start_dt = datetime.fromisoformat(start_datetime)
                end_dt = datetime.fromisoformat(end_datetime)
                
                date_str = start_dt.strftime("%B %d, %Y")
                start_time_str = start_dt.strftime("%I:%M %p")
                end_time_str = end_dt.strftime("%I:%M %p")
                
                # Build the event creation message
                message = f"""Schedule an event titled "{summary}" on {date_str} from {start_time_str} to {end_time_str}.
                
Event details:
{description}"""
                
                if attendee_email:
                    message += f"\n\nAdd {attendee_email} as an attendee."
                
                # Send to assistant
                response = await self.assistant.send_message(message)
                
                # Check if successful
                if "successfully" in response.lower() or "created" in response.lower():
                    # Extract event ID if possible (simplified - would need better parsing)
                    return True, response, "calendar_event_created"
                else:
                    return False, response, None
                    
        except Exception as e:
            return False, f"Error creating event: {e}", None
    
    async def _delete_event_async(self, event_description: str) -> Tuple[bool, str]:
        """
        Delete a calendar event asynchronously.
        
        Args:
            event_description: Description to identify the event
            
        Returns:
            Tuple of (success, message)
        """
        if not self.initialized:
            return False, "Calendar not initialized"
        
        try:
            async with self.assistant.mcp_client:
                await self.assistant.create_chat_session()
                
                message = f"Cancel/delete the event: {event_description}"
                response = await self.assistant.send_message(message)
                
                if "cancelled" in response.lower() or "deleted" in response.lower():
                    return True, response
                else:
                    return False, response
                    
        except Exception as e:
            return False, f"Error deleting event: {e}"
    
    async def _check_free_time_async(self, date: str) -> Tuple[bool, str]:
        """
        Check for free time on a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Tuple of (success, message with free time info)
        """
        if not self.initialized:
            return False, "Calendar not initialized"
        
        try:
            async with self.assistant.mcp_client:
                await self.assistant.create_chat_session()
                
                # Format date nicely
                dt = datetime.strptime(date, "%Y-%m-%d")
                date_str = dt.strftime("%A, %B %d, %Y")
                
                message = f"Show me my schedule for {date_str} and tell me what free time I have."
                response = await self.assistant.send_message(message)
                
                return True, response
                
        except Exception as e:
            return False, f"Error checking free time: {e}"
    
    def create_event(self, summary: str, description: str, 
                    start_datetime: str, end_datetime: str,
                    attendee_email: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Create a calendar event (synchronous wrapper).
        
        Args:
            summary: Event title
            description: Event description
            start_datetime: Start time in ISO format
            end_datetime: End time in ISO format
            attendee_email: Optional attendee email
            
        Returns:
            Tuple of (success, message, event_id)
        """
        if not self.initialized:
            return False, "Calendar not available", None
        
        return asyncio.run(self._create_event_async(
            summary, description, start_datetime, end_datetime, attendee_email
        ))
    
    def delete_event(self, event_description: str) -> Tuple[bool, str]:
        """
        Delete a calendar event (synchronous wrapper).
        
        Args:
            event_description: Description to identify the event
            
        Returns:
            Tuple of (success, message)
        """
        if not self.initialized:
            return False, "Calendar not available"
        
        return asyncio.run(self._delete_event_async(event_description))
    
    def check_free_time(self, date: str) -> Tuple[bool, str]:
        """
        Check for free time on a specific date (synchronous wrapper).
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Tuple of (success, message with free time info)
        """
        if not self.initialized:
            return False, "Calendar not available"
        
        return asyncio.run(self._check_free_time_async(date))


def test_wrapper():
    """Quick test of the wrapper."""
    from datetime import datetime, timedelta
    
    print("\n" + "=" * 70)
    print("TESTING CALENDAR ASSISTANT WRAPPER")
    print("=" * 70 + "\n")
    
    wrapper = CalendarAssistantWrapper()
    
    if not wrapper.initialized:
        print("❌ Calendar wrapper not initialized")
        return
    
    print("✅ Calendar wrapper initialized\n")
    
    # Test 1: Check free time for tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    print(f"📅 Checking free time for {tomorrow}...\n")
    
    success, message = wrapper.check_free_time(str(tomorrow))
    
    if success:
        print("✅ Free time check successful:")
        print(message)
    else:
        print(f"❌ Failed: {message}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    test_wrapper()
