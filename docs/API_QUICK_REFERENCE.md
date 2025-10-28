# API Integration Quick Reference

## 🚀 Quick Start

```bash
# Terminal 1: Start Backend
cd api && python3 main.py

# Terminal 2: Start Frontend
cd Frontend && npm run dev
```

## 📋 Import API Client

```tsx
import api from "@/lib/api";
import type { Patient, Doctor, Appointment } from "@/lib/api";
```

## 🔐 Patient Portal - Quick Examples

### Register
```tsx
const result = await api.patient.register({
  name: "John Doe",
  email: "john@example.com",
  phone: "1234567890",
  dob: "1990-01-01",
  gender: "male"
});

localStorage.setItem("user_id", result.data.user_id);
```

### Login
```tsx
const result = await api.patient.login({
  email: "john@example.com",
  phone: "1234567890"
});

localStorage.setItem("user_id", result.data.user_id);
localStorage.setItem("user_name", result.data.user.name);
```

### Get Profile
```tsx
const userId = parseInt(localStorage.getItem("user_id") || "0");
const result = await api.patient.getProfile(userId);
// result.data = Patient object
```

### Get Greeting
```tsx
const result = await api.patient.getGreeting(userId);
console.log(result.data.greeting); // "Good morning, John!"
```

## 📅 Appointments - Quick Examples

### Get All Doctors
```tsx
const result = await api.doctor.getAll();
const doctors = result.data.doctors; // Doctor[]
```

### Check Availability
```tsx
const result = await api.doctor.getAvailability(
  doctorId,
  "2025-10-30"  // YYYY-MM-DD
);
const slots = result.data.available_slots; // TimeSlot[]
```

### Book Appointment
```tsx
const result = await api.appointment.book({
  user_id: parseInt(localStorage.getItem("user_id") || "0"),
  doctor_id: 1,
  date: "2025-10-30",
  time: "10:00",
  reason: "Checkup",
  sync_calendar: false
});

const appointmentId = result.data.appointment_id;
```

### Get My Appointments
```tsx
const result = await api.appointment.getByPatient(userId, true); // true = future only
const appointments = result.data.appointments; // Appointment[]
```

### Cancel Appointment
```tsx
await api.appointment.cancel(appointmentId);
```

## 💬 Chat - Quick Examples

### Send Message (REST)
```tsx
const result = await api.chat.sendMessage(userId, "What causes diabetes?");
const answer = result.data.answer;
const sources = result.data.sources; // optional
```

### WebSocket Chat
```tsx
const ws = api.chat.connectWebSocket(userId, (data) => {
  console.log("Received:", data);
  // Handle incoming message
});

ws.send("Hello!");
ws.close(); // when done
```

## 👨‍⚕️ Doctor Portal - Quick Examples

### Doctor Login
```tsx
const result = await api.doctor.login(1); // doctor_id
const doctor = result.data.doctor;
localStorage.setItem("doctor_id", doctor.doctor_id);
```

### Get Stats
```tsx
const result = await api.doctor.getStats(doctorId);
console.log(result.data.total_patients);
console.log(result.data.upcoming_appointments);
```

### Get Appointments
```tsx
const result = await api.doctor.getAppointments(doctorId, {
  date: "2025-10-30",
  status: "scheduled"
});
```

### Get Patients
```tsx
const result = await api.doctor.getPatients(doctorId);
const patients = result.data.patients;
```

### Add Notes
```tsx
await api.appointment.addNotes(
  appointmentId,
  "Patient shows improvement"
);
```

### Update Status
```tsx
await api.appointment.updateStatus(
  appointmentId,
  "completed"
);
```

### Get Analytics
```tsx
const result = await api.doctor.getAnalytics(doctorId, {
  start_date: "2025-10-01",
  end_date: "2025-10-31"
});
```

## 🎨 Error Handling Pattern

```tsx
try {
  setIsLoading(true);
  const result = await api.patient.login(credentials);
  
  if (result.success) {
    toast.success("Login successful!");
    // Handle success
  } else {
    toast.error(result.message || "Operation failed");
  }
} catch (error: any) {
  toast.error(error.message || "Something went wrong");
  console.error(error);
} finally {
  setIsLoading(false);
}
```

## 📦 Response Format

All API responses follow this pattern:

```typescript
{
  success: boolean;
  data?: any;      // Present on success
  message?: string; // Optional success message
  error?: string;  // Present on failure
}
```

## 🔗 Common URLs

- **Backend API**: `http://localhost:8000/api/v1`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Frontend**: `http://localhost:5173`

## 🔑 LocalStorage Keys

```tsx
localStorage.setItem("user_type", "patient" | "doctor");
localStorage.setItem("user_id", "123");
localStorage.setItem("user_name", "John Doe");
localStorage.setItem("user_email", "john@example.com");
localStorage.setItem("doctor_id", "1");
```

## 🧪 Test API from Terminal

```bash
# Health check
curl http://localhost:8000/health

# Register patient
curl -X POST http://localhost:8000/api/v1/patients/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","phone":"1234567890"}'

# Get doctors
curl http://localhost:8000/api/v1/doctors

# Check availability
curl "http://localhost:8000/api/v1/doctors/1/availability?date=2025-10-30"
```

## 📊 Data Types Reference

```typescript
interface Patient {
  user_id: number;
  name: string;
  email: string;
  phone: string;
  date_of_birth?: string;
  gender?: string;
}

interface Doctor {
  doctor_id: number;
  name: string;
  specialty: string;
  rating?: number;
}

interface Appointment {
  appointment_id: number;
  user_id: number;
  doctor_id: number;
  appointment_date: string; // YYYY-MM-DD
  start_time: string;       // HH:MM
  end_time: string;         // HH:MM
  status: 'scheduled' | 'completed' | 'cancelled' | 'no-show';
  reason?: string;
  notes?: string;
}

interface TimeSlot {
  start_time: string;
  end_time: string;
  duration: number; // minutes
}
```

---

**File**: Save as `/docs/API_QUICK_REFERENCE.md`
