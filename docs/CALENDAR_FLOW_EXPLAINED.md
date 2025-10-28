# 📅 Calendar Integration & User Flow - Complete Explanation

## 🔍 Current Setup Overview

### **YES - Same Calendar for Everyone**
All appointments (from both patient and doctor portals) sync to the **SAME Google Calendar**:
- **Calendar Email**: `pinkpantherking20@gmail.com`
- **All 3 doctors** share this calendar
- **All patients** sync their appointments to this calendar
- **Configured via**: Pipedream (MCP - Model Context Protocol)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HEALTHCARE ASSISTANT SYSTEM                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐              ┌──────────────────┐            │
│  │  Patient Portal  │              │  Doctor Portal   │            │
│  │                  │              │                  │            │
│  │  • Book appt     │              │  • View schedule │            │
│  │  • Sync calendar │              │  • Sync appts    │            │
│  └────────┬─────────┘              └────────┬─────────┘            │
│           │                                 │                       │
│           └────────────┬────────────────────┘                       │
│                        │                                            │
│                        ▼                                            │
│           ┌────────────────────────┐                                │
│           │  CalendarSync Module   │                                │
│           │  (calendar_sync.py)    │                                │
│           └────────────┬───────────┘                                │
│                        │                                            │
│                        ▼                                            │
│           ┌────────────────────────┐                                │
│           │  SmartCalendarAssistant│                                │
│           │  (calendar_assistant.py)│                               │
│           └────────────┬───────────┘                                │
│                        │                                            │
│                        ▼                                            │
│           ┌────────────────────────┐                                │
│           │   Pipedream MCP        │                                │
│           │   (Model Context       │                                │
│           │    Protocol)           │                                │
│           └────────────┬───────────┘                                │
│                        │                                            │
│                        ▼                                            │
│           ┌────────────────────────┐                                │
│           │  Google Calendar API   │                                │
│           │                        │                                │
│           │  pinkpantherking20     │                                │
│           │  @gmail.com            │                                │
│           └────────────────────────┘                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Configuration

### Doctors Table:
```sql
doctor_id | name              | specialty                     | calendar_id
----------|-------------------|-------------------------------|---------------------------
1         | Dr. Sarah Johnson | Neurology - Stroke Specialist | pinkpantherking20@gmail.com
2         | Dr. Michael Chen  | Emergency Medicine            | pinkpantherking20@gmail.com
3         | Dr. Aisha Khan    | Rehabilitation & Recovery     | pinkpantherking20@gmail.com
```

**All doctors share the SAME calendar_id** = `pinkpantherking20@gmail.com`

---

## 🔄 Complete User Flow

### **PATIENT PORTAL FLOW**

#### 1. **Patient Books Appointment**
```
Patient Portal (healthcare_assistant.py)
  ↓
User selects: [2] Book an appointment
  ↓
1. Choose Doctor (Dr. Sarah Johnson)
2. Enter Date (2025-10-29)
3. Select Time (10:00 AM)
4. Enter Reason ("Stroke prevention consultation")
5. Confirm booking
  ↓
AppointmentScheduler.book_appointment()
  ↓
Appointment saved to SQLite database:
  - appointment_id: 11
  - user_id: 5
  - doctor_id: 1
  - appointment_date: 2025-10-29
  - start_time: 10:00:00
  - end_time: 10:30:00
  - status: 'scheduled'
  - reason: "Stroke prevention consultation"
```

#### 2. **Calendar Sync Prompt**
```
System asks: "Would you like to sync to Google Calendar? (Y/n)"
  ↓
If user says YES:
  ↓
CalendarSync.sync_appointment(appointment_id=11)
  ↓
Fetches appointment details from database
  ↓
Formats natural language command:
  "Schedule an event titled 'Appointment: John Doe with Dr. Sarah Johnson'
   on Tuesday, October 29, 2025 from 10:00 AM to 10:30 AM.
   
   Description:
   Patient: John Doe
   Email: john@example.com
   Doctor: Dr. Sarah Johnson (Neurology - Stroke Specialist)
   Reason: Stroke prevention consultation
   
   Appointment ID: 11"
```

