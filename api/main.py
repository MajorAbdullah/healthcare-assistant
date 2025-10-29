"""
Healthcare Assistant - FastAPI Backend
Provides REST API endpoints for Patient and Doctor portals
Runs locally on device (no external dependencies)
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date, timedelta
import pytz
import json
import sys
import os

# Set Pakistan/Asia timezone
PAKISTAN_TZ = pytz.timezone('Asia/Karachi')

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.scheduler import AppointmentScheduler
from modules.rag_engine import RAGEngine
from modules.memory_manager import MemoryManager
from modules.calendar_integration import CalendarIntegration

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Assistant API",
    description="Local REST API for Patient and Doctor portals",
    version="1.0.0"
)

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vite alternative port
        "http://localhost:8081",  # Vite alternative port 2
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core modules
# Get the correct database path (parent directory)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'healthcare.db')

scheduler = AppointmentScheduler()
calendar_integration = CalendarIntegration(scheduler)
memory_manager = MemoryManager(db_path=DB_PATH)

# RAG Engine (lazy loading to avoid startup delay)
rag_engine = None

def get_rag_engine():
    global rag_engine
    if rag_engine is None:
        try:
            # Import config for API key and settings
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from config import GOOGLE_API_KEY, LLM_MODEL, CHROMA_COLLECTION_NAME, VECTOR_DB_DIR, RAG_SYSTEM_PROMPT
            
            if not GOOGLE_API_KEY:
                print("Warning: GOOGLE_API_KEY not set in environment")
                return None
            
            # Use the same vector DB path as the main app
            rag_engine = RAGEngine(
                collection_name=CHROMA_COLLECTION_NAME,
                persist_directory=str(VECTOR_DB_DIR),
                api_key=GOOGLE_API_KEY,
                model_name=LLM_MODEL,
                system_prompt=RAG_SYSTEM_PROMPT
            )
            print(f"✓ RAG Engine initialized with {rag_engine.collection.count()} documents")
        except Exception as e:
            print(f"Warning: RAG engine not initialized - {e}")
            import traceback
            traceback.print_exc()
            return None
    return rag_engine


# ============================================
# PYDANTIC MODELS (Request/Response schemas)
# ============================================

class PatientRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    dob: Optional[str] = None
    gender: Optional[str] = None

class PatientLogin(BaseModel):
    email: EmailStr
    phone: str

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None

class AppointmentBook(BaseModel):
    user_id: int
    doctor_id: int
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    reason: Optional[str] = None
    sync_calendar: bool = True  # Default to True - sync appointments to Google Calendar

class MedicalNote(BaseModel):
    notes: str

class ChatMessage(BaseModel):
    user_id: int
    message: str

class DoctorLogin(BaseModel):
    doctor_id: int

class PreferencesUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    sms_reminders: Optional[bool] = None
    auto_sync_calendar: Optional[bool] = None


# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_db_connection():
    """Get database connection from scheduler"""
    return scheduler._get_connection()

def format_datetime(date_str: str, time_str: str) -> str:
    """Combine date and time into readable format"""
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return f"{date_str} at {time_str}"


# ============================================
# PATIENT PORTAL ENDPOINTS
# ============================================

@app.post("/api/v1/patients/register")
async def register_patient(patient: PatientRegister):
    """Register a new patient"""
    try:
        user_id = scheduler.get_or_create_patient(
            name=patient.name,
            email=patient.email,
            phone=patient.phone
        )
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "name": patient.name
            },
            "message": "Registration successful!"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/patients/login")
async def login_patient(credentials: PatientLogin):
    """Login existing patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, name, email, phone, created_at
            FROM users
            WHERE email = ? AND phone = ?
        ''', (credentials.email, credentials.phone))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Please check your email and phone number.")
        
        return {
            "success": True,
            "data": {
                "user_id": user['user_id'],
                "name": user['name'],
                "email": user['email'],
                "phone": user['phone'],
                "token": f"patient_{user['user_id']}"  # Simple token for prototype
            },
            "message": "Login successful!"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patients/{user_id}")
async def get_patient(user_id: int):
    """Get patient details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, name, email, phone, created_at
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Get appointment statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'scheduled' THEN 1 ELSE 0 END) as upcoming,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM appointments
            WHERE user_id = ?
        ''', (user_id,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "user_id": user['user_id'],
                "name": user['name'],
                "email": user['email'],
                "phone": user['phone'],
                "created_at": user['created_at'],
                "stats": {
                    "total_appointments": stats['total'] or 0,
                    "upcoming_appointments": stats['upcoming'] or 0,
                    "completed_appointments": stats['completed'] or 0
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/patients/{user_id}")
async def update_patient(user_id: int, updates: PatientUpdate):
    """Update patient information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        if updates.name:
            update_fields.append("name = ?")
            values.append(updates.name)
        if updates.email:
            update_fields.append("email = ?")
            values.append(updates.email)
        if updates.phone:
            update_fields.append("phone = ?")
            values.append(updates.phone)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Profile updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patients/{user_id}/greeting")
async def get_patient_greeting(user_id: int):
    """Get personalized greeting and upcoming appointment"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user name
        cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Get current time in Pakistan timezone
        now_pakistan = datetime.now(PAKISTAN_TZ)
        today_pakistan = now_pakistan.date().strftime('%Y-%m-%d')
        current_time = now_pakistan.time().strftime('%H:%M')
        
        # Get next upcoming appointment
        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ? AND a.status = 'scheduled'
            AND (a.appointment_date > ? OR 
                 (a.appointment_date = ? AND a.start_time > ?))
            ORDER BY a.appointment_date, a.start_time
            LIMIT 1
        ''', (user_id, today_pakistan, today_pakistan, current_time))
        
        upcoming = cursor.fetchone()
        conn.close()
        
        # Generate greeting using Pakistan timezone
        hour = now_pakistan.hour
        if hour < 12:
            time_greeting = "Good morning"
        elif hour < 17:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        greeting = f"{time_greeting}, {user['name']}!"
        
        upcoming_info = None
        if upcoming:
            # Check if appointment is tomorrow
            appt_date = datetime.strptime(upcoming['appointment_date'], "%Y-%m-%d").date()
            today = now_pakistan.date()
            
            if appt_date == today:
                when = "today"
            elif appt_date == today + timedelta(days=1):
                when = "tomorrow"
            else:
                when = appt_date.strftime("%B %d")
            
            upcoming_info = {
                "appointment_id": upcoming['appointment_id'],
                "when": when,
                "time": upcoming['start_time'],
                "doctor_name": upcoming['doctor_name'],
                "specialty": upcoming['specialty'],
                "message": f"You have an appointment {when} at {upcoming['start_time']} with {upcoming['doctor_name']}"
            }
        
        return {
            "success": True,
            "data": {
                "greeting": greeting,
                "upcoming_appointment": upcoming_info
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors")
async def get_all_doctors():
    """Get list of all doctors"""
    try:
        doctors = scheduler.get_all_doctors()
        
        # Get appointment count for each doctor
        conn = get_db_connection()
        cursor = conn.cursor()
        
        doctors_with_stats = []
        for doctor in doctors:
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM appointments
                WHERE doctor_id = ? AND status = 'scheduled'
            ''', (doctor['doctor_id'],))
            
            count = cursor.fetchone()['count']
            
            doctors_with_stats.append({
                "doctor_id": doctor['doctor_id'],
                "name": doctor['name'],
                "specialty": doctor['specialty'],
                "active_appointments": count
            })
        
        conn.close()
        
        return {
            "success": True,
            "data": doctors_with_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors/{doctor_id}/availability")
async def get_doctor_availability(doctor_id: int, date: str):
    """Get available time slots for a doctor on a specific date"""
    try:
        # Validate date format
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Use scheduler's method
        available_slots = scheduler.get_doctor_availability(doctor_id, date_obj)
        
        # Format slots for frontend (just return start times)
        slot_times = [slot['start_time'] for slot in available_slots]
        
        return {
            "success": True,
            "data": {
                "date": date,
                "doctor_id": doctor_id,
                "available_slots": slot_times,
                "total_slots": len(slot_times)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/appointments")
async def book_appointment(booking: AppointmentBook):
    """Book a new appointment"""
    try:
        # Use calendar integration if sync_calendar is True (default), otherwise use scheduler directly
        if booking.sync_calendar:
            success, message, appointment_id = await calendar_integration.book_appointment_with_calendar_async(
                user_id=booking.user_id,
                doctor_id=booking.doctor_id,
                appointment_date=booking.date,
                start_time=booking.time,
                reason=booking.reason,
                create_calendar_event=True
            )
        else:
            success, message, appointment_id = scheduler.book_appointment(
                user_id=booking.user_id,
                doctor_id=booking.doctor_id,
                appointment_date=booking.date,
                start_time=booking.time,
                reason=booking.reason
            )
        
        if not success or not appointment_id:
            raise HTTPException(status_code=400, detail=message or "Unable to book appointment. Time slot may be unavailable.")
        
        # Get the created appointment details
        appointment = scheduler.get_appointment(appointment_id)
        calendar_event_id = appointment.get('calendar_event_id') if appointment else None
        
        return {
            "success": True,
            "data": {
                "appointment_id": appointment_id,
                "date": booking.date,
                "time": booking.time,
                "calendar_event_id": calendar_event_id
            },
            "message": "Appointment booked successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/appointments/{user_id}")
async def get_patient_appointments(user_id: int, limit: Optional[int] = None, status: Optional[str] = None):
    """Get all appointments for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT a.*, d.name as doctor_name, d.specialty as doctor_specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ?
        '''
        
        params = [user_id]
        
        if status:
            query += ' AND a.status = ?'
            params.append(status)
        
        query += ' ORDER BY a.appointment_date DESC, a.start_time DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        cursor.execute(query, params)
        appointments = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "data": [dict(appt) for appt in appointments]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/appointments/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: int):
    """Cancel an appointment"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments
            SET status = 'cancelled'
            WHERE appointment_id = ?
        ''', (appointment_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Appointment cancelled successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chat")
async def chat_with_ai(message: ChatMessage):
    """Chat with medical AI assistant (REST alternative to WebSocket)"""
    try:
        rag = get_rag_engine()
        
        if not rag:
            raise HTTPException(status_code=503, detail="AI assistant not available. Please configure GOOGLE_API_KEY.")
        
        # Save user message
        memory_manager.save_conversation(
            user_id=message.user_id,
            role="user",
            message=message.message
        )
        
        # Get AI response using RAG query method
        result = rag.query(message.message, n_results=5, verbose=False)
        response_text = result.get('answer', 'I apologize, but I encountered an error.')
        
        # Save assistant response
        memory_manager.save_conversation(
            user_id=message.user_id,
            role="assistant",
            message=response_text
        )
        
        return {
            "success": True,
            "data": {
                "answer": response_text,
                "citations": result.get('citations', []),
                "timestamp": datetime.now().isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.get("/api/v1/patients/{user_id}/preferences")
async def get_preferences(user_id: int):
    """Get patient preferences"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT email_notifications, sms_reminders, calendar_sync
            FROM user_preferences
            WHERE user_id = ?
        ''', (user_id,))
        
        prefs = cursor.fetchone()
        conn.close()
        
        if not prefs:
            # Return defaults if not set
            return {
                "success": True,
                "data": {
                    "email_notifications": True,
                    "sms_reminders": True,
                    "auto_sync_calendar": False
                }
            }
        
        return {
            "success": True,
            "data": {
                "email_notifications": bool(prefs['email_notifications']),
                "sms_reminders": bool(prefs['sms_reminders']),
                "auto_sync_calendar": bool(prefs['calendar_sync'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/patients/{user_id}/preferences")
async def update_preferences(user_id: int, prefs: PreferencesUpdate):
    """Update patient preferences"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if preferences exist
        cursor.execute('SELECT user_id FROM user_preferences WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update
            updates = []
            values = []
            
            if prefs.email_notifications is not None:
                updates.append("email_notifications = ?")
                values.append(int(prefs.email_notifications))
            if prefs.sms_reminders is not None:
                updates.append("sms_reminders = ?")
                values.append(int(prefs.sms_reminders))
            if prefs.auto_sync_calendar is not None:
                updates.append("calendar_sync = ?")
                values.append(int(prefs.auto_sync_calendar))
            
            if updates:
                values.append(user_id)
                cursor.execute(f"UPDATE user_preferences SET {', '.join(updates)} WHERE user_id = ?", values)
        else:
            # Insert
            cursor.execute('''
                INSERT INTO user_preferences (user_id, email_notifications, sms_reminders, calendar_sync)
                VALUES (?, ?, ?, ?)
            ''', (
                user_id,
                int(prefs.email_notifications if prefs.email_notifications is not None else True),
                int(prefs.sms_reminders if prefs.sms_reminders is not None else True),
                int(prefs.auto_sync_calendar if prefs.auto_sync_calendar is not None else False)
            ))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Preferences updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# DOCTOR PORTAL ENDPOINTS
# ============================================

@app.post("/api/v1/doctors/login")
async def doctor_login(credentials: DoctorLogin):
    """Doctor login"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT doctor_id, name, specialty, calendar_id
            FROM doctors
            WHERE doctor_id = ?
        ''', (credentials.doctor_id,))
        
        doctor = cursor.fetchone()
        conn.close()
        
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        return {
            "success": True,
            "data": {
                "doctor_id": doctor['doctor_id'],
                "name": doctor['name'],
                "specialty": doctor['specialty'],
                "token": f"doctor_{doctor['doctor_id']}"
            },
            "message": f"Welcome, {doctor['name']}!"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors/{doctor_id}/stats")
async def get_doctor_stats(doctor_id: int):
    """Get doctor dashboard statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get Pakistan time
        now_pakistan = datetime.now(PAKISTAN_TZ)
        today_pakistan = now_pakistan.date().strftime('%Y-%m-%d')
        
        # Calculate week start (Monday) in Pakistan timezone
        days_since_monday = now_pakistan.weekday()
        week_start = (now_pakistan.date() - timedelta(days=days_since_monday)).strftime('%Y-%m-%d')
        week_end = today_pakistan
        
        # Today's appointments
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date = ?
        ''', (doctor_id, today_pakistan))
        today_count = cursor.fetchone()['count']
        
        # Total patients
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) as count
            FROM appointments
            WHERE doctor_id = ?
        ''', (doctor_id,))
        total_patients = cursor.fetchone()['count']
        
        # This week's appointments
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? 
            AND appointment_date >= ?
            AND appointment_date <= ?
        ''', (doctor_id, week_start, week_end))
        week_count = cursor.fetchone()['count']
        
        # Completion rate
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM appointments
            WHERE doctor_id = ?
        ''', (doctor_id,))
        
        stats = cursor.fetchone()
        total = stats['total']
        completed = stats['completed'] or 0
        completion_rate = round((completed / total * 100) if total > 0 else 0, 1)
        
        conn.close()
        
        return {
            "success": True,
            "data": {
                "today_count": today_count,
                "total_patients": total_patients,
                "week_count": week_count,
                "completion_rate": completion_rate
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors/{doctor_id}/appointments")
async def get_doctor_appointments(
    doctor_id: int,
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get doctor's appointments (today, specific date, or date range)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get today's date in Pakistan timezone
        today_pakistan = datetime.now(PAKISTAN_TZ).date().strftime('%Y-%m-%d')
        
        query = '''
            SELECT a.*, u.name as patient_name, u.email as patient_email, u.phone as patient_phone
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.doctor_id = ?
        '''
        
        params = [doctor_id]
        
        if date == "today":
            query += " AND a.appointment_date = ?"
            params.append(today_pakistan)
        elif date:
            query += " AND a.appointment_date = ?"
            params.append(date)
        elif start_date and end_date:
            query += " AND a.appointment_date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        
        query += " ORDER BY a.appointment_date, a.start_time"
        
        cursor.execute(query, params)
        appointments = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "appointments": [dict(appt) for appt in appointments]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors/{doctor_id}/patients")
async def get_doctor_patients(
    doctor_id: int,
    search: Optional[str] = None,
    sort: Optional[str] = "name",
    page: int = 1,
    per_page: int = 20
):
    """Get all patients for a doctor with pagination"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query
        query = '''
            SELECT DISTINCT
                u.user_id,
                u.name,
                u.email,
                u.phone,
                COUNT(a.appointment_id) as total_visits,
                MAX(a.appointment_date) as last_visit
            FROM users u
            JOIN appointments a ON u.user_id = a.user_id
            WHERE a.doctor_id = ?
        '''
        
        params = [doctor_id]
        
        if search:
            query += " AND (u.name LIKE ? OR u.email LIKE ? OR u.phone LIKE ?)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])
        
        query += " GROUP BY u.user_id, u.name, u.email, u.phone"
        
        # Add sorting
        if sort == "name":
            query += " ORDER BY u.name"
        elif sort == "last_visit":
            query += " ORDER BY last_visit DESC"
        elif sort == "total_visits":
            query += " ORDER BY total_visits DESC"
        
        # Get total count
        cursor.execute(query, params)
        all_patients = cursor.fetchall()
        total_count = len(all_patients)
        
        # Apply pagination
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"
        
        cursor.execute(query, params)
        patients = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "data": {
                "patients": [dict(p) for p in patients],
                "total_count": total_count,
                "pages": (total_count + per_page - 1) // per_page,
                "current_page": page
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patients/{patient_id}/appointments")
async def get_patient_history(patient_id: int):
    """Get complete appointment history for a patient"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ?
            ORDER BY a.appointment_date DESC, a.start_time DESC
        ''', (patient_id,))
        
        appointments = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "data": [dict(appt) for appt in appointments]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/appointments/{appointment_id}/notes")
async def add_medical_notes(appointment_id: int, note: MedicalNote):
    """Add or update medical notes for an appointment"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments
            SET notes = ?
            WHERE appointment_id = ?
        ''', (note.notes, appointment_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Medical notes saved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/v1/appointments/{appointment_id}/notes")
async def update_medical_notes(appointment_id: int, note: MedicalNote):
    """Update medical notes (same as add)"""
    return await add_medical_notes(appointment_id, note)


@app.put("/api/v1/appointments/{appointment_id}/status")
async def update_appointment_status(appointment_id: int, status: str):
    """Update appointment status (completed, cancelled, etc.)"""
    try:
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments
            SET status = ?
            WHERE appointment_id = ?
        ''', (status, appointment_id))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Appointment marked as {status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctors/{doctor_id}/analytics")
async def get_doctor_analytics(
    doctor_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get analytics data for doctor dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Default to last 30 days if not specified
        if not start_date:
            start_date = (date.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = date.today().strftime("%Y-%m-%d")
        
        # Total appointments in period
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
        ''', (doctor_id, start_date, end_date))
        total_appointments = cursor.fetchone()['count']
        
        # Total unique patients
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
        ''', (doctor_id, start_date, end_date))
        total_patients = cursor.fetchone()['count']
        
        # Status breakdown
        cursor.execute('''
            SELECT 
                status,
                COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
            GROUP BY status
        ''', (doctor_id, start_date, end_date))
        
        status_breakdown = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Calculate completion rate
        completed = status_breakdown.get('completed', 0)
        completion_rate = round((completed / total_appointments * 100) if total_appointments > 0 else 0, 1)
        
        # Daily breakdown
        cursor.execute('''
            SELECT 
                appointment_date,
                COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
            GROUP BY appointment_date
            ORDER BY appointment_date
        ''', (doctor_id, start_date, end_date))
        
        daily_breakdown = [{"date": row['appointment_date'], "count": row['count']} for row in cursor.fetchall()]
        
        # Weekly breakdown (day of week)
        cursor.execute('''
            SELECT 
                CASE cast(strftime('%w', appointment_date) as integer)
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END as day_name,
                COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
            GROUP BY strftime('%w', appointment_date)
            ORDER BY strftime('%w', appointment_date)
        ''', (doctor_id, start_date, end_date))
        
        weekly_breakdown = {row['day_name']: row['count'] for row in cursor.fetchall()}
        
        # Patient growth (unique patients per week)
        cursor.execute('''
            SELECT 
                strftime('%Y-%W', appointment_date) as week,
                COUNT(DISTINCT user_id) as count
            FROM appointments
            WHERE doctor_id = ? AND appointment_date BETWEEN ? AND ?
            GROUP BY strftime('%Y-%W', appointment_date)
            ORDER BY week
        ''', (doctor_id, start_date, end_date))
        
        patient_growth = [{"week": row['week'], "count": row['count']} for row in cursor.fetchall()]
        
        # Average appointments per day
        days_in_period = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
        avg_daily = round(total_appointments / days_in_period, 1) if days_in_period > 0 else 0
        
        conn.close()
        
        return {
            "success": True,
            "data": {
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "total_appointments": total_appointments,
                "total_patients": total_patients,
                "avg_daily_appointments": avg_daily,
                "completion_rate": completion_rate,
                "status_breakdown": status_breakdown,
                "daily_breakdown": daily_breakdown,
                "weekly_breakdown": weekly_breakdown,
                "patient_growth": patient_growth
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# WEBSOCKET FOR REAL-TIME CHAT
# ============================================

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    try:
        rag = get_rag_engine()
        
        if not rag:
            await websocket.send_json({
                "error": "AI assistant not available. Please configure GOOGLE_API_KEY.",
                "timestamp": datetime.now().isoformat()
            })
            await websocket.close()
            return
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            # Save user message
            memory_manager.save_conversation(
                user_id=user_id,
                role="user",
                message=user_message
            )
            
            # Get AI response using RAG query method
            result = rag.query(user_message, n_results=5, verbose=False)
            response_text = result.get('answer', 'I apologize, but I encountered an error.')
            
            # Save assistant response
            memory_manager.save_conversation(
                user_id=user_id,
                role="assistant",
                message=response_text
            )
            
            # Send response back to client
            await websocket.send_json({
                "content": response_text,
                "citations": result.get('citations', []),
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.send_json({
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        except:
            pass
        await websocket.close()


# ============================================
# HEALTH CHECK & INFO
# ============================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🏥 Healthcare Assistant API Starting...")
    print("="*60)
    print(f"📡 API Server: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🔌 WebSocket: ws://localhost:8000/ws/chat/{{user_id}}")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
