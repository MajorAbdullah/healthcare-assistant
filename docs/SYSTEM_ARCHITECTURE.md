# Healthcare Assistant System - Complete Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Project Structure](#project-structure)
3. [RAG System (Recommendation Engine)](#rag-system-recommendation-engine)
4. [Appointment Scheduling System](#appointment-scheduling-system)
5. [Database Architecture](#database-architecture)
6. [External Integrations](#external-integrations)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [Technology Stack](#technology-stack)

---

## System Overview

This is a comprehensive healthcare management system that combines:
- **AI-Powered Medical Q&A** using RAG (Retrieval Augmented Generation)
- **Intelligent Appointment Scheduling** with conflict detection
- **Google Calendar Integration** for automatic event synchronization
- **Patient and Doctor Portals** with CLI and web interfaces
- **Vector Database** for semantic search of medical documents
- **Conversation Memory** for context-aware interactions

### Key Statistics
- **Total Core Code:** ~4,663 lines of Python
- **API Endpoints:** 30+ REST endpoints
- **React Components:** 50+ components
- **Database Records:** 23 users, 3 doctors, 36 appointments, 60 conversations
- **Test Coverage:** 20+ test files

---

## Project Structure

```
/Users/abdullah/my projects/pipedream/
│
├── api/
│   └── main.py                          # FastAPI backend (1,282 lines)
│                                        # 30+ REST endpoints
│                                        # WebSocket support for real-time chat
│
├── modules/                             # Core Python modules (2,660 lines)
│   ├── rag_engine.py                    # RAG Q&A system (402 lines)
│   │                                    # Semantic search + LLM generation
│   │
│   ├── scheduler.py                     # Appointment scheduling (546 lines)
│   │                                    # Booking, conflicts, availability
│   │
│   ├── memory_manager.py                # Conversation & context (694 lines)
│   │                                    # Chat history, recommendations
│   │
│   ├── calendar_integration.py          # Google Calendar sync (453 lines)
│   │                                    # Pipedream MCP integration
│   │
│   ├── calendar_sync.py                 # Calendar utilities (313 lines)
│   └── calendar_assistant_wrapper.py    # Calendar assistant (251 lines)
│
├── utils/                               # Utility modules (720 lines)
│   ├── embeddings.py                    # Vector embeddings (181 lines)
│   │                                    # Gemini embedding-001 integration
│   │
│   ├── document_processor.py            # PDF/text processing (260 lines)
│   │                                    # Chunking strategy
│   │
│   └── db_setup.py                      # Database initialization (279 lines)
│
├── Frontend/                            # React/TypeScript UI
│   └── src/
│       ├── pages/                       # Patient & Doctor portals
│       ├── components/                  # Reusable UI components
│       └── lib/api.ts                   # Centralized API client (478 lines)
│
├── data/                                # Database & documents
│   ├── healthcare.db                    # SQLite database (structured data)
│   ├── vector_db/                       # ChromaDB vector store
│   │   ├── chroma.sqlite3               # ChromaDB metadata (688KB)
│   │   └── cca50074.../                 # Vector embeddings storage
│   └── medical_docs/                    # Medical documents for RAG
│
├── tests/                               # Comprehensive test suite
│   ├── test_rag_engine.py
│   ├── test_scheduler.py
│   └── ... (20+ test files)
│
├── docs/                                # Documentation
│   ├── COMPREHENSIVE_USER_GUIDE.md
│   └── SYSTEM_ARCHITECTURE.md           # This file
│
├── healthcare_assistant.py              # Patient CLI portal
├── doctor_portal.py                     # Doctor CLI portal
├── calendar_assistant.py                # Calendar integration CLI
└── config.py                            # System configuration
```

---

## RAG System (Recommendation Engine)

### Overview

The system uses **RAG (Retrieval Augmented Generation)** for intelligent medical Q&A. While not a traditional "recommendation system," it provides:
- **Semantic medical information retrieval** from vector database
- **Context-aware answers** with source citations
- **Pattern-based appointment recommendations** using conversation history

### Architecture Components

#### 1. Vector Database: ChromaDB

**Location:** `data/vector_db/`

**Purpose:** Stores medical document embeddings for semantic search

**Configuration:**
```python
# modules/rag_engine.py:47-60
client = chromadb.PersistentClient(path="./data/vector_db")
collection = client.get_or_create_collection(
    name="stroke_medical_docs",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity
)
```

**Storage Structure:**
- **Documents:** Original text chunks (500 chars, 50 char overlap)
- **Embeddings:** 768-dimensional vectors from Gemini
- **Metadata:** Source file, doc type, author, URL
- **IDs:** Unique identifiers like `chunk_0_stroke_overview`

**Files:**
- `chroma.sqlite3` - Metadata and index (688KB)
- `cca50074-13be-4a7e-9282-38935ebc0fab/` - Binary vector data

#### 2. Embedding Generation

**Location:** `utils/embeddings.py`

**Model:** Google Gemini `models/embedding-001`

**Features:**
```python
# utils/embeddings.py:37-120
def get_embeddings(texts, task_type="RETRIEVAL_DOCUMENT"):
    """
    Generate embeddings with:
    - Batch processing (50 texts per batch)
    - Exponential backoff retry (2s, 4s, 8s)
    - Task-specific embeddings:
        - RETRIEVAL_DOCUMENT: For indexing documents
        - RETRIEVAL_QUERY: For search queries
    - Output: 768-dimensional vectors
    """
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = 'models/embedding-001'

    # Generate embeddings with retry logic
    for attempt in range(max_retries):
        try:
            result = genai.embed_content(
                model=model,
                content=texts,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            time.sleep(2 ** attempt)  # Exponential backoff
```

#### 3. Document Processing

**Location:** `utils/document_processor.py`

**Supported Formats:** PDF, TXT, MD

**Chunking Strategy:**
```python
# utils/document_processor.py:86-181
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Smart text chunking:
    1. Split by sentences using spaCy
    2. Combine sentences into chunks (~500 chars)
    3. Add 50-character overlap between chunks
    4. Preserve sentence boundaries

    Why this matters:
    - Maintains semantic coherence
    - Prevents mid-sentence splits
    - Overlap ensures context isn't lost
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            chunks.append(current_chunk)
            # Add overlap from previous chunk
            current_chunk = current_chunk[-overlap:] + sentence
        else:
            current_chunk += sentence

    return chunks
```

**PDF Processing:**
- **Primary:** `pdfplumber` (better text extraction)
- **Fallback:** `pypdf` (if pdfplumber fails)
- **Cleaning:** Remove headers, footers, page numbers

#### 4. RAG Query Pipeline

**Location:** `modules/rag_engine.py:252-294`

**Process Flow:**
```python
def query(question: str, n_results: int = 5):
    """
    Complete RAG pipeline:

    1. EMBEDDING GENERATION
       question → Gemini embedding-001 → 768-dim query vector

    2. SEMANTIC SEARCH
       query_vector → ChromaDB.query() → Top 5 similar chunks
       Uses cosine similarity for matching

    3. CONTEXT FORMATTING
       Format retrieved chunks with citations:
       [1] Source: stroke_overview.md
       Text from first chunk...

       [2] Source: treatment_guidelines.md
       Text from second chunk...

    4. ANSWER GENERATION
       Prompt: "Answer based on context below..."
       Context: [formatted chunks with citations]
       Question: [user question]
       ↓
       Gemini LLM (gemini-2.5-flash, temp=0.1)
       ↓
       Answer with inline citations like [1], [2]

    5. RETURN STRUCTURED RESPONSE
       {
         "answer": "Stroke is... [1] Treatment involves... [2]",
         "citations": ["stroke_overview.md", "treatment_guidelines.md"],
         "sources": [metadata objects],
         "timestamp": "2025-10-29T10:30:00"
       }
    """

    # Step 1: Generate query embedding
    query_embedding = get_embeddings([question], task_type="RETRIEVAL_QUERY")[0]

    # Step 2: Semantic search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Step 3: Format context
    context = format_context_with_citations(results)

    # Step 4: Generate answer
    prompt = f"""Answer this question based on the context below.
    Use citations like [1], [2] to reference sources.

    Context:
    {context}

    Question: {question}

    Answer:"""

    answer = generate_with_gemini(prompt, temperature=0.1, max_tokens=1024)

    # Step 5: Return response
    return {
        "answer": answer,
        "citations": results['metadatas'],
        "sources": results['documents']
    }
```

**LLM Configuration:**
- **Model:** `gemini-2.5-flash`
- **Temperature:** 0.1 (factual, consistent responses)
- **Max Tokens:** 1,024
- **Context Window:** Top 5 relevant chunks (~2,500 characters)

### Smart Appointment Recommendations

**Location:** `modules/memory_manager.py:513-593`

While the main RAG system handles medical Q&A, the memory manager provides intelligent appointment suggestions based on user patterns:

**Features:**

1. **Pattern Analysis**
```python
def get_recommendations(user_id):
    """
    Analyze user's appointment history:
    - Most visited doctor (by specialty)
    - Preferred time slots (morning/afternoon/evening)
    - Booking frequency patterns
    - Average consultation duration
    """
    conversations = get_user_conversations(user_id, limit=50)
    appointments = scheduler.get_patient_appointments(user_id)

    # Analyze patterns
    most_visited_doctor = max(set(appointments), key=appointments.count)
    preferred_times = analyze_time_preferences(appointments)

    return {
        "suggested_doctor": most_visited_doctor,
        "preferred_slots": preferred_times,
        "needs_followup": check_followup_needed(appointments)
    }
```

2. **Follow-up Suggestions**
```python
# Suggest follow-up after 30+ days
last_appointment = max(appointments, key=lambda x: x['date'])
if (today - last_appointment['date']).days > 30:
    return "It's been over a month. Would you like to schedule a follow-up?"
```

3. **Health Topic Tracking**
```python
# Extract topics from conversation history
# Stored in conversations.context_data JSON field
{
    "topics": ["stroke recovery", "physical therapy", "medication"],
    "sentiment": "concerned",
    "urgency": "moderate"
}
```

4. **Personalized Greetings**
```python
def generate_greeting(user_id):
    """
    Context-aware messages:
    - "Welcome back! You have an appointment tomorrow with Dr. Smith."
    - "How are you feeling after your last consultation?"
    - "I noticed you asked about stroke prevention. Would you like more info?"
    """
```

---

## Appointment Scheduling System

### Core Scheduler Module

**Location:** `modules/scheduler.py` (546 lines)

The scheduling system provides complete appointment lifecycle management with intelligent conflict detection.

### Key Components

#### 1. Doctor Management

```python
# modules/scheduler.py:50-100

def get_all_doctors():
    """
    Retrieve all doctors from database.

    Returns:
        List of doctor objects with:
        - doctor_id, name, specialty
        - email, phone
        - calendar_id (for Google Calendar sync)
        - consultation_duration (default 30 min)

    Sample doctors:
    - Dr. Sarah Johnson (Neurology - Stroke Specialist)
    - Dr. Michael Chen (Emergency Medicine)
    - Dr. Aisha Khan (Rehabilitation & Recovery)
    """
    query = "SELECT * FROM doctors WHERE is_active = 1"
    return db.execute(query).fetchall()

def get_doctors_by_specialty(specialty):
    """
    Filter doctors by medical specialty.
    Useful for specialty-specific appointment booking.
    """
    query = """
        SELECT * FROM doctors
        WHERE specialty LIKE ? AND is_active = 1
    """
    return db.execute(query, [f"%{specialty}%"]).fetchall()
```

#### 2. Availability System

**Location:** `modules/scheduler.py:148-227`

**Database Schema:**
```sql
CREATE TABLE doctor_availability (
    availability_id INTEGER PRIMARY KEY,
    doctor_id INTEGER,
    day_of_week INTEGER,  -- 0=Monday, 6=Sunday
    start_time TEXT,      -- "09:00"
    end_time TEXT,        -- "17:00"
    is_active BOOLEAN,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);
```

**Availability Algorithm:**
```python
def get_doctor_availability(doctor_id, date):
    """
    Generate available time slots for a specific doctor and date.

    Process:
    1. Get doctor's working hours for day_of_week
    2. Generate 30-minute slots (or custom duration)
    3. Filter out already booked appointments
    4. Return list of available slots

    Example:
    Input: doctor_id=1, date="2025-10-30"
    Output: ["09:00", "09:30", "10:00", "14:00", "14:30"]
    """

    # Step 1: Get doctor's schedule for this day
    day_of_week = datetime.strptime(date, "%Y-%m-%d").weekday()

    query = """
        SELECT start_time, end_time
        FROM doctor_availability
        WHERE doctor_id = ? AND day_of_week = ? AND is_active = 1
    """
    schedule = db.execute(query, [doctor_id, day_of_week]).fetchone()

    if not schedule:
        return []  # Doctor not available on this day

    # Step 2: Generate time slots
    consultation_duration = get_doctor(doctor_id)['consultation_duration']
    slots = generate_time_slots(
        schedule['start_time'],
        schedule['end_time'],
        duration=consultation_duration
    )

    # Step 3: Filter booked slots
    query = """
        SELECT start_time, end_time
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND status IN ('scheduled', 'confirmed')
    """
    booked = db.execute(query, [doctor_id, date]).fetchall()

    available_slots = [
        slot for slot in slots
        if not is_slot_booked(slot, booked)
    ]

    return available_slots
```

#### 3. Conflict Detection

**Location:** `modules/scheduler.py:229-260`

**Algorithm:**
```python
def check_conflict(doctor_id, date, start_time, end_time):
    """
    Check for appointment conflicts using SQL overlap detection.

    Conflict occurs when:
    - Same doctor
    - Same date
    - Time ranges overlap
    - Existing appointment is not cancelled

    Time overlap logic:
    Two ranges [A_start, A_end] and [B_start, B_end] overlap if:
    NOT (A_end <= B_start OR A_start >= B_end)

    Which simplifies to:
    (A_end > B_start) AND (A_start < B_end)
    """

    query = """
        SELECT COUNT(*) as count
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND status IN ('scheduled', 'confirmed')
        AND (
            -- Overlap condition
            (end_time > ? AND start_time < ?)
        )
    """

    result = db.execute(query, [doctor_id, date, start_time, end_time]).fetchone()

    return result['count'] > 0
```

**Visual Example:**
```
Existing appointment:  [09:00 -------- 09:30]
New request:           [09:15 -------- 09:45]
                                ↑ CONFLICT!

Existing appointment:  [09:00 -------- 09:30]
New request:                             [10:00 -------- 10:30]
                                         ↑ NO CONFLICT ✓
```

#### 4. Booking Process

**Location:** `modules/scheduler.py:262-314`

**Complete Workflow:**
```python
def book_appointment(user_id, doctor_id, appointment_date, start_time, reason):
    """
    Complete appointment booking workflow.

    Steps:
    1. Validate inputs
    2. Calculate end time
    3. Check conflicts
    4. Insert into database
    5. Return result

    Returns:
        (success: bool, message: str, appointment_id: int)
    """

    # Step 1: Validate doctor exists
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return (False, "Doctor not found", None)

    # Step 2: Calculate end time
    consultation_duration = doctor['consultation_duration']  # default: 30
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = start_dt + timedelta(minutes=consultation_duration)
    end_time = end_dt.strftime("%H:%M")

    # Step 3: Check for conflicts
    has_conflict = check_conflict(doctor_id, appointment_date, start_time, end_time)
    if has_conflict:
        return (False, "Time slot not available", None)

    # Step 4: Insert into database
    query = """
        INSERT INTO appointments (
            user_id, doctor_id, appointment_date,
            start_time, end_time, status, reason, created_at
        ) VALUES (?, ?, ?, ?, ?, 'scheduled', ?, datetime('now'))
    """

    cursor = db.execute(query, [
        user_id, doctor_id, appointment_date,
        start_time, end_time, reason
    ])

    appointment_id = cursor.lastrowid
    db.commit()

    # Step 5: Return success
    return (True, "Appointment booked successfully", appointment_id)
```

#### 5. Appointment Management

**Additional Functions:**

```python
# Retrieve appointment with full details (JOIN query)
def get_appointment(appointment_id):
    """
    Fetch appointment with patient and doctor information.

    Returns:
        {
            'appointment_id': 123,
            'patient_name': 'John Doe',
            'patient_email': 'john@example.com',
            'doctor_name': 'Dr. Sarah Johnson',
            'specialty': 'Neurology',
            'appointment_date': '2025-10-30',
            'start_time': '10:00',
            'end_time': '10:30',
            'status': 'confirmed',
            'reason': 'Follow-up consultation',
            'calendar_event_id': 'abc123xyz'
        }
    """
    query = """
        SELECT
            a.*,
            u.name as patient_name,
            u.email as patient_email,
            d.name as doctor_name,
            d.specialty,
            d.calendar_id
        FROM appointments a
        JOIN users u ON a.user_id = u.user_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_id = ?
    """
    return db.execute(query, [appointment_id]).fetchone()

# Get patient's appointment history
def get_patient_appointments(user_id, include_cancelled=False):
    """Fetch all appointments for a patient"""
    status_filter = "" if include_cancelled else "AND status != 'cancelled'"
    query = f"""
        SELECT * FROM appointments
        WHERE user_id = ? {status_filter}
        ORDER BY appointment_date DESC, start_time DESC
    """
    return db.execute(query, [user_id]).fetchall()

# Get doctor's schedule
def get_doctor_appointments(doctor_id, date=None):
    """Fetch appointments for a doctor (optionally filtered by date)"""
    date_filter = f"AND appointment_date = '{date}'" if date else ""
    query = f"""
        SELECT * FROM appointments
        WHERE doctor_id = ? {date_filter}
        AND status IN ('scheduled', 'confirmed')
        ORDER BY appointment_date, start_time
    """
    return db.execute(query, [doctor_id]).fetchall()

# Cancel appointment
def cancel_appointment(appointment_id):
    """
    Update status to 'cancelled'.
    Note: Does NOT delete from database (maintains history)
    """
    query = "UPDATE appointments SET status = 'cancelled' WHERE appointment_id = ?"
    db.execute(query, [appointment_id])
    db.commit()

# Confirm appointment
def confirm_appointment(appointment_id):
    """Update status from 'scheduled' to 'confirmed'"""
    query = "UPDATE appointments SET status = 'confirmed' WHERE appointment_id = ?"
    db.execute(query, [appointment_id])
    db.commit()
```

### Booking Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Initiates Booking                    │
│   {user_id, doctor_id, date, time, reason, sync_calendar}  │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│                  Validation & Preparation                     │
├──────────────────────────────────────────────────────────────┤
│  1. Validate doctor exists     ✓                             │
│  2. Calculate end_time         start + consultation_duration │
│  3. Check user exists          ✓                             │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│                    Conflict Detection                         │
├──────────────────────────────────────────────────────────────┤
│  SQL Query: Check for overlapping appointments               │
│  WHERE doctor_id = ? AND date = ?                            │
│  AND (end_time > start_time AND start_time < end_time)      │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
                 Conflict exists?
                       ↓
         ┌─────────────┴─────────────┐
         ↓                           ↓
       YES                          NO
         ↓                           ↓
   Return error:              ┌──────────────┐
   "Time slot not             │ INSERT INTO  │
   available"                 │ appointments │
                              └──────┬───────┘
                                     ↓
                              appointment_id created
                                     ↓
                          sync_calendar = True?
                                     ↓
                       ┌─────────────┴─────────────┐
                       ↓                           ↓
                      YES                         NO
                       ↓                           ↓
         ┌──────────────────────┐          Return success
         │ Google Calendar Sync │          {appointment_id}
         └──────────┬───────────┘
                    ↓
      create_calendar_event_async()
                    ↓
         ┌──────────────────────┐
         │ 1. Fetch details     │
         │ 2. Format event      │
         │ 3. Call MCP API      │
         │ 4. Update DB with    │
         │    calendar_event_id │
         └──────────┬───────────┘
                    ↓
           Return full success
           {appointment_id, calendar_event_id}
```

---

## Database Architecture

The system uses a dual-database architecture:
- **SQLite** for structured, relational data
- **ChromaDB** for vector embeddings and semantic search

### A. SQLite Database

**Location:** `data/healthcare.db`

**Schema:**

#### 1. `users` Table (23 records)

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automatic timestamp update trigger
CREATE TRIGGER update_users_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = datetime('now')
    WHERE user_id = NEW.user_id;
END;
```

**Purpose:** Store patient information and authentication

**Indexes:**
- `PRIMARY KEY` on `user_id` (auto-increment)
- `UNIQUE` constraint on `email`

#### 2. `doctors` Table (3 records)

```sql
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    calendar_id TEXT,  -- Google Calendar email
    consultation_duration INTEGER DEFAULT 30,  -- minutes
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_doctors_specialty ON doctors(specialty);
```

**Sample Data:**
```
doctor_id | name              | specialty                    | calendar_id
----------|-------------------|------------------------------|---------------------------
1         | Dr. Sarah Johnson | Neurology - Stroke Specialist| pinkpantherking20@gmail.com
2         | Dr. Michael Chen  | Emergency Medicine           | NULL
3         | Dr. Aisha Khan    | Rehabilitation & Recovery    | NULL
```

**Purpose:** Store doctor profiles and calendar integration settings

#### 3. `appointments` Table (36 records)

```sql
CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TEXT NOT NULL,  -- "HH:MM" format
    end_time TEXT NOT NULL,
    status TEXT DEFAULT 'scheduled',  -- scheduled, confirmed, cancelled, completed
    reason TEXT,
    notes TEXT,  -- Doctor's notes after consultation
    calendar_event_id TEXT,  -- Google Calendar event ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Performance indexes
CREATE INDEX idx_appointments_user ON appointments(user_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Composite index for common query
CREATE INDEX idx_appointments_doctor_date
ON appointments(doctor_id, appointment_date);
```

**Status Values:**
- `scheduled` - Initial booking state
- `confirmed` - Doctor/patient confirmed
- `cancelled` - Appointment cancelled (soft delete)
- `completed` - Consultation finished

**Purpose:** Core appointment management with full history

#### 4. `doctor_availability` Table

```sql
CREATE TABLE doctor_availability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,  -- 0=Monday, 6=Sunday
    start_time TEXT NOT NULL,      -- "09:00"
    end_time TEXT NOT NULL,        -- "17:00"
    is_active BOOLEAN DEFAULT 1,

    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE INDEX idx_availability_doctor ON doctor_availability(doctor_id);
```

**Sample Data:**
```
availability_id | doctor_id | day_of_week | start_time | end_time | is_active
----------------|-----------|-------------|------------|----------|----------
1               | 1         | 0           | 09:00      | 17:00    | 1
2               | 1         | 1           | 09:00      | 17:00    | 1
3               | 1         | 2           | 09:00      | 17:00    | 1
4               | 1         | 3           | 09:00      | 17:00    | 1
5               | 1         | 4           | 09:00      | 13:00    | 1
```

**Purpose:** Define doctor working hours for availability checks

#### 5. `conversations` Table (60 records)

```sql
CREATE TABLE conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message_type TEXT NOT NULL,  -- 'user', 'assistant', 'system'
    message_text TEXT NOT NULL,
    context_data TEXT,  -- JSON string for additional context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_created ON conversations(created_at);
```

**context_data JSON Structure:**
```json
{
    "topics": ["stroke recovery", "medication"],
    "sentiment": "concerned",
    "urgency": "moderate",
    "extracted_entities": {
        "symptoms": ["headache", "dizziness"],
        "medications": ["aspirin"]
    }
}
```

**Purpose:** Store conversation history for context-aware responses

#### 6. `user_preferences` Table

```sql
CREATE TABLE user_preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    email_notifications BOOLEAN DEFAULT 1,
    sms_reminders BOOLEAN DEFAULT 1,
    calendar_sync BOOLEAN DEFAULT 1,
    preferred_language TEXT DEFAULT 'en',
    timezone TEXT DEFAULT 'Asia/Karachi',

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

**Purpose:** User-specific settings and preferences

### Database Statistics

**Current Data (as of analysis):**
- **23 registered users**
- **3 active doctors**
- **36 appointments** (scheduled, confirmed, completed)
- **60 conversation messages** (user + assistant)

**Storage Size:**
- `healthcare.db` - ~2-3 MB
- Properly indexed for fast queries
- Foreign key constraints enforced

### B. Vector Database: ChromaDB

**Location:** `data/vector_db/`

**Purpose:** Store document embeddings for semantic search in the RAG system

#### File Structure

```
vector_db/
├── chroma.sqlite3                              # Metadata & index (688KB)
└── cca50074-13be-4a7e-9282-38935ebc0fab/      # Collection ID
    ├── data_level0.bin                         # HNSW index (binary)
    ├── header.bin                              # Collection header
    ├── length.bin                              # Document lengths
    └── link_lists.bin                          # Graph links for HNSW
```

#### Collection Configuration

```python
# modules/rag_engine.py:47-60

client = chromadb.PersistentClient(path="./data/vector_db")

collection = client.get_or_create_collection(
    name="stroke_medical_docs",
    metadata={
        "hnsw:space": "cosine",  # Cosine similarity for semantic search
        "hnsw:construction_ef": 200,  # Build quality
        "hnsw:search_ef": 100  # Search quality
    }
)
```

**HNSW Algorithm:**
- **Hierarchical Navigable Small World** graph
- Fast approximate nearest neighbor search
- Trade-off: Speed vs. accuracy (tunable)
- O(log n) query time complexity

#### Data Storage Format

**Add Documents:**
```python
collection.add(
    documents=[
        "Stroke is a medical emergency that occurs when blood flow to the brain is interrupted..."
    ],
    embeddings=[
        [0.123, -0.456, 0.789, ..., 0.234]  # 768-dimensional vector
    ],
    metadatas=[
        {
            'source': 'stroke_overview.md',
            'doc_type': 'Document',
            'author': 'Medical Team',
            'url': 'https://example.com/stroke-overview',
            'chunk_index': 0,
            'total_chunks': 15
        }
    ],
    ids=['chunk_0_stroke_overview']  # Unique identifier
)
```

**Query Process:**
```python
results = collection.query(
    query_embeddings=[[0.111, -0.222, 0.333, ..., 0.444]],
    n_results=5,  # Top 5 most similar
    include=['documents', 'metadatas', 'distances']
)

# Returns:
{
    'ids': [['chunk_0_stroke_overview', 'chunk_5_treatment', ...]],
    'documents': [['Full text of chunk 0', 'Full text of chunk 5', ...]],
    'metadatas': [[{'source': '...', ...}, ...]],
    'distances': [[0.12, 0.18, 0.23, 0.29, 0.31]]  # Cosine distances (lower = more similar)
}
```

#### Storage Characteristics

**Embedding Vector:**
- **Dimensions:** 768 (from Gemini embedding-001)
- **Data Type:** float32
- **Storage per vector:** 768 × 4 bytes = 3,072 bytes (~3KB)

**Typical Collection Size:**
- 1,000 chunks × 3KB = ~3MB (vectors only)
- Additional metadata: ~1MB
- HNSW index overhead: ~2MB
- **Total:** ~6MB for 1,000 documents

**Current Size:**
- `chroma.sqlite3`: 688KB
- Binary files: ~2-3MB
- Estimated ~500-800 document chunks indexed

#### Performance Optimization

**Indexes:**
- HNSW graph for fast nearest neighbor search
- SQLite B-tree for metadata queries

**Query Speed:**
- Average: 10-50ms for semantic search
- Depends on collection size and `search_ef` parameter

**Scalability:**
- Can handle 100,000+ documents efficiently
- Persistent storage (survives restarts)
- Incremental updates supported

### Database Relationship Diagram

```
┌─────────────────────┐
│       users         │
│  ───────────────    │
│  • user_id (PK)     │
│  • name             │
│  • email (UNIQUE)   │
│  • phone            │
│  • date_of_birth    │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ↓
┌───────────────────────────┐          ┌─────────────────────┐
│     appointments          │  N:1     │      doctors        │
│  ──────────────────────   │──────────│  ────────────────   │
│  • appointment_id (PK)    │          │  • doctor_id (PK)   │
│  • user_id (FK)           │          │  • name             │
│  • doctor_id (FK)         │←─────────│  • specialty        │
│  • appointment_date       │          │  • calendar_id      │
│  • start_time             │          │  • consultation_    │
│  • end_time               │          │    duration         │
│  • status                 │          └──────────┬──────────┘
│  • reason                 │                     │
│  • notes                  │                     │ 1:N
│  • calendar_event_id      │                     │
└───────────────────────────┘                     ↓
           │                         ┌──────────────────────┐
           │ 1:1 (optional)          │ doctor_availability  │
           │                         │  ─────────────────   │
           ↓                         │  • availability_id   │
┌───────────────────────┐            │  • doctor_id (FK)    │
│  Google Calendar      │            │  • day_of_week       │
│  ──────────────────   │            │  • start_time        │
│  • event_id           │            │  • end_time          │
│  • meet_link          │            │  • is_active         │
│  • attendees          │            └──────────────────────┘
└───────────────────────┘

┌─────────────────────┐
│   conversations     │
│  ────────────────   │
│  • conversation_id  │
│  • user_id (FK)     │──┐
│  • message_type     │  │ N:1
│  • message_text     │  │
│  • context_data     │  │
│  • created_at       │  │
└─────────────────────┘  │
                         │
                         ↓
            ┌────────────────────┐
            │  users (linked)    │
            └────────────────────┘

┌──────────────────────────────────────┐
│         ChromaDB (Vector DB)         │
│  ─────────────────────────────────   │
│  Collection: stroke_medical_docs     │
│  • document chunks                   │
│  • 768-dim embeddings                │
│  • metadata (source, type)           │
│  • HNSW index                        │
└──────────────────────────────────────┘
     ↑                          ↑
     │ Writes                   │ Queries
     │                          │
┌────┴──────────┐   ┌───────────┴──────┐
│  document_    │   │   rag_engine.py  │
│  processor.py │   │   (semantic      │
│  (indexing)   │   │    search)       │
└───────────────┘   └──────────────────┘
```

---

## External Integrations

### Google Calendar Integration

The system integrates with Google Calendar to automatically sync appointments, generate Google Meet links, and send email notifications.

**Primary Implementation:** `modules/calendar_integration.py` (453 lines)

#### Architecture: Pipedream MCP (Model Context Protocol)

**What is Pipedream MCP?**
- **MCP:** Model Context Protocol - a standard for LLM-external service communication
- **Pipedream:** Integration platform that provides OAuth and API access layer
- **Benefits:**
  - Handles OAuth flow automatically
  - Manages token refresh
  - Provides unified API across multiple services

**Configuration:**
```python
# modules/calendar_integration.py:47-64

from pipedream import Client as PipedreamClient

# Pipedream project credentials
project_id = os.getenv("PIPEDREAM_PROJECT_ID")
client_id = os.getenv("PIPEDREAM_CLIENT_ID")
client_secret = os.getenv("PIPEDREAM_CLIENT_SECRET")
environment = "development"  # or "production"

# Initialize Pipedream client
pd_client = PipedreamClient(
    project_id=project_id,
    environment=environment
)

# Generate access token
access_token = pd_client.generate_access_token(
    client_id=client_id,
    client_secret=client_secret
)
```

**MCP Server Configuration:**
```python
# modules/calendar_integration.py:66-89

from mcp import Client as MCPClient

mcp_client = MCPClient({
    "mcpServers": {
        "pipedream": {
            "transport": "http",
            "url": "https://remote.mcp.pipedream.net",
            "headers": {
                "Authorization": f"Bearer {access_token}",
                "x-pd-project-id": project_id,
                "x-pd-environment": environment,
                "x-pd-external-user-id": "user-123",  # Your user ID
                "x-pd-app-slug": "google_calendar"
            }
        }
    }
})
```

#### Event Creation Process

**Function:** `create_calendar_event_async(appointment_id)`

**Location:** `modules/calendar_integration.py:149-241`

**Step-by-Step Process:**

```python
async def create_calendar_event_async(appointment_id):
    """
    Create Google Calendar event from appointment.

    Process:
    1. Fetch appointment details from database
    2. Handle timezone conversion (Asia/Karachi)
    3. Format event data
    4. Call MCP API to create event
    5. Store event_id back in database
    6. Handle errors gracefully
    """

    # STEP 1: Fetch appointment details
    appointment = scheduler.get_appointment(appointment_id)

    if not appointment:
        logger.error(f"Appointment {appointment_id} not found")
        return None

    # Extract data
    patient_name = appointment['patient_name']
    patient_email = appointment['patient_email']
    doctor_name = appointment['doctor_name']
    doctor_email = appointment['calendar_id']  # Doctor's Google Calendar email
    specialty = appointment['specialty']
    date = appointment['appointment_date']
    start_time = appointment['start_time']
    end_time = appointment['end_time']
    reason = appointment['reason']

    # STEP 2: Timezone Handling (CRITICAL!)
    import pytz
    from datetime import datetime

    # Create timezone-aware datetimes
    pkt_tz = pytz.timezone('Asia/Karachi')  # UTC+5

    # Parse date and time
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

    # Localize to timezone (adds UTC offset)
    start_aware = pkt_tz.localize(start_dt)
    end_aware = pkt_tz.localize(end_dt)

    # Convert to ISO 8601 format for Google Calendar API
    start_iso = start_aware.isoformat()  # "2025-10-30T10:00:00+05:00"
    end_iso = end_aware.isoformat()      # "2025-10-30T10:30:00+05:00"

    # STEP 3: Format event data
    summary = f"Medical Appointment: {patient_name} with {doctor_name}"

    description = f"""
    Healthcare Assistant Appointment
    ================================

    Patient Information:
    -------------------
    Name: {patient_name}
    Email: {patient_email}

    Doctor Information:
    ------------------
    Name: {doctor_name}
    Specialty: {specialty}
    Email: {doctor_email}

    Appointment Details:
    -------------------
    Date: {date}
    Time: {start_time} - {end_time}
    Reason: {reason}
    Appointment ID: {appointment_id}

    Please arrive 5 minutes early.
    A Google Meet link has been generated for this appointment.
    """

    # Attendees list
    attendees = [patient_email, doctor_email]

    # STEP 4: Call MCP API
    try:
        # Create MCP client connection
        async with mcp_client:
            # Call google_calendar-create-event tool
            result = await mcp_client.call_tool(
                tool_name='google_calendar-create-event',
                arguments={
                    'instruction': f"""
                        Create a calendar event with these details:
                        - Summary: {summary}
                        - Start: {start_iso}
                        - End: {end_iso}
                        - Attendees: {', '.join(attendees)}
                        - Description: {description}
                        - Add Google Meet video conferencing link
                        - Send email notifications to all attendees
                        - Set reminder 30 minutes before
                    """
                }
            )

            # Parse response
            event_data = json.loads(result['content'][0]['text'])
            event_id = event_data['id']
            meet_link = event_data['hangoutLink']

            logger.info(f"Created event: {event_id}")
            logger.info(f"Meet link: {meet_link}")

    except Exception as e:
        logger.error(f"Failed to create calendar event: {str(e)}")
        return None

    # STEP 5: Update database with event_id
    query = """
        UPDATE appointments
        SET calendar_event_id = ?
        WHERE appointment_id = ?
    """
    db.execute(query, [event_id, appointment_id])
    db.commit()

    logger.info(f"Updated appointment {appointment_id} with event {event_id}")

    return {
        'event_id': event_id,
        'meet_link': meet_link,
        'success': True
    }
```

#### Timezone Handling Deep Dive

**Why Timezone Handling is Critical:**
```python
# WITHOUT proper timezone handling:
start_dt = datetime(2025, 10, 30, 10, 0)  # Naive datetime
# → Google interprets as UTC
# → Shows as 10:00 UTC = 15:00 PKT (wrong!)

# WITH proper timezone handling:
start_dt = pkt_tz.localize(datetime(2025, 10, 30, 10, 0))
# → Creates: 2025-10-30T10:00:00+05:00
# → Google correctly shows 10:00 in Pakistan time ✓
```

**Location:** `modules/calendar_integration.py:173-191`

**Implementation:**
```python
import pytz
from datetime import datetime

# Define timezone
pkt_tz = pytz.timezone('Asia/Karachi')  # UTC+5

# Parse datetime string
naive_dt = datetime.strptime("2025-10-30 10:00", "%Y-%m-%d %H:%M")

# Add timezone information
aware_dt = pkt_tz.localize(naive_dt)

# Convert to ISO 8601 for Google Calendar API
iso_string = aware_dt.isoformat()
# Result: "2025-10-30T10:00:00+05:00"
```

**Supported Timezones:**
- Default: `Asia/Karachi` (UTC+5)
- Configurable in `config.py`
- All pytz timezones supported

#### Features Provided by Integration

1. **Automatic Event Creation**
   - Triggered on appointment booking
   - Adds to both patient and doctor calendars

2. **Google Meet Links**
   - Auto-generated for each appointment
   - Included in calendar event
   - Sent to all attendees

3. **Email Notifications**
   - Sent to patient and doctor
   - Includes appointment details
   - Calendar invite attached

4. **Reminders**
   - 30 minutes before appointment
   - Configurable in event creation

5. **Attendee Management**
   - Adds patient and doctor as attendees
   - Optional: Add additional participants

6. **Event Updates**
   - Can modify existing events
   - Cancel events when appointment cancelled

#### Configuration Requirements

**Environment Variables (.env):**
```bash
# Pipedream credentials
PIPEDREAM_PROJECT_ID=proj_abc123
PIPEDREAM_CLIENT_ID=client_xyz789
PIPEDREAM_CLIENT_SECRET=secret_def456

# Google Calendar settings
TIMEZONE=Asia/Karachi
CALENDAR_SYNC_ENABLED=true

# Doctor's Google Calendar email (in doctors table)
# calendar_id column should contain doctor's Gmail address
```

**config.py Settings:**
```python
# modules/calendar_integration.py references config.py

TIMEZONE = "Asia/Karachi"
CALENDAR_SYNC_ENABLED = True
DEFAULT_REMINDER_MINUTES = 30
INCLUDE_MEET_LINK = True
SEND_EMAIL_NOTIFICATIONS = True
```

#### Error Handling

```python
# modules/calendar_integration.py:230-241

try:
    result = await create_calendar_event_async(appointment_id)
    if result and result['success']:
        logger.info(f"Calendar sync successful: {result['event_id']}")
        return result
    else:
        logger.warning(f"Calendar sync failed for appointment {appointment_id}")
        # Appointment still created, just without calendar sync
        return None
except Exception as e:
    logger.error(f"Calendar integration error: {str(e)}")
    # Fail gracefully - appointment booking succeeds even if calendar fails
    return None
```

**Graceful Degradation:**
- If calendar sync fails, appointment is still booked
- User can manually add to calendar later
- Error logged for debugging

#### API Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                  Appointment Booking (api/main.py)           │
└────────────────────────────┬─────────────────────────────────┘
                             ↓
                    sync_calendar=True?
                             ↓
              ┌──────────────┴───────────────┐
              ↓                              ↓
             YES                             NO
              ↓                              │
┌──────────────────────────────────┐        │
│  calendar_integration.py         │        │
│  create_calendar_event_async()   │        │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  1. Fetch appointment details   │         │
│  2. Localize timezone            │         │
│  3. Format event data            │         │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  Pipedream Client                │         │
│  • Generate access_token         │         │
│  • Add auth headers              │         │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  MCP Client                      │         │
│  POST https://remote.mcp.        │         │
│       pipedream.net              │         │
│  Headers:                        │         │
│    Authorization: Bearer token   │         │
│    x-pd-project-id: ...          │         │
│    x-pd-app-slug: google_calendar│         │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  Pipedream MCP Server            │         │
│  • Validates OAuth token         │         │
│  • Routes to Google Calendar API │         │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  Google Calendar API             │         │
│  • Creates calendar event        │         │
│  • Generates Meet link           │         │
│  • Sends email notifications     │         │
│  • Returns event_id              │         │
└─────────────┬────────────────────┘        │
              ↓                              │
┌─────────────────────────────────┐         │
│  Response Processing             │         │
│  • Extract event_id              │         │
│  • Extract meet_link             │         │
│  • Update appointments table     │         │
└─────────────┬────────────────────┘        │
              ↓                              │
              └──────────────┬───────────────┘
                             ↓
┌──────────────────────────────────────────────────────────────┐
│  Return to API                                               │
│  {                                                           │
│    appointment_id: 123,                                      │
│    calendar_event_id: "abc123xyz",                           │
│    meet_link: "https://meet.google.com/abc-defg-hij",        │
│    success: true                                             │
│  }                                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. Medical Q&A Flow (RAG System)

```
┌─────────────────────────────────────────────────────────────┐
│                     User asks question                       │
│   "What are the symptoms of stroke?"                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│                Frontend/CLI Input                            │
│  • React chat component (Frontend/src/components/Chat.tsx)  │
│  • CLI input (healthcare_assistant.py)                      │
│  • WebSocket connection (/api/v1/ws/chat/{user_id})         │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              FastAPI Backend (api/main.py:1200)              │
│  POST /api/v1/chat OR WebSocket message                     │
│  {user_id, message, conversation_id}                        │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│         Memory Manager (modules/memory_manager.py)           │
│  • Retrieve last 10 conversations for context               │
│  • Extract user patterns and preferences                    │
│  • Check for appointment-related intents                    │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
                Intent Detection
                       ↓
       ┌───────────────┴────────────────┐
       ↓                                ↓
Medical Question                 Appointment Intent
       ↓                                ↓
┌──────────────────────┐    ┌──────────────────────┐
│   RAG Engine         │    │   Scheduler          │
│   modules/           │    │   modules/           │
│   rag_engine.py      │    │   scheduler.py       │
└──────┬───────────────┘    └──────────────────────┘
       ↓
┌──────────────────────────────────────────────────────────────┐
│              RAG Query Pipeline                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  STEP 1: Generate Query Embedding                           │
│  ─────────────────────────────────                          │
│  question → utils/embeddings.py                             │
│           ↓                                                 │
│  genai.embed_content(                                       │
│      model="models/embedding-001",                          │
│      content=question,                                      │
│      task_type="RETRIEVAL_QUERY"                            │
│  )                                                          │
│           ↓                                                 │
│  768-dimensional vector: [0.123, -0.456, ...]              │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  STEP 2: Semantic Search in ChromaDB                        │
│  ────────────────────────────────                           │
│  query_vector → data/vector_db/                             │
│               ↓                                             │
│  collection.query(                                          │
│      query_embeddings=[query_vector],                       │
│      n_results=5  # Top 5 most relevant chunks              │
│  )                                                          │
│               ↓                                             │
│  HNSW Algorithm: Fast approximate nearest neighbor          │
│  Cosine similarity: 1 - (A·B)/(||A||×||B||)                 │
│               ↓                                             │
│  Retrieved chunks:                                          │
│  [1] "Stroke occurs when blood flow..." (distance: 0.12)   │
│  [2] "Common symptoms include..." (distance: 0.18)         │
│  [3] "Risk factors are..." (distance: 0.23)                │
│  [4] "Treatment options..." (distance: 0.29)               │
│  [5] "Recovery and rehabilitation..." (distance: 0.31)     │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  STEP 3: Format Context with Citations                      │
│  ───────────────────────────────                            │
│  Format retrieved chunks as context:                        │
│                                                              │
│  [1] Source: stroke_overview.md                             │
│  Stroke occurs when blood flow to the brain is              │
│  interrupted, causing brain cells to die...                 │
│                                                              │
│  [2] Source: symptoms_guide.md                              │
│  Common symptoms include sudden numbness,                   │
│  confusion, trouble speaking...                             │
│                                                              │
│  [Continue for all 5 chunks]                                │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  STEP 4: Generate Answer with LLM                           │
│  ─────────────────────────────                              │
│  Construct prompt:                                          │
│                                                              │
│  """                                                        │
│  You are a medical assistant. Answer the question           │
│  based ONLY on the context below. Use citations like        │
│  [1], [2] to reference sources.                             │
│                                                              │
│  Context:                                                   │
│  [formatted context with all 5 chunks]                      │
│                                                              │
│  Question: What are the symptoms of stroke?                 │
│                                                              │
│  Answer:                                                    │
│  """                                                        │
│                ↓                                            │
│  genai.generate_content(                                    │
│      model="gemini-2.5-flash",                              │
│      contents=prompt,                                       │
│      generation_config={                                    │
│          "temperature": 0.1,  # Consistent, factual         │
│          "max_output_tokens": 1024                          │
│      }                                                      │
│  )                                                          │
│                ↓                                            │
│  Generated answer with citations:                           │
│  "Stroke symptoms include sudden numbness or weakness       │
│  in the face, arm, or leg [2], confusion or trouble         │
│  speaking [2], severe headache [1], and vision problems     │
│  [1]. These symptoms occur because blood flow to the        │
│  brain is disrupted [1]."                                   │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│         Memory Manager (Save Conversation)                   │
│  INSERT INTO conversations:                                  │
│  • User message: "What are the symptoms of stroke?"         │
│  • Assistant response: [generated answer]                   │
│  • Context data: {topics: ["stroke", "symptoms"], ...}      │
│  • Timestamp: 2025-10-29T10:30:00                           │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│                  Return Response                             │
│  {                                                           │
│    "answer": "Stroke symptoms include...",                  │
│    "citations": [                                           │
│      {"source": "stroke_overview.md", "chunk": 0},          │
│      {"source": "symptoms_guide.md", "chunk": 5}            │
│    ],                                                       │
│    "timestamp": "2025-10-29T10:30:00",                      │
│    "conversation_id": 456                                   │
│  }                                                           │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Display to User                                 │
│  Frontend: Render in chat bubble with citation links        │
│  CLI: Print formatted response with colored citations       │
└──────────────────────────────────────────────────────────────┘
```

### 2. Appointment Booking Flow

```
┌─────────────────────────────────────────────────────────────┐
│              User Requests Appointment                       │
│  "I want to book an appointment with Dr. Johnson"          │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Frontend Booking Form                           │
│  Components:                                                 │
│  • Doctor selection dropdown                                │
│  • Date picker                                              │
│  • Time slot selector                                       │
│  • Reason textarea                                          │
│  • "Sync with Calendar" checkbox                            │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│        API Request: POST /api/v1/appointments                │
│  Body:                                                       │
│  {                                                           │
│    "user_id": 5,                                            │
│    "doctor_id": 1,                                          │
│    "appointment_date": "2025-10-30",                        │
│    "start_time": "10:00",                                   │
│    "reason": "Follow-up consultation",                      │
│    "sync_calendar": true                                    │
│  }                                                           │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│         Scheduler Module (modules/scheduler.py)              │
│         book_appointment()                                   │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Validation Phase                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Validate Doctor Exists                                  │
│     ─────────────────────────                               │
│     SELECT * FROM doctors WHERE doctor_id = 1               │
│     ✓ Found: Dr. Sarah Johnson (Neurology)                  │
│                                                              │
│  2. Validate User Exists                                    │
│     ───────────────────────                                 │
│     SELECT * FROM users WHERE user_id = 5                   │
│     ✓ Found: John Doe                                       │
│                                                              │
│  3. Calculate End Time                                      │
│     ──────────────────────                                  │
│     consultation_duration = 30 minutes                      │
│     start_time = 10:00                                      │
│     end_time = 10:00 + 30min = 10:30                        │
│                                                              │
│  4. Validate Date                                           │
│     ───────────────────                                     │
│     • Date is in future? ✓                                  │
│     • Within booking window (30 days)? ✓                    │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Conflict Detection                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  check_conflict(doctor_id=1, date="2025-10-30",             │
│                 start="10:00", end="10:30")                 │
│                                                              │
│  SQL Query:                                                 │
│  SELECT COUNT(*) FROM appointments                          │
│  WHERE doctor_id = 1                                        │
│    AND appointment_date = "2025-10-30"                      │
│    AND status IN ('scheduled', 'confirmed')                 │
│    AND (                                                    │
│      -- Time overlap detection                              │
│      end_time > "10:00" AND start_time < "10:30"            │
│    )                                                        │
│                                                              │
│  Existing appointments for this doctor on 2025-10-30:       │
│  ┌────────────┬────────────┐                                │
│  │ Start      │ End        │ Conflicts?                     │
│  ├────────────┼────────────┤                                │
│  │ 09:00      │ 09:30      │ No  (ends before 10:00)        │
│  │ 14:00      │ 14:30      │ No  (starts after 10:30)       │
│  └────────────┴────────────┘                                │
│                                                              │
│  Result: COUNT = 0 → No conflicts ✓                         │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
                 Conflict exists?
                       ↓
         ┌─────────────┴─────────────┐
         ↓                           ↓
        YES                         NO
         ↓                           ↓
   ┌──────────────┐           ┌─────────────────────┐
   │ Return Error │           │ Insert Appointment  │
   │ 409 Conflict │           │ into Database       │
   └──────────────┘           └──────┬──────────────┘
                                     ↓
┌──────────────────────────────────────────────────────────────┐
│              Database Insertion                              │
│                                                              │
│  INSERT INTO appointments (                                 │
│      user_id, doctor_id, appointment_date,                  │
│      start_time, end_time, status, reason,                  │
│      created_at                                             │
│  ) VALUES (                                                 │
│      5, 1, "2025-10-30",                                    │
│      "10:00", "10:30", "scheduled",                         │
│      "Follow-up consultation",                              │
│      "2025-10-29T10:30:00"                                  │
│  )                                                          │
│                                                              │
│  Result: appointment_id = 123                               │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
                 sync_calendar = true?
                       ↓
         ┌─────────────┴─────────────┐
         ↓                           ↓
        YES                         NO
         ↓                           │
┌────────────────────┐               │
│ Calendar           │               │
│ Integration        │               │
└────────┬───────────┘               │
         ↓                           │
┌──────────────────────────────────────────────────────────────┐
│    create_calendar_event_async(appointment_id=123)          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Fetch Full Appointment Details                          │
│     ─────────────────────────────────                       │
│     SELECT a.*, u.name, u.email, d.name, d.calendar_id      │
│     FROM appointments a                                     │
│     JOIN users u ON a.user_id = u.user_id                   │
│     JOIN doctors d ON a.doctor_id = d.doctor_id             │
│     WHERE appointment_id = 123                              │
│                                                              │
│  2. Timezone Localization                                   │
│     ────────────────────────                                │
│     import pytz                                             │
│     pkt_tz = pytz.timezone('Asia/Karachi')                  │
│                                                              │
│     start_naive = "2025-10-30 10:00:00"                     │
│     start_aware = pkt_tz.localize(start_naive)              │
│     # Result: 2025-10-30T10:00:00+05:00                     │
│                                                              │
│     end_naive = "2025-10-30 10:30:00"                       │
│     end_aware = pkt_tz.localize(end_naive)                  │
│     # Result: 2025-10-30T10:30:00+05:00                     │
│                                                              │
│  3. Format Event Data                                       │
│     ───────────────────                                     │
│     summary = "Medical Appointment: John Doe"               │
│     description = """                                       │
│       Patient: John Doe (john@example.com)                  │
│       Doctor: Dr. Sarah Johnson (Neurology)                 │
│       Reason: Follow-up consultation                        │
│       ID: 123                                               │
│     """                                                     │
│     attendees = [john@example.com,                          │
│                  pinkpantherking20@gmail.com]               │
│                                                              │
│  4. Pipedream MCP Call                                      │
│     ──────────────────────                                  │
│     mcp_client.call_tool(                                   │
│         'google_calendar-create-event',                     │
│         {                                                   │
│             'instruction': f"""                             │
│                 Create event from {start_iso}               │
│                 to {end_iso} with attendees                 │
│                 {attendees}. Add Meet link.                 │
│                 Send notifications.                         │
│             """                                             │
│         }                                                   │
│     )                                                       │
│              ↓                                              │
│     [Pipedream processes OAuth and calls Google API]        │
│              ↓                                              │
│     Response:                                               │
│     {                                                       │
│         "id": "abc123xyz",                                  │
│         "hangoutLink": "https://meet.google.com/xxx-yyy",   │
│         "status": "confirmed"                               │
│     }                                                       │
│                                                              │
│  5. Update Database with Event ID                           │
│     ────────────────────────────────                        │
│     UPDATE appointments                                     │
│     SET calendar_event_id = "abc123xyz"                     │
│     WHERE appointment_id = 123                              │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
         ↓             │
         └─────────────┘
                ↓
┌──────────────────────────────────────────────────────────────┐
│              Return Success Response                         │
│  {                                                           │
│    "success": true,                                         │
│    "message": "Appointment booked successfully",            │
│    "data": {                                                │
│      "appointment_id": 123,                                 │
│      "appointment_date": "2025-10-30",                      │
│      "start_time": "10:00",                                 │
│      "end_time": "10:30",                                   │
│      "doctor_name": "Dr. Sarah Johnson",                    │
│      "status": "scheduled",                                 │
│      "calendar_event_id": "abc123xyz",                      │
│      "meet_link": "https://meet.google.com/xxx-yyy"         │
│    }                                                         │
│  }                                                           │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Frontend Updates                                │
│  • Display success message                                  │
│  • Show appointment details                                 │
│  • Provide Meet link (if synced)                            │
│  • Refresh appointment list                                 │
│  • Send confirmation email (if enabled)                     │
└──────────────────────────────────────────────────────────────┘
```

### 3. Doctor Portal Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Doctor Login                                    │
│  Enter Doctor ID: 1                                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│       Fetch Doctor Information                               │
│  SELECT * FROM doctors WHERE doctor_id = 1                  │
│  → Dr. Sarah Johnson (Neurology - Stroke Specialist)        │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Main Menu                                       │
│  ┌────────────────────────────────────────────────┐         │
│  │ 1. View Today's Schedule                       │         │
│  │ 2. View Patient Details                        │         │
│  │ 3. Add Medical Notes                           │         │
│  │ 4. View Analytics                              │         │
│  │ 5. Logout                                      │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
              User selects option
                       ↓
       ┌───────────────┼────────────────┬──────────────┐
       ↓               ↓                ↓              ↓
   Option 1        Option 2         Option 3      Option 4
       ↓               ↓                ↓              ↓

┌──────────────┐  ┌───────────────┐  ┌─────────────┐  ┌──────────────┐
│ View Today's │  │ View Patient  │  │ Add Medical │  │ View         │
│ Schedule     │  │ Details       │  │ Notes       │  │ Analytics    │
└──────┬───────┘  └───────┬───────┘  └──────┬──────┘  └──────┬───────┘
       ↓                  ↓                  ↓                ↓

┌──────────────────────────────────────────────────────────────┐
│ Option 1: View Today's Schedule                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  today = date.today()                                       │
│  appointments = get_doctor_appointments(doctor_id=1,        │
│                                          date=today)         │
│                                                              │
│  SQL:                                                       │
│  SELECT a.*, u.name, u.email, u.phone                       │
│  FROM appointments a                                        │
│  JOIN users u ON a.user_id = u.user_id                      │
│  WHERE a.doctor_id = 1                                      │
│    AND a.appointment_date = "2025-10-29"                    │
│    AND a.status IN ('scheduled', 'confirmed')               │
│  ORDER BY a.start_time                                      │
│                                                              │
│  Display in table:                                          │
│  ┌──────┬───────┬────────────┬────────────────┬──────────┐ │
│  │ Time │ Name  │ Phone      │ Reason         │ Status   │ │
│  ├──────┼───────┼────────────┼────────────────┼──────────┤ │
│  │ 09:00│ Alice │ 555-1234   │ Initial consult│ Confirmed│ │
│  │ 10:00│ Bob   │ 555-5678   │ Follow-up      │ Scheduled│ │
│  │ 14:00│ Carol │ 555-9012   │ Rehabilitation │ Confirmed│ │
│  └──────┴───────┴────────────┴────────────────┴──────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Option 2: View Patient Details                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Display list of recent patients                         │
│     SELECT DISTINCT u.user_id, u.name                       │
│     FROM users u                                            │
│     JOIN appointments a ON u.user_id = a.user_id            │
│     WHERE a.doctor_id = 1                                   │
│     ORDER BY a.appointment_date DESC                        │
│     LIMIT 10                                                │
│                                                              │
│  2. User selects patient (e.g., user_id = 5)               │
│                                                              │
│  3. Fetch patient info                                      │
│     SELECT * FROM users WHERE user_id = 5                   │
│                                                              │
│  4. Fetch appointment history                               │
│     appointments = get_patient_appointments(5)              │
│                                                              │
│  5. Display comprehensive view:                             │
│     ┌────────────────────────────────────────────┐         │
│     │ Patient: John Doe                          │         │
│     │ Email: john@example.com                    │         │
│     │ Phone: 555-1234                            │         │
│     │ DOB: 1980-05-15                            │         │
│     ├────────────────────────────────────────────┤         │
│     │ Appointment History:                       │         │
│     ├──────────┬─────────────┬──────────────────┤         │
│     │ Date     │ Time        │ Reason           │         │
│     ├──────────┼─────────────┼──────────────────┤         │
│     │ 10-30    │ 10:00       │ Follow-up        │         │
│     │ 09-15    │ 14:00       │ Initial consult  │         │
│     │ 08-01    │ 09:30       │ Symptoms check   │         │
│     └──────────┴─────────────┴──────────────────┘         │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Option 3: Add Medical Notes                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Display today's completed appointments                  │
│     SELECT * FROM appointments                              │
│     WHERE doctor_id = 1                                     │
│       AND appointment_date = today                          │
│       AND status = 'completed'                              │
│                                                              │
│  2. User selects appointment (e.g., appointment_id = 123)   │
│                                                              │
│  3. Display current notes (if any)                          │
│     Current notes: "Patient reported improvement..."        │
│                                                              │
│  4. Prompt for new notes                                    │
│     Enter medical notes:                                    │
│     > Patient shows significant progress in recovery.       │
│     > Recommended continued physical therapy.               │
│     > Follow-up in 2 weeks.                                 │
│                                                              │
│  5. Update database                                         │
│     UPDATE appointments                                     │
│     SET notes = ?                                           │
│     WHERE appointment_id = 123                              │
│                                                              │
│  6. Confirm success                                         │
│     ✓ Medical notes saved successfully                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Option 4: View Analytics                                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  GET /api/v1/doctors/{doctor_id}/analytics                  │
│                                                              │
│  Aggregate Queries:                                         │
│                                                              │
│  1. Total Patients                                          │
│     SELECT COUNT(DISTINCT user_id)                          │
│     FROM appointments                                       │
│     WHERE doctor_id = 1                                     │
│     Result: 45 patients                                     │
│                                                              │
│  2. Total Appointments                                      │
│     SELECT COUNT(*)                                         │
│     FROM appointments                                       │
│     WHERE doctor_id = 1                                     │
│     Result: 128 appointments                                │
│                                                              │
│  3. Appointments by Month (last 6 months)                   │
│     SELECT                                                  │
│       strftime('%Y-%m', appointment_date) as month,         │
│       COUNT(*) as count                                     │
│     FROM appointments                                       │
│     WHERE doctor_id = 1                                     │
│       AND appointment_date >= date('now', '-6 months')      │
│     GROUP BY month                                          │
│     ORDER BY month                                          │
│                                                              │
│     Result:                                                 │
│     2025-05: 18 | 2025-06: 22 | 2025-07: 25                 │
│     2025-08: 20 | 2025-09: 21 | 2025-10: 22                 │
│                                                              │
│  4. Completion Rate                                         │
│     SELECT                                                  │
│       COUNT(CASE WHEN status='completed' THEN 1 END)        │
│         * 100.0 / COUNT(*) as rate                          │
│     FROM appointments                                       │
│     WHERE doctor_id = 1                                     │
│     Result: 87.5% completion rate                           │
│                                                              │
│  5. Display dashboard:                                      │
│     ┌──────────────────────────────────────────┐           │
│     │ Dr. Sarah Johnson - Analytics            │           │
│     ├──────────────────────────────────────────┤           │
│     │ Total Patients: 45                       │           │
│     │ Total Appointments: 128                  │           │
│     │ Completion Rate: 87.5%                   │           │
│     │ Average per Month: 21.3                  │           │
│     ├──────────────────────────────────────────┤           │
│     │ Monthly Trend:                           │           │
│     │ May  ████████████████ 18                 │           │
│     │ Jun  ████████████████████ 22             │           │
│     │ Jul  ██████████████████████ 25           │           │
│     │ Aug  ████████████████████ 20             │           │
│     │ Sep  ████████████████████ 21             │           │
│     │ Oct  ████████████████████ 22             │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend

**Core Framework:**
- **FastAPI** - Modern, high-performance web framework
  - Automatic OpenAPI/Swagger docs
  - Async/await support
  - Dependency injection
  - WebSocket support

**Database:**
- **SQLite3** - Embedded relational database
  - Zero configuration
  - ACID compliant
  - Perfect for development and small-to-medium deployments
- **ChromaDB** - Vector database
  - Optimized for embeddings
  - Fast similarity search
  - Persistent storage

**AI/ML:**
- **Google Gemini API**
  - **gemini-2.5-flash** - LLM for answer generation
  - **embedding-001** - 768-dim embeddings
- **Retrieval Augmented Generation (RAG)** pattern

**Python Libraries:**
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration
- `pytz` - Timezone handling
- `pdfplumber` & `pypdf` - PDF processing
- `spacy` - NLP and text chunking
- `rich` - Beautiful CLI output

### Frontend

**Framework:**
- **React 18** - Component-based UI
- **TypeScript** - Type safety
- **Vite** - Fast build tool

**UI Library:**
- **shadcn/ui** - Modern component library
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icon system

**State Management:**
- React hooks (useState, useEffect)
- Context API for global state

**HTTP Client:**
- **Axios** - Promise-based HTTP client
- Centralized API client (`lib/api.ts`)

### Integrations

**Google Calendar:**
- **Pipedream MCP** - OAuth and API abstraction
- Model Context Protocol (MCP)
- HTTP transport

**Authentication:**
- OAuth 2.0 via Pipedream
- Bearer token authentication

### Development Tools

**Testing:**
- `pytest` - Unit and integration tests
- Test fixtures for database setup
- Mock objects for external APIs

**Linting & Formatting:**
- `pylint` or `flake8` - Python linting
- `black` - Code formatting
- `mypy` - Type checking

**Version Control:**
- Git
- GitHub for hosting

**Documentation:**
- Markdown files in `/docs`
- Inline docstrings
- OpenAPI/Swagger (auto-generated)

### Deployment

**Recommended Stack:**
- **Backend:** Uvicorn/Gunicorn on Linux server
- **Frontend:** Nginx serving static build
- **Database:** SQLite (or migrate to PostgreSQL for scale)
- **Vector DB:** ChromaDB on same server
- **Reverse Proxy:** Nginx
- **HTTPS:** Let's Encrypt

**Environment:**
- Python 3.8+
- Node.js 18+
- 2GB+ RAM recommended

---

## Summary

This healthcare assistant system is a sophisticated, production-ready application that combines:

### Core Strengths:
1. **Advanced AI**: RAG-powered medical Q&A with source citations
2. **Smart Scheduling**: Conflict-free appointment booking with pattern recognition
3. **Seamless Integration**: Google Calendar sync with timezone awareness
4. **Dual Interfaces**: Modern web UI + feature-rich CLI
5. **Robust Architecture**: Modular design with clear separation of concerns
6. **Data Intelligence**: Dual database approach (relational + vector)

### Key Features:
- Semantic search using 768-dimensional embeddings
- Context-aware conversation memory
- Real-time WebSocket chat
- Automatic Google Meet link generation
- Doctor portal with analytics
- Patient appointment history
- Medical notes management
- Timezone-correct calendar integration

### Code Quality:
- 4,663 lines of well-structured Python
- Comprehensive test suite (20+ files)
- Proper error handling and logging
- Foreign key constraints and indexes
- Type hints and documentation

### Scalability:
- Can handle 100,000+ document chunks
- Efficient HNSW indexing for fast search
- Async operations for non-blocking I/O
- Ready for PostgreSQL migration if needed

This documentation provides a complete technical reference for understanding, maintaining, and extending the healthcare assistant system.
