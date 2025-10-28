# 📡 Healthcare Assistant - API Endpoints Reference

**Base URL:** `http://localhost:8000/api/v1`

**API Documentation:** http://localhost:8000/docs (Swagger UI)

---

## 🏥 PATIENT PORTAL ENDPOINTS

### Authentication & Registration

#### Register New Patient
```
POST /api/v1/patients/register
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "dob": "1990-01-01",        // Optional
  "gender": "Male"             // Optional
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 15,
    "name": "John Doe"
  },
  "message": "Registration successful!"
}
```

---

#### Patient Login
```
POST /api/v1/patients/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "phone": "1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 15,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "token": "patient_15"
  },
  "message": "Login successful!"
}
```

---

### Patient Profile

#### Get Patient Details
```
GET /api/v1/patients/{user_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 15,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "created_at": "2025-10-28 03:00:00",
    "stats": {
      "total_appointments": 5,
      "upcoming_appointments": 2,
      "completed_appointments": 3
    }
  }
}
```

---

#### Update Patient Information
```
PUT /api/v1/patients/{user_id}
```

**Request Body:**
```json
{
  "name": "John Updated",      // Optional
  "email": "new@example.com",  // Optional
  "phone": "9876543210",       // Optional
  "dob": "1990-01-01",         // Optional
  "gender": "Male"             // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

---

#### Get Personalized Greeting
```
GET /api/v1/patients/{user_id}/greeting
```

**Response:**
```json
{
  "success": true,
  "data": {
    "greeting": "Good morning, John Doe!",
    "upcoming_appointment": {
      "appointment_id": 13,
      "when": "tomorrow",
      "time": "11:30",
      "doctor_name": "Dr. Aisha Khan",
      "specialty": "Rehabilitation & Recovery",
      "message": "You have an appointment tomorrow at 11:30 with Dr. Aisha Khan"
    }
  }
}
```

**Note:** If no upcoming appointment, `upcoming_appointment` will be `null`.

---

### Patient Preferences

#### Get Patient Preferences
```
GET /api/v1/patients/{user_id}/preferences
```

**Response:**
```json
{
  "success": true,
  "data": {
    "email_notifications": true,
    "sms_reminders": true,
    "auto_sync_calendar": false
  }
}
```

---

#### Update Patient Preferences
```
PUT /api/v1/patients/{user_id}/preferences
```

**Request Body:**
```json
{
  "email_notifications": true,    // Optional
  "sms_reminders": false,         // Optional
  "auto_sync_calendar": true      // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Preferences updated successfully"
}
```

---

### Doctors

#### Get All Doctors
```
GET /api/v1/doctors
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "doctor_id": 1,
      "name": "Dr. Sarah Johnson",
      "specialty": "Neurology - Stroke Specialist",
      "active_appointments": 2
    },
    {
      "doctor_id": 2,
      "name": "Dr. Michael Chen",
      "specialty": "Emergency Medicine",
      "active_appointments": 1
    },
    {
      "doctor_id": 3,
      "name": "Dr. Aisha Khan",
      "specialty": "Rehabilitation & Recovery",
      "active_appointments": 10
    }
  ]
}
```

---

#### Get Doctor Availability
```
GET /api/v1/doctors/{doctor_id}/availability?date=YYYY-MM-DD
```

**Query Parameters:**
- `date` (required): Date in YYYY-MM-DD format

**Example:**
```
GET /api/v1/doctors/1/availability?date=2025-10-29
```

**Response:**
```json
{
  "success": true,
  "data": {
    "date": "2025-10-29",
    "doctor_id": 1,
    "available_slots": [
      "09:00",
      "09:30",
      "10:00",
      "10:30",
      "11:00",
      "11:30",
      "13:00",
      "13:30",
      "14:00",
      "14:30",
      "15:00",
      "15:30",
      "16:00",
      "16:30"
    ],
    "total_slots": 14
  }
}
```

---

### Appointments

#### Book Appointment
```
POST /api/v1/appointments
```

**Request Body:**
```json
{
  "user_id": 15,
  "doctor_id": 1,
  "date": "2025-10-29",
  "time": "14:00",
  "reason": "Regular checkup",        // Optional
  "sync_calendar": true               // Optional, default: false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "appointment_id": 14,
    "date": "2025-10-29",
    "time": "14:00"
  },
  "message": "Appointment booked successfully!"
}
```

**Error Response (Slot Taken):**
```json
{
  "detail": "Unable to book appointment. Time slot may be unavailable."
}
```

---

#### Get Patient Appointments
```
GET /api/v1/appointments/{user_id}
```

**Query Parameters (Optional):**
- `limit`: Number of appointments to return
- `status`: Filter by status (scheduled, completed, cancelled)

**Examples:**
```
GET /api/v1/appointments/15
GET /api/v1/appointments/15?limit=5
GET /api/v1/appointments/15?status=scheduled
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "appointment_id": 14,
      "user_id": 15,
      "doctor_id": 1,
      "appointment_date": "2025-10-29",
      "start_time": "14:00",
      "end_time": "14:30",
      "status": "scheduled",
      "reason": "Regular checkup",
      "notes": null,
      "synced_to_calendar": 1,
      "created_at": "2025-10-28 03:30:00",
      "doctor_name": "Dr. Sarah Johnson",
      "doctor_specialty": "Neurology - Stroke Specialist"
    }
  ]
}
```

---

#### Cancel Appointment
```
PUT /api/v1/appointments/{appointment_id}/cancel
```

**Response:**
```json
{
  "success": true,
  "message": "Appointment cancelled successfully"
}
```

---

### Chat with AI

#### Chat (REST API)
```
POST /api/v1/chat
```

**Request Body:**
```json
{
  "user_id": 15,
  "message": "What are the symptoms of diabetes?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "The common symptoms of diabetes include...",
    "timestamp": "2025-10-28T03:45:00"
  }
}
```

**Note:** For real-time chat, use WebSocket endpoint below.

---

#### Chat (WebSocket)
```
WS ws://localhost:8000/ws/chat/{user_id}
```

**Connect:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/15');
```

