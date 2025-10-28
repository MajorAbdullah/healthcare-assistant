# 🗺️ Healthcare Assistant - Implementation Roadmap

## Overview
This document provides a step-by-step guide to building the Healthcare Assistant prototype.

---

## 📅 Development Timeline (11-14 Days)

```
Week 1: Foundation
├── Days 1-2: RAG System Core
├── Day 3: Testing RAG
│
Week 2: Scheduling
├── Days 4-5: Database & Doctor Profiles
├── Day 6: Calendar Integration
│
Week 3: Integration
├── Days 7-8: Memory & Context
├── Days 9-10: Full Integration
├── Day 11: Polish & Testing
│
Week 4 (Optional): Web UI
└── Days 12-14: Frontend Development
```

---

## 🎯 Phase 1: RAG System Setup (Days 1-3)

### Day 1: Vector Database Setup

**Goal**: Set up ChromaDB and process first medical document

**Tasks**:
1. Install dependencies:
   ```bash
   pip install chromadb sentence-transformers pypdf
   ```

2. Create `utils/document_processor.py`:
   ```python
   def load_pdf(filepath: str) -> str
   def chunk_text(text: str, chunk_size=500) -> List[dict]
   def add_metadata(chunks: List, source: str) -> List[dict]
   ```

3. Create `modules/rag_engine.py`:
   ```python
   class RAGEngine:
       def __init__(self)
       def add_documents(self, chunks: List[dict])
       def search(self, query: str) -> List[dict]
   ```

4. Download sample documents:
   - WHO Stroke Fact Sheet
   - Mayo Clinic Stroke Guide
   - CDC Stroke Prevention

**Deliverable**: Vector DB with 1 document processed and searchable

**Test**:
```python
# Simple test
rag = RAGEngine()
results = rag.search("stroke symptoms")
print(f"Found {len(results)} relevant chunks")
```

---

### Day 2: Answer Generation

**Goal**: Generate answers with citations from retrieved documents

**Tasks**:
1. Integrate Gemini for answer generation:
   ```python
   def generate_answer(self, query: str, context: List[dict]) -> dict:
       # Build prompt with context
       # Call Gemini
       # Extract citations
       # Format response
       return {
           "answer": "...",
           "citations": [...]
       }
   ```

2. Create citation system:
   ```python
   def format_citations(self, sources: List[dict]) -> str:
       """
       Format: [1] Mayo Clinic, Page 3
               [2] WHO Fact Sheet
       """
   ```

3. Add more medical documents (target: 5+ PDFs)

**Deliverable**: Working Q&A with citations

**Test**:
```python
rag = RAGEngine()
result = rag.query("What is a stroke?")
print(result["answer"])
print("\nSources:")
for citation in result["citations"]:
    print(f"  {citation}")
```

---

### Day 3: RAG Polish & Testing

**Goal**: Test RAG system thoroughly and improve quality

**Tasks**:
1. Test various questions:
   - What is a stroke?
   - What are the symptoms?
   - How to prevent stroke?
   - What is F.A.S.T.?
   - Treatment options?

2. Improve retrieval:
   - Tune chunk size
   - Adjust top_k results
   - Filter irrelevant chunks

3. Improve answer quality:
   - Better prompts
   - Citation accuracy
   - Answer formatting

4. Create `test_rag.py` for automated testing

**Deliverable**: Production-ready RAG system

**Acceptance Criteria**:
- ✅ Answers 10+ test questions correctly
- ✅ All answers include citations
- ✅ Citations are accurate
- ✅ Response time < 3 seconds

---

## 🏥 Phase 2: Appointment System (Days 4-6)

### Day 4: Database Schema

**Goal**: Set up SQLite database with all tables

**Tasks**:
1. Create `data/init_db.py`:
   ```python
   def create_tables():
       # Users table
       # Appointments table
       # Conversations table
       # Documents table
       # User preferences
   ```

2. Create `data/seed_data.py`:
   ```python
   def seed_doctors():
       # Add 3 sample doctors
   
   def seed_patient():
       # Add test patient
   ```

3. Create `modules/models.py`:
   ```python
   class User:
       def __init__(self, user_id, name, role, ...)
   
   class Appointment:
       def __init__(self, appointment_id, patient, doctor, ...)
   ```

**Deliverable**: Database with schema and sample data

**Test**:
```bash
python data/init_db.py
python data/seed_data.py
sqlite3 data/healthcare.db "SELECT * FROM users;"
```

---

### Day 5: Scheduler Module

**Goal**: Build appointment booking logic

**Tasks**:
1. Create `modules/scheduler.py`:
   ```python
   class AppointmentScheduler:
       def get_doctor_availability(self, doctor_id, date)
       def check_conflicts(self, doctor_id, patient_id, start, end)
       def create_appointment(self, patient_id, doctor_id, ...)
       def confirm_appointment(self, appointment_id)
       def cancel_appointment(self, appointment_id, reason)
   ```

