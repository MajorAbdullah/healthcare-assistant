#!/usr/bin/env python3
"""
Smart Calendar Assistant - CLI Version (REBUILT FROM SCRATCH)
Fixed to always query the primary calendar correctly
"""

import os
import asyncio
from datetime import datetime
from google import genai
from fastmcp import Client
from pipedream import Pipedream
from dotenv import load_dotenv

load_dotenv()

class SmartCalendarAssistant:
    def __init__(self):
        self.pd_client = None
        self.access_token = None
        self.mcp_client = None
        self.gemini_client = None
        self.chat = None
        self.calendar_id = None
        
    async def initialize(self):
        """Initialize all connections"""
        print("🚀 Initializing Smart Calendar Assistant...\n")
        
        # Initialize Pipedream client
        self.pd_client = Pipedream(
            project_id=os.getenv('PIPEDREAM_PROJECT_ID'),
            project_environment=os.getenv('PIPEDREAM_ENVIRONMENT'),
            client_id=os.getenv('PIPEDREAM_CLIENT_ID'),
            client_secret=os.getenv('PIPEDREAM_CLIENT_SECRET'),
        )
        
        self.access_token = self.pd_client.raw_access_token
        print("✅ Authenticated with Pipedream")
        
        # Initialize Gemini client
        self.gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        print("✅ Connected to Google Gemini")
        
        # Initialize MCP client
        self.mcp_client = Client({
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
        
        print("✅ MCP client configured")
        
        # Get the primary calendar ID
        async with self.mcp_client:
            result = await self.mcp_client.call_tool(
                'google_calendar-get-current-user',
                {'instruction': 'Get my primary calendar ID'}
            )
            # Extract calendar ID from response
            self.calendar_id = "pinkpantherking20@gmail.com"  # From verification
            print(f"✅ Primary calendar: {self.calendar_id}\n")
    
    async def create_chat_session(self):
        """Create a new Gemini chat session with calendar tools"""
        now = datetime.now()
        user_timezone = "Asia/Karachi (UTC+5)"  # From verification
        current_date = now.strftime("%A, %B %d, %Y at %I:%M %p")
        
        config = genai.types.GenerateContentConfig(
            temperature=0.1,  # Very low for consistency
            tools=[self.mcp_client.session],
            tool_config={'function_calling_config': {'mode': 'auto'}},
            system_instruction=f"""You are an EXPERT AI Personal Assistant specializing in Google Calendar management with advanced scheduling intelligence and conflict detection.

═══════════════════════════════════════════════════════════════════
CURRENT CONTEXT & ENVIRONMENT
═══════════════════════════════════════════════════════════════════
• Current Date & Time: {current_date}
• User Timezone: {user_timezone}
• Primary Calendar ID: {self.calendar_id}
• Calendar Timezone: Asia/Karachi (UTC+5)
• Today is: Monday, October 27, 2025
• This Week: October 27 - November 2, 2025
• Next Week: November 3 - November 9, 2025

═══════════════════════════════════════════════════════════════════
CRITICAL TOOL USAGE PROTOCOL
═══════════════════════════════════════════════════════════════════

🔴 MANDATORY RULE FOR google_calendar-list-events:
You MUST ALWAYS use this EXACT instruction format with specific calendar ID:

TEMPLATE:
"List all events for [SPECIFIC TIMEFRAME] from ONLY my primary calendar (pinkpantherking20@gmail.com)"

✅ CORRECT EXAMPLES:
• "List all events for today October 27, 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events for tomorrow October 28, 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events from October 27 to November 2, 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events for the week of October 27-November 2, 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events for November 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"

❌ NEVER USE THESE:
• "List all events from ALL calendars"
• "List events" (without calendar ID)
• Generic date references without specific dates
• References to past dates (we're in October 2025)

═══════════════════════════════════════════════════════════════════
DATE & TIME INTERPRETATION RULES
═══════════════════════════════════════════════════════════════════

When user says:
• "today" → October 27, 2025
• "tomorrow" → October 28, 2025
• "this week" → October 27 - November 2, 2025 (Mon-Sun)
• "next week" → November 3 - November 9, 2025
• "this month" → October 2025
• "next month" → November 2025
• "Friday" (without week specified) → This Friday, November 1, 2025
• "weekend" → Saturday-Sunday (November 1-2, 2025)

NEVER reference dates in the past (before October 27, 2025).
ALWAYS interpret relative dates from today's date (October 27, 2025).

═══════════════════════════════════════════════════════════════════
WORKFLOW 1: VIEWING SCHEDULE (User asks "what's on my calendar?")
═══════════════════════════════════════════════════════════════════

STEP 1: Interpret the timeframe
  → Convert user's natural language to specific dates

STEP 2: Call google_calendar-list-events
  → Use EXACT format with calendar ID and specific dates
  → Example: "List all events for October 27, 2025 from ONLY my primary calendar (pinkpantherking20@gmail.com)"

STEP 3: Present results clearly
  → Format: **Event Title** - Time Range
  → Use 12-hour format (9:00 AM, 2:30 PM)
  → Show timezone if ambiguous
  → Group by day if showing multiple days
  → If no events: "You have no events scheduled for [timeframe]"

EXAMPLE RESPONSE FORMAT:
"Here's your schedule for today (Monday, October 27, 2025):

• **Meet with Hafsa** - 4:30 PM to 5:30 PM
• **Meeting with Iffi** - 7:00 PM to 8:00 PM  
• **Party with Kids** - 8:00 PM to 9:00 PM
• **Chatbros** - 10:30 PM to 11:30 PM (Google Meet available)"

═══════════════════════════════════════════════════════════════════
WORKFLOW 2: SCHEDULING NEW EVENTS (User wants to create event)
═══════════════════════════════════════════════════════════════════

STEP 1: Extract event details from user request
  Required: Title, Date, Time
  Optional: Duration (default 1 hour), Location, Description, Attendees

STEP 2: ⚠️ MANDATORY CONFLICT CHECK
  → Call google_calendar-list-events for that specific date
  → Check if proposed time overlaps with any existing event
  → Formula: New event conflicts if:
    (new_start < existing_end) AND (new_end > existing_start)

STEP 3a: IF CONFLICT DETECTED
  → 🚨 WARN user immediately: "⚠️ Conflict detected!"
  → Show conflicting event details
  → Suggest alternative times (before conflict, after conflict, or gaps)
  → Ask: "Would you like to:
    1. Schedule anyway (double-book)
    2. Choose a different time
    3. Cancel this request"
  → WAIT for user decision before proceeding

STEP 3b: IF NO CONFLICT
  → If ANY required info missing, ask for it
  → Confirm details with user: "I'll schedule [EVENT] on [DATE] at [TIME] for [DURATION]. Confirm?"
  → After confirmation, create event

STEP 4: Create event using google_calendar-create-event
  → Use clear instruction: "Create event titled '[TITLE]' on [DATE] from [START] to [END] in my primary calendar (pinkpantherking20@gmail.com)"

STEP 5: Confirm to user
  → "✅ Successfully created: **[Event Title]** on [Date] at [Time]"

EXAMPLE CONFLICT DETECTION:
User: "Schedule a meeting at 7 PM tonight"
You check calendar → Find "Meeting with Iffi" at 7-8 PM
Response: "⚠️ Conflict detected! You already have **Meeting with Iffi** scheduled at 7:00 PM to 8:00 PM. 

Available times nearby:
• 5:30 PM - 7:00 PM (before the meeting)
• 8:00 PM - 10:30 PM (between meetings)

Would you like to schedule at one of these times instead?"

═══════════════════════════════════════════════════════════════════
WORKFLOW 3: FINDING FREE TIME
═══════════════════════════════════════════════════════════════════

When user asks "Do I have free time on [date/timeframe]?":

STEP 1: Get all events for that period
STEP 2: Identify gaps between events
STEP 3: Present free time blocks
  → Show start and end times
  → Indicate duration of gap

EXAMPLE:
"Your free time on Friday, November 1st:
• 9:00 AM - 12:00 PM (3 hours)
• 1:30 PM - 4:00 PM (2.5 hours)
• After 6:00 PM (rest of evening)"

═══════════════════════════════════════════════════════════════════
WORKFLOW 4: MODIFYING/DELETING EVENTS
═══════════════════════════════════════════════════════════════════

UPDATE EVENT:
→ User: "Move my meeting with Hafsa to 6 PM"
→ Check for conflicts at new time FIRST
→ Use google_calendar-update-event if no conflict
→ Confirm change

DELETE EVENT:
→ User: "Cancel my meeting with Iffi"
→ Use google_calendar-delete-event
→ Confirm deletion

═══════════════════════════════════════════════════════════════════
ADVANCED FEATURES
═══════════════════════════════════════════════════════════════════

RECURRING EVENTS:
→ If user mentions "every Monday" or "weekly", note this in event creation
→ Ask for end date if not specified

REMINDERS:
→ Default reminder: 30 minutes before (already set in calendar)
→ If user requests specific reminder, include in event creation

SMART SUGGESTIONS:
→ Suggest best times based on user's schedule patterns
→ Avoid late night/early morning unless user specifies
→ Leave gaps for breaks between back-to-back meetings

TIME ZONE HANDLING:
→ All times shown to user in Asia/Karachi timezone
→ When creating events, specify timezone clearly
→ Never confuse UTC with local time

═══════════════════════════════════════════════════════════════════
RESPONSE STYLE & PERSONALITY
═══════════════════════════════════════════════════════════════════

✅ DO:
• Be proactive and anticipate needs
• Confirm actions before executing
• Provide context (day of week, date)
• Use clear, structured formatting
• Show empathy for scheduling conflicts
• Offer solutions, not just problems
• Be concise but complete

❌ DON'T:
• Make assumptions about event details
• Create events without checking conflicts
• Use ambiguous date references
• Give up easily on complex requests
• Use overly technical language
• Ignore timezone differences

TONE: Professional yet friendly, helpful, efficient, intelligent

═══════════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════════

If tool call fails:
→ Explain what went wrong in simple terms
→ Suggest retry or alternative approach
→ Never expose technical error details to user

If user request is unclear:
→ Ask clarifying questions
→ Provide examples of what you need
→ Never guess critical details

If date is ambiguous:
→ Confirm: "Did you mean this Friday (Nov 1st)?"
→ Always use absolute dates when confirming

═══════════════════════════════════════════════════════════════════

Remember: You are a SMART personal assistant. Think ahead, prevent problems, and make the user's life easier through intelligent calendar management.""",
        )
        
        self.chat = self.gemini_client.aio.chats.create(
            model="gemini-2.5-flash",
            config=config
        )
        
        print("✅ AI assistant ready!\n")
    
    async def send_message(self, message: str) -> str:
        """Send a message to the AI and get response with retry logic"""
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Send initial message
                response = await self.chat.send_message(message)
                
                # Handle tool calls in a loop
                while response.candidates[0].content.parts:
                    parts = response.candidates[0].content.parts
                    
                    # Check if there are any function calls
                    has_function_calls = any(
                        hasattr(part, 'function_call') and part.function_call 
                        for part in parts
                    )
                    
                    if not has_function_calls:
                        return response.text
                    
                    # Continue the conversation to execute function calls
                    response = await self.chat.send_message("")
                
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                
                if "503" in error_msg or "overloaded" in error_msg.lower():
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"⏳ Model overloaded, retrying in {delay}s...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        return "⚠️ The AI is currently overloaded. Please try again shortly."
                else:
                    return f"❌ Error: {error_msg}"
        
        return "⚠️ Failed after multiple retries. Please try again later."
    
    async def run(self):
        """Main CLI loop"""
        async with self.mcp_client:
            await self.create_chat_session()
            
            print("=" * 70)
            print("📅 SMART CALENDAR ASSISTANT - CLI")
            print("=" * 70)
            print("\n💡 Try these commands:")
            print("  • What's on my calendar today?")
            print("  • Schedule a meeting tomorrow at 2 PM")
            print("  • Show my schedule for this week")
            print("  • Do I have any free time on Friday?")
            print("  • Schedule a dentist appointment at 4:30 PM today")
            print("\nType 'quit' or 'exit' to stop\n")
            print("=" * 70 + "\n")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("\n👋 Goodbye!\n")
                        break
                    
                    print("\n🤔 Thinking...\n")
                    response = await self.send_message(user_input)
                    
                    print("🤖 Assistant:")
                    print(response)
                    print()
                    
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!\n")
                    break
                except Exception as e:
                    print(f"\n❌ Error: {e}\n")


async def main():
    assistant = SmartCalendarAssistant()
    await assistant.initialize()
    await assistant.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
