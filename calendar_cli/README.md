# Smart Calendar Assistant - CLI

A standalone command-line interface for managing your Google Calendar with AI assistance powered by Google Gemini.

## Features

- 📅 View your calendar schedule (today, tomorrow, this week, etc.)
- ➕ Schedule new events with natural language
- 🔍 Find free time in your schedule
- ⚠️ Automatic conflict detection
- 🤖 AI-powered intelligent scheduling suggestions
- 🌍 Timezone-aware (Asia/Karachi UTC+5)

## Prerequisites

1. Python 3.8 or higher
2. Pipedream account with Google Calendar connected
3. Google API key for Gemini
4. Required environment variables

## Installation

1. Install dependencies:
```bash
pip install google-genai fastmcp pipedream python-dotenv
```

2. Set up environment variables in your `.env` file:
```
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
GOOGLE_API_KEY=your_gemini_api_key
```

## Usage

Run the calendar assistant:
```bash
python calendar_assistant.py
```

### Example Commands

- "What's on my calendar today?"
- "Schedule a meeting tomorrow at 2 PM"
- "Show my schedule for this week"
- "Do I have any free time on Friday?"
- "Schedule a dentist appointment at 4:30 PM today"

### Exit

Type `quit`, `exit`, or press `Ctrl+C` to exit the application.

## How It Works

1. **Authentication**: Connects to Pipedream for Google Calendar access
2. **AI Integration**: Uses Google Gemini for natural language processing
3. **MCP Protocol**: Leverages Model Context Protocol for tool calling
4. **Conflict Detection**: Automatically checks for scheduling conflicts
5. **Smart Scheduling**: Suggests optimal times based on your schedule

## Configuration

The calendar ID is automatically detected from your primary Google Calendar. The default timezone is set to Asia/Karachi (UTC+5). You can modify these in the code if needed.

## Error Handling

- Automatic retry logic for API overload
- Clear error messages for user guidance
- Graceful handling of network issues

## License

This is a standalone CLI tool for personal calendar management.