2. Add CRUD operations:
   - Create appointment
   - Read appointments (by patient, by doctor)
   - Update appointment status
   - Delete/cancel appointment

3. Add conflict detection algorithm:
   ```python
   def has_conflict(new_start, new_end, existing_appointments):
       for appt in existing_appointments:
           if (new_start < appt.end_time) and (new_end > appt.start_time):
               return True
       return False
   ```

**Deliverable**: Working scheduler with conflict detection

**Test**:
```python
scheduler = AppointmentScheduler()

# Create appointment
appt_id = scheduler.create_appointment(
    patient_id=1,
    doctor_id=2,
    start="2025-10-28 14:00",
    end="2025-10-28 14:30"
)

# Try to book conflicting appointment
try:
    scheduler.create_appointment(
        patient_id=1,
        doctor_id=2,
        start="2025-10-28 14:15",
        end="2025-10-28 14:45"
    )
except ConflictError:
    print("✅ Conflict detection working!")
```

---

### Day 6: Calendar Integration

**Goal**: Integrate scheduler with Google Calendar via Pipedream

**Tasks**:
1. Extend existing `calendar_assistant.py`:
   ```python
   class CalendarIntegration:
       def create_appointment_event(self, appointment: Appointment)
       def update_appointment_event(self, event_id, status)
       def delete_appointment_event(self, event_id)
       def get_doctor_events(self, doctor_id, date)
   ```

2. Add appointment tags to calendar events:
   - PENDING: Yellow color
   - CONFIRMED: Green color
   - CANCELLED: Red color

3. Include metadata in event description:
   ```
   Patient: John Doe
   Reason: Stroke consultation
   Status: PENDING
   ID: 12345
   ```

4. Test bi-directional sync:
   - Create in DB → Create in Calendar
   - Confirm in system → Update Calendar color
   - Cancel in system → Remove from Calendar

**Deliverable**: Full calendar integration

**Test**:
```python
# Book appointment
appt = scheduler.create_appointment(...)

# Check Google Calendar
# Should see event with yellow color and "PENDING" tag

# Confirm appointment
scheduler.confirm_appointment(appt.appointment_id)

# Check Google Calendar again
# Should see event with green color and "CONFIRMED" tag
```

---

## 💾 Phase 3: Memory & Personalization (Days 7-8)

### Day 7: Conversation History

**Goal**: Store and retrieve conversation history

**Tasks**:
1. Create `modules/memory_manager.py`:
   ```python
   class MemoryManager:
       def save_message(self, user_id, role, message, context)
       def get_history(self, user_id, limit=10)
       def get_user_context(self, user_id)
       def clear_history(self, user_id)
   ```

2. Store conversations with metadata:
   ```python
   {
       "user_id": 1,
       "role": "user",
       "message": "What is a stroke?",
       "context": {
           "sources": ["Mayo Clinic", "WHO"],
           "timestamp": "2025-10-27 10:30:00"
       }
   }
   ```

3. Implement context window:
   - Keep last 10 messages in active memory
   - Retrieve full history when needed

**Deliverable**: Working memory system

**Test**:
```python
memory = MemoryManager()

# Save conversation
memory.save_message(1, "user", "What is a stroke?")
memory.save_message(1, "assistant", "A stroke is...")

# Retrieve history
history = memory.get_history(1, limit=5)
print(f"Retrieved {len(history)} messages")
```

---

### Day 8: Personalization

**Goal**: Add user profiles and context-aware responses

**Tasks**:
1. User profile management:
   ```python
   def update_user_profile(self, user_id, preferences):
       # Preferred doctor
       # Notification settings
       # Timezone
   ```

2. Context-aware greetings:
   ```python
   def get_personalized_greeting(self, user_id):
       context = self.get_user_context(user_id)
       
       if context["last_question"]:
           return f"Welcome back! Last time you asked about {topic}"
       
       if context["upcoming_appointments"]:
           return f"You have an appointment with {doctor} on {date}"
   ```

3. Analytics:
   ```python
   def get_user_stats(self, user_id):
       return {
           "total_questions": 15,
           "total_appointments": 3,
           "topics_explored": ["symptoms", "prevention"],
           "preferred_doctor": "Dr. Johnson"
       }
   ```

**Deliverable**: Personalized experience

**Test**:
```python
# First visit
greeting = memory.get_personalized_greeting(1)
# "Welcome! How can I help you today?"

# Return visit
greeting = memory.get_personalized_greeting(1)
# "Welcome back! Last time you asked about stroke prevention."
```

---

## 🔗 Phase 4: Integration & Polish (Days 9-11)

### Day 9: Main Orchestrator

**Goal**: Build unified CLI that connects all modules

**Tasks**:
1. Create `healthcare_assistant.py`:
   ```python
   class HealthcareAssistant:
       def __init__(self):
           self.rag = RAGEngine()
           self.scheduler = AppointmentScheduler()
           self.memory = MemoryManager()
           self.current_user = None
       
       def login(self, user_id, role)
       def handle_patient_mode(self)
       def handle_doctor_mode(self)
       def process_message(self, message)
       def run(self)
   ```

