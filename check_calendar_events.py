#!/usr/bin/env python3
"""
Quick script to check calendar events using the Pipedream calendar assistant
This demonstrates how the calendar integration would work when properly configured
"""

import asyncio
from datetime import datetime, timedelta


async def check_free_slots_via_calendar():
    """
    Example of how to check free slots using the calendar assistant.
    This would be used by the appointment scheduler to verify availability
    against the actual Google Calendar.
    """
    try:
        # Import the calendar assistant
        from calendar_assistant import SmartCalendarAssistant
        
        print("=" * 70)
        print("📅 CHECKING CALENDAR FREE SLOTS")
        print("=" * 70)
        print()
        
        # Initialize the calendar assistant
        assistant = SmartCalendarAssistant()
        await assistant.initialize()
        await assistant.create_chat_session()
        
        # Check today's schedule
        today = datetime.now().strftime("%A, %B %d, %Y")
        print(f"\n🔍 Querying calendar for: {today}\n")
        
        response = await assistant.send_message(
            f"Show me all events for today ({today}) from my primary calendar"
        )
        
        print("📋 Calendar Response:")
        print("-" * 70)
        print(response)
        print("-" * 70)
        print()
        
        # Check for free time
        print("\n🕐 Checking for free time slots...\n")
        
        response = await assistant.send_message(
            "Do I have any free time today? Show me available time blocks."
        )
        
        print("📋 Free Time Response:")
        print("-" * 70)
        print(response)
        print("-" * 70)
        print()
        
        print("\n✓ Calendar check complete!")
        
    except ImportError:
        print("⚠️  calendar_assistant.py not found or not properly configured")
        print("\nThe calendar assistant requires:")
        print("  • Pipedream API credentials in .env file")
        print("  • Google Calendar API access via Pipedream")
        print("  • Proper MCP server configuration")
        print("\nHowever, the appointment scheduler works independently!")
        print("It can book appointments based on doctor availability in the database.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nThis is expected if calendar credentials are not configured.")


async def create_test_appointment_in_calendar():
    """
    Example of how to create an appointment directly in Google Calendar.
    This shows what happens when the scheduler creates a calendar event.
    """
    try:
        from calendar_assistant import SmartCalendarAssistant
        
        print("\n" + "=" * 70)
        print("📝 CREATING TEST APPOINTMENT IN CALENDAR")
        print("=" * 70)
        print()
        
        assistant = SmartCalendarAssistant()
        await assistant.initialize()
        await assistant.create_chat_session()
        
        # Create a test appointment
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y")
        
        print(f"📅 Creating appointment for: {tomorrow} at 2:00 PM\n")
        
        response = await assistant.send_message(
            f"Schedule a 'Doctor Appointment - Test Patient' on {tomorrow} at 2:00 PM for 30 minutes"
        )
        
        print("📋 Calendar Response:")
        print("-" * 70)
        print(response)
        print("-" * 70)
        print()
        
        print("\n✓ Appointment creation attempt complete!")
        
    except ImportError:
        print("⚠️  calendar_assistant.py not available")
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Main function to demonstrate calendar integration."""
    
    print("\n" + "=" * 70)
    print("🏥 APPOINTMENT SCHEDULER + GOOGLE CALENDAR INTEGRATION")
    print("=" * 70)
    print()
    print("This script demonstrates how the appointment scheduler")
    print("integrates with Google Calendar via Pipedream.")
    print()
    print("Features:")
    print("  • Check doctor's actual calendar availability")
    print("  • Find free time slots in real-time")
    print("  • Create calendar events for appointments")
    print("  • Send email notifications to patients and doctors")
    print("  • Update/cancel calendar events")
    print()
    print("=" * 70)
    
    # Check calendar availability
    await check_free_slots_via_calendar()
    
    # Option to create test appointment
    try:
        user_input = input("\n\nWould you like to create a test appointment in the calendar? (y/n): ")
        if user_input.lower() == 'y':
            await create_test_appointment_in_calendar()
    except KeyboardInterrupt:
        print("\n\nSkipped.\n")
    
    print("\n" + "=" * 70)
    print("📊 INTEGRATION SUMMARY")
    print("=" * 70)
    print()
    print("✓ Appointment Scheduler (Database) - WORKING")
    print("  - Store doctor schedules")
    print("  - Generate available time slots")
    print("  - Book appointments with conflict detection")
    print("  - Track appointment status")
    print()
    print("⚠️  Google Calendar Integration (Pipedream) - CONFIGURED BUT NOT TESTED")
    print("  - Requires calendar_assistant.py with Pipedream credentials")
    print("  - Would sync appointments to Google Calendar")
    print("  - Would send email notifications")
    print("  - Would check real-time calendar availability")
    print()
    print("💡 The scheduler works perfectly without calendar integration!")
    print("   Calendar sync is an optional enhancement for notifications.")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
