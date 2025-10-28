# 🧠 Smart Calendar Assistant# 🧠 Smart Calendar Assistant# 📅 Google Calendar Assistant with Pipedream MCP



An intelligent AI-powered Google Calendar assistant with advanced conflict detection and natural language scheduling.



## ✨ FeaturesIntelligent AI-powered calendar assistant with a beautiful minimal web UI.An AI-powered calendar assistant that helps you schedule appointments on Google Calendar using Gemini AI and Pipedream's Model Context Protocol.



- 🗓️ **Smart Schedule Viewing** - View today's events, weekly schedule, or any custom timeframe

- 🤖 **Natural Language Queries** - "What's my schedule this week?" or "Do I have free time on Friday?"

- ⚠️ **Intelligent Conflict Detection** - Automatically checks for scheduling conflicts before creating events## 🚀 Quick Start## ✨ Features

- 💡 **Alternative Suggestions** - Suggests available time slots when conflicts are found

- ⏰ **Smart Date Interpretation** - Understands "today", "tomorrow", "this week", "next Friday", etc.

- 🌍 **Timezone-Aware** - Configured for Asia/Karachi (UTC+5)

- 🎯 **Personal Assistant** - Create, update, delete events with conversation```bash- 🗓️ **Schedule appointments** with natural language



## 🚀 Quick Start# 1. Check configuration- � **Smart conflict detection** - automatically checks for overlapping events



### Prerequisitespython check_config.py- ⚠️ **Warns before double-booking** - never accidentally create conflicting meetings

- Python 3.7 or higher

- Pipedream account with Google Calendar connected- 💡 **Suggests alternatives** - finds free time slots when there are conflicts

- Google Gemini API key

# 2. Run the server- �📋 **Check upcoming events** on your calendar

### Installation

python smart_calendar_assistant.py- 🎯 **Find available time slots** automatically

1. **Install dependencies:**

   ```bash- ✏️ **Update or cancel events** easily

   pip install -r requirements.txt

   ```# 3. Open browser- 🤖 **Conversational AI interface** powered by Gemini



2. **Configure environment:**http://localhost:8000- 🔐 **Secure authentication** via Pipedream Connect

   

   Create a `.env` file with:```

   ```env

   PIPEDREAM_PROJECT_ID=proj_xxxxxxx## 🎯 Two Versions Available

   PIPEDREAM_ENVIRONMENT=development

   PIPEDREAM_CLIENT_ID=your_client_id_here## ✨ Features

   PIPEDREAM_CLIENT_SECRET=your_client_secret_here

   GOOGLE_API_KEY=your_google_api_key_here### 1. Basic Calendar Assistant (`calendar_assistant.py`)

   EXTERNAL_USER_ID=user-123

   ```- 🎨 Beautiful minimal UI with dark modeStandard version with conflict detection via AI instructions.



3. **Verify configuration:**- 🔍 Smart conflict detection

   ```bash

   python3 check_config.py- ⏰ Time & date intelligence### 2. Smart Calendar Assistant (`smart_calendar_assistant.py`) ⭐ **RECOMMENDED**

   ```

- 📊 Schedule summariesEnhanced version with:

### Usage

- 💡 Natural language understanding- **Mandatory conflict checking** before every event creation

Run the interactive CLI:

```bash- **Proactive warnings** about overlapping events

python3 calendar_assistant.py

```## 💬 Example Queries- **Alternative time suggestions** when conflicts are found



Try these commands:- **Lower temperature** (0.3) for more consistent behavior

- `What's on my calendar today?`

- `Show my schedule this week`- "What time is it?"- **Detailed system instructions** to prevent double-booking

- `Schedule a dentist appointment tomorrow at 3 PM`

- `Do I have any free time on Friday?`- "What's my schedule today?"

- `Cancel my meeting with John`

- "Schedule meeting tomorrow at 2 PM"Run the smart version:

Type `quit` or `exit` to stop.

- "Am I free this afternoon?"```bash

## 💬 Example Conversations

- "Show my week"python smart_calendar_assistant.py

### View Today's Schedule

``````

You: What's on my calendar today?

🤖: Here's your schedule for today (Monday, October 27, 2025):## 🌓 UI Features

    • meet with hafsa - 4:30 PM to 5:30 PM

```## 🚀 Quick Start



### Check Weekly Schedule- Light/Dark mode toggle

