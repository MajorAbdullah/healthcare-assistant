"""
Database Setup Script
Initializes the SQLite database with schema and seeds sample data
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import DATABASE_PATH, SAMPLE_DOCTORS

console = None
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    pass


def print_info(message, style="cyan"):
    """Print message with optional Rich formatting."""
    if console:
        console.print(message, style=style)
    else:
        print(message)


def create_database():
    """Create the database and tables."""
    print_info("\n🗄️  Creating database...", "bold cyan")
    
    # Ensure data directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Read schema
    schema_path = Path(__file__).parent / "db_schema.sql"
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Create database and execute schema
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Execute schema using executescript (handles multiple statements)
    cursor.executescript(schema_sql)
    
    conn.commit()
    print_info("  ✅ Database created successfully", "green")
    
    return conn


def seed_sample_doctors(conn):
    """Seed the database with sample doctors from config."""
    print_info("\n👨‍⚕️  Seeding sample doctors...", "bold cyan")
    
    cursor = conn.cursor()
    
    for doctor in SAMPLE_DOCTORS:
        cursor.execute("""
            INSERT INTO doctors (name, specialty, email, phone, calendar_id, consultation_duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            doctor['name'],
            doctor.get('specialization', 'General Medicine'),
            doctor.get('email', f"{doctor['name'].lower().replace(' ', '.')}@hospital.com"),
            doctor.get('phone', '555-0100'),
            doctor.get('calendar_id', ''),
            30  # 30-minute consultations
        ))
        
        doctor_id = cursor.lastrowid
        
        # Add weekly availability (Monday-Friday, 9 AM - 5 PM)
        for day in range(5):  # Monday to Friday
            # Morning session: 9 AM - 12 PM
            cursor.execute("""
                INSERT INTO doctor_availability (doctor_id, day_of_week, start_time, end_time)
                VALUES (?, ?, ?, ?)
            """, (doctor_id, day, '09:00', '12:00'))
            
            # Afternoon session: 1 PM - 5 PM
            cursor.execute("""
                INSERT INTO doctor_availability (doctor_id, day_of_week, start_time, end_time)
                VALUES (?, ?, ?, ?)
            """, (doctor_id, day, '13:00', '17:00'))
        
        print_info(f"  ✅ Added Dr. {doctor['name']} ({doctor.get('specialization', 'General Medicine')})", "green")
    
    conn.commit()
    print_info(f"\n  📊 Total doctors added: {len(SAMPLE_DOCTORS)}", "cyan")


def seed_sample_patients(conn):
    """Seed the database with sample patients."""
    print_info("\n👥 Seeding sample patients...", "bold cyan")
    
    cursor = conn.cursor()
    
    sample_patients = [
        {
            'name': 'John Doe',
            'email': 'john.doe@email.com',
            'phone': '555-0101',
            'date_of_birth': '1980-05-15'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@email.com',
            'phone': '555-0102',
            'date_of_birth': '1975-08-22'
        },
        {
            'name': 'Robert Johnson',
            'email': 'robert.j@email.com',
            'phone': '555-0103',
            'date_of_birth': '1992-03-10'
        },
        {
            'name': 'Maria Garcia',
            'email': 'maria.garcia@email.com',
            'phone': '555-0104',
            'date_of_birth': '1988-11-30'
        }
    ]
    
    for patient in sample_patients:
        cursor.execute("""
            INSERT INTO users (name, email, phone, date_of_birth)
            VALUES (?, ?, ?, ?)
        """, (
            patient['name'],
            patient['email'],
            patient['phone'],
            patient['date_of_birth']
        ))
        print_info(f"  ✅ Added patient: {patient['name']}", "green")
    
    conn.commit()
    print_info(f"\n  📊 Total patients added: {len(sample_patients)}", "cyan")


def seed_sample_appointments(conn):
    """Create a few sample appointments for testing."""
    print_info("\n📅 Seeding sample appointments...", "bold cyan")
    
    cursor = conn.cursor()
    
    # Get tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    next_week = datetime.now() + timedelta(days=7)
    
    sample_appointments = [
        {
            'user_id': 1,  # John Doe
            'doctor_id': 1,  # Dr. Sarah Johnson
            'appointment_date': tomorrow.strftime('%Y-%m-%d'),
            'start_time': '10:00',
            'end_time': '10:30',
            'reason': 'Follow-up consultation',
            'status': 'scheduled'
        },
        {
            'user_id': 2,  # Jane Smith
            'doctor_id': 2,  # Dr. Michael Chen
            'appointment_date': next_week.strftime('%Y-%m-%d'),
            'start_time': '14:00',
            'end_time': '14:30',
            'reason': 'Initial assessment',
            'status': 'scheduled'
        }
    ]
    
    for appt in sample_appointments:
        cursor.execute("""
            INSERT INTO appointments 
            (user_id, doctor_id, appointment_date, start_time, end_time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            appt['user_id'],
            appt['doctor_id'],
            appt['appointment_date'],
            appt['start_time'],
            appt['end_time'],
            appt['reason'],
            appt['status']
        ))
        print_info(f"  ✅ Added appointment for patient {appt['user_id']} with doctor {appt['doctor_id']}", "green")
    
    conn.commit()
    print_info(f"\n  📊 Total appointments added: {len(sample_appointments)}", "cyan")


def display_summary(conn):
    """Display database statistics."""
    cursor = conn.cursor()
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM doctors")
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments")
    appointment_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctor_availability")
    availability_count = cursor.fetchone()[0]
    
    if console:
        from rich.table import Table
        from rich import box
        
        table = Table(title="\n📊 Database Summary", box=box.ROUNDED)
        table.add_column("Table", style="cyan")
        table.add_column("Records", style="green")
        
        table.add_row("Doctors", str(doctor_count))
        table.add_row("Patients", str(user_count))
        table.add_row("Appointments", str(appointment_count))
        table.add_row("Availability Slots", str(availability_count))
        
        console.print(table)
    else:
        print(f"\n📊 Database Summary:")
        print(f"  Doctors: {doctor_count}")
        print(f"  Patients: {user_count}")
        print(f"  Appointments: {appointment_count}")
        print(f"  Availability Slots: {availability_count}")


def main():
    """Main setup function."""
    if console:
        panel = Panel(
            "[bold cyan]Healthcare Database Setup[/bold cyan]\n\n"
            "This script will create the SQLite database and seed it with sample data.",
            border_style="cyan"
        )
        console.print(panel)
    else:
        print("\n=== Healthcare Database Setup ===\n")
    
    try:
        # Create database
        conn = create_database()
        
        # Seed data
        seed_sample_doctors(conn)
        seed_sample_patients(conn)
        seed_sample_appointments(conn)
        
        # Display summary
        display_summary(conn)
        
        # Close connection
        conn.close()
        
        print_info("\n✅ Database setup complete!", "bold green")
        print_info(f"📁 Database location: {DATABASE_PATH}", "dim")
        
    except Exception as e:
        print_info(f"\n❌ Error during setup: {e}", "bold red")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