**Send Message:**
```javascript
ws.send(JSON.stringify({
  message: "What causes high blood pressure?"
}));
```

**Receive Response:**
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.content);      // AI response
  console.log(data.timestamp);    // Response time
};
```

---

## 👨‍⚕️ DOCTOR PORTAL ENDPOINTS

### Authentication

#### Doctor Login
```
POST /api/v1/doctors/login
```

**Request Body:**
```json
{
  "doctor_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "doctor_id": 1,
    "name": "Dr. Sarah Johnson",
    "specialty": "Neurology - Stroke Specialist",
    "token": "doctor_1"
  },
  "message": "Welcome, Dr. Sarah Johnson!"
}
```

---

### Dashboard Statistics

#### Get Doctor Stats
```
GET /api/v1/doctors/{doctor_id}/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "today_count": 0,
    "total_patients": 7,
    "week_count": 2,
    "completion_rate": 85.5
  }
}
```

**Fields:**
- `today_count`: Appointments scheduled for today
- `total_patients`: Total unique patients seen
- `week_count`: Appointments this week
- `completion_rate`: Percentage of completed appointments

---

### Schedule Management

#### Get Doctor Appointments
```
GET /api/v1/doctors/{doctor_id}/appointments
```

**Query Parameters (Optional):**
- `date`: Specific date (YYYY-MM-DD) or "today"
- `start_date`: Start of date range (YYYY-MM-DD)
- `end_date`: End of date range (YYYY-MM-DD)

**Examples:**
```
GET /api/v1/doctors/1/appointments?date=today
GET /api/v1/doctors/1/appointments?date=2025-10-29
GET /api/v1/doctors/1/appointments?start_date=2025-10-01&end_date=2025-10-31
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "appointment_id": 14,
      "user_id": 15,
      "doctor_id": 1,
      "appointment_date": "2025-10-29",
      "start_time": "14:00",
      "end_time": "14:30",
      "status": "scheduled",
      "reason": "Regular checkup",
      "notes": null,
      "patient_name": "John Doe",
      "patient_email": "john@example.com",
      "patient_phone": "1234567890"
    }
  ]
}
```

---

### Patient Management

#### Get Doctor's Patients
```
GET /api/v1/doctors/{doctor_id}/patients
```

**Query Parameters (Optional):**
- `search`: Search by name, email, or phone
- `sort`: Sort by "name", "last_visit", or "total_visits"
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

**Examples:**
```
GET /api/v1/doctors/1/patients
GET /api/v1/doctors/1/patients?search=john
GET /api/v1/doctors/1/patients?sort=total_visits&page=1&per_page=10
```

**Response:**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "user_id": 15,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "total_visits": 5,
        "last_visit": "2025-10-28"
      }
    ],
    "total_count": 25,
    "pages": 3,
    "current_page": 1
  }
}
```

