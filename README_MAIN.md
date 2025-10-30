# 🏥 Healthcare Assistant# 🧠 Smart Calendar Assistant# 🧠 Smart Calendar Assistant# 📅 Google Calendar Assistant with Pipedream MCP



A comprehensive healthcare management system with dual portals (Patient & Doctor), AI-powered medical Q&A, appointment scheduling, and calendar integration.



## ✨ FeaturesAn intelligent AI-powered Google Calendar assistant with advanced conflict detection and natural language scheduling.



### Patient Portal

- 🔐 Registration & Login

- 📅 Browse doctors and book appointments## ✨ FeaturesIntelligent AI-powered calendar assistant with a beautiful minimal web UI.An AI-powered calendar assistant that helps you schedule appointments on Google Calendar using Gemini AI and Pipedream's Model Context Protocol.

- 💬 AI-powered medical Q&A chat

- 📋 View appointment history

- 👤 Profile management

- 🔔 Preferences & notifications- 🗓️ **Smart Schedule Viewing** - View today's events, weekly schedule, or any custom timeframe



### Doctor Portal- 🤖 **Natural Language Queries** - "What's my schedule this week?" or "Do I have free time on Friday?"

- 👨‍⚕️ Doctor authentication

- 📊 Dashboard with statistics- ⚠️ **Intelligent Conflict Detection** - Automatically checks for scheduling conflicts before creating events## 🚀 Quick Start## ✨ Features

- 🗓️ View daily/weekly schedule

- 👥 Patient directory & search- 💡 **Alternative Suggestions** - Suggests available time slots when conflicts are found

- 📝 Add medical notes

- 📈 Analytics & reporting- ⏰ **Smart Date Interpretation** - Understands "today", "tomorrow", "this week", "next Friday", etc.



### Backend API- 🌍 **Timezone-Aware** - Configured for Asia/Karachi (UTC+5)

- 🚀 FastAPI REST API (30+ endpoints)

- 🔌 WebSocket for real-time chat- 🎯 **Personal Assistant** - Create, update, delete events with conversation```bash- 🗓️ **Schedule appointments** with natural language

- 📚 Interactive API documentation

- 🗄️ SQLite database (local)

- 🔗 Google Calendar integration

## 🚀 Quick Start# 1. Check configuration- � **Smart conflict detection** - automatically checks for overlapping events

## 🚀 Quick Start



### 1. Start the API Server

```bash### Prerequisitespython check_config.py- ⚠️ **Warns before double-booking** - never accidentally create conflicting meetings

./start_api.sh

```- Python 3.7 or higher



**Access:**- Pipedream account with Google Calendar connected- 💡 **Suggests alternatives** - finds free time slots when there are conflicts

- API: http://localhost:8000

- Swagger Docs: http://localhost:8000/docs- Google Gemini API key



### 2. Use CLI Portals# 2. Run the server- �📋 **Check upcoming events** on your calendar

```bash

# Launch menu### Installation

python3 start.py

python smart_calendar_assistant.py- 🎯 **Find available time slots** automatically

# Or directly:

python3 healthcare_assistant.py  # Patient portal1. **Install dependencies:**

python3 doctor_portal.py         # Doctor portal

```   ```bash- ✏️ **Update or cancel events** easily



### 3. Run Tests   pip install -r requirements.txt

```bash

# Test API endpoints   ```# 3. Open browser- 🤖 **Conversational AI interface** powered by Gemini

python3 tests/test_api.py



# Complete system tests

python3 tests/test_complete_system.py2. **Configure environment:**http://localhost:8000- 🔐 **Secure authentication** via Pipedream Connect

```

   

## 📁 Project Structure

   Create a `.env` file with:```

```

pipedream/   ```env

├── api/                    # FastAPI backend

├── modules/                # Core Python modules   PIPEDREAM_PROJECT_ID=proj_xxxxxxx## 🎯 Two Versions Available

├── tests/                  # All test files

├── docs/                   # Documentation   PIPEDREAM_ENVIRONMENT=development

├── data/                   # SQLite database

├── chroma_db/              # RAG vector database   PIPEDREAM_CLIENT_ID=your_client_id_here## ✨ Features

└── Main files (see below)