2. Create menu system:
   ```
   === HEALTHCARE ASSISTANT ===
   
   Select your role:
   1. Patient
   2. Doctor
   3. Exit
   
   Your choice:
   ```

3. Route commands to appropriate modules:
   - Medical question → RAG Engine
   - Book appointment → Scheduler
   - View history → Memory Manager

**Deliverable**: Working CLI orchestrator

---

### Day 10: UI with Rich Library

**Goal**: Beautiful terminal interface

**Tasks**:
1. Install Rich: `pip install rich`

2. Create beautiful outputs:
   ```python
   from rich.console import Console
   from rich.panel import Panel
   from rich.table import Table
   
   console = Console()
   
   # Display answer with panel
   console.print(Panel(answer, title="Answer", border_style="green"))
   
   # Display appointments in table
   table = Table(title="Your Appointments")
   table.add_column("Doctor", style="cyan")
   table.add_column("Date", style="magenta")
   table.add_column("Time", style="green")
   table.add_column("Status", style="yellow")
   # ... add rows
   console.print(table)
   ```

3. Add progress indicators:
   ```python
   with console.status("[bold green]Searching medical documents..."):
       results = rag.search(query)
   ```

4. Color coding:
   - User messages: Cyan
   - System messages: Yellow
   - Errors: Red
   - Success: Green

**Deliverable**: Beautiful CLI experience

---

### Day 11: Testing & Polish

**Goal**: Comprehensive testing and bug fixes

**Tasks**:
1. Create test suite:
   ```python
   # test_end_to_end.py
   def test_patient_asks_question()
   def test_patient_books_appointment()
   def test_conflict_detection()
   def test_doctor_confirms_appointment()
   def test_conversation_history()
   def test_personalization()
   ```

2. Manual testing checklist:
   - [ ] Patient can ask questions
   - [ ] Answers have citations
   - [ ] Citations are accurate
   - [ ] Patient can book appointments
   - [ ] Conflicts are detected
   - [ ] Doctor can confirm appointments
   - [ ] Calendar syncs correctly
   - [ ] History is saved
   - [ ] Greetings are personalized
   - [ ] Error messages are helpful

3. Edge cases:
   - Invalid dates
   - Past dates
   - Non-existent doctors
   - Malformed questions
   - Database errors
   - Calendar API failures

4. Performance optimization:
   - Vector search speed
   - Database queries
   - Answer generation time

**Deliverable**: Production-ready prototype

---

## 🌐 Phase 5: Web UI (Optional, Days 12-14)

### Day 12-13: Frontend Development

**Goal**: Create web-based interface

**Tasks**:
1. Set up FastAPI backend:
   ```python
   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.post("/api/ask")
   async def ask_question(question: str):
       result = rag.query(question)
       return result
   
   @app.post("/api/appointments")
   async def book_appointment(data: AppointmentRequest):
       appt = scheduler.create_appointment(...)
       return appt
   ```

2. Create HTML/CSS/JS frontend:
   - Patient portal
   - Doctor dashboard
   - Chat interface
   - Calendar view

3. WebSocket for real-time updates

**Deliverable**: Working web interface

---

### Day 14: Deployment Prep

**Goal**: Prepare for deployment

**Tasks**:
1. Documentation:
   - Installation guide
   - User manual
   - API documentation

2. Configuration:
   - Environment variables
   - Deployment settings

3. Testing on clean environment

**Deliverable**: Ready for deployment

---

## ✅ Final Checklist

### Functionality
- [ ] RAG answers medical questions
- [ ] Citations are included and accurate
- [ ] Appointment booking works end-to-end
- [ ] Conflict detection prevents double-booking
- [ ] Doctor confirmation workflow complete
- [ ] Conversation history persists
- [ ] Personalization works

### Code Quality
- [ ] All functions documented
- [ ] Error handling implemented
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Code is clean and readable

### User Experience
- [ ] CLI is intuitive
- [ ] Output is well-formatted
- [ ] Error messages are helpful
- [ ] Performance is acceptable

### Documentation
- [ ] README is complete
- [ ] Installation guide clear
- [ ] User manual written
- [ ] Code is commented

---

## 🚀 Launch Plan

### Soft Launch
1. Test with 2-3 beta users
2. Gather feedback
3. Fix critical bugs
4. Improve UX based on feedback

### Full Launch
1. Deploy to production
2. Monitor performance
3. Track user engagement
4. Iterate based on usage

---

## 📈 Future Enhancements

### Priority 1 (Next Sprint)
- Email notifications
- SMS reminders
- Mobile app
- Video consultation

### Priority 2 (Future)
- Multi-language support
- Voice interface
- Health records integration
- Prescription management

---

**Ready to build?** Start with Phase 1, Day 1! 🚀
