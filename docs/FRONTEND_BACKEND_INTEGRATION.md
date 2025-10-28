# Frontend-Backend Integration Complete Guide

## 📋 Overview

This document provides a complete guide for integrating the React/TypeScript frontend with the FastAPI backend for the Healthcare Assistant application.

## ✅ What Has Been Completed

### 1. Backend API (FastAPI) - ✅ COMPLETE
- **Location**: `/api/main.py`
- **Status**: Fully implemented with 26+ REST endpoints
- **Port**: `http://localhost:8000`
- **Documentation**: Swagger UI at `http://localhost:8000/docs`

### 2. Frontend Application (React + TypeScript + Vite) - ✅ COMPLETE
- **Location**: `/Frontend/`
- **Tech Stack**:
  - React 18 + TypeScript
  - Vite (build tool)
  - Tailwind CSS + shadcn/ui
  - React Router DOM
  - TanStack Query (React Query)
  - Zod (validation)

### 3. API Integration Layer - ✅ COMPLETE
- **Location**: `/Frontend/src/lib/api.ts`
- **Features**:
  - Centralized API client
  - Type-safe interfaces
  - Error handling
  - WebSocket support for real-time chat

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│                   Port: 5173 (Vite)                         │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Patient    │      │    Doctor    │                    │
│  │   Portal     │      │    Portal    │                    │
│  │  (6 screens) │      │  (6 screens) │                    │
│  └──────────────┘      └──────────────┘                    │
│          │                     │                            │
│          └─────────┬───────────┘                            │
│                    │                                        │
│            ┌───────▼────────┐                               │
│            │  API Client    │                               │
│            │  (api.ts)      │                               │
│            └───────┬────────┘                               │
└────────────────────┼──────────────────────────────────────┘
                     │
                     │ HTTP/REST + WebSocket
                     │
┌────────────────────▼──────────────────────────────────────┐
│                  BACKEND (FastAPI)                         │
│                 Port: 8000                                 │
│                                                            │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │ REST API (26)    │  │  WebSocket       │              │
│  │ Endpoints        │  │  Chat            │              │
│  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                          │
│           └──────────┬──────────┘                          │
│                      │                                     │
│          ┌───────────▼──────────┐                          │
│          │  Core Modules        │                          │
│          │  • RAG Engine        │                          │
│          │  • Scheduler         │                          │
│          │  • Memory Manager    │                          │
│          └───────────┬──────────┘                          │
│                      │                                     │
│          ┌───────────▼──────────┐                          │
│          │  Databases           │                          │
│          │  • SQLite            │                          │
│          │  • ChromaDB          │                          │
│          └──────────────────────┘                          │
└───────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
pipedream/
├── Frontend/                    # React frontend application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── patient/        # Patient portal screens
│   │   │   │   ├── Auth.tsx    # ✅ INTEGRATED - Login/Register
│   │   │   │   ├── Dashboard.tsx   # ⚠️ NEEDS UPDATE
│   │   │   │   ├── DashboardNew.tsx # ✅ NEW - Real API version
│   │   │   │   ├── Book.tsx    # ⚠️ NEEDS UPDATE
│   │   │   │   ├── Chat.tsx    # ⚠️ NEEDS UPDATE
│   │   │   │   ├── Appointments.tsx # ⚠️ NEEDS UPDATE
│   │   │   │   └── Profile.tsx # ⚠️ NEEDS UPDATE
│   │   │   └── doctor/         # Doctor portal screens
│   │   │       ├── Auth.tsx    # ⚠️ NEEDS UPDATE
│   │   │       ├── Dashboard.tsx # ⚠️ NEEDS UPDATE
│   │   │       ├── Calendar.tsx # ⚠️ NEEDS UPDATE
│   │   │       ├── Patients.tsx # ⚠️ NEEDS UPDATE
│   │   │       ├── PatientDetail.tsx # ⚠️ NEEDS UPDATE
│   │   │       └── Analytics.tsx # ⚠️ NEEDS UPDATE
│   │   ├── lib/
│   │   │   └── api.ts          # ✅ NEW - API integration layer
│   │   ├── components/ui/      # shadcn/ui components
│   │   └── App.tsx
│   ├── .env                    # ✅ NEW - Environment config
│   └── package.json
│
├── api/
│   └── main.py                 # ✅ COMPLETE - FastAPI backend
│
├── modules/                    # Backend modules
│   ├── rag_engine.py          # Medical Q&A
│   ├── scheduler.py           # Appointments
│   ├── memory_manager.py      # User context
│   └── calendar_sync.py       # Google Calendar
│
├── data/
│   ├── healthcare.db          # SQLite database
│   └── vector_db/             # ChromaDB for RAG
│
└── docs/
    ├── API_ENDPOINTS.md       # Complete API reference
    └── FRONTEND_PROMPTS.md    # Frontend specifications