```

You: Show my schedule this week- Quick action buttons### 1. Prerequisites

🤖: Here's your schedule for this week (Oct 27 - Nov 2, 2025):

- Real-time chat via WebSocket

    Monday, October 27:

    • meet with hafsa - 4:30 PM to 5:30 PM- Typing indicators- Python 3.8 or higher

    

    Tuesday, October 28:- Auto-scroll messages- A [Pipedream account](https://pipedream.com/auth/signup)

    • meeting with iffi - 7:00 PM to 8:00 PM

    • party with kids - 8:00 PM to 9:00 PM- A [Google Gemini API key](https://ai.google.dev/)

    ...

```---- Google Calendar connected to your Pipedream project



### Conflict Detection

```

You: Schedule a team sync meeting at 7 PM tonightBuilt with Pipedream MCP + Google Gemini### 2. Installation

🤖: ⚠️ Conflict detected! You already have "meeting with iffi" scheduled at 7:00 PM to 8:00 PM.



    Available times nearby:```bash

    • 5:30 PM - 7:00 PM (before the meeting)# Clone or navigate to the project directory

    • 8:00 PM onwardscd "/Users/abdullah/my projects/pipedream"



    Would you like to:# Install dependencies

    1. Schedule anyway (double-book)pip install -r requirements.txt

    2. Choose a different time```

    3. Cancel this request

```### 3. Configuration



## 🛠️ How It Works1. **Copy the example environment file:**

   ```bash

```   cp .env.example .env

User Input   ```

    ↓

Google Gemini AI (with comprehensive prompt)2. **Fill in your credentials in `.env`:**

    ↓

MCP Protocol   ```env

    ↓   # Get these from Pipedream Dashboard → Your Project → Settings → OAuth Clients

Pipedream Remote MCP Server   PIPEDREAM_PROJECT_ID=proj_xxxxxxx

    ↓   PIPEDREAM_ENVIRONMENT=development

Google Calendar API   PIPEDREAM_CLIENT_ID=your_client_id_here

```   PIPEDREAM_CLIENT_SECRET=your_client_secret_here



1. **Pipedream Connect** - Handles OAuth authentication with Google Calendar   # Get from Google AI Studio: https://ai.google.dev/

2. **MCP (Model Context Protocol)** - Provides calendar API tools to the AI   GOOGLE_API_KEY=your_google_api_key_here

3. **Google Gemini 2.0 Flash** - AI model with function calling for intelligent responses

4. **Smart Prompt Engineering** - 200+ lines of system instructions for reliable behavior   # Your unique user identifier (can be any string)

   EXTERNAL_USER_ID=user-123

## 📋 Environment Variables   ```



| Variable | Description | Where to Get |3. **Connect Google Calendar in Pipedream:**

