# 🏥 Healthcare Assistant - Complete Project Plan

**A RAG-based Medical Chatbot + Doctor Appointment System**

---

## 📋 Project Overview

### Goal

Build a comprehensive healthcare assistant prototype that:

1. **Educates users** about stroke through RAG-based Q&A with medical sources
2. **Schedules appointments** with doctors using real calendar integration
3. **Manages conversations** with memory and personalization
4. **Supports dual roles** - patients and doctors with appropriate interfaces

### Key Features

✅ RAG system with cited medical sources
✅ Real-time appointment booking (leveraging existing Pipedream + Google Calendar)
✅ Conflict detection and smart scheduling
✅ Conversation history and memory
✅ Doctor approval workflow
✅ Patient and doctor dashboards

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Healthcare Assistant Platform                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐              ┌──────────────────┐          │
│  │  Patient Mode   │              │   Doctor Mode    │          │
│  │                 │              │                  │          │
│  │ • Ask Questions │              │ • View Bookings  │          │
│  │ • Book Appts    │              │ • Manage Calendar│          │
│  │ • View History  │              │ • Confirm Appts  │          │
│  └────────┬────────┘              └────────┬─────────┘          │
│           │                                │                     │
│           └────────────┬───────────────────┘                     │
│                        │                                         │
│  ┌─────────────────────▼────────────────────────┐               │
│  │         Core Modules (Orchestrator)          │               │
│  └──────────────────────────────────────────────┘               │
│                        │                                         │
│        ┌───────────────┼───────────────┐                        │
│        │               │               │                        │
│  ┌─────▼──────┐  ┌────▼─────┐  ┌──────▼────────┐              │
│  │   RAG Q&A  │  │ Scheduler │  │    Memory     │              │
│  │   Engine   │  │  Module   │  │   Manager     │              │
│  │            │  │           │  │               │              │
│  │ • Vector DB│  │ • Calendar│  │ • History     │              │
│  │ • Embeddings│ │ • Booking │  │ • Profiles    │              │
│  │ • Retrieval│  │ • Conflicts│  │ • Context     │              │
│  │ • Citations│  │ • Confirm │  │ • Analytics   │              │
│  └────────────┘  └───────────┘  └───────────────┘              │
│        │               │               │                        │
│  ┌─────▼───────────────▼───────────────▼─────┐                 │
│  │          Data Layer (SQLite + Vector DB)   │                 │
│  │  • Medical Documents (Stroke Knowledge)    │                 │
│  │  • User Profiles (Patients & Doctors)      │                 │
│  │  • Appointments (Pending, Confirmed)       │                 │
│  │  • Conversation Logs                       │                 │
│  └────────────────────────────────────────────┘                 │
│                        │                                         │
│  ┌─────────────────────▼──────────────────────┐                 │
│  │    External Services Integration           │                 │
│  │  • Google Gemini 2.0 (LLM)                │                 │
│  │  • Pipedream + Google Calendar             │                 │
│  │  • Embedding API (Gemini/OpenAI)           │                 │
│  └────────────────────────────────────────────┘                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
pipedream/
├── healthcare_assistant.py        # Main entry point (CLI orchestrator)
├── config.py                       # Configuration and constants
│
├── modules/
│   ├── __init__.py
│   ├── rag_engine.py              # RAG Q&A system
│   ├── scheduler.py               # Appointment booking logic
│   ├── memory_manager.py          # Conversation history & context
│   ├── doctor_dashboard.py        # Doctor interface
│   └── patient_interface.py       # Patient interface
│
├── data/
│   ├── medical_docs/              # Stroke articles (PDF, TXT)
│   │   ├── stroke_overview.pdf
│   │   ├── symptoms_treatment.pdf
│   │   └── prevention_guide.pdf
│   ├── vector_db/                 # ChromaDB storage
│   └── healthcare.db              # SQLite database
│
├── utils/
│   ├── __init__.py
│   ├── document_processor.py      # PDF/text chunking
│   ├── embeddings.py              # Embedding generation
│   └── validators.py              # Input validation
│
├── static/                         # Web UI (Phase 5)
│   ├── index.html
│   ├── patient.html
│   └── doctor.html
│
├── calendar_assistant.py          # (Existing - will integrate)
├── check_config.py                # (Existing)
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
├── README_HEALTHCARE.md           # Healthcare system docs
└── HEALTHCARE_PROJECT_PLAN.md     # This file
```

---

## 🗄️ Database Schema

### SQLite Schema (`healthcare.db`)

```sql
-- Users (both patients and doctors)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT UNIQUE NOT NULL,  -- Links to Pipedream
    role TEXT CHECK(role IN ('patient', 'doctor')) NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    specialization TEXT,  -- For doctors only
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments
CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    event_id TEXT,  -- Google Calendar event ID
    appointment_date TEXT NOT NULL,  -- ISO format
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending', 'confirmed', 'cancelled', 'completed')) DEFAULT 'pending',
    reason TEXT,  -- Why patient is booking
    notes TEXT,   -- Doctor notes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES users(user_id)
);