```

## 🔌 API Integration Status

### ✅ Completed Integrations

1. **API Client (`/Frontend/src/lib/api.ts`)**
   - All 26 endpoints wrapped
   - Type-safe interfaces
   - Error handling
   - WebSocket client

2. **Patient Auth (`/Frontend/src/pages/patient/Auth.tsx`)**
   - Real login API call
   - Real registration API call
   - Error handling with toast notifications
   - LocalStorage for session management

3. **Patient Dashboard (`/Frontend/src/pages/patient/DashboardNew.tsx`)**
   - Fetches personalized greeting
   - Loads upcoming appointments
   - Shows recent activity
   - Real-time data

### ⚠️ Pending Integrations

The following pages still use mock data and need to be updated:

#### Patient Portal
1. **Book Appointment** (`Book.tsx`)
   - Replace mock doctors → `api.doctor.getAll()`
   - Replace mock availability → `api.doctor.getAvailability(doctorId, date)`
   - Replace mock booking → `api.appointment.book(...)`

2. **Medical Chat** (`Chat.tsx`)
   - Replace mock AI responses → `api.chat.sendMessage(userId, message)`
   - Optionally use WebSocket → `api.chat.connectWebSocket(userId, onMessage)`

3. **View Appointments** (`Appointments.tsx`)
   - Replace mock data → `api.appointment.getByPatient(userId)`
   - Add cancel functionality → `api.appointment.cancel(appointmentId)`

4. **Patient Profile** (`Profile.tsx`)
   - Fetch profile → `api.patient.getProfile(userId)`
   - Update profile → `api.patient.updateProfile(userId, data)`
   - Get/Update preferences → `api.patient.getPreferences/updatePreferences`

#### Doctor Portal
5. **Doctor Auth** (`doctor/Auth.tsx`)
   - Replace mock login → `api.doctor.login(doctorId)`

6. **Doctor Dashboard** (`doctor/Dashboard.tsx`)
   - Fetch stats → `api.doctor.getStats(doctorId)`
   - Fetch appointments → `api.doctor.getAppointments(doctorId)`

7. **Doctor Calendar** (`doctor/Calendar.tsx`)
   - Fetch appointments → `api.doctor.getAppointments(doctorId, {date})`
   - Update status → `api.appointment.updateStatus(appointmentId, status)`

8. **Doctor Patients** (`doctor/Patients.tsx`)
   - Fetch patients → `api.doctor.getPatients(doctorId)`

9. **Patient Detail** (`doctor/PatientDetail.tsx`)
   - Fetch history → `api.appointment.getPatientHistory(patientId)`
   - Add notes → `api.appointment.addNotes(appointmentId, notes)`

10. **Doctor Analytics** (`doctor/Analytics.tsx`)
    - Fetch analytics → `api.doctor.getAnalytics(doctorId)`

## 🚀 Quick Start Guide

### Step 1: Start Backend API

```bash
# From project root
cd api
python3 main.py

# Or use the start script
./start_api.sh
```

Verify: Visit `http://localhost:8000/health`

### Step 2: Install Frontend Dependencies

```bash
cd Frontend
npm install
```

### Step 3: Start Frontend Dev Server

```bash
npm run dev
```

Frontend will run on: `http://localhost:5173`

### Step 4: Test Integration

1. Open browser to `http://localhost:5173`
2. Go to Patient Login
3. Register a new account
4. Dashboard should load with real data

## 📝 Integration Examples

### Example 1: Updating Book Appointment Page

**Before (Mock):**
```tsx
// Book.tsx - OLD CODE
const handleConfirm = () => {
  toast.success("Appointment booked successfully!");
  setStep(5);
};
```

**After (Real API):**
```tsx
// Book.tsx - NEW CODE
import api from "@/lib/api";

const handleConfirm = async () => {
  try {
    const userId = parseInt(localStorage.getItem("user_id") || "0");
    
    const result = await api.appointment.book({
      user_id: userId,
      doctor_id: selectedDoctor!.id,
      date: selectedDate!.toISOString().split('T')[0],
      time: selectedTime,
      reason: reason,
      sync_calendar: false
    });

    if (result.success) {
      toast.success("Appointment booked successfully!");
      setStep(5);
    } else {
      toast.error(result.message || "Booking failed");
    }
  } catch (error: any) {
    toast.error(error.message || "Failed to book appointment");
  }
};
```

### Example 2: Updating Chat Page

**Before (Mock):**
```tsx
// Chat.tsx - OLD CODE
const getAIResponse = (question: string): string => {
  if (question.includes("blood pressure")) {
    return "High blood pressure can be caused by...";
  }
  // ... more hardcoded responses
};
```