|----------|-------------|--------------|   - Go to your [Pipedream project](https://pipedream.com/projects)

| `PIPEDREAM_PROJECT_ID` | Your Pipedream project ID | Pipedream Dashboard → Project → Settings |   - Navigate to **Connect** → **Users**

| `PIPEDREAM_ENVIRONMENT` | Environment (development/production) | Use `development` for testing |   - Click **Connect account** and choose Google Calendar

| `PIPEDREAM_CLIENT_ID` | OAuth client ID | Auto-generated via `pd init connect` |   - Make sure to use the same `EXTERNAL_USER_ID` you set in `.env`

| `PIPEDREAM_CLIENT_SECRET` | OAuth client secret | Auto-generated via `pd init connect` |

| `GOOGLE_API_KEY` | Gemini API key | [Google AI Studio](https://ai.google.dev/) |### 4. Run the Assistant

| `EXTERNAL_USER_ID` | Your user identifier | Any unique string (e.g., `user-123`) |

```bash

## 📁 Filespython calendar_assistant.py

```

- `calendar_assistant.py` - Main CLI application (18KB)

- `check_config.py` - Configuration verification tool (2.5KB)## 💬 Example Conversations

- `requirements.txt` - Python dependencies

- `.env` - Environment variables (not in git)### Schedule a Meeting

- `static/index.html` - Web UI (future enhancement)```

You: Schedule a team meeting tomorrow at 2pm for 1 hour

## 🎯 Key Features🤖 Assistant: I'll create a team meeting for tomorrow at 2:00 PM...

```

### Advanced Conflict Detection

The assistant uses a precise algorithm to detect scheduling conflicts:### Check Your Calendar

``````

(new_start < existing_end) AND (new_end > existing_start)You: What do I have scheduled this week?

```🤖 Assistant: Here are your upcoming events this week...

```

### Smart Date Understanding

- **Today** = October 27, 2025### Find Available Time

- **Tomorrow** = October 28, 2025```

- **This week** = Oct 27 - Nov 2, 2025You: When am I free tomorrow afternoon?

- **Next week** = Nov 3 - Nov 9, 2025🤖 Assistant: Looking at your calendar, you have these free slots...

- **Next Friday** = Calculates based on current date```



### Consistent Behavior### Quick Appointment

- Temperature set to **0.1** for reliable responses```

- Retry logic with exponential backoff (3 retries: 2s, 4s, 8s)You: Book a dentist appointment next Monday at 10am

- Handles 503 service overload errors gracefully🤖 Assistant: I'll schedule a dentist appointment for Monday at 10:00 AM...

```

## 🐛 Troubleshooting

## 🛠️ How It Works

### "No events found" when you know events exist

✅ **Fixed!** The assistant now specifies the exact calendar ID in all queries.1. **Pipedream Connect** handles OAuth authentication with Google Calendar

2. **MCP Server** provides Google Calendar API tools to the AI

### Events not showing up3. **Gemini AI** processes your natural language requests

Run the config checker:4. **Calendar Assistant** orchestrates the conversation and executes actions

```bash

python3 check_config.py## 📋 Environment Variables

```

| Variable | Description | Where to Get |

Verify Google Calendar is connected in Pipedream with the same `EXTERNAL_USER_ID`.|----------|-------------|--------------|

| `PIPEDREAM_PROJECT_ID` | Your Pipedream project ID | Pipedream Dashboard → Project → Settings |

### Authentication errors| `PIPEDREAM_ENVIRONMENT` | Environment (development/production) | Use `development` for testing |

- Check `PIPEDREAM_CLIENT_ID` and `PIPEDREAM_CLIENT_SECRET`| `PIPEDREAM_CLIENT_ID` | OAuth client ID | Pipedream Dashboard → Project → OAuth Clients |

- Verify `PIPEDREAM_PROJECT_ID` is correct| `PIPEDREAM_CLIENT_SECRET` | OAuth client secret | Pipedream Dashboard → Project → OAuth Clients |

- Ensure Google Calendar is connected in Pipedream| `GOOGLE_API_KEY` | Gemini API key | [Google AI Studio](https://ai.google.dev/) |

| `EXTERNAL_USER_ID` | Your user identifier | Any unique string (e.g., `user-123`) |

### Gemini API errors

- Verify `GOOGLE_API_KEY` is valid## 🔒 Security Notes

- Check API quotas in Google AI Studio

- ✅ Never commit `.env` file to version control

## 📚 Resources- ✅ Keep your API keys and secrets secure

- ✅ Use `development` environment for testing

- [Pipedream Documentation](https://pipedream.com/docs)- ✅ Switch to `production` only when ready

- [Pipedream MCP Guide](https://pipedream.com/docs/connect/mcp/developers)

- [Google Gemini API](https://ai.google.dev/)## 🐛 Troubleshooting

- [MCP Protocol](https://modelcontextprotocol.io/)

### "No connected account found"

## 🔒 Security- Make sure you've connected Google Calendar in Pipedream

- Verify the `EXTERNAL_USER_ID` matches between `.env` and Pipedream

- ✅ Never commit `.env` to version control

- ✅ Keep API keys and OAuth credentials secure### "Authentication failed"

- ✅ Use `development` environment for testing- Double-check your `PIPEDREAM_CLIENT_ID` and `PIPEDREAM_CLIENT_SECRET`

- ✅ Review Google Calendar permissions in Pipedream- Ensure your `PIPEDREAM_PROJECT_ID` is correct



## 📝 License### "Google API error"

- Verify your `GOOGLE_API_KEY` is valid

MIT License - Feel free to use and modify!- Check if Gemini API is enabled in your Google Cloud project



---## 📚 Resources



Built with ❤️ using Pipedream MCP, Google Gemini 2.0 Flash, and Python- [Pipedream Documentation](https://pipedream.com/docs)

- [Pipedream MCP Developers Guide](https://pipedream.com/docs/connect/mcp/developers)
- [Google Gemini API](https://ai.google.dev/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 🤝 Support

Need help? Check out:
- [Pipedream Support](https://pipedream.com/support)
- [Pipedream Community Slack](https://pipedream.com/join-slack)

## 📝 License

MIT License - Feel free to use and modify!

---

Built with ❤️ using Pipedream MCP, Google Gemini, and Python