-- Conversation History
CREATE TABLE conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message_type TEXT CHECK(message_type IN ('user', 'assistant', 'system')) NOT NULL,
    message TEXT NOT NULL,
    context TEXT,  -- JSON metadata (sources, citations, etc.)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Medical Documents Metadata
CREATE TABLE documents (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    title TEXT,
    source_url TEXT,
    doc_type TEXT,  -- PDF, article, research paper
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chunk_count INTEGER DEFAULT 0
);

-- User Preferences
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    preferred_doctor_id INTEGER,
    notification_enabled BOOLEAN DEFAULT 1,
    timezone TEXT DEFAULT 'Asia/Karachi',
    language TEXT DEFAULT 'en',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (preferred_doctor_id) REFERENCES users(user_id)
);
```

---

## 🔧 Technical Stack

### Core Technologies

| Component            | Technology                  | Purpose                          |
| -------------------- | --------------------------- | -------------------------------- |
| **LLM**        | Google Gemini 2.5 Flash    | Question answering, conversation |
| **Vector DB**  | ChromaDB                    | Semantic search for medical docs |
| **Embeddings** | Gemini Embeddings API       | Document and query embeddings    |
| **Calendar**   | Pipedream + Google Calendar | Appointment scheduling           |
| **Database**   | SQLite3                     | User data, appointments, history |
| **CLI**        | Rich library                | Beautiful terminal interface     |
| **Auth**       | Pipedream Connect           | OAuth for Google Calendar        |

### Python Libraries

```txt
# Existing
google-genai>=0.2.0
fastmcp>=0.1.0
pipedream>=0.3.0
python-dotenv>=1.0.0

# New for Healthcare System
chromadb>=0.4.0              # Vector database
pypdf>=3.0.0                 # PDF processing
pdfplumber>=0.10.0           # Advanced PDF parsing
sentence-transformers>=2.2.0 # Alternative embeddings
rich>=13.0.0                 # Beautiful CLI
sqlalchemy>=2.0.0            # Database ORM (optional)
python-dateutil>=2.8.0       # Date handling
validators>=0.22.0           # Input validation
```

---

## 📊 Data Flow Diagrams

### 1. RAG Q&A Flow

```
User Question: "What are the symptoms of a stroke?"
    │
    ▼
┌─────────────────────────────┐
│  Embed Question             │
│  (Gemini Embeddings API)    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Search Vector DB           │
│  (ChromaDB)                 │
│  Returns top 5 chunks       │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Build Context              │
│  Chunk 1: [source, text]    │
│  Chunk 2: [source, text]    │
│  Chunk 3: [source, text]    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Generate Answer            │
│  (Gemini 2.0)               │
│  Prompt: Answer using docs  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Format Response            │
│  Answer + Citations         │
│  [1] Source A, Page 3       │
│  [2] Source B, Page 7       │
└──────────┬──────────────────┘
           │
           ▼
    Display to User
    Save to Conversation History
```

### 2. Appointment Booking Flow

```
Patient: "I want to book an appointment with Dr. Smith"
    │
    ▼