---

#### Get Patient Appointment History
```
GET /api/v1/patients/{patient_id}/appointments
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "appointment_id": 14,
      "user_id": 15,
      "doctor_id": 1,
      "appointment_date": "2025-10-29",
      "start_time": "14:00",
      "end_time": "14:30",
      "status": "scheduled",
      "reason": "Regular checkup",
      "notes": "Patient reports feeling better",
      "doctor_name": "Dr. Sarah Johnson",
      "specialty": "Neurology - Stroke Specialist"
    }
  ]
}
```

---

### Medical Notes

#### Add Medical Notes
```
POST /api/v1/appointments/{appointment_id}/notes
```

**Request Body:**
```json
{
  "notes": "Patient presented with mild headache. Prescribed rest and hydration. Follow-up in 2 weeks."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Medical notes saved successfully"
}
```

---

#### Update Medical Notes
```
PUT /api/v1/appointments/{appointment_id}/notes
```

**Request Body:**
```json
{
  "notes": "Updated notes: Patient condition improved. Continue current treatment."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Medical notes saved successfully"
}
```

---

### Appointment Status

#### Update Appointment Status
```
PUT /api/v1/appointments/{appointment_id}/status
```

**Request Body:**
```json
{
  "status": "completed"
}
```

**Valid Status Values:**
- `scheduled`
- `completed`
- `cancelled`
- `no-show`

**Response:**
```json
{
  "success": true,
  "message": "Appointment marked as completed"
}
```

---

### Analytics

#### Get Doctor Analytics
```
GET /api/v1/doctors/{doctor_id}/analytics
```

**Query Parameters (Optional):**
- `start_date`: Start date (YYYY-MM-DD), default: 30 days ago
- `end_date`: End date (YYYY-MM-DD), default: today

**Example:**
```
GET /api/v1/doctors/1/analytics?start_date=2025-10-01&end_date=2025-10-31
```

**Response:**
```json
{
  "success": true,
  "data": {
    "period": {
      "start_date": "2025-10-01",
      "end_date": "2025-10-31"
    },
    "total_appointments": 45,
    "total_patients": 32,
    "avg_daily_appointments": 1.5,
    "completion_rate": 88.9,
    "status_breakdown": {
      "scheduled": 12,
      "completed": 30,
      "cancelled": 2,
      "no-show": 1
    },
    "daily_breakdown": [
      {
        "date": "2025-10-01",
        "count": 3
      },
      {
        "date": "2025-10-02",
        "count": 2
      }
    ],
    "weekly_breakdown": {
      "Monday": 8,
      "Tuesday": 10,
      "Wednesday": 9,
      "Thursday": 7,
      "Friday": 11,
      "Saturday": 0,
      "Sunday": 0
    },
    "patient_growth": [
      {
        "week": "2025-40",
        "count": 15
      },
      {
        "week": "2025-41",
        "count": 18
      }
    ]
  }
}
```

**Use Cases:**
- **daily_breakdown**: For line/area charts showing trends
- **weekly_breakdown**: For bar charts showing busiest days
- **patient_growth**: For patient growth over time
- **status_breakdown**: For pie/donut charts

---

