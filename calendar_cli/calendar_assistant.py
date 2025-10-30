#!/usr/bin/env python3
"""
Smart Calendar Assistant - CLI Version
A standalone CLI application for managing Google Calendar with AI assistance
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
            self.calendar_id = "pinkpantherking20@gmail.com"
            print(f"✅ Primary calendar: {self.calendar_id}\n")
    
    async def create_chat_session(self):
        """Create a new Gemini chat session with calendar tools"""
        now = datetime.now()
        user_timezone = "Asia/Karachi (UTC+5)"
        current_date = now.strftime("%A, %B %d, %Y at %I:%M %p")
        
        config = genai.types.GenerateContentConfig(
            temperature=0.1,
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

═══════════════════════════════════════════════════════════════════
CRITICAL TOOL USAGE PROTOCOL
═══════════════════════════════════════════════════════════════════

🔴 MANDATORY RULE FOR google_calendar-list-events:
You MUST ALWAYS use this EXACT instruction format with specific calendar ID:

TEMPLATE:
"List all events for [SPECIFIC TIMEFRAME] from ONLY my primary calendar (pinkpantherking20@gmail.com)"

✅ CORRECT EXAMPLES:
• "List all events for today from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events for tomorrow from ONLY my primary calendar (pinkpantherking20@gmail.com)"
• "List all events for this week from ONLY my primary calendar (pinkpantherking20@gmail.com)"

❌ NEVER USE THESE:
• "List all events from ALL calendars"
• "List events" (without calendar ID)
• Generic date references without specific dates

═══════════════════════════════════════════════════════════════════
WORKFLOW 1: VIEWING SCHEDULE
═══════════════════════════════════════════════════════════════════

STEP 1: Interpret the timeframe
  → Convert user's natural language to specific dates

STEP 2: Call google_calendar-list-events
  → Use EXACT format with calendar ID and specific dates

STEP 3: Present results clearly
  → Format: **Event Title** - Time Range
  → Use 12-hour format (9:00 AM, 2:30 PM)
  → Group by day if showing multiple days
  → If no events: "You have no events scheduled for [timeframe]"

EXAMPLE RESPONSE:
"Here's your schedule for today:

• **Team Meeting** - 9:00 AM to 10:00 AM
• **Lunch with Client** - 12:30 PM to 1:30 PM
• **Project Review** - 3:00 PM to 4:00 PM"

═══════════════════════════════════════════════════════════════════
WORKFLOW 2: SCHEDULING NEW EVENTS
═══════════════════════════════════════════════════════════════════

STEP 1: Extract event details from user request
  Required: Title, Date, Time
  Optional: Duration (default 1 hour), Location, Description

STEP 2: ⚠️ MANDATORY CONFLICT CHECK
  → Call google_calendar-list-events for that specific date
  → Check if proposed time overlaps with any existing event

STEP 3a: IF CONFLICT DETECTED
  → 🚨 WARN user immediately: "⚠️ Conflict detected!"
  → Show conflicting event details
  → Suggest alternative times
  → Ask for confirmation before proceeding

STEP 3b: IF NO CONFLICT
  → Confirm details with user
  → Create event using google_calendar-create-event

STEP 4: Confirm to user
  → "✅ Successfully created: **[Event Title]** on [Date] at [Time]"

═══════════════════════════════════════════════════════════════════
WORKFLOW 3: FINDING FREE TIME
═══════════════════════════════════════════════════════════════════

When user asks "Do I have free time on [date/timeframe]?":

STEP 1: Get all events for that period
STEP 2: Identify gaps between events
STEP 3: Present free time blocks with duration

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

❌ DON'T:
• Make assumptions about event details
• Create events without checking conflicts
• Use ambiguous date references
• Use overly technical language

TONE: Professional yet friendly, helpful, efficient, intelligent

═══════════════════════════════════════════════════════════════════""",
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