┌─────────────────────────────┐
│  Parse Request              │
│  Extract: Doctor, Date      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Fetch Doctor's Calendar    │
│  (Pipedream MCP)            │
│  Get availability           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Show Available Slots       │
│  Oct 28: 10am, 2pm, 4pm     │
└──────────┬──────────────────┘
           │
           ▼
Patient selects: "2pm tomorrow"
    │
    ▼
┌─────────────────────────────┐
│  Conflict Check             │
│  Check patient & doctor cal │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Create Appointment         │
│  Status: PENDING            │
│  Save to SQLite             │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Add to Doctor's Calendar   │
│  (with PENDING tag)         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Notify Both Parties        │
│  Patient: Confirmation      │
│  Doctor: Approval needed    │
└──────────┬──────────────────┘
           │
           ▼
    Doctor Reviews & Confirms
    Status → CONFIRMED
    Update Calendar Event
```

### 3. Doctor Confirmation Flow

```
Doctor logs in
    │
    ▼
┌─────────────────────────────┐
│  Show Pending Appointments  │
│  List all status=PENDING    │
└──────────┬──────────────────┘
           │
           ▼
Doctor selects appointment
    │
    ├──→ CONFIRM ──→ Update status to CONFIRMED
    │                Update calendar event color
    │                Notify patient
    │
    ├──→ RESCHEDULE ──→ Suggest new times
    │                    Update appointment
    │                    Notify patient
    │
    └──→ CANCEL ──→ Update status to CANCELLED
                    Remove from calendar
                    Notify patient with reason