#### 3. **Pipedream Integration**
```
SmartCalendarAssistant (calendar_assistant.py)
  ↓
Connects to Pipedream MCP server
  ↓
Sends natural language request via Gemini AI
  ↓
Pipedream processes request through:
  - Authentication (OAuth 2.0)
  - MCP protocol translation
  - Google Calendar API call
  ↓
Creates event on: pinkpantherking20@gmail.com
  ↓
Returns success confirmation
```

#### 4. **Database Update**
```
Update appointments table:
  SET calendar_event_id = 'synced_via_assistant'
  SET notes = notes || '\n[Calendar synced to pinkpantherking20@gmail.com]'
  WHERE appointment_id = 11
  ↓
Patient sees:
  ✅ Appointment synced to Google Calendar!
  📧 Email notification sent
  📅 Check your calendar at pinkpantherking20@gmail.com
```

---

### **DOCTOR PORTAL FLOW**

#### 1. **Doctor Views Schedule**
```
Doctor Portal (doctor_portal.py)
  ↓
Login as Dr. Sarah Johnson (ID: 1)
  ↓
Select: [1] View Today's Schedule
  ↓
Queries database:
  SELECT * FROM appointments
  WHERE doctor_id = 1
    AND appointment_date = '2025-10-28'
  ↓
Displays table:
  Time    | Patient   | Contact      | Reason              | Status
  10:00AM | John Doe  | 555-1234     | Stroke prevention   | 🟢 Scheduled
  2:00PM  | Jane Smith| 555-5678     | Follow-up           | 🟢 Scheduled
```

#### 2. **Doctor Syncs Appointments**
```
Doctor selects: [7] Sync to Calendar
  ↓
System finds all upcoming scheduled appointments:
  - Filters: status='scheduled', date >= today
  ↓
Found 5 upcoming appointments
  ↓
Prompt: "Sync these to Google Calendar? (Y/n)"
  ↓
If YES:
  ↓
For each appointment (in parallel or sequence):
  CalendarSync.sync_appointment(appointment_id)
  ↓
  Formats event details
  ↓
  Sends to Pipedream → Google Calendar
  ↓
  Updates database with sync status
  ↓
Progress: ████████████ 100% (5/5 synced)
  ↓
✅ Successfully synced 5/5 appointments!
```

#### 3. **Doctor Adds Notes**
```
Doctor selects: [4] Add Medical Notes
  ↓
Shows recent appointments (last 7 days)
  ↓
Doctor enters appointment ID: 11
  ↓
Doctor types notes:
  "Patient presented with concerns about stroke prevention.
   Discussed lifestyle modifications:
   - Blood pressure monitoring
   - Regular exercise
   - Mediterranean diet
   
   Prescribed: Low-dose aspirin
   Follow-up: 3 months"
  ↓
Updates database:
  UPDATE appointments
  SET notes = '[entered text]'
  WHERE appointment_id = 11
  ↓
✅ Medical notes saved successfully!
```

---

## 🔐 Authentication & Configuration

### Pipedream Configuration (.env file):
```env
# Pipedream OAuth Setup
PIPEDREAM_PROJECT_ID=proj_PNsKbWY
PIPEDREAM_ENVIRONMENT=development
PIPEDREAM_CLIENT_ID=Yvd50ERegpRGxMdmqAxQZ5zJmONx82esjU_Sbjn8pNs
PIPEDREAM_CLIENT_SECRET=ndjulzYS7NJKcCqzIAQD9BV5W3cJpVHhvNxKnCwGDsE

# Google Gemini AI (for natural language processing)
GOOGLE_API_KEY=AIzaSyAB-nZ0o5Fdva3Ibi6f5LIxuySkNNk5Ats

# User Identifier
EXTERNAL_USER_ID=user-123
```