## 🔧 SYSTEM ENDPOINTS

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-28T03:49:26.053756"
}
```

---

### API Root
```
GET /
```

**Response:**
```json
{
  "message": "Healthcare Assistant API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "endpoints": {
    "patient_portal": "/api/v1/patients/...",
    "doctor_portal": "/api/v1/doctors/...",
    "chat": "/api/v1/chat or ws://localhost:8000/ws/chat/{user_id}"
  }
}
```

---

## 📋 RESPONSE FORMATS

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (validation error)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## 🔐 AUTHENTICATION

**Current Implementation:**
- Simple token-based (for prototype)
- Patient login: Returns `token: "patient_{user_id}"`
- Doctor login: Returns `token: "doctor_{doctor_id}"`

**Future Enhancement:**
- Implement JWT tokens
- Add token to Authorization header: `Authorization: Bearer {token}`

---

## 📊 ENDPOINT SUMMARY

### Patient Portal (10 endpoints):
1. `POST /api/v1/patients/register` - Register
2. `POST /api/v1/patients/login` - Login
3. `GET /api/v1/patients/{user_id}` - Get profile
4. `PUT /api/v1/patients/{user_id}` - Update profile
5. `GET /api/v1/patients/{user_id}/greeting` - Greeting
6. `GET /api/v1/patients/{user_id}/preferences` - Get preferences
7. `PUT /api/v1/patients/{user_id}/preferences` - Update preferences
8. `GET /api/v1/doctors` - List doctors
9. `GET /api/v1/doctors/{id}/availability` - Check slots
10. `POST /api/v1/chat` - Chat with AI

### Appointments (3 endpoints):
11. `POST /api/v1/appointments` - Book
12. `GET /api/v1/appointments/{user_id}` - Get all
13. `PUT /api/v1/appointments/{id}/cancel` - Cancel

### Doctor Portal (9 endpoints):
14. `POST /api/v1/doctors/login` - Login
15. `GET /api/v1/doctors/{id}/stats` - Dashboard stats
16. `GET /api/v1/doctors/{id}/appointments` - Schedule
17. `GET /api/v1/doctors/{id}/patients` - Patient list
18. `GET /api/v1/patients/{id}/appointments` - Patient history
19. `POST /api/v1/appointments/{id}/notes` - Add notes
20. `PUT /api/v1/appointments/{id}/notes` - Update notes
21. `PUT /api/v1/appointments/{id}/status` - Update status
22. `GET /api/v1/doctors/{id}/analytics` - Analytics

### System (2 endpoints):
23. `GET /health` - Health check
24. `GET /` - API info

### WebSocket (1 endpoint):
25. `WS /ws/chat/{user_id}` - Real-time chat

**Total: 25 REST endpoints + 1 WebSocket**

---

## 🧪 TESTING ENDPOINTS

### Using cURL:
```bash
# Health check
curl http://localhost:8000/health

# Get doctors
curl http://localhost:8000/api/v1/doctors

# Register patient
curl -X POST http://localhost:8000/api/v1/patients/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"1234567890"}'

# Check availability
curl "http://localhost:8000/api/v1/doctors/1/availability?date=2025-10-29"
```

### Using Python:
```python
import requests

# Get all doctors
response = requests.get("http://localhost:8000/api/v1/doctors")
doctors = response.json()["data"]

# Book appointment
response = requests.post(
    "http://localhost:8000/api/v1/appointments",
    json={
        "user_id": 15,
        "doctor_id": 1,
        "date": "2025-10-29",
        "time": "14:00",
        "reason": "Checkup"
    }
)
```

### Using JavaScript/TypeScript:
```typescript
// Fetch doctors
const response = await fetch('http://localhost:8000/api/v1/doctors');
const data = await response.json();
const doctors = data.data;

// Book appointment
const bookResponse = await fetch('http://localhost:8000/api/v1/appointments', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 15,
    doctor_id: 1,
    date: '2025-10-29',
    time: '14:00',
    reason: 'Checkup'
  })
});
```

---

## 📚 INTERACTIVE DOCUMENTATION

**Swagger UI:** http://localhost:8000/docs
- Try all endpoints directly in browser
- See request/response schemas
- No Postman needed!

**ReDoc:** http://localhost:8000/redoc
- Alternative documentation view
- Better for reading/printing

---

## 🚀 QUICK START

1. **Start API server:**
   ```bash
   cd api
   python3 main.py
   ```

2. **Test health:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Open docs:**
   - Browser: http://localhost:8000/docs

4. **Start building frontend:**
   - Use these endpoints in your UI
   - Base URL: `http://localhost:8000/api/v1`

---

**API is ready to use! Happy coding! 🎉**
