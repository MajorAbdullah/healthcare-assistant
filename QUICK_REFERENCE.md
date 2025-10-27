# 🏥 Healthcare Assistant - Quick Reference

## 🎯 What We're Building

A **dual-purpose healthcare assistant** that:
1. **Educates** patients about stroke using RAG (Retrieval-Augmented Generation)
2. **Schedules** doctor appointments with real calendar integration

---

## 🏗️ System Architecture (Visual)

```
┌─────────────────────────────────────────────┐
│         HEALTHCARE ASSISTANT                │
├─────────────────────────────────────────────┤
│                                             │
│  👤 PATIENT                🩺 DOCTOR        │
│  ├─ Ask medical questions  ├─ View bookings│
│  ├─ Book appointments      ├─ Confirm appts│
│  └─ View history           └─ Manage cal   │
│         │                        │          │
│         └──────────┬─────────────┘          │
│                    │                        │
│  ┌─────────────────▼──────────────────┐    │
│  │      CORE INTELLIGENCE              │    │
│  ├─────────────────────────────────────┤    │
│  │  📚 RAG Engine    📅 Scheduler      │    │
│  │  • Vector Search  • Calendar Sync   │    │
│  │  • Citations      • Conflict Check  │    │
│  │         💾 Memory Manager           │    │
│  └─────────────────────────────────────┘    │
│                    │                        │
│  ┌─────────────────▼──────────────────┐    │
│  │  🗄️  DATA LAYER                    │    │
│  │  • Medical Docs • Vector DB        │    │
│  │  • SQLite DB    • Conversations    │    │
│  └─────────────────────────────────────┘    │
│                    │                        │
│  ┌─────────────────▼──────────────────┐    │
│  │  🔌 EXTERNAL SERVICES              │    │
│  │  • Gemini AI • Pipedream • GCal   │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 📊 Implementation Phases

### **Phase 1: RAG System** (Days 1-3)
- Set up vector database with stroke documents
- Implement semantic search
- Build answer generation with citations
- **Output**: Can answer "What is a stroke?" with sources

### **Phase 2: Appointment System** (Days 4-6)
- Create database schema
- Add doctor profiles
- Build booking workflow
- Integrate with Google Calendar
- **Output**: Patient can book appointments

### **Phase 3: Memory & Context** (Days 7-8)
- Conversation history storage
- User profile management
- Context-aware responses
- **Output**: System remembers previous interactions

### **Phase 4: Integration** (Days 9-11)
- Unified CLI interface
- Role-based menus
- Error handling
- Testing
- **Output**: Complete working prototype

### **Phase 5: Web UI** (Optional, Days 12-14)
- Web interface
- Real-time updates
- Dashboard visualizations

---

## 🗂️ File Organization

```
pipedream/
├── healthcare_assistant.py          # Main entry point
├── config.py                        # Configuration
│
├── modules/
│   ├── rag_engine.py               # Medical Q&A
│   ├── scheduler.py                # Appointments
│   ├── memory_manager.py           # History tracking
│   ├── patient_interface.py        # Patient UI
│   └── doctor_dashboard.py         # Doctor UI
│
├── data/
│   ├── medical_docs/               # Stroke PDFs
│   ├── vector_db/                  # ChromaDB storage
│   └── healthcare.db               # SQLite database
│
├── utils/
│   ├── document_processor.py       # PDF processing
│   ├── embeddings.py               # Vector generation
│   └── validators.py               # Input validation
│
└── docs/
    ├── HEALTHCARE_PROJECT_PLAN.md  # Detailed plan
    ├── QUICK_REFERENCE.md          # This file
    └── README_HEALTHCARE.md        # User guide
```

---

## 🔄 User Workflows

### Patient Flow
```
Login → Choose Action
   ├─→ Ask Question
   │   └─→ RAG retrieves answer + citations
   ├─→ Book Appointment
   │   └─→ View doctors → Select time → Confirm
   └─→ View History
       └─→ Past appointments + conversations
```

### Doctor Flow
```
Login → View Pending
   ├─→ Confirm Appointment
   │   └─→ Update calendar → Notify patient
   ├─→ Reschedule
   │   └─→ Suggest new times → Patient chooses
   └─→ View Schedule
       └─→ Today's appointments + availability
```

---

## 💡 Key Concepts

### RAG (Retrieval-Augmented Generation)
```
Question: "What are stroke symptoms?"
    ↓
1. Embed question using Gemini
2. Search vector DB for similar chunks
3. Retrieve top 5 relevant passages
4. Feed to LLM with context
5. Generate answer with citations
    ↓
Answer: "Sudden numbness [1], severe headache [2]..."
Sources: [1] Mayo Clinic, [2] WHO
```

### Smart Scheduling
```
Request: "Book with Dr. Johnson at 2pm tomorrow"
    ↓
1. Parse request (doctor, date, time)
2. Check doctor's calendar via Pipedream
3. Check patient's calendar for conflicts
4. If available: Create PENDING appointment
5. Add to both calendars with tag
6. Notify doctor for confirmation
    ↓
Doctor confirms → Status: CONFIRMED
Calendar updated → Both parties notified
```

### Memory Management
```
Every interaction saved:
- User message
- Assistant response
- Timestamp
- Context (sources, appointments)

Used for:
- Personalized greetings
- Context-aware answers
- Follow-up recommendations
- Analytics
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI** | Google Gemini 2.0 Flash | LLM for Q&A and conversation |
| **Embeddings** | Gemini Embeddings API | Convert text to vectors |
| **Vector DB** | ChromaDB | Semantic search |
| **Calendar** | Google Calendar + Pipedream | Scheduling |
| **Database** | SQLite | User data, appointments |
| **CLI** | Rich library | Beautiful terminal UI |
| **Language** | Python 3.7+ | All components |

---

## 📈 Success Metrics

### Must Have ✅
- [ ] Answer stroke questions with 90%+ accuracy
- [ ] Include citations in all answers
- [ ] Zero double-booking (100% conflict detection)
- [ ] Doctor confirmation workflow works
- [ ] Conversation history persists across sessions

### Nice to Have 🎯
- [ ] Personalized greetings
- [ ] Analytics dashboard
- [ ] Multi-doctor support
- [ ] Web UI
- [ ] Email notifications

---

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.7+
python --version

# Install dependencies
pip install -r requirements_healthcare.txt

# Verify config
python config.py
```

### Quick Test Run
```bash
# Start the assistant
python healthcare_assistant.py

# Login as patient
> patient

# Ask a question
> What is a stroke?

# Book an appointment
> book appointment with Dr. Johnson
```

---

## 💬 Example Conversations

### Medical Q&A
```
Patient: What are the early warning signs of a stroke?