# Health-Buddy: Comprehensive Application Documentation

> **Version:** 1.0
> **Generated:** 2026-02-14
> **Application:** Health-Buddy Healthcare Assistant

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [System Flow](#2-system-flow)
3. [User Flow](#3-user-flow)
4. [Architecture](#4-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Backend Overview](#6-backend-overview)
7. [Frontend Overview](#7-frontend-overview)
8. [Schema](#8-schema)
9. [Essentials Checklist](#9-essentials-checklist)
10. [Deployments Checklist](#10-deployments-checklist)
11. [Payment Integration & Credit Token System](#11-payment-integration--credit-token-system)

---

## 1. System Overview

Health-Buddy is an AI-powered healthcare assistant built as a full-stack web application. It provides three distinct portals — **Patient**, **Doctor**, and **Admin** — connected to a FastAPI backend that integrates medical AI (RAG-based Q&A), appointment scheduling with conflict resolution, Google Calendar synchronization, and conversation memory.

### Primary Features

| Feature | Description |
|---------|-------------|
| **AI Medical Chat** | RAG-powered medical Q&A using Google Gemini 2.5 Flash with ChromaDB vector search over uploaded medical documents. |
| **Appointment Scheduling** | Multi-step booking wizard with real-time conflict detection, doctor availability checks, and an approval workflow (patient books → doctor approves/rejects). |
| **Google Calendar Sync** | Approved appointments are automatically synced to Google Calendar via Pipedream MCP, creating events with Google Meet links and email notifications. |
| **Doctor Portal** | Dashboard with stats, calendar view, patient directory, appointment management (approve/reject/add notes), and analytics with charts. |
| **Patient Portal** | Registration/login, appointment booking, AI chat, appointment history, profile management, and preference settings. |
| **Admin Panel** | Upload medical documents (PDF, TXT, MD) to the RAG knowledge base, monitor indexing status, and view system statistics. |
| **Conversation Memory** | Persistent chat history, user context tracking, pattern analysis, personalized greetings, and smart follow-up suggestions. |

### Technology Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Vite 5, Tailwind CSS, shadcn/ui, Recharts |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Database | SQLite (relational data), ChromaDB (vector embeddings) |
| AI / LLM | Google Gemini 2.5 Flash, Gemini Embeddings (`models/embedding-001`) |
| Calendar | Google Calendar API via Pipedream MCP |
| State Mgmt | React Query (TanStack Query v5), localStorage |

---

## 2. System Flow

### 2.1 End-to-End Data Flow

```
                          +-----------------+
                          |   React Frontend|
                          |  (Vite @ :8080) |
                          +--------+--------+
                                   |
                    REST (HTTP)    |    WebSocket
                   /api/v1/*      |    /ws/chat/{id}
                                   |
                          +--------v--------+
                          |  FastAPI Backend |
                          |  (Uvicorn @:8000)|
                          +--------+--------+
                                   |
              +--------------------+--------------------+
              |                    |                    |
    +---------v------+   +--------v--------+   +-------v--------+
    | AppointmentScheduler|  |   RAG Engine    |   | MemoryManager  |
    | (scheduler.py)      |  |  (rag_engine.py)|   |(memory_mgr.py) |
    +--------+-----------+  +---+--------+---+   +-------+--------+
             |                  |        |               |
    +--------v--------+  +-----v---+ +--v-----------+  |
    | SQLite DB       |  |ChromaDB | |Google Gemini |  |
    | healthcare.db   |  |vector_db| |  API         |  |
    +-----------------+  +---------+ +--------------+  |
                                                        |
                          +-----------------------------+
                          |
              +-----------v-----------+
              | CalendarIntegration   |
              | (Pipedream MCP)       |
              +-----------+-----------+
                          |
              +-----------v-----------+
              | Google Calendar API   |
              +-----------------------+
```

### 2.2 Process Flow: Appointment Lifecycle

```
Patient books appointment
        |
        v
POST /api/v1/appointments
        |
        v
Validate doctor exists + calculate end_time
        |
        v
Check time slot conflicts (interval overlap check)
        |
    [Conflict?]--Yes--> Return 409 Conflict
        |
        No
        |
        v
INSERT into appointments (status = 'pending_approval')
        |
        v
Return appointment_id to patient
        |
        v
Doctor sees pending appointment in dashboard
        |
    [Approve?]
    /         \
  Yes          No
   |            |
   v            v
PUT .../approve   PUT .../reject
   |            |
   v            v
status='confirmed'   status='cancelled'
   |
   v
CalendarIntegration.book_appointment_with_calendar_async()
   |
   v
Pipedream MCP → Google Calendar event created
   |
   v
Email notifications sent to patient + doctor
```

### 2.3 Process Flow: RAG Query Pipeline

```
User sends question (REST or WebSocket)
        |
        v
MemoryManager.save_conversation(role='user')
        |
        v
EmbeddingGenerator.generate_query_embedding(question)
        |  (Gemini API, task_type='retrieval_query')
        v
ChromaDB cosine similarity search → Top 5 chunks
        |
        v
RAGEngine.format_context(chunks + citations)
        |
        v
Gemini LLM generates answer (system_prompt + context + question)
        |
        v
MemoryManager.save_conversation(role='assistant')
        |
        v
Return: { answer, citations[], timestamp }
```

### 2.4 Process Flow: Document Upload & Indexing

```
Admin uploads files (PDF/TXT/MD)
        |
        v
POST /api/v1/admin/documents/upload
        |
        v
Files saved to data/uploaded_docs/{uuid}_{filename}
        |
        v
Metadata stored in metadata.json (status='pending')
        |
        v
Background: process_documents_for_rag()
        |
        v
DocumentProcessor.process_document()
   ├── load_pdf() / load_text_file()
   ├── chunk_text(size=500, overlap=50)
   └── add_metadata(source, doc_type, author)
        |
        v
EmbeddingGenerator.generate_batch(chunks)
   (Gemini API, batch_size=100, rate-limited)
        |
        v
RAGEngine.add_documents(chunks + embeddings) → ChromaDB
        |
        v
Metadata updated: status='indexed', chunks_count=N
```

---

## 3. User Flow

### 3.1 Patient Journey

1. **Landing Page** (`/`) — Patient clicks "Patient Portal".
2. **Authentication** (`/patient/auth`) — New users register (name, email, phone, DOB, gender); returning users log in (email + phone).
3. **Dashboard** (`/patient/dashboard`) — Sees personalized greeting, upcoming appointment alert, quick action cards (Book, Chat, View Appointments).
4. **Book Appointment** (`/patient/book`) — 5-step wizard:
   - Step 1: Select a doctor from the grid.
   - Step 2: Pick a date from the calendar (past dates disabled).
   - Step 3: Choose a time slot (available slots fetched from backend; booked slots shown as disabled).
   - Step 4: Review details, add optional reason for visit, confirm.
   - Step 5: Success confirmation with links back to dashboard.
5. **AI Chat** (`/patient/chat`) — Ask medical questions; receive RAG-powered answers with citations. Suggested questions provided. Conversation history preserved.
6. **Appointments** (`/patient/appointments`) — View all appointments in tabs (All, Upcoming, Past, Cancelled). Cancel appointments with confirmation dialog.
7. **Profile** (`/patient/profile`) — Edit personal info, toggle notification preferences (email, SMS, calendar sync).
8. **Logout** — Clears localStorage, returns to landing page.

### 3.2 Doctor Journey

1. **Landing Page** (`/`) — Doctor clicks "Doctor Portal".
2. **Authentication** (`/doctor/auth`) — Select doctor from dropdown, login by doctor_id.
3. **Dashboard** (`/doctor/dashboard`) — View stats (today's appointments, total patients, upcoming, total). See today's schedule with approve/reject actions for pending appointments.
4. **Calendar** (`/doctor/calendar`) — Calendar view with day/week/month toggle. Click appointment to open detail modal (view patient info, add medical notes, mark complete).
5. **Patients** (`/doctor/patients`) — Searchable, sortable patient directory. Click to view patient detail page with appointment timeline and medical notes.
6. **Analytics** (`/doctor/analytics`) — Charts: appointment trends (line), completion rate (pie), busiest days (bar), patient growth (area). Date range filter and CSV export.
7. **Profile** (`/doctor/profile`) — Edit personal/professional info, set availability, toggle preferences.

### 3.3 Admin Journey

1. **Landing Page** (`/`) — Click admin link at bottom.
2. **Authentication** (`/admin/auth`) — Login with username/password (hardcoded: `admin` / `admin123`).
3. **Dashboard** (`/admin/dashboard`) — View RAG stats (total documents, indexed chunks, collection name). Upload medical documents. Monitor indexing status. Delete documents.

---

## 4. Architecture

### 4.1 High-Level Architecture

The system follows a **client-server architecture** with a single-page application (SPA) frontend communicating with a monolithic Python backend via REST and WebSocket.

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                  │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Patient   │  │ Doctor   │  │ Admin Portal     │  │
│  │ Portal    │  │ Portal   │  │                  │  │
│  └─────┬────┘  └─────┬────┘  └────────┬─────────┘  │
│        └──────────────┼────────────────┘             │
│                       │                              │
│              React Router + React Query              │
│              lib/api.ts (HTTP + WS client)           │
└───────────────────────┼──────────────────────────────┘
                        │
            HTTP REST + WebSocket
                        │
┌───────────────────────┼──────────────────────────────┐
│               SERVER  (FastAPI + Uvicorn)             │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐     │
│  │            api/main.py                      │     │
│  │  (Routes, Pydantic models, request handling)│     │
│  └───┬────────┬────────────┬───────────┬───────┘     │
│      │        │            │           │             │
│  ┌───┴──┐ ┌──┴───┐ ┌──────┴──┐ ┌─────┴──────┐     │
│  │Sched-│ │RAG   │ │Memory   │ │Calendar    │     │
│  │uler  │ │Engine│ │Manager  │ │Integration │     │
│  └──┬───┘ └──┬───┘ └────┬────┘ └─────┬──────┘     │
│     │        │          │            │             │
│  ┌──┴────────┴──┐  ┌────┴───┐  ┌────┴──────┐     │
│  │  SQLite DB   │  │ChromaDB│  │Pipedream  │     │
│  │healthcare.db │  │vector  │  │MCP Client │     │
│  └──────────────┘  └────────┘  └─────┬──────┘     │
│                                       │             │
└───────────────────────────────────────┼─────────────┘
                                        │
                              ┌─────────┴──────────┐
                              │ Google Calendar API │
                              │ + Google Gemini API │
                              └────────────────────┘
```

### 4.2 Major Components and Interactions

| Component | Responsibility | Interacts With |
|-----------|---------------|----------------|
| **api/main.py** | HTTP/WS request routing, validation, response formatting | All modules below |
| **AppointmentScheduler** (`modules/scheduler.py`) | Doctor/patient CRUD, availability calculation, conflict detection, appointment CRUD | SQLite DB |
| **RAGEngine** (`modules/rag_engine.py`) | Document indexing, semantic search, LLM answer generation | ChromaDB, Google Gemini API |
| **MemoryManager** (`modules/memory_manager.py`) | Conversation persistence, user context, pattern analysis, personalized greetings | SQLite DB |
| **CalendarIntegration** (`modules/calendar_integration.py`) | Create/update/cancel Google Calendar events via Pipedream MCP | Pipedream API, Google Calendar |
| **DocumentProcessor** (`utils/document_processor.py`) | PDF/TXT/MD parsing, text chunking with overlap | File system |
| **EmbeddingGenerator** (`utils/embeddings.py`) | Text-to-vector conversion with batching and retry | Google Gemini API |
| **db_setup.py** (`utils/db_setup.py`) | Database initialization, schema creation, seed data | SQLite DB |
| **React Frontend** | SPA with three portals, API client, UI rendering | Backend API (HTTP + WS) |

---

## 5. Folder Structure

```
Health-Buddy/
├── api/                              # FastAPI backend server
│   ├── main.py                       # Main API (1668 lines) — all endpoints, models, handlers
│   └── __init__.py
│
├── modules/                          # Core business logic modules
│   ├── scheduler.py                  # Appointment scheduling, conflict detection, doctor/patient ops
│   ├── rag_engine.py                 # RAG pipeline: embed → search → generate (ChromaDB + Gemini)
│   ├── memory_manager.py             # Conversation history, user context, smart suggestions
│   ├── calendar_integration.py       # Google Calendar sync via Pipedream MCP (primary)
│   ├── calendar_sync.py              # Alternative calendar sync via SmartCalendarAssistant
│   ├── calendar_assistant_wrapper.py # Sync wrapper around async calendar operations
│   └── __init__.py
│
├── utils/                            # Utility modules
│   ├── db_setup.py                   # Database initialization and seed data
│   ├── document_processor.py         # PDF/TXT/MD parsing and chunking
│   ├── embeddings.py                 # Gemini embedding generation with batching
│   ├── apply_approval_migration.py   # DB migration for approval system
│   ├── db_schema.sql                 # Full SQL schema definition
│   ├── db_migration_approval.sql     # Approval columns migration
│   └── __init__.py
│
├── Frontend/                         # React SPA
│   ├── src/
│   │   ├── App.tsx                   # Router with all routes
│   │   ├── main.tsx                  # React entry point
│   │   ├── pages/
│   │   │   ├── Index.tsx             # Landing page / portal selector
│   │   │   ├── NotFound.tsx          # 404 page
│   │   │   ├── patient/             # Patient portal pages (Auth, Dashboard, Book, Chat, etc.)
│   │   │   ├── doctor/              # Doctor portal pages (Auth, Dashboard, Calendar, Analytics, etc.)
│   │   │   └── admin/               # Admin portal pages (Auth, Dashboard)
│   │   ├── components/ui/           # 51 shadcn/ui components
│   │   ├── hooks/                   # use-mobile, use-toast
│   │   └── lib/
│   │       ├── api.ts               # API client (REST + WebSocket)
│   │       └── utils.ts             # Utility helpers (cn class merger)
│   ├── public/                       # Static assets
│   ├── dist/                         # Production build output
│   ├── .env                          # Frontend environment variables
│   ├── package.json                  # Dependencies and scripts
│   ├── vite.config.ts                # Vite dev server and build config
│   ├── tailwind.config.ts            # Tailwind CSS theme and plugins
│   └── tsconfig.json                 # TypeScript configuration
│
├── data/                             # Data storage
│   ├── healthcare.db                 # SQLite database (users, doctors, appointments, conversations)
│   ├── vector_db/                    # ChromaDB persistent storage (embeddings)
│   ├── medical_docs/                 # Pre-loaded medical documents (stroke articles)
│   └── uploaded_docs/                # Admin-uploaded documents + metadata.json
│
├── tests/                            # Test suite (22 files)
│   ├── test_api.py                   # API endpoint tests
│   ├── test_complete_system.py       # Full system integration tests
│   ├── test_scheduler.py             # Scheduler unit tests
│   ├── test_memory_manager.py        # Memory manager tests
│   ├── test_rag_*.py                 # RAG engine tests (4 files)
│   ├── test_live_calendar_integration.py # Calendar integration tests
│   ├── check_environment.py          # Environment verification
│   └── demo_*.py                     # Demo scripts
│
├── scripts/                          # Utility scripts
│   └── reprocess_documents.py        # Re-index documents into RAG
│
├── docs/                             # Project documentation (24 markdown files)
│
├── calendar_cli/                     # Standalone calendar CLI tool
│   ├── calendar_assistant.py
│   └── requirements.txt
│
├── config.py                         # Central configuration (paths, API keys, RAG settings, prompts)
├── healthcare_assistant.py           # CLI healthcare assistant (terminal-based)
├── doctor_portal.py                  # CLI doctor portal (terminal-based)
├── calendar_assistant.py             # CLI calendar assistant
├── start.py                          # Interactive startup menu
├── start_api.sh                      # Shell script to start API server
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables (API keys)
├── .env.example                      # Example environment template
└── README.md                         # Project README
```

---

## 6. Backend Overview

### 6.1 Technologies

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework (async-capable, auto-docs at `/docs`) |
| **Uvicorn** | ASGI server (auto-reload in dev, port 8000) |
| **SQLite** | Relational database (local, zero-config) |
| **ChromaDB** | Vector database for RAG embeddings (persistent at `data/vector_db/`) |
| **Google Gemini** | LLM for answer generation (`gemini-2.5-flash`) and embeddings (`models/embedding-001`) |
| **Pipedream MCP** | Model Context Protocol client for Google Calendar API |
| **Pydantic** | Request/response validation |
| **pytz** | Timezone handling (Asia/Karachi) |
| **pdfplumber / pypdf** | PDF text extraction |

### 6.2 Principal Modules

#### `api/main.py` (1668 lines) — API Server

The monolithic API file contains all endpoints, Pydantic models, and request handlers. It initializes and orchestrates the four core modules:

```python
scheduler = AppointmentScheduler()             # Eager
calendar_integration = CalendarIntegration(scheduler)  # Eager
memory_manager = MemoryManager(db_path=DB_PATH)        # Eager
rag_engine = None  # Lazy-loaded on first chat request
```

**Endpoint Groups (35+ endpoints):**

| Group | Prefix | Endpoints |
|-------|--------|-----------|
| Patient Portal | `/api/v1/patients/` | register, login, getProfile, updateProfile, greeting, preferences |
| Appointments | `/api/v1/appointments` | book, getByPatient, approve, reject, cancel, notes, status |
| Doctor Portal | `/api/v1/doctors/` | login, getAll, availability, stats, appointments, patients, analytics |
| AI Chat | `/api/v1/chat`, `/ws/chat/{user_id}` | REST chat, WebSocket chat |
| Admin | `/api/v1/admin/` | documents list/upload/delete, stats |
| System | `/`, `/health` | API info, health check |

**Pydantic Models:**
- `PatientRegister`, `PatientLogin`, `PatientUpdate`
- `AppointmentBook`, `MedicalNote`
- `ChatMessage`, `DoctorLogin`, `PreferencesUpdate`

**CORS:** Allows requests from `localhost:3000`, `:5173`, `:8080`, `:8081` with all methods and headers.

#### `modules/scheduler.py` (546 lines) — Appointment Engine

- **Doctor/Patient CRUD**: `get_or_create_patient()`, `get_all_doctors()`, `get_doctor_by_id()`
- **Availability Calculation**: Generates 30-minute time slots from weekly availability templates, subtracting booked slots via interval overlap detection (`NOT (end1 <= start2 OR start1 >= end2)`)
- **Conflict Detection**: `check_conflict()` prevents double-booking
- **Appointment Management**: `book_appointment()`, `cancel_appointment()`, `confirm_appointment()`
- **Database**: Direct SQL queries with parameterized `?` placeholders (no ORM)

#### `modules/rag_engine.py` (414 lines) — Medical AI

- **Vector Store**: ChromaDB persistent collection (`stroke_medical_docs`)
- **Embedding**: Gemini `models/embedding-001` (768 dimensions)
- **Search**: Cosine similarity, top-K=5 results
- **Generation**: Gemini 2.5 Flash with temperature=0.1 and a medical system prompt (HealthBot persona)
- **Pipeline**: `query()` → embed question → search ChromaDB → format context with citations → generate answer
- **Document Management**: `add_documents()`, `clear_collection()`, `get_stats()`

#### `modules/memory_manager.py` (694 lines) — Context & History

- **Conversation Storage**: Saves every user/assistant message with timestamps and optional JSON context
- **User Context Building**: Aggregates name, preferences, health topics, appointment stats
- **Pattern Analysis**: Identifies preferred doctors, appointment times (morning/afternoon/evening), frequency
- **Smart Features**: Personalized greetings (time-of-day + last interaction), follow-up suggestions, contextual recommendations

#### `modules/calendar_integration.py` (453 lines) — Calendar Sync

- **Integration Method**: Pipedream MCP (Model Context Protocol) → Google Calendar API
- **Event Creation**: Natural language instruction sent via `fastmcp.Client` to `google_calendar-create-event`
- **Features**: Google Meet link generation, email notifications to attendees, timezone-aware (PKT)
- **Trigger**: Called only on doctor appointment approval (not on booking)
- **Auth**: OAuth via Pipedream (client_id, client_secret, project_id)

### 6.3 Request Handling Pattern

All endpoints follow a consistent pattern:

```python
@app.post("/api/v1/example")
async def example_endpoint(data: PydanticModel):
    try:
        conn = get_db_connection()   # Get SQLite connection
        cursor = conn.cursor()
        cursor.execute("SQL...", (params,))
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        return {"success": True, "data": {...}, "message": "..."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- Database connections are opened/closed per request (no connection pooling)
- All SQL uses parameterized queries (SQL injection safe)
- Responses follow `{"success": bool, "data": {...}, "message": str}` format
- HTTP exceptions: 400 (bad request), 404 (not found), 409 (conflict), 500 (server error), 503 (RAG unavailable)

---

## 7. Frontend Overview

### 7.1 Frameworks & Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| React | 18.3.1 | UI framework |
| TypeScript | 5.8.3 | Type safety |
| Vite | 5.4.19 | Build tool and dev server (SWC for fast refresh) |
| React Router | 6.30.1 | Client-side routing |
| TanStack React Query | 5.83.0 | Server state management |
| Tailwind CSS | 3.4.17 | Utility-first styling |
| shadcn/ui | — | 51 accessible UI components (built on Radix UI) |
| Recharts | 2.15.4 | Charts (line, pie, bar, area) |
| Lucide React | 0.462.0 | Icon library |
| React Hook Form | 7.61.1 | Form management |
| Zod | 3.25.76 | Schema validation |
| Sonner | — | Toast notifications |
| react-day-picker | — | Calendar date picker |

### 7.2 Component Breakdown

#### Pages (18 page components)

**Patient Portal (8 pages):**
| Page | Route | Description |
|------|-------|-------------|
| `patient/Auth.tsx` | `/patient/auth` | Tabbed login/register forms |
| `patient/Dashboard.tsx` | `/patient/dashboard` | Greeting, upcoming appointment, quick actions |
| `patient/DashboardNew.tsx` | — | Enhanced dashboard with live data fetching |
| `patient/Book.tsx` | `/patient/book` | 5-step appointment booking wizard |
| `patient/Chat.tsx` | `/patient/chat` | AI medical assistant chat interface |
| `patient/Appointments.tsx` | `/patient/appointments` | Tabbed appointment list with cancel actions |
| `patient/Profile.tsx` | `/patient/profile` | Editable profile, preferences, danger zone |

**Doctor Portal (7 pages):**
| Page | Route | Description |
|------|-------|-------------|
| `doctor/Auth.tsx` | `/doctor/auth` | Doctor selection dropdown login |
| `doctor/Dashboard.tsx` | `/doctor/dashboard` | Stats cards, today's schedule, approve/reject |
| `doctor/Calendar.tsx` | `/doctor/calendar` | Calendar view, appointment detail modals |
| `doctor/Patients.tsx` | `/doctor/patients` | Searchable patient directory |
| `doctor/PatientDetail.tsx` | `/doctor/patients/:id` | Patient timeline, medical notes |
| `doctor/Analytics.tsx` | `/doctor/analytics` | 4 charts, date range filter, CSV export |
| `doctor/Profile.tsx` | `/doctor/profile` | Profile tabs (info, availability, preferences) |

**Admin Portal (2 pages):**
| Page | Route | Description |
|------|-------|-------------|
| `admin/Auth.tsx` | `/admin/auth` | Username/password login (hardcoded credentials) |
| `admin/Dashboard.tsx` | `/admin/dashboard` | Document upload, RAG stats, document management |

**Shared (2 pages):**
| Page | Route | Description |
|------|-------|-------------|
| `Index.tsx` | `/` | Landing page with portal selection cards |
| `NotFound.tsx` | `*` | 404 error page |

#### UI Components (51 shadcn/ui components)

All located in `src/components/ui/`. Key components used across the app:
- **Layout**: `card`, `tabs`, `separator`, `scroll-area`
- **Forms**: `button`, `input`, `label`, `select`, `checkbox`, `switch`, `textarea`, `radio-group`
- **Feedback**: `toast`, `sonner`, `alert`, `alert-dialog`, `dialog`, `progress`, `skeleton`
- **Data**: `table`, `badge`, `avatar`, `calendar`, `chart`
- **Navigation**: `breadcrumb`, `navigation-menu`, `dropdown-menu`, `popover`

#### API Service Layer (`lib/api.ts`)

Centralized API client with modules:

```typescript
const api = {
  patients: { register, login, getProfile, updateProfile, getGreeting, getPreferences, updatePreferences },
  doctors:  { getAll, getAvailability, login, getStats, getAppointments, getPatients, getAnalytics },
  appointments: { book, getByPatient, cancel, approve, reject, addNotes, updateNotes, updateStatus, getPatientHistory },
  chat: { sendMessage, connectWebSocket },
  system: { health, info }
};
```

- Base URL from `VITE_API_URL` env var (default: `http://localhost:8000/api/v1`)
- WebSocket URL from `VITE_WS_URL` env var (default: `ws://localhost:8000`)
- Custom `ApiError` class with status codes
- All methods return typed `ApiResponse<T>`

### 7.3 Major Workflows

**Authentication Flow:**
1. User fills login/register form.
2. API call to `/patients/register` or `/patients/login`.
3. On success, store `user_id`, `user_name`, `user_email`, `user_type` in localStorage.
4. Navigate to respective dashboard.
5. Logout clears localStorage and redirects to `/`.

**Appointment Booking Flow:**
1. Select doctor → Select date → Backend fetches available slots → Select time → Review → Confirm.
2. POST to `/appointments` with `user_id`, `doctor_id`, `date`, `time`, `reason`.
3. Handles 409 conflicts, displays toast on success/failure.
4. Prevents double-submission with loading state.

**Chat Flow:**
1. User types message in input field.
2. POST to `/api/v1/chat` with `user_id` and `message`.
3. Response displayed as assistant bubble with typing indicator animation.
4. Suggested questions provided as clickable buttons.

### 7.4 Styling Approach

- **Tailwind CSS** with custom theme (HSL color variables, gradients, glass-morphism effects)
- **shadcn/ui** for consistent, accessible component primitives
- **Custom classes**: `gradient-bg`, `gradient-card`, `glass-header`, `glass-card`, `shadow-card`
- **Dark mode** supported via `darkMode: ["class"]` in Tailwind config
- **Animations**: `tailwindcss-animate` plugin + custom accordion animations

---

## 8. Schema

### 8.1 SQLite Database Schema (`data/healthcare.db`)

```sql
-- ============================================================
-- PATIENTS (users table)
-- ============================================================
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- Full name
    email TEXT UNIQUE NOT NULL,            -- Login identifier
    phone TEXT,                            -- Login verifier
    date_of_birth DATE,                    -- Optional DOB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Auto-updated via trigger
);

-- ============================================================
-- DOCTORS
-- ============================================================
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- Dr. Full Name
    specialty TEXT NOT NULL,               -- e.g., "Neurology - Stroke Specialist"
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    calendar_id TEXT,                      -- Google Calendar ID for Pipedream sync
    consultation_duration INTEGER DEFAULT 30,  -- Minutes per appointment
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Auto-updated via trigger
);

-- ============================================================
-- DOCTOR AVAILABILITY (weekly schedule template)
-- ============================================================
CREATE TABLE doctor_availability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,            -- FK → doctors
    day_of_week INTEGER NOT NULL,          -- 0=Monday ... 6=Sunday
    start_time TIME NOT NULL,              -- e.g., "09:00"
    end_time TIME NOT NULL,                -- e.g., "12:00"
    is_active BOOLEAN DEFAULT 1,           -- Slot active/disabled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    CHECK (day_of_week BETWEEN 0 AND 6)
);

-- ============================================================
-- APPOINTMENTS
-- ============================================================
CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,              -- FK → users (patient)
    doctor_id INTEGER NOT NULL,            -- FK → doctors
    appointment_date DATE NOT NULL,        -- YYYY-MM-DD
    start_time TIME NOT NULL,              -- HH:MM
    end_time TIME NOT NULL,                -- Calculated: start + consultation_duration
    status TEXT DEFAULT 'scheduled',       -- pending_approval | confirmed | scheduled | completed | cancelled
    reason TEXT,                           -- Chief complaint
    notes TEXT,                            -- Doctor's medical notes
    calendar_event_id TEXT,                -- Google Calendar event ID
    approval_email_sent INTEGER DEFAULT 0, -- Flag: approval notification sent
    confirmation_email_sent INTEGER DEFAULT 0, -- Flag: confirmation notification sent
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Auto-updated via trigger
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    CHECK (status IN ('scheduled', 'confirmed', 'cancelled', 'completed'))
);

-- ============================================================
-- CONVERSATIONS (chat history for memory manager)
-- ============================================================
CREATE TABLE conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,              -- FK → users
    message_type TEXT NOT NULL,            -- 'user' | 'assistant' | 'system'
    message_text TEXT NOT NULL,            -- Message content
    context_data TEXT,                     -- JSON: { topic, category, appointment_id, ... }
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CHECK (message_type IN ('user', 'assistant', 'system'))
);

-- ============================================================
-- USER PREFERENCES
-- ============================================================
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    email_notifications BOOLEAN DEFAULT 1,
    sms_reminders BOOLEAN DEFAULT 1,
    calendar_sync BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_appointments_user ON appointments(user_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_availability_doctor ON doctor_availability(doctor_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_doctors_specialty ON doctors(specialty);

-- ============================================================
-- TRIGGERS (auto-update updated_at)
-- ============================================================
CREATE TRIGGER update_users_timestamp AFTER UPDATE ON users
BEGIN UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id; END;

CREATE TRIGGER update_doctors_timestamp AFTER UPDATE ON doctors
BEGIN UPDATE doctors SET updated_at = CURRENT_TIMESTAMP WHERE doctor_id = NEW.doctor_id; END;

CREATE TRIGGER update_appointments_timestamp AFTER UPDATE ON appointments
BEGIN UPDATE appointments SET updated_at = CURRENT_TIMESTAMP WHERE appointment_id = NEW.appointment_id; END;
```

### 8.2 Entity Relationship Diagram

```
users (patients)              doctors
┌──────────────┐              ┌───────────────────┐
│ user_id (PK) │──┐       ┌──│ doctor_id (PK)    │
│ name         │  │       │  │ name              │
│ email (UQ)   │  │       │  │ specialty         │
│ phone        │  │       │  │ email (UQ)        │
│ date_of_birth│  │       │  │ calendar_id       │
└──────────────┘  │       │  │ consultation_dur  │
                  │       │  └───────────────────┘
                  │       │           │
                  │       │           │ 1:N
                  │       │           ▼
                  │       │  doctor_availability
                  │       │  ┌─────────────────┐
                  │       │  │ availability_id  │
                  │       │  │ doctor_id (FK)   │
                  │       │  │ day_of_week      │
                  │       │  │ start_time       │
                  │       │  │ end_time         │
                  │       │  └─────────────────┘
                  │       │
                  │  N:1  │  1:N
                  ▼       ▼
              appointments
              ┌─────────────────────┐
              │ appointment_id (PK) │
              │ user_id (FK)        │
              │ doctor_id (FK)      │
              │ appointment_date    │
              │ start_time          │
              │ end_time            │
              │ status              │
              │ reason              │
              │ notes               │
              │ calendar_event_id   │
              └─────────────────────┘

users 1:N conversations              users 1:1 user_preferences
              ┌──────────────────┐            ┌──────────────────┐
              │ conversation_id  │            │ user_id (PK, FK) │
              │ user_id (FK)     │            │ email_notifs     │
              │ message_type     │            │ sms_reminders    │
              │ message_text     │            │ calendar_sync    │
              │ context_data     │            └──────────────────┘
              └──────────────────┘
```

### 8.3 Vector Database (ChromaDB)

```
Collection: "stroke_medical_docs"
Storage: data/vector_db/ (persistent)

Document structure:
{
  "id": "uuid_timestamp_chunkIndex",     // Unique chunk ID
  "embedding": [float x 768],            // Gemini embedding vector
  "document": "chunk text content...",    // 500-char text chunk
  "metadata": {
    "source": "filename.pdf",            // Original document name
    "doc_type": "PDF|TXT|MD",           // File type
    "author": "Admin Upload",           // Uploader
    "url": "",                           // Optional source URL
    "chunk_id": "uuid_timestamp_index"  // Same as ID
  }
}
```

### 8.4 Document Metadata (JSON file)

```json
// data/uploaded_docs/metadata.json
[
  {
    "id": "e709e900-98d6-4e27-aff8-ef8eef64f67e",
    "filename": "research_ai_nurse_app.md",
    "size": 12345,
    "uploaded_at": "2025-10-30T12:00:00",
    "status": "indexed",
    "doc_type": "MD",
    "file_path": "data/uploaded_docs/e709e900_research_ai_nurse_app.md",
    "chunks_count": 25
  }
]
```

---

## 9. Essentials Checklist

### 9.1 System Requirements

- [ ] **Python 3.10+** (developed with 3.13)
- [ ] **Node.js 18+** and **npm**
- [ ] **SQLite 3** (included with Python)
- [ ] **Git** (for version control)

### 9.2 Python Dependencies (`requirements.txt`)

```
google-genai>=0.2.0         # Google Gemini API client
fastmcp>=0.1.0              # Model Context Protocol client (Pipedream)
pipedream>=0.3.0             # Pipedream SDK
python-dotenv>=1.0.0         # .env file loading
websockets>=12.0             # WebSocket support
python-multipart>=0.0.6      # File upload handling
```

**Additional dependencies** (not in requirements.txt but required):
```
fastapi                      # Web framework
uvicorn                      # ASGI server
pydantic[email]              # Data validation (with EmailStr)
chromadb                     # Vector database
pytz                         # Timezone handling
rich                         # Terminal UI
pdfplumber                   # PDF text extraction
pypdf                        # PDF fallback
httpx                        # HTTP client
```

### 9.3 Frontend Dependencies

Installed via `npm install` in `Frontend/` directory. Key packages:
```
react, react-dom, react-router-dom
@tanstack/react-query
tailwindcss, @radix-ui/*, recharts
lucide-react, react-hook-form, zod
```

### 9.4 Environment Variables

**Backend** (`.env` in project root):
```env
GOOGLE_API_KEY=<your-google-gemini-api-key>
PIPEDREAM_PROJECT_ID=<your-pipedream-project-id>
PIPEDREAM_ENVIRONMENT=development
PIPEDREAM_CLIENT_ID=<your-pipedream-client-id>
PIPEDREAM_CLIENT_SECRET=<your-pipedream-client-secret>
EXTERNAL_USER_ID=user-123
```

**Frontend** (`Frontend/.env`):
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME="Healthcare Assistant"
```

### 9.5 Configuration (`config.py`)

Key settings that may need adjustment:
| Setting | Default | Description |
|---------|---------|-------------|
| `LLM_MODEL` | `gemini-2.5-flash` | Google Gemini model for chat |
| `EMBEDDING_MODEL` | `models/embedding-001` | Embedding model |
| `CHUNK_SIZE` | 500 | Characters per document chunk |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks |
| `TOP_K_RESULTS` | 5 | Number of search results |
| `TEMPERATURE` | 0.1 | LLM creativity (low = factual) |
| `TIMEZONE` | `Asia/Karachi` | Application timezone |
| `DEFAULT_APPOINTMENT_DURATION` | 30 | Minutes per slot |
| `BOOKING_ADVANCE_DAYS` | 30 | Max days ahead for booking |

### 9.6 How to Run Locally

```bash
# 1. Clone the repository
git clone <repo-url> && cd Health-Buddy

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Also install unlisted dependencies:
pip install fastapi uvicorn chromadb pytz rich pdfplumber pypdf httpx pydantic[email]

# 3. Configure environment
cp .env.example .env
# Edit .env with your Google API key and Pipedream credentials

# 4. Initialize database (if fresh)
python3 utils/db_setup.py

# 5. Start backend
cd api && python3 main.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs

# 6. Start frontend (new terminal)
cd Frontend
npm install
npm run dev
# Frontend runs at http://localhost:8080
```

### 9.7 Seed Data

The database comes pre-seeded with:
- **3 Doctors**: Dr. Sarah Johnson (Neurology), Dr. Ahmad Khan (Cardiology), Dr. Fatima Malik (General Medicine)
- **Doctor availability**: Monday-Friday, 9:00-12:00 and 13:00-17:00
- **Medical documents**: Stroke overview articles in `data/medical_docs/`

---

## 10. Deployments Checklist

### 10.1 Current Deployment Status

**Platform: Local development only.** There is no cloud deployment configuration (no Dockerfile, docker-compose.yml, Procfile, vercel.json, or CI/CD pipeline). The application is designed to run entirely on a local machine.

### 10.2 Deployment Artifacts Present

| File | Purpose |
|------|---------|
| `start_api.sh` | Shell script to set up venv + install deps + start API |
| `start.py` | Interactive CLI menu to launch various components |
| `docs/GITHUB_DEPLOYMENT.md` | Documentation about GitHub deployment (repo hosting) |
| `Frontend/dist/` | Pre-built frontend (static files) |

### 10.3 Cloud Deployment Guide (Recommended Approach)

To deploy this application to a cloud platform, the following steps would be required:

#### Option A: VPS / VM (e.g., AWS EC2, DigitalOcean Droplet)

```bash
# Prerequisites on server:
# - Python 3.10+, Node.js 18+, nginx

# 1. Clone and set up backend
git clone <repo> && cd Health-Buddy
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install fastapi uvicorn chromadb pytz rich pdfplumber pypdf httpx gunicorn

# 2. Set environment variables
export GOOGLE_API_KEY=...
export PIPEDREAM_PROJECT_ID=...
# ... (all env vars from .env)

# 3. Run backend with gunicorn (production ASGI server)
cd api
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 4. Build frontend
cd Frontend
npm install && npm run build
# Serve dist/ via nginx

# 5. Configure nginx as reverse proxy
# - Serve Frontend/dist/ on port 80
# - Proxy /api/* and /ws/* to localhost:8000
```

#### Option B: Containerized (Docker)

A `Dockerfile` would need to be created:

```dockerfile
# Dockerfile (does not exist yet — must be created)
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt fastapi uvicorn chromadb pytz pdfplumber pypdf httpx
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Frontend would need a separate build step or multi-stage Docker build.

#### Option C: Platform-as-a-Service

| Platform | Backend | Frontend | Notes |
|----------|---------|----------|-------|
| **Railway** | Python service | Static deploy | Needs `Procfile` |
| **Render** | Web service | Static site | Needs `render.yaml` |
| **Vercel** | Not ideal (Python) | Ideal | Backend needs separate host |
| **Fly.io** | Docker | Docker | Needs `Dockerfile` + `fly.toml` |

### 10.4 Deployment Blockers

- [ ] **No Dockerfile** — Must be created
- [ ] **No CI/CD pipeline** — No GitHub Actions, no deploy scripts
- [ ] **SQLite is not production-ready** — Should migrate to PostgreSQL for concurrent access
- [ ] **ChromaDB local storage** — Needs persistent volume or managed vector DB
- [ ] **Hardcoded admin credentials** — `admin` / `admin123` must be replaced with proper auth
- [ ] **No HTTPS configuration** — Needs TLS/SSL setup
- [ ] **CORS allows only localhost** — Must be updated for production domain
- [ ] **No authentication middleware** — No JWT/session tokens; localStorage-only auth is insecure
- [ ] **`requirements.txt` is incomplete** — Missing fastapi, uvicorn, chromadb, pytz, etc.
- [ ] **Uploaded files stored locally** — Needs cloud storage (S3, GCS) for production
- [ ] **No health monitoring** — No logging service, no error tracking (Sentry, etc.)

---

## 11. Payment Integration & Credit Token System

### 11.1 Current Status: **Not Implemented**

After a thorough analysis of the entire codebase — every Python module, every API endpoint, every frontend page, all configuration files, and all database tables — **there is no payment integration or credit token system** in this application.

### 11.2 Evidence

| Area Searched | Result |
|---------------|--------|
| Database schema | No `payments`, `transactions`, `credits`, `tokens`, `billing`, or `subscriptions` table |
| API endpoints | No `/payment`, `/billing`, `/credits`, `/subscribe`, or `/checkout` route |
| Python modules | No Stripe, PayPal, Razorpay, or any payment SDK imported |
| Frontend pages | No payment form, checkout page, billing dashboard, or credit balance UI |
| `config.py` | No `STRIPE_KEY`, `PAYMENT_SECRET`, or billing configuration |
| `.env` files | No payment-related environment variables |
| `requirements.txt` | No `stripe`, `paypal`, `razorpay`, or payment library dependency |
| `package.json` | No `@stripe/react-stripe-js`, `react-paypal`, or payment frontend library |

### 11.3 Current Access Model

The application currently operates as a **free, open-access system**:
- **Patient registration**: Free, requires only name + email + phone
- **Appointment booking**: Unlimited, no payment or credit check
- **AI chat**: Unlimited queries (cost borne by the GOOGLE_API_KEY holder)
- **Doctor portal**: Free access by doctor_id selection
- **Admin panel**: Hardcoded credentials, no billing
- **No usage limits**: No rate limiting, no quotas, no credit tracking

### 11.4 Considerations for Future Implementation

If a payment/credit system were to be added, it would require:

1. **New database tables**: `payments`, `credit_transactions`, `user_credits`, `plans`
2. **Payment gateway integration**: Stripe SDK (Python + React), webhook handlers
3. **Credit middleware**: Deduct credits per chat query or appointment booking
4. **Billing UI**: Credit balance display, purchase page, transaction history
5. **Authentication upgrade**: JWT tokens to secure payment endpoints
6. **Webhook endpoint**: For async payment confirmations from Stripe/PayPal

---

## Appendix: Critical Blockers & Missing Requirements

### Blockers That Could Prevent the App from Running

| # | Blocker | Severity | Description |
|---|---------|----------|-------------|
| 1 | **Incomplete `requirements.txt`** | High | Missing `fastapi`, `uvicorn`, `chromadb`, `pytz`, `rich`, `pdfplumber`, `pypdf`, `httpx`, `pydantic[email]`. Users who `pip install -r requirements.txt` will get import errors. |
| 2 | **Google API key required** | High | Without a valid `GOOGLE_API_KEY`, the RAG engine and AI chat will fail (HTTP 503). The app partially works without it (appointments, registration). |
| 3 | **Pipedream credentials required** | Medium | Without valid Pipedream credentials, calendar sync will fail silently. Appointments still work but won't sync to Google Calendar. |
| 4 | **Database must be initialized** | Medium | If `data/healthcare.db` doesn't exist or is empty, the app will crash. `utils/db_setup.py` must be run first. The current repo includes a pre-populated database. |
| 5 | **Port conflicts** | Low | Backend defaults to port 8000, frontend to 8080. If these ports are occupied, manual port changes are needed. The frontend auto-falls back to 8081, but CORS must match. |
| 6 | **No real authentication** | Low (functionality) / High (security) | No JWT, no session tokens, no password hashing. Anyone with a user_id can access any patient's data. Admin uses hardcoded `admin/admin123`. |