```

---

## 🎯 Implementation Phases

### **Phase 1: RAG System Setup** (Days 1-3)

**Objectives:**

- Set up vector database
- Process medical documents
- Implement semantic search
- Build citation system

**Tasks:**

1. **Collect Medical Documents**

   ```python
   # Sample documents about stroke:
   - WHO Stroke Fact Sheet
   - Mayo Clinic: Stroke Symptoms
   - CDC: Stroke Prevention
   - NIH: Treatment Guidelines
   - Research papers on stroke recovery
   ```
2. **Document Processing** (`utils/document_processor.py`)

   ```python
   class DocumentProcessor:
       def load_pdf(self, filepath: str) -> str
       def chunk_text(self, text: str, chunk_size: int = 500) -> List[dict]
       def add_metadata(self, chunks: List, source: str) -> List[dict]
   ```
3. **Vector Database Setup** (`modules/rag_engine.py`)

   ```python
   class RAGEngine:
       def __init__(self):
           self.chroma_client = chromadb.Client()
           self.collection = self.chroma_client.create_collection("medical_docs")

       def add_documents(self, chunks: List[dict])
       def search(self, query: str, n_results: int = 5) -> List[dict]
       def generate_answer(self, query: str, context: List[dict]) -> str
   ```
4. **Citation System**

   ```python
   # Answer format:
   """
   Stroke symptoms include sudden numbness or weakness [1],
   severe headache [2], and difficulty speaking [1][3].

   Sources:
   [1] Mayo Clinic - Stroke Symptoms, Page 2
   [2] WHO Fact Sheet - Warning Signs
   [3] CDC Guide - Recognizing Stroke
   """
   ```

**Deliverables:**

- ✅ Vector database with 50+ stroke document chunks
- ✅ Working semantic search
- ✅ Answer generation with citations
- ✅ CLI test for Q&A functionality

---

### **Phase 2: Enhanced Appointment System** (Days 4-6)

**Objectives:**

- Extend existing calendar system
- Add doctor profiles
- Implement booking workflow
- Build confirmation system

**Tasks:**

1. **Database Setup** (`data/healthcare.db`)

   ```python
   # Create tables as per schema above
   # Seed with sample doctors:
   - Dr. Sarah Johnson (Neurologist, Stroke Specialist)
   - Dr. Michael Chen (Emergency Medicine)
   - Dr. Aisha Khan (Rehabilitation)
   ```
2. **Scheduler Module** (`modules/scheduler.py`)

   ```python
   class AppointmentScheduler:
       def __init__(self, db_path: str, calendar_assistant):
           self.db = sqlite3.connect(db_path)
           self.calendar = calendar_assistant

       def get_doctor_availability(self, doctor_id: int, date: str) -> List[dict]
       def check_conflicts(self, doctor_id: int, patient_id: int, start: str, end: str) -> bool
       def create_appointment(self, patient_id: int, doctor_id: int, ...) -> int
       def confirm_appointment(self, appointment_id: int) -> bool
       def cancel_appointment(self, appointment_id: int, reason: str) -> bool
   ```
3. **Integrate with Calendar** (extend `calendar_assistant.py`)

   ```python
   # Add appointment tags/categories
   # Color coding: PENDING (yellow), CONFIRMED (green), CANCELLED (red)
   # Event description includes patient details
   ```
4. **Booking Workflow**

   ```
   1. Patient: "Book appointment with Dr. Johnson"
   2. System: Shows doctor's available slots
   3. Patient: Selects time
   4. System: Checks conflicts, creates PENDING appointment
   5. System: Notifies doctor (console message for now)
   6. Doctor: Reviews and confirms
   7. System: Updates status, notifies patient
   ```

**Deliverables:**

- ✅ SQLite database with schema
- ✅ 3 sample doctors seeded
- ✅ Appointment CRUD operations
- ✅ Integration with Google Calendar
- ✅ Conflict detection working

---

### **Phase 3: Memory & Personalization** (Days 7-8)

**Objectives:**

- Track conversation history
- Implement user profiles
- Add context-aware responses
- Build analytics

**Tasks:**

1. **Memory Manager** (`modules/memory_manager.py`)

   ```python
   class MemoryManager:
       def save_conversation(self, user_id: int, role: str, message: str, context: dict)
       def get_conversation_history(self, user_id: int, limit: int = 10) -> List[dict]
       def get_user_context(self, user_id: int) -> dict
       def update_user_profile(self, user_id: int, preferences: dict)
   ```
2. **Context Features**

   ```python
   # Track:
   - Previous questions asked
   - Appointments history
   - Preferred doctors
   - Common concerns
   - Follow-up recommendations
   ```
3. **Personalization**

   ```python
   # Examples:
   "Welcome back, John! Last time you asked about stroke prevention."
   "You have an upcoming appointment with Dr. Johnson on Oct 28."
   "Based on your history, you might also be interested in..."
   ```
4. **Analytics**

   ```python
   # For doctors:
   - Total appointments this week/month
   - Most common patient concerns
   - Appointment confirmation rate

   # For patients:
   - Appointment history
   - Topics explored
   - Upcoming appointments
   ```

**Deliverables:**

- ✅ Conversation history saved to DB
- ✅ Context retrieval working
- ✅ Personalized greetings
- ✅ Basic analytics dashboard

---

### **Phase 4: Integration & UX Polish** (Days 9-11)

**Objectives:**

- Build unified CLI interface
- Role-based menus
- Error handling
- Testing

**Tasks:**

1. **Main Orchestrator** (`healthcare_assistant.py`)

   ```python
   class HealthcareAssistant:
       def __init__(self):
           self.rag = RAGEngine()
           self.scheduler = AppointmentScheduler()
           self.memory = MemoryManager()
           self.current_user = None
           self.current_role = None

       def login(self, user_id: str, role: str)
       def handle_patient_mode(self)
       def handle_doctor_mode(self)
       def process_message(self, message: str)
       def run(self)
   ```
2. **Beautiful CLI with Rich**

   ```python
   from rich.console import Console
   from rich.panel import Panel
   from rich.table import Table
   from rich.progress import Progress

   # Color-coded outputs
   # Tables for appointment listings
   # Progress bars for document loading
   # Panels for answers with citations
   ```
3. **Menu System**

   ```
   === PATIENT MODE ===
   1. Ask a medical question
   2. Book an appointment
   3. View my appointments
   4. View conversation history
   5. Switch to doctor mode
   6. Exit

   === DOCTOR MODE ===
   1. View pending appointments
   2. Confirm/reschedule appointments
   3. View today's schedule
   4. Manage availability
   5. View patient history
   6. Switch to patient mode
   7. Exit
   ```
4. **Error Handling**

   ```python
   # Handle:
   - Invalid inputs
   - Database errors
   - Calendar API failures
   - Embedding errors
   - No search results
   - Booking conflicts
   ```
5. **Testing Scenarios**

   ```
   Test 1: Patient asks "What is a stroke?"
   Test 2: Patient books appointment successfully
   Test 3: Patient tries to double-book (should warn)
   Test 4: Doctor confirms pending appointment
   Test 5: Conversation history retrieval
   Test 6: Citation accuracy in answers
   ```

**Deliverables:**

- ✅ Complete CLI application
- ✅ Role switching working
- ✅ Beautiful formatted output
- ✅ All features integrated
- ✅ Error handling robust
- ✅ 10+ test scenarios passed

---

### **Phase 5: Web UI (Optional)** (Days 12-14)

**Objectives:**

- Create web interface
- Real-time updates
- Dashboard visualizations

**Components:**

```
Frontend:
- Patient Portal (ask questions, book appointments)
- Doctor Dashboard (manage appointments, view analytics)
- Admin Panel (manage doctors, view system stats)

