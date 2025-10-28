# Healthcare Assistant - Project Structure

```
pipedream/
│
├── api/                          # FastAPI Backend
│   ├── __init__.py
│   └── main.py                   # API server (30+ endpoints)
│
├── modules/                      # Core Python modules
│   ├── __init__.py
│   ├── calendar_assistant_wrapper.py
│   ├── calendar_integration.py
│   ├── calendar_sync.py
│   ├── memory_manager.py
│   ├── rag_engine.py
│   └── scheduler.py
│
├── tests/                        # All test files
│   ├── test_api.py               # API endpoint tests
│   ├── test_complete_system.py   # Full system tests
│   ├── test_doctor_portal.py
│   ├── test_memory_manager.py
│   ├── test_rag.py
│   ├── test_scheduler.py
│   ├── demo_appointment_calendar.py
│   ├── demo_qa.py
│   ├── final_demo.py
│   └── ... (other test/demo files)
│
├── docs/                         # Documentation
│   ├── API_ENDPOINTS.md          # Complete API reference
│   ├── FRONTEND_PROMPTS.md       # Frontend build specs
│   ├── API_GUIDE.md              # API usage guide
│   ├── BACKEND_COMPLETE.md       # Backend summary
│   ├── CALENDAR_FLOW_EXPLAINED.md
│   ├── HEALTHCARE_README.md
│   ├── db_schema.sql             # Database schema
│   └── ... (other documentation)
│
├── data/                         # SQLite database
│   └── healthcare.db
│
├── chroma_db/                    # RAG vector database
│   └── ... (vector embeddings)
│
├── utils/                        # Utility functions
│
├── calendar_assistant.py         # Calendar integration
├── config.py                     # Configuration
├── db_setup.py                   # Database setup script
├── doctor_portal.py              # Doctor CLI portal
├── healthcare_assistant.py       # Patient CLI portal
├── start.py                      # Quick launcher
├── start_api.sh                  # API server startup script
├── requirements_healthcare.txt   # Python dependencies
├── .env                          # Environment variables
└── README.md                     # Main project README
```

## Main Files

### Core Applications:
- **healthcare_assistant.py** - Patient portal (CLI)
- **doctor_portal.py** - Doctor portal (CLI)
- **api/main.py** - REST API backend for web UI

### Configuration:
- **config.py** - App configuration
- **db_setup.py** - Initialize database
- **.env** - Environment variables (API keys)

### Launchers:
- **start.py** - Quick menu to launch any feature
- **start_api.sh** - Start the API server

## Quick Start

```bash
# 1. Start API server
./start_api.sh

# 2. Access API docs
open http://localhost:8000/docs

# 3. Or use CLI
python3 start.py
```
