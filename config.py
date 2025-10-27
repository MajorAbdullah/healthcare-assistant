# Healthcare Assistant Configuration

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MEDICAL_DOCS_DIR = DATA_DIR / "medical_docs"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
DATABASE_PATH = DATA_DIR / "healthcare.db"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MEDICAL_DOCS_DIR.mkdir(exist_ok=True)
VECTOR_DB_DIR.mkdir(exist_ok=True)

# Pipedream Configuration (from existing .env)
PIPEDREAM_PROJECT_ID = os.getenv("PIPEDREAM_PROJECT_ID")
PIPEDREAM_ENVIRONMENT = os.getenv("PIPEDREAM_ENVIRONMENT", "development")
PIPEDREAM_CLIENT_ID = os.getenv("PIPEDREAM_CLIENT_ID")
PIPEDREAM_CLIENT_SECRET = os.getenv("PIPEDREAM_CLIENT_SECRET")
EXTERNAL_USER_ID = os.getenv("EXTERNAL_USER_ID", "user-123")

# Google API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# RAG Configuration
EMBEDDING_MODEL = "models/embedding-001"  # Gemini embeddings
LLM_MODEL = "gemini-2.5-flash"
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 50  # Overlap between chunks
TOP_K_RESULTS = 5  # Number of relevant chunks to retrieve
TEMPERATURE = 0.1  # LLM temperature for consistent answers

# Vector Database Configuration
CHROMA_COLLECTION_NAME = "stroke_medical_docs"

# Appointment Configuration
DEFAULT_APPOINTMENT_DURATION = 30  # minutes
TIMEZONE = "Asia/Karachi"
BOOKING_ADVANCE_DAYS = 30  # How far in advance patients can book

# Doctor Configuration (Sample data)
SAMPLE_DOCTORS = [
    {
        "external_id": "doctor-sarah",
        "name": "Dr. Sarah Johnson",
        "email": "sarah.johnson@hospital.com",
        "specialization": "Neurology - Stroke Specialist",
        "calendar_id": "pinkpantherking20@gmail.com"  # Using your existing calendar for demo
    },
    {
        "external_id": "doctor-michael",
        "name": "Dr. Michael Chen",
        "email": "michael.chen@hospital.com",
        "specialization": "Emergency Medicine",
        "calendar_id": "pinkpantherking20@gmail.com"  # Using same for demo
    },
    {
        "external_id": "doctor-aisha",
        "name": "Dr. Aisha Khan",
        "email": "aisha.khan@hospital.com",
        "specialization": "Rehabilitation & Recovery",
        "calendar_id": "pinkpantherking20@gmail.com"  # Using same for demo
    }
]

# Sample Patient
SAMPLE_PATIENT = {
    "external_id": "patient-john",
    "name": "John Doe",
    "email": "john.doe@email.com"
}

# System Prompts
RAG_SYSTEM_PROMPT = """You are a medical education assistant specializing in stroke awareness and education.

Your role is to:
1. Answer questions about strokes using ONLY the provided medical documents
2. Always cite your sources using [1], [2], etc. format
3. Be clear, accurate, and compassionate
4. If information is not in the provided documents, say so
5. Never provide medical diagnosis or treatment advice
6. Encourage users to consult healthcare professionals for personal medical concerns

Format your answers as:
- Clear, concise explanation
- Use bullet points when appropriate
- Include citations inline [1], [2]
- List sources at the end

Remember: You are educational only, not a replacement for medical professionals.
"""

SCHEDULER_SYSTEM_PROMPT = """You are an appointment scheduling assistant for a stroke care clinic.

Your role is to:
1. Help patients find available appointment slots with doctors
2. Check for scheduling conflicts
3. Confirm booking details with patients
4. Be helpful and empathetic
5. Explain the booking process clearly

Available doctors:
- Dr. Sarah Johnson (Neurologist, Stroke Specialist)
- Dr. Michael Chen (Emergency Medicine)
- Dr. Aisha Khan (Rehabilitation & Recovery)

Standard appointment duration: 30 minutes
Timezone: Asia/Karachi (UTC+5)
"""

# Conversation History Configuration
MAX_CONVERSATION_HISTORY = 50  # Messages to keep in memory
CONTEXT_WINDOW_MESSAGES = 10  # Recent messages to include in context

# UI Configuration
CLI_WIDTH = 100
CLI_THEME = "monokai"

# Feature Flags (for development)
ENABLE_WEB_UI = False
ENABLE_NOTIFICATIONS = False
ENABLE_ANALYTICS = True
DEBUG_MODE = True

def validate_config():
    """Validate that all required configuration is present."""
    required_vars = [
        ("PIPEDREAM_PROJECT_ID", PIPEDREAM_PROJECT_ID),
        ("PIPEDREAM_CLIENT_ID", PIPEDREAM_CLIENT_ID),
        ("PIPEDREAM_CLIENT_SECRET", PIPEDREAM_CLIENT_SECRET),
        ("GOOGLE_API_KEY", GOOGLE_API_KEY),
    ]
    
    missing = [var[0] for var in required_vars if not var[1]]
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    print("✅ Configuration validated successfully")
    return True

if __name__ == "__main__":
    validate_config()
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"📚 Medical docs: {MEDICAL_DOCS_DIR}")
    print(f"🗄️  Database: {DATABASE_PATH}")
    print(f"🔍 Vector DB: {VECTOR_DB_DIR}")