**After (Real API):**
```tsx
// Chat.tsx - NEW CODE
import api from "@/lib/api";

const handleSendMessage = async (messageText?: string) => {
  const text = messageText || input.trim();
  if (!text) return;

  const userId = parseInt(localStorage.getItem("user_id") || "0");

  // Add user message
  const userMessage: Message = {
    id: Date.now().toString(),
    role: "user",
    content: text,
    timestamp: new Date(),
  };
  setMessages((prev) => [...prev, userMessage]);
  setInput("");
  setIsLoading(true);

  try {
    // Call real API
    const result = await api.chat.sendMessage(userId, text);
    
    if (result.success && result.data) {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: result.data.answer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } else {
      throw new Error(result.message || "Failed to get response");
    }
  } catch (error: any) {
    toast.error(error.message || "Failed to send message");
  } finally {
    setIsLoading(false);
  }
};
```

### Example 3: WebSocket Chat (Real-time)

```tsx
// Chat.tsx - WebSocket version
import { useEffect, useRef } from "react";
import api from "@/lib/api";

const Chat = () => {
  const wsRef = useRef<ReturnType<typeof api.chat.connectWebSocket> | null>(null);

  useEffect(() => {
    const userId = parseInt(localStorage.getItem("user_id") || "0");
    
    // Connect WebSocket
    wsRef.current = api.chat.connectWebSocket(userId, (data) => {
      // Handle incoming message
      if (data.type === "answer") {
        const aiMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: data.content,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, aiMessage]);
      }
    });

    return () => {
      // Cleanup on unmount
      wsRef.current?.close();
    };
  }, []);

  const sendMessage = (text: string) => {
    wsRef.current?.send(text);
    
    // Add user message to UI immediately
    setMessages((prev) => [...prev, {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date(),
    }]);
  };
};
```

## 🔐 Authentication Flow

1. **Register/Login**: User enters credentials → API validates → Returns `user_id`
2. **Store Session**: Save `user_id`, `user_name`, `user_type` in localStorage
3. **Protected Routes**: Check localStorage on component mount → Redirect if not authenticated
4. **API Calls**: Include `user_id` in request (from localStorage)
5. **Logout**: Clear localStorage → Redirect to auth page

## 🎨 Environment Variables

### Frontend (`.env`)
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME="Healthcare Assistant"
```

### Backend (`.env`)
```env
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
GOOGLE_API_KEY=your_google_api_key
```

## 🧪 Testing Checklist

- [ ] Backend API running on port 8000
- [ ] Frontend running on port 5173
- [ ] Patient Registration works
- [ ] Patient Login works
- [ ] Dashboard loads real data
- [ ] Book appointment works
- [ ] Medical chat works
- [ ] View appointments works
- [ ] Update profile works
- [ ] Doctor login works
- [ ] Doctor dashboard shows real stats
- [ ] WebSocket chat works
- [ ] Error handling shows toast notifications

## 📚 API Documentation

### Complete API Reference
See `/docs/API_ENDPOINTS.md` for full documentation of all 26 endpoints with:
- Request/Response schemas
- cURL examples
- Python examples
- JavaScript/Fetch examples

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐛 Common Issues & Solutions

### Issue 1: CORS Errors
**Problem**: Browser blocks requests from frontend to backend

**Solution**: Backend already configured with CORS middleware for `localhost:5173` and `localhost:3000`

### Issue 2: 404 Not Found
**Problem**: API endpoint not found

**Check**:
- Backend is running: `curl http://localhost:8000/health`
- Correct URL: Should be `http://localhost:8000/api/v1/...`
- Endpoint exists: Check `/docs/API_ENDPOINTS.md`

### Issue 3: Type Errors in TypeScript
**Problem**: TypeScript complains about API response types

**Solution**: Use the types exported from `api.ts`:
```tsx
import api, { type Appointment, type Doctor } from "@/lib/api";
```

### Issue 4: WebSocket Connection Failed
**Problem**: WebSocket won't connect

**Check**:
- Backend WebSocket endpoint is running
- URL is `ws://localhost:8000` (not `http://`)
- User ID is valid

## 🔄 Next Steps

### Immediate (Priority 1)
1. Update remaining patient portal pages (Book, Chat, Appointments, Profile)
2. Test all patient flows end-to-end
3. Fix any bugs discovered during testing

### Short-term (Priority 2)
4. Update all doctor portal pages
5. Implement WebSocket chat for real-time
6. Add loading states and skeleton screens
7. Improve error handling

### Future Enhancements (Priority 3)
8. Add authentication tokens (JWT)
9. Implement refresh tokens
10. Add offline support with service workers
11. Deploy to production
12. Add analytics tracking
13. Implement rate limiting
14. Add API caching with React Query
15. Add unit and integration tests

## 📞 Support

For issues or questions:
1. Check `/docs/API_ENDPOINTS.md` for API details
2. Check `/docs/FRONTEND_PROMPTS.md` for UI specifications
3. Test API directly: `http://localhost:8000/docs`
4. Check backend logs in terminal

---

**Status**: Frontend-Backend integration layer complete ✅
**Next Action**: Update remaining pages to use real API calls
**Estimated Time**: 2-3 hours for all remaining integrations
