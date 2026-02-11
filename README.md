# Healthcare Assistant - AI-Powered Medical Platform

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

A full-stack healthcare management system with AI-powered medical assistance, appointment scheduling, Google Calendar integration, and intelligent approval workflows.

---

## Table of Contents

- [Features](#features)
  - [Doctor Portal](#doctor-portal)
  - [Patient Portal](#patient-portal)
  - [AI Capabilities](#ai-capabilities)
  - [Appointment Workflow](#appointment-workflow)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Key Features Explained](#key-features-explained)
- [Security Features](#security-features)
- [Testing](#testing)
- [Additional Documentation](#additional-documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Doctor Portal

- **Comprehensive Dashboard** - Real-time statistics and analytics
- **Appointment Management** - View, approve, and manage patient appointments
- **Patient Records** - Access complete patient history and medical notes
- **Approval Workflow** - Review and approve/reject appointment requests
- **Analytics** - Detailed insights into practice performance
- **Google Calendar Sync** - Automatic synchronization with Google Calendar

### Patient Portal

- **Secure Authentication** - Email and phone-based login
- **Smart Booking** - AI-powered appointment scheduling with conflict detection
- **Double-Booking Prevention** - Real-time slot availability checking
- **AI Medical Assistant** - Chat with RAG-powered medical AI for health queries
- **Calendar Invitations** - Automatic Google Calendar invites on approval
- **Responsive Design** - Works seamlessly on desktop and mobile

### AI Capabilities

- **RAG Engine** - Retrieval-Augmented Generation for accurate medical information
- **Google Gemini Integration** - Advanced AI model for natural conversations
- **Medical Knowledge Base** - Vector database with curated medical documents
- **Contextual Responses** - AI remembers conversation history for better assistance

### Appointment Workflow

1. Patient selects doctor and time slot
2. System checks for conflicts (including pending approvals)
3. Appointment created with `pending_approval` status
4. Doctor reviews request on dashboard (highlighted in amber)
5. Doctor approves or rejects
6. On approval:
   - Status changes to `confirmed`
   - Google Calendar event created
   - Both parties receive calendar invitations
   - Automatic email notifications via Google Calendar

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **FastAPI** | Modern, fast web framework for APIs |
| **SQLite** | Lightweight database for appointments and users |
| **Google Gemini AI** | Advanced language model (Gemini 2.5 Flash) |
| **ChromaDB** | Vector database for RAG |
| **Pipedream** | Google Calendar integration |
| **FastMCP** | Model Context Protocol for tool calling |

### Frontend

| Technology | Purpose |
|---|---|
| **React 18** | Modern UI library |
| **TypeScript** | Type-safe JavaScript |
| **Vite** | Lightning-fast build tool |
| **Tailwind CSS** | Utility-first CSS framework |
| **Shadcn/ui** | Beautiful component library |
| **React Router** | Client-side routing |

---

## Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm/bun
- Google API Key (for Gemini AI)
- Pipedream account with Google Calendar connected

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/MajorAbdullah/healthcare-assistant.git
cd healthcare-assistant
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Google Gemini AI
GOOGLE_API_KEY=your_gemini_api_key_here

# Pipedream (for Google Calendar)
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
```

#### Initialize Database

```bash
python db_setup.py
```

#### Run Database Migration (for approval system)

```bash
python migrate_approval_system.py
```

#### Start Backend Server

```bash
cd api
python main.py
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install
# or
bun install

# Start development server
npm run dev
# or
bun run dev
```

Frontend will run on `http://localhost:8080`

---

## API Documentation

Once the backend is running, visit:

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Key Endpoints

#### Patient Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/patients/register` | Register new patient |
| `POST` | `/api/v1/patients/login` | Patient login |
| `GET` | `/api/v1/doctors` | Get all doctors |
| `GET` | `/api/v1/doctors/{id}/availability` | Get available time slots |
| `POST` | `/api/v1/appointments` | Book appointment |
| `POST` | `/api/v1/chat` | Chat with AI assistant |

#### Doctor Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/doctors/login` | Doctor login |
| `GET` | `/api/v1/doctors/{id}/stats` | Get doctor statistics |
| `GET` | `/api/v1/doctors/{id}/appointments` | Get appointments |
| `PUT` | `/api/v1/appointments/{id}/approve` | Approve appointment |
| `PUT` | `/api/v1/appointments/{id}/reject` | Reject appointment |
| `POST` | `/api/v1/appointments/{id}/notes` | Add medical notes |

---

## Project Structure

```
healthcare-assistant/
├── api/                          # Backend API
│   ├── main.py                  # FastAPI application (46K+ lines)
│   └── __init__.py
├── Frontend/                     # React frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── patient/        # Patient portal pages
│   │   │   └── doctor/         # Doctor portal pages
│   │   ├── components/         # Reusable components
│   │   ├── lib/                # Utilities and API client
│   │   └── App.tsx
│   ├── public/
│   └── package.json
├── modules/                      # Core Python modules
│   ├── scheduler.py            # Appointment scheduling logic
│   ├── rag_engine.py           # RAG implementation with ChromaDB
│   ├── memory_manager.py       # Conversation memory management
│   ├── calendar_integration.py # Google Calendar sync via Pipedream
│   ├── calendar_sync.py        # Calendar synchronization helpers
│   └── calendar_assistant_wrapper.py
├── data/
│   ├── healthcare.db           # SQLite database
│   ├── medical_docs/           # Medical knowledge base
│   └── vector_db/              # ChromaDB vector store
├── docs/                         # Documentation
├── tests/                        # Test files (20+ test scripts)
├── calendar_cli/                # Standalone calendar CLI
├── config.py                    # Configuration
├── db_setup.py                  # Database initialization
├── migrate_approval_system.py   # Migration script
├── requirements.txt             # Python dependencies
└── README.md
```

---

## Key Features Explained

### Double-Booking Prevention

- Real-time slot availability checking
- Disabled UI for already booked slots
- Database-level conflict detection
- Checks both confirmed and pending appointments

### Approval Workflow

```
Patient Books --> pending_approval --> Doctor Approves --> confirmed
                                      |
                                      +--> Doctor Rejects --> cancelled
```

### Google Calendar Integration

- Automatic event creation on approval
- Email invitations sent by Google Calendar
- Bi-directional sync (patient and doctor calendars)
- Professional calendar invites with reminders

### AI Medical Assistant

- Powered by Google Gemini 2.5 Flash
- RAG for accurate medical information
- Context-aware conversations
- Cited sources for transparency

---

## Security Features

- Secure authentication for patients and doctors
- Database-level conflict prevention
- Status validation before approval
- Environment variables for sensitive data
- CORS protection
- Input validation and sanitization

---

## Testing

```bash
# Run basic tests
python tests/test_basic.py

# Test complete system
python tests/test_complete_system.py

# Test calendar integration
python tests/test_live_calendar_integration.py

# Test doctor portal
python tests/test_doctor_portal.py

# Test RAG engine
python tests/test_rag.py

# Test appointment scheduler
python tests/test_scheduler.py

# Test memory manager
python tests/test_memory_manager.py
```

---

## Additional Documentation

- [Approval System Implementation](docs/APPROVAL_SYSTEM_IMPLEMENTATION.md)
- [Quick Start Guide](docs/APPROVAL_SYSTEM_QUICK_START.md)
- [Why No Email Setup?](docs/WHY_NO_EMAIL_SETUP.md)
- [API Guide](docs/API_GUIDE.md)
- [System Architecture](SYSTEM_ARCHITECTURE.md)

---

## Roadmap

- [ ] SMS notifications
- [ ] Mobile app (React Native)
- [ ] Video consultations
- [ ] Prescription management
- [ ] Lab results integration
- [ ] Multi-language support
- [ ] Dark mode

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Syed Abdullah Shah (Major Abdullah)**

- GitHub: [@MajorAbdullah](https://github.com/MajorAbdullah)

## Acknowledgments

- Google Gemini AI for powerful language models
- Pipedream for seamless integrations
- Shadcn/ui for beautiful components
- FastAPI for excellent developer experience

---

**Built by [Major Abdullah](https://github.com/MajorAbdullah)**