### How It Works:
1. **Pipedream acts as middleware** between your app and Google Calendar
2. **MCP (Model Context Protocol)** translates natural language → API calls
3. **Gemini AI** processes the natural language requests
4. **OAuth 2.0** handles secure authentication
5. **Single calendar** (`pinkpantherking20@gmail.com`) receives all events

---

## 📝 Event Format on Google Calendar

### What appears on the calendar:

```
Title: Appointment: John Doe with Dr. Sarah Johnson
Date: Tuesday, October 29, 2025
Time: 10:00 AM - 10:30 AM

Description:
Patient: John Doe
Email: john@example.com
Doctor: Dr. Sarah Johnson (Neurology - Stroke Specialist)
Reason: Stroke prevention consultation

Appointment ID: 11

Reminder: 30 minutes before
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    APPOINTMENT BOOKING                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Save to SQLite Database (data/healthcare.db)            │
│     • appointments table                                     │
│     • Status: 'scheduled'                                    │
│     • calendar_event_id: NULL (initially)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. User Chooses Calendar Sync (Y/n)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                 YES                NO
                   │                 │
                   ▼                 ▼
      ┌────────────────────┐   ┌──────────────┐
      │ 3. CalendarSync    │   │ End (DB only)│
      │    Module          │   └──────────────┘
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 4. Format Natural  │
      │    Language Event  │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 5. SmartCalendar   │
      │    Assistant       │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 6. Pipedream MCP   │
      │    Server          │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 7. Google Calendar │
      │    API Call        │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 8. Event Created   │
      │    on Calendar     │
      │    pinkpantherking │
      │    20@gmail.com    │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 9. Update DB       │
      │    calendar_event_ │
      │    id='synced'     │
      └────────────────────┘
                   │
                   ▼
      ┌────────────────────┐
      │ 10. Success!       │
      │     ✅ Synced      │
      └────────────────────┘
```

---

## ⚙️ Key Components

### 1. **CalendarSync Module** (`modules/calendar_sync.py`)
- **Purpose**: Bridge between scheduler and calendar
- **Methods**:
  - `sync_appointment(appointment_id)` - Sync single appointment
  - `book_with_calendar()` - Book + sync in one operation
- **Features**:
  - Async support
  - Auto-retry on failure
  - Natural language formatting

### 2. **SmartCalendarAssistant** (`calendar_assistant.py`)
- **Purpose**: Interact with Google Calendar via Pipedream
- **Technology**: 
  - MCP (Model Context Protocol)
  - Gemini AI for NLP
  - Async/await pattern
- **Methods**:
  - `initialize()` - Connect to Pipedream
  - `send_message()` - Send calendar commands
  - `create_event()` - Create calendar events

### 3. **AppointmentScheduler** (`modules/scheduler.py`)
- **Purpose**: Core appointment management
- **Database**: SQLite (data/healthcare.db)
- **Features**:
  - Conflict detection
  - Availability checking
  - Doctor/patient management

---

## 🎯 Current Limitations & Solutions

### **Issue 1: Single Shared Calendar**
**Current**: All doctors use `pinkpantherking20@gmail.com`

**Impact**:
- All appointments appear on same calendar
- No separation between doctors
- Harder to manage individual schedules

**Potential Solutions**:
```python
# Option A: Create separate calendars for each doctor
doctors_calendars = {
    1: 'dr.sarah.johnson@gmail.com',
    2: 'dr.michael.chen@gmail.com',
    3: 'dr.aisha.khan@gmail.com'
}

# Option B: Use color-coding on shared calendar
event_colors = {
    1: 'blue',    # Dr. Sarah Johnson
    2: 'green',   # Dr. Michael Chen
    3: 'yellow'   # Dr. Aisha Khan
}

# Option C: Add doctor name as prefix
event_title = f"[Dr. {doctor_name}] Appointment: {patient_name}"
```