Backend:
- FastAPI or Flask server
- WebSocket for real-time updates
- REST API endpoints
```

**Out of Scope for Initial Prototype**
(Can be added later if needed)

---

## 🧪 Testing Strategy

### Unit Tests

```python
# test_rag_engine.py
def test_document_chunking()
def test_embedding_generation()
def test_semantic_search()
def test_citation_extraction()

# test_scheduler.py
def test_create_appointment()
def test_conflict_detection()
def test_confirm_appointment()
def test_cancel_appointment()

# test_memory.py
def test_save_conversation()
def test_retrieve_history()
def test_user_context()
```

### Integration Tests

```python
# test_end_to_end.py
def test_patient_books_appointment()
def test_doctor_confirms_appointment()
def test_rag_answer_quality()
def test_calendar_sync()
```

### Manual Testing Checklist

```
[ ] Patient can ask medical questions
[ ] Answers include proper citations
[ ] Sources are accurate and traceable
[ ] Patient can view available doctors
[ ] Patient can book appointment
[ ] Conflict detection prevents double-booking
[ ] Doctor receives notification of pending appointment
[ ] Doctor can confirm appointment
[ ] Calendar updates correctly
[ ] Conversation history is saved
[ ] Personalized greetings work
[ ] Error messages are helpful
[ ] System handles edge cases gracefully
```

---

## 📈 Success Metrics

### Functionality

- ✅ RAG answers 90%+ questions with citations
- ✅ Zero double-bookings (100% conflict detection)
- ✅ Appointment booking in < 5 steps
- ✅ Doctor confirmation in < 3 clicks
- ✅ Conversation context retained for session

### Performance

- ⚡ Answer generation < 3 seconds
- ⚡ Calendar availability check < 2 seconds
- ⚡ Vector search < 1 second
- ⚡ Database queries < 500ms

### User Experience

- 📱 Clear, intuitive CLI menus
- 🎨 Beautiful formatted output
- ⚠️ Helpful error messages
- 📚 Complete documentation

---

## 🚀 Deployment Plan (Future)

### For Production

1. **Cloud Hosting**: Deploy to AWS/GCP/Azure
2. **Database**: Migrate to PostgreSQL
3. **Vector DB**: Use Pinecone or Weaviate
4. **Web UI**: Deploy frontend separately
5. **Authentication**: Implement proper OAuth
6. **Notifications**: Email/SMS for appointments
7. **Monitoring**: Add logging and analytics
8. **Scaling**: Load balancing, caching

---

## 💡 Future Enhancements

### Advanced Features

- 📹 Video consultation integration
- 💊 Prescription management
- 📊 Health metrics tracking
- 🔔 Automated reminders
- 📱 Mobile app
- 🌐 Multi-language support
- 🤖 Voice interface
- 📈 Patient outcome tracking
- 🔬 Integration with lab results
- 📝 Medical records management

### AI Improvements

- Fine-tuned model on medical literature
- Multi-modal RAG (images, diagrams)
- Symptom checker with decision trees
- Risk assessment algorithms
- Personalized health recommendations

---

## 📝 Sample Conversations

### Conversation 1: Learning About Stroke

```
Patient: Hi, I want to learn about strokes.
```