```   PIPEDREAM_CLIENT_SECRET=your_client_secret_here



**Main Files:**   GOOGLE_API_KEY=your_google_api_key_here### 1. Basic Calendar Assistant (`calendar_assistant.py`)

- `healthcare_assistant.py` - Patient portal (CLI)

- `doctor_portal.py` - Doctor portal (CLI)   EXTERNAL_USER_ID=user-123

- `start.py` - Quick launcher menu

- `start_api.sh` - API server startup   ```- 🎨 Beautiful minimal UI with dark modeStandard version with conflict detection via AI instructions.

- `db_setup.py` - Database initialization



## 📚 Documentation

3. **Verify configuration:**- 🔍 Smart conflict detection

### For Frontend Developers:

- **[API Endpoints](docs/API_ENDPOINTS.md)** - Complete API reference   ```bash

- **[Frontend Prompts](docs/FRONTEND_PROMPTS.md)** - UI specifications

- **[API Guide](docs/API_GUIDE.md)** - Usage examples   python3 check_config.py- ⏰ Time & date intelligence### 2. Smart Calendar Assistant (`smart_calendar_assistant.py`) ⭐ **RECOMMENDED**



### For Backend Developers:   ```

- **[Backend Complete](docs/BACKEND_COMPLETE.md)** - Backend summary

- **[Calendar Flow](docs/CALENDAR_FLOW_EXPLAINED.md)** - Calendar integration- 📊 Schedule summariesEnhanced version with:

- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - File organization

### Usage

## 🛠️ Setup

- 💡 Natural language understanding- **Mandatory conflict checking** before every event creation

### Prerequisites

- Python 3.8+Run the interactive CLI:

- pip

- SQLite3```bash- **Proactive warnings** about overlapping events



### Installationpython3 calendar_assistant.py

```bash

# 1. Install dependencies```## 💬 Example Queries- **Alternative time suggestions** when conflicts are found

pip install -r requirements_healthcare.txt



# 2. Setup database

python3 db_setup.pyTry these commands:- **Lower temperature** (0.3) for more consistent behavior



# 3. Configure environment (optional)- `What's on my calendar today?`

cp .env.example .env

# Edit .env with your API keys- `Show my schedule this week`- "What time is it?"- **Detailed system instructions** to prevent double-booking

```

- `Schedule a dentist appointment tomorrow at 3 PM`

## 🧪 Testing

- `Do I have any free time on Friday?`- "What's my schedule today?"

**Run all tests:**

```bash- `Cancel my meeting with John`

cd tests

python3 test_complete_system.py- "Schedule meeting tomorrow at 2 PM"Run the smart version:

```

Type `quit` or `exit` to stop.

**Test specific features:**

```bash- "Am I free this afternoon?"```bash

python3 tests/test_api.py              # API endpoints

python3 tests/test_memory_manager.py   # Memory system## 💬 Example Conversations

python3 tests/test_scheduler.py        # Appointment scheduling

python3 tests/test_rag.py              # RAG Q&A system- "Show my week"python smart_calendar_assistant.py

```

### View Today's Schedule

## 🔧 Technology Stack

``````

### Backend

- **FastAPI** - REST API frameworkYou: What's on my calendar today?

- **Uvicorn** - ASGI server

- **SQLite** - Database🤖: Here's your schedule for today (Monday, October 27, 2025):## 🌓 UI Features

- **ChromaDB** - Vector database for RAG

- **Sentence Transformers** - Text embeddings    • meet with hafsa - 4:30 PM to 5:30 PM



### AI & ML```## 🚀 Quick Start

- **Google Gemini** - LLM for chat

- **RAG (Retrieval Augmented Generation)** - Medical Q&A

- **Memory Manager** - Conversation context

### Check Weekly Schedule- Light/Dark mode toggle

### Integrations

- **Google Calendar** - Appointment sync via Pipedream```

- **Pipedream MCP** - Calendar integration

You: Show my schedule this week- Quick action buttons### 1. Prerequisites

## 📊 Database Schema

🤖: Here's your schedule for this week (Oct 27 - Nov 2, 2025):

**Tables:**

- `users` - Patient information- Real-time chat via WebSocket

- `doctors` - Doctor profiles

- `appointments` - Appointment records    Monday, October 27:

- `conversations` - Chat history

- `user_preferences` - User settings    • meet with hafsa - 4:30 PM to 5:30 PM- Typing indicators- Python 3.8 or higher



See [db_schema.sql](docs/db_schema.sql) for details.    



## 🌐 API Endpoints    Tuesday, October 28:- Auto-scroll messages- A [Pipedream account](https://pipedream.com/auth/signup)



### Patient Portal    • meeting with iffi - 7:00 PM to 8:00 PM

- `POST /api/v1/patients/register` - Register

- `POST /api/v1/patients/login` - Login    • party with kids - 8:00 PM to 9:00 PM- A [Google Gemini API key](https://ai.google.dev/)

- `GET /api/v1/doctors` - List doctors

- `POST /api/v1/appointments` - Book appointment    ...

- `POST /api/v1/chat` - Chat with AI

```---- Google Calendar connected to your Pipedream project

