"""
Appointment Scheduler Module
Handles appointment booking, cancellation, availability checking, and conflict detection
"""

import sqlite3
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATABASE_PATH
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


class AppointmentScheduler:
    """Manages doctor appointments with conflict detection and calendar integration."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the scheduler.
        
        Args:
            db_path: Path to SQLite database (uses config default if not provided)
        """
        self.db_path = db_path or DATABASE_PATH
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure database file exists."""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(
                f"Database not found at {self.db_path}. "
                "Run 'python3 db_setup.py' first to create it."
            )
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    # ==================== DOCTOR MANAGEMENT ====================
    
    def get_all_doctors(self) -> List[Dict]:
        """Get all doctors in the system."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT doctor_id, name, specialty, email,
                   calendar_id, consultation_duration
            FROM doctors
            ORDER BY name
        """)
        
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return doctors
    
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Dict]:
        """Get doctor details by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT doctor_id, name, specialty, email,
                   calendar_id, consultation_duration
            FROM doctors
            WHERE doctor_id = ?
        """, (doctor_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_doctors_by_specialty(self, specialty: str) -> List[Dict]:
        """Get all doctors with a specific specialty."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT doctor_id, name, specialty, email,
                   calendar_id, consultation_duration
            FROM doctors
            WHERE specialty LIKE ?
            ORDER BY name
        """, (f'%{specialty}%',))
        
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return doctors
    
    # ==================== PATIENT MANAGEMENT ====================
    
    def get_or_create_patient(self, name: str, email: str, password_hash: str = None) -> int:
        """
        Get existing patient or create new one.

        Returns:
            user_id of the patient
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Try to find existing patient by email
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            user_id = row['user_id']
        else:
            # Create new patient
            cursor.execute("""
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
            """, (name, email, password_hash))
            user_id = cursor.lastrowid
            conn.commit()

        conn.close()
        return user_id
    
    def get_patient_by_id(self, user_id: int) -> Optional[Dict]:
        """Get patient details by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, name, email, date_of_birth
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # ==================== AVAILABILITY CHECKING ====================
    
    def get_doctor_availability(self, doctor_id: int, date: datetime.date) -> List[Dict]:
        """
        Get doctor's availability slots for a specific date.
        
        Returns:
            List of available time slots
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get day of week (0=Monday, 6=Sunday)
        day_of_week = date.weekday()
        
        # Get doctor's general availability for this day
        cursor.execute("""
            SELECT start_time, end_time
            FROM doctor_availability
            WHERE doctor_id = ? AND day_of_week = ? AND is_active = 1
        """, (doctor_id, day_of_week))
        
        availability_slots = cursor.fetchall()
        
        if not availability_slots:
            conn.close()
            return []
        
        # Get existing appointments for this date
        cursor.execute("""
            SELECT start_time, end_time
            FROM appointments
            WHERE doctor_id = ? AND appointment_date = ? 
                  AND status IN ('scheduled', 'confirmed')
        """, (doctor_id, date.strftime('%Y-%m-%d')))
        
        booked_slots = cursor.fetchall()
        conn.close()
        
        # Get consultation duration
        doctor = self.get_doctor_by_id(doctor_id)
        duration = doctor['consultation_duration']
        
        # Generate available slots
        available_slots = []
        
        for avail in availability_slots:
            start = datetime.strptime(avail['start_time'], '%H:%M').time()
            end = datetime.strptime(avail['end_time'], '%H:%M').time()
            
            # Generate slots within this availability window
            current = datetime.combine(date, start)
            end_datetime = datetime.combine(date, end)
            
            while current + timedelta(minutes=duration) <= end_datetime:
                slot_start = current.time()
                slot_end = (current + timedelta(minutes=duration)).time()
                
                # Check if this slot conflicts with existing appointments
                is_available = True
                for booked in booked_slots:
                    booked_start = datetime.strptime(booked['start_time'], '%H:%M').time()
                    booked_end = datetime.strptime(booked['end_time'], '%H:%M').time()
                    
                    # Check for overlap
                    if not (slot_end <= booked_start or slot_start >= booked_end):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'start_time': slot_start.strftime('%H:%M'),
                        'end_time': slot_end.strftime('%H:%M'),
                        'duration': duration
                    })
                
                current += timedelta(minutes=duration)
        
        return available_slots
    
    def check_conflict(self, doctor_id: int, appointment_date: str, 
                      start_time: str, end_time: str, 
                      exclude_appointment_id: int = None) -> bool:
        """
        Check if a time slot conflicts with existing appointments.
        
        Returns:
            True if there's a conflict, False if slot is available
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT COUNT(*) as count
            FROM appointments
            WHERE doctor_id = ? 
                AND appointment_date = ?
                AND status IN ('scheduled', 'confirmed')
                AND NOT (end_time <= ? OR start_time >= ?)
        """
        
        params = [doctor_id, appointment_date, start_time, end_time]
        
        if exclude_appointment_id:
            query += " AND appointment_id != ?"
            params.append(exclude_appointment_id)
        
        cursor.execute(query, params)
        count = cursor.fetchone()['count']
        conn.close()
        
        return count > 0
    
    # ==================== APPOINTMENT BOOKING ====================
    
    def book_appointment(self, user_id: int, doctor_id: int,
                        appointment_date: str, start_time: str,
                        reason: str = None, notes: str = None) -> Tuple[bool, str, Optional[int]]:
        """
        Book a new appointment.
        
        Args:
            user_id: Patient user ID
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            reason: Reason for visit
            notes: Additional notes
            
        Returns:
            Tuple of (success, message, appointment_id)
        """
        # Get doctor info for consultation duration
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return False, f"Doctor with ID {doctor_id} not found", None
        
        # Calculate end time
        start_dt = datetime.strptime(start_time, '%H:%M')
        end_dt = start_dt + timedelta(minutes=doctor['consultation_duration'])
        end_time = end_dt.strftime('%H:%M')
        
        # Check for conflicts
        if self.check_conflict(doctor_id, appointment_date, start_time, end_time):
            return False, "Time slot is already booked", None
        
        # Book the appointment
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO appointments 
                (user_id, doctor_id, appointment_date, start_time, end_time, reason, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled')
            """, (user_id, doctor_id, appointment_date, start_time, end_time, reason, notes))
            
            appointment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "Appointment booked successfully", appointment_id
            
        except Exception as e:
            conn.close()
            return False, f"Error booking appointment: {e}", None
    
    # ==================== APPOINTMENT MANAGEMENT ====================
    
    def get_appointment(self, appointment_id: int) -> Optional[Dict]:
        """Get appointment details by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.*, 
                   u.name as patient_name, u.email as patient_email,
                   d.name as doctor_name, d.specialty as doctor_specialty
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = ?
        """, (appointment_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_patient_appointments(self, user_id: int, 
                                 status: str = None,
                                 future_only: bool = True) -> List[Dict]:
        """Get all appointments for a patient."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT a.*, d.name as doctor_name, d.specialty as doctor_specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ?
        """
        params = [user_id]
        
        if status:
            query += " AND a.status = ?"
            params.append(status)
        
        if future_only:
            query += " AND a.appointment_date >= date('now')"
        
        query += " ORDER BY a.appointment_date, a.start_time"
        
        cursor.execute(query, params)
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return appointments
    
    def get_doctor_appointments(self, doctor_id: int,
                               date: str = None,
                               status: str = None) -> List[Dict]:
        """Get all appointments for a doctor."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT a.*, u.name as patient_name, u.email as patient_email
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.doctor_id = ?
        """
        params = [doctor_id]
        
        if date:
            query += " AND a.appointment_date = ?"
            params.append(date)
        
        if status:
            query += " AND a.status = ?"
            params.append(status)
        
        query += " ORDER BY a.appointment_date, a.start_time"
        
        cursor.execute(query, params)
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return appointments
    
    def cancel_appointment(self, appointment_id: int, reason: str = None) -> Tuple[bool, str]:
        """
        Cancel an appointment.
        
        Returns:
            Tuple of (success, message)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if appointment exists
            cursor.execute("SELECT status FROM appointments WHERE appointment_id = ?", 
                          (appointment_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return False, "Appointment not found"
            
            if row['status'] == 'cancelled':
                conn.close()
                return False, "Appointment is already cancelled"
            
            # Update status
            cursor.execute("""
                UPDATE appointments 
                SET status = 'cancelled', notes = COALESCE(notes || '\n' || ?, ?)
                WHERE appointment_id = ?
            """, (f"Cancellation reason: {reason}" if reason else None, 
                  f"Cancellation reason: {reason}" if reason else "Cancelled",
                  appointment_id))
            
            conn.commit()
            conn.close()
            
            return True, "Appointment cancelled successfully"
            
        except Exception as e:
            conn.close()
            return False, f"Error cancelling appointment: {e}"
    
    def confirm_appointment(self, appointment_id: int) -> Tuple[bool, str]:
        """Confirm an appointment."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE appointments 
                SET status = 'confirmed'
                WHERE appointment_id = ? AND status = 'scheduled'
            """, (appointment_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Appointment not found or already confirmed/cancelled"
            
            conn.commit()
            conn.close()
            
            return True, "Appointment confirmed"
            
        except Exception as e:
            conn.close()
            return False, f"Error confirming appointment: {e}"
    
    # ==================== DISPLAY HELPERS ====================
    
    def display_doctors(self, doctors: List[Dict]) -> None:
        """Display doctors in a formatted table."""
        if not doctors:
            console.print("No doctors found.", style="yellow")
            return
        
        table = Table(title="👨‍⚕️ Available Doctors", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Specialty", style="yellow")
        table.add_column("Email", style="dim")
        
        for doc in doctors:
            table.add_row(
                str(doc['doctor_id']),
                doc['name'],
                doc['specialty'],
                doc['email']
            )
        
        console.print(table)
    
    def display_appointments(self, appointments: List[Dict], title: str = "Appointments") -> None:
        """Display appointments in a formatted table."""
        if not appointments:
            console.print("No appointments found.", style="yellow")
            return
        
        table = Table(title=f"📅 {title}", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Time", style="yellow")
        table.add_column("Doctor/Patient", style="white")
        table.add_column("Status", style="magenta")
        
        for appt in appointments:
            # Determine display name based on available fields
            if 'doctor_name' in appt:
                other_party = appt['doctor_name']
            elif 'patient_name' in appt:
                other_party = appt['patient_name']
            else:
                other_party = "N/A"
            
            table.add_row(
                str(appt['appointment_id']),
                appt['appointment_date'],
                f"{appt['start_time']} - {appt['end_time']}",
                other_party,
                appt['status']
            )
        
        console.print(table)
    
    def display_available_slots(self, slots: List[Dict], doctor_name: str = None) -> None:
        """Display available appointment slots."""
        if not slots:
            console.print("No available slots found.", style="yellow")
            return
        
        title = f"🕒 Available Slots"
        if doctor_name:
            title += f" - {doctor_name}"
        
        table = Table(title=title, box=box.ROUNDED)
        table.add_column("Slot #", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Time", style="yellow")
        table.add_column("Duration", style="dim")
        
        for i, slot in enumerate(slots, 1):
            table.add_row(
                str(i),
                slot['date'],
                f"{slot['start_time']} - {slot['end_time']}",
                f"{slot['duration']} min"
            )
        
        console.print(table)