### **Issue 2: No Calendar Event ID Storage**
**Current**: We store `'synced_via_assistant'` as a flag

**Impact**:
- Cannot update/delete events later
- Cannot verify sync status
- No way to handle conflicts

**Solution**:
```python
# Store actual Google Calendar event ID
# Modify calendar_sync.py to capture event ID from response
cursor.execute("""
    UPDATE appointments 
    SET calendar_event_id = ?
    WHERE appointment_id = ?
""", (actual_event_id, appointment_id))
```

---

## 🔮 Future Enhancements

### 1. **Multi-Calendar Support**
```python
class CalendarSync:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.calendars = {
            'doctor_1': 'dr.sarah@gmail.com',
            'doctor_2': 'dr.michael@gmail.com',
            'doctor_3': 'dr.aisha@gmail.com',
            'shared': 'pinkpantherking20@gmail.com'
        }
    
    def sync_to_doctor_calendar(self, appointment_id):
        appointment = self.scheduler.get_appointment(appointment_id)
        doctor_id = appointment['doctor_id']
        
        # Get doctor-specific calendar
        calendar_email = self.get_doctor_calendar(doctor_id)
        
        # Sync to that calendar
        self.sync_to_calendar(appointment_id, calendar_email)
```

### 2. **Bidirectional Sync**
- Read events FROM Google Calendar
- Detect external changes
- Update local database
- Handle conflicts

### 3. **Event Updates & Cancellations**
```python
async def update_calendar_event(self, appointment_id):
    """Update existing calendar event when appointment changes"""
    
async def cancel_calendar_event(self, appointment_id):
    """Remove event from calendar when appointment is cancelled"""
```

### 4. **Patient Calendar Sync**
```python
# Allow patients to sync to their OWN calendars
patient_email = appointment['patient_email']
send_calendar_invite(patient_email, event_details)
```

---

## 🧪 Testing the Flow

### Test Patient Booking:
```bash
python3 healthcare_assistant.py
# 1. Login as patient
# 2. Book appointment
# 3. Sync to calendar
# 4. Check pinkpantherking20@gmail.com
```

### Test Doctor View:
```bash
python3 doctor_portal.py
# 1. Login as doctor
# 2. View schedule
# 3. Bulk sync appointments
# 4. Check calendar
```

### Verify Database:
```bash
sqlite3 data/healthcare.db "
SELECT 
    a.appointment_id,
    u.name as patient,
    d.name as doctor,
    a.appointment_date,
    a.start_time,
    a.calendar_event_id,
    d.calendar_id
FROM appointments a
JOIN users u ON a.user_id = u.user_id
JOIN doctors d ON a.doctor_id = d.doctor_id
ORDER BY a.appointment_date, a.start_time;
"
```

---

## 📋 Summary

### **Current Setup:**
✅ **Single Calendar**: `pinkpantherking20@gmail.com`  
✅ **Shared by**: All 3 doctors + all patients  
✅ **Technology**: Pipedream MCP + Gemini AI  
✅ **Both Portals**: Patient and Doctor can sync  
✅ **Natural Language**: AI processes event creation  
✅ **Database Tracked**: SQLite stores sync status  

### **How It Works:**
1. Appointment booked → Saved to SQLite
2. User chooses sync → CalendarSync module activated
3. Event formatted → Natural language description
4. Sent to Pipedream → MCP protocol translation
5. Google Calendar API → Event created
6. Database updated → Sync status saved
7. User notified → Success confirmation

### **Key Files:**
- `modules/calendar_sync.py` - Calendar integration logic
- `calendar_assistant.py` - Pipedream MCP interface
- `modules/scheduler.py` - Appointment management
- `.env` - Pipedream credentials
- `data/healthcare.db` - Appointments & doctor data

---

*Last Updated: October 28, 2025*  
*Healthcare Assistant v1.0.0 - Dual Portal System*