### Doctor Portal

- `POST /api/v1/doctors/login` - Login

- `GET /api/v1/doctors/{id}/stats` - Dashboard stats

- `GET /api/v1/doctors/{id}/appointments` - Schedule### Conflict Detection

- `POST /api/v1/appointments/{id}/notes` - Add notes

- `GET /api/v1/doctors/{id}/analytics` - Analytics```



**Full API Reference:** [API_ENDPOINTS.md](docs/API_ENDPOINTS.md)You: Schedule a team sync meeting at 7 PM tonightBuilt with Pipedream MCP + Google Gemini### 2. Installation



## 🎯 Features Status🤖: ⚠️ Conflict detected! You already have "meeting with iffi" scheduled at 7:00 PM to 8:00 PM.



### ✅ Implemented

- Patient registration & login

- Doctor authentication    Available times nearby:```bash

- Appointment booking with conflict detection

- Medical Q&A chat (RAG)    • 5:30 PM - 7:00 PM (before the meeting)# Clone or navigate to the project directory

- Conversation memory & context

- Calendar integration (Google Calendar)    • 8:00 PM onwardscd "/Users/abdullah/my projects/pipedream"

- Medical notes

- Analytics dashboard

- RESTful API (30+ endpoints)

- WebSocket chat    Would you like to:# Install dependencies

- Smart suggestions & personalization

    1. Schedule anyway (double-book)pip install -r requirements.txt

### 🔄 Coming Soon

- Frontend UI (React/Next.js)    2. Choose a different time```

- Email notifications

- SMS reminders    3. Cancel this request

- Multi-calendar support

- Advanced analytics```### 3. Configuration

- Export reports



## 🤝 Contributing

## 🛠️ How It Works1. **Copy the example environment file:**

This is a prototype/blueprint project. To extend:

   ```bash

1. **Add features** in `modules/`

2. **Create API endpoints** in `api/main.py````   cp .env.example .env

3. **Add tests** in `tests/`

4. **Update docs** in `docs/`User Input   ```



## 📝 License    ↓



This project is a prototype for educational purposes.Google Gemini AI (with comprehensive prompt)2. **Fill in your credentials in `.env`:**



## 🆘 Support    ↓



- **API Docs**: http://localhost:8000/docsMCP Protocol   ```env

- **Issues**: Check test results

- **Logs**: Terminal output    ↓   # Get these from Pipedream Dashboard → Your Project → Settings → OAuth Clients



## 🎉 Quick DemoPipedream Remote MCP Server   PIPEDREAM_PROJECT_ID=proj_xxxxxxx



```bash    ↓   PIPEDREAM_ENVIRONMENT=development

# 1. Start API server

./start_api.shGoogle Calendar API   PIPEDREAM_CLIENT_ID=your_client_id_here



# 2. In another terminal, test it```   PIPEDREAM_CLIENT_SECRET=your_client_secret_here

curl http://localhost:8000/health



# 3. Open Swagger docs in browser

open http://localhost:8000/docs1. **Pipedream Connect** - Handles OAuth authentication with Google Calendar   # Get from Google AI Studio: https://ai.google.dev/



# 4. Try the patient portal2. **MCP (Model Context Protocol)** - Provides calendar API tools to the AI   GOOGLE_API_KEY=your_google_api_key_here

python3 healthcare_assistant.py

```3. **Google Gemini 2.0 Flash** - AI model with function calling for intelligent responses



---4. **Smart Prompt Engineering** - 200+ lines of system instructions for reliable behavior   # Your unique user identifier (can be any string)



**Built with ❤️ for healthcare innovation**   EXTERNAL_USER_ID=user-123



🚀 **System Status:** Production Ready  ## 📋 Environment Variables   ```

✅ **Test Coverage:** 94.4%  

📊 **API Endpoints:** 30+  

💾 **Database:** SQLite (Local)

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
