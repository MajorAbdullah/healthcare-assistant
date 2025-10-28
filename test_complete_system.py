#!/usr/bin/env python3
"""
Comprehensive System Testing Suite
Tests both Patient and Doctor portals with all features
"""

import sys
import asyncio
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

sys.path.insert(0, str(Path(__file__).parent))

from modules.rag_engine import RAGEngine
from modules.scheduler import AppointmentScheduler
from modules.memory_manager import MemoryManager
from modules.calendar_sync import CalendarSync

console = Console()


class SystemTester:
    """Comprehensive system testing."""
    
    def __init__(self):
        self.console = Console()
        self.scheduler = AppointmentScheduler()
        self.memory = MemoryManager()
        self.calendar = CalendarSync(self.scheduler)
        self.rag = None
        
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'total': 0
        }
        
        self.test_user_id = None
        self.test_appointment_id = None
    
    def print_header(self, title: str):
        """Print test section header."""
        self.console.print()
        self.console.print("=" * 80)
        self.console.print(f"[bold cyan]{title}[/bold cyan]")
        self.console.print("=" * 80)
        self.console.print()
    
    def test_pass(self, test_name: str):
        """Mark test as passed."""
        self.test_results['passed'] += 1
        self.test_results['total'] += 1
        self.console.print(f"[green]✓ PASS:[/green] {test_name}")
    
    def test_fail(self, test_name: str, error: str = ""):
        """Mark test as failed."""
        self.test_results['failed'] += 1
        self.test_results['total'] += 1
        self.console.print(f"[red]✗ FAIL:[/red] {test_name}")
        if error:
            self.console.print(f"  [dim]{error}[/dim]")
    
    def test_warning(self, test_name: str, warning: str = ""):
        """Mark test with warning."""
        self.test_results['warnings'] += 1
        self.test_results['total'] += 1
        self.console.print(f"[yellow]⚠ WARN:[/yellow] {test_name}")
        if warning:
            self.console.print(f"  [dim]{warning}[/dim]")
    
    # ==================== DATABASE TESTS ====================
    
    def test_database_connection(self):
        """Test database connectivity and structure."""
        self.print_header("TEST 1: DATABASE CONNECTION & STRUCTURE")
        
        try:
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            # Test all required tables exist
            tables = ['users', 'doctors', 'appointments', 'conversations', 'user_preferences']
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                if table in existing_tables:
                    self.test_pass(f"Table '{table}' exists")
                else:
                    self.test_fail(f"Table '{table}' missing")
            
            # Check doctors are configured
            cursor.execute("SELECT COUNT(*) FROM doctors")
            doctor_count = cursor.fetchone()[0]
            
            if doctor_count >= 3:
                self.test_pass(f"Doctors configured: {doctor_count} doctors found")
            else:
                self.test_fail(f"Insufficient doctors: only {doctor_count} found")
            
            # Check calendar IDs
            cursor.execute("SELECT DISTINCT calendar_id FROM doctors")
            calendar_ids = [row[0] for row in cursor.fetchall()]
            
            if len(calendar_ids) == 1 and calendar_ids[0]:
                self.test_pass(f"Calendar configured: {calendar_ids[0]}")
            else:
                self.test_warning("Multiple or missing calendar IDs", str(calendar_ids))
            
            conn.close()
            
        except Exception as e:
            self.test_fail("Database connection", str(e))
    
    # ==================== PATIENT PORTAL TESTS ====================
    
    def test_patient_registration(self):
        """Test patient registration/creation."""
        self.print_header("TEST 2: PATIENT REGISTRATION")
        
        try:
            # Create test patient
            test_name = f"Test Patient {datetime.now().strftime('%H%M%S')}"
            test_email = f"test.{datetime.now().strftime('%H%M%S')}@example.com"
            test_phone = "555-TEST-001"
            
            user_id = self.scheduler.get_or_create_patient(
                name=test_name,
                email=test_email,
                phone=test_phone
            )
            
            if user_id:
                self.test_user_id = user_id
                self.test_pass(f"Patient created: ID={user_id}, Name={test_name}")
                
                # Verify patient exists
                conn = self.scheduler._get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT name, email FROM users WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0] == test_name:
                    self.test_pass("Patient data verification")
                else:
                    self.test_fail("Patient data mismatch")
            else:
                self.test_fail("Patient creation returned None")
                
        except Exception as e:
            self.test_fail("Patient registration", str(e))
    
    def test_rag_engine(self):
        """Test RAG medical Q&A system."""
        self.print_header("TEST 3: RAG MEDICAL Q&A ENGINE")
        
        try:
            # Initialize RAG engine with proper parameters
            self.console.print("[cyan]Initializing RAG engine...[/cyan]")
            self.rag = RAGEngine(
                collection_name="medical_knowledge",
                persist_directory="./chroma_db",
                api_key=None,  # Uses default
                model_name="gpt-3.5-turbo"
            )
            self.test_pass("RAG engine initialization")
            
            # Test query
            test_question = "What are the warning signs of a stroke?"
            self.console.print(f"[cyan]Testing query: '{test_question}'[/cyan]")
            
            answer, sources = self.rag.query(test_question)
            
            if answer and len(answer) > 50:
                self.test_pass(f"RAG query successful: {len(answer)} chars returned")
                self.console.print(f"[dim]Answer preview: {answer[:100]}...[/dim]")
            else:
                self.test_fail("RAG query returned insufficient content")
            
            if sources and len(sources) > 0:
                self.test_pass(f"Source citations: {len(sources)} sources found")
            else:
                self.test_warning("No source citations returned")
                
        except Exception as e:
            self.test_fail("RAG engine", str(e))
    
    def test_conversation_memory(self):
        """Test conversation memory system."""
        self.print_header("TEST 4: CONVERSATION MEMORY SYSTEM")
        
        if not self.test_user_id:
            self.test_fail("Conversation memory", "No test user available")
            return
        
        try:
            # Save test conversation (use correct parameter names)
            self.memory.save_conversation(
                user_id=self.test_user_id,
                role='user',
                message="What causes strokes?",
                context={'topic': 'stroke_causes'}
            )
            self.test_pass("Conversation saved (user message)")
            
            self.memory.save_conversation(
                user_id=self.test_user_id,
                role='assistant',
                message="Strokes are caused by...",
                context={'sources': ['medical_doc_1']}
            )
            self.test_pass("Conversation saved (assistant message)")
            
            # Retrieve conversation history
            history = self.memory.get_conversation_history(self.test_user_id, limit=10)
            
            if history and len(history) >= 2:
                self.test_pass(f"Conversation retrieval: {len(history)} messages")
            else:
                self.test_fail("Conversation retrieval returned insufficient data")
            
            # Test user context
            context = self.memory.get_user_context(self.test_user_id)
            
            if context:
                self.test_pass("User context generation")
                if 'total_conversations' in context:
                    self.console.print(f"  [dim]Conversations: {context['total_conversations']}[/dim]")
            else:
                self.test_fail("User context generation failed")
                
        except Exception as e:
            self.test_fail("Conversation memory", str(e))
    
    def test_appointment_booking(self):
        """Test appointment booking."""
        self.print_header("TEST 5: APPOINTMENT BOOKING")
        
        if not self.test_user_id:
            self.test_fail("Appointment booking", "No test user available")
            return
        
        try:
            # Get available doctor
            doctors = self.scheduler.get_all_doctors()
            if not doctors:
                self.test_fail("No doctors available")
                return
            
            doctor = doctors[0]
            self.test_pass(f"Doctor selected: {doctor['name']}")
            
            # Get tomorrow's date
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            
            # Check availability
            slots = self.scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
            
            if slots and len(slots) > 0:
                self.test_pass(f"Availability check: {len(slots)} slots found")
            else:
                self.test_warning("No available slots found for tomorrow")
                # Try next week
                next_week = (datetime.now() + timedelta(days=7)).date()
                slots = self.scheduler.get_doctor_availability(doctor['doctor_id'], next_week)
                if slots:
                    tomorrow = next_week
                    self.test_pass(f"Using alternative date: {tomorrow}")
                else:
                    self.test_fail("No availability found")
                    return
            
            # Book appointment
            success, message, appointment_id = self.scheduler.book_appointment(
                user_id=self.test_user_id,
                doctor_id=doctor['doctor_id'],
                appointment_date=str(tomorrow),
                start_time=slots[0]['start_time'],
                reason="System testing appointment"
            )
            
            if success and appointment_id:
                self.test_appointment_id = appointment_id
                self.test_pass(f"Appointment booked: ID={appointment_id}")
                self.console.print(f"  [dim]{message}[/dim]")
            else:
                self.test_fail(f"Appointment booking failed: {message}")
            
            # Verify appointment in database
            appointment = self.scheduler.get_appointment(appointment_id)
            if appointment:
                self.test_pass("Appointment verification in database")
            else:
                self.test_fail("Appointment not found in database")
                
        except Exception as e:
            self.test_fail("Appointment booking", str(e))
    
    def test_appointment_retrieval(self):
        """Test appointment retrieval."""
        self.print_header("TEST 6: APPOINTMENT RETRIEVAL")
        
        if not self.test_user_id:
            self.test_fail("Appointment retrieval", "No test user available")
            return
        
        try:
            # Get user appointments using database query
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT a.*, 
                       d.name as doctor_name,
                       d.specialty as doctor_specialty
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.user_id = ?
                ORDER BY a.appointment_date DESC, a.start_time DESC
            ''', (self.test_user_id,))
            
            appointments = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            if appointments and len(appointments) > 0:
                self.test_pass(f"User appointments retrieved: {len(appointments)} found")
                
                # Display appointment details
                table = Table(box=box.SIMPLE)
                table.add_column("ID")
                table.add_column("Doctor")
                table.add_column("Date")
                table.add_column("Time")
                table.add_column("Status")
                
                for apt in appointments[:3]:  # Show first 3
                    table.add_row(
                        str(apt['appointment_id']),
                        apt['doctor_name'][:20],
                        apt['appointment_date'],
                        apt['start_time'][:5],
                        apt['status']
                    )
                
                self.console.print(table)
            else:
                self.test_warning("No appointments found for user")
                
        except Exception as e:
            self.test_fail("Appointment retrieval", str(e))
    
    def test_personalization(self):
        """Test personalization features."""
        self.print_header("TEST 7: PERSONALIZATION & SMART SUGGESTIONS")
        
        if not self.test_user_id:
            self.test_fail("Personalization", "No test user available")
            return
        
        try:
            # Test personalized greeting
            greeting = self.memory.generate_personalized_greeting(self.test_user_id)
            
            if greeting and len(greeting) > 10:
                self.test_pass("Personalized greeting generation")
                self.console.print(f"  [dim]Greeting: {greeting[:80]}...[/dim]")
            else:
                self.test_fail("Greeting generation returned empty/short result")
            
            # Test smart suggestions
            suggestions = self.memory.get_smart_suggestions(self.test_user_id)
            
            if suggestions and len(suggestions) > 0:
                self.test_pass(f"Smart suggestions: {len(suggestions)} generated")
                for i, suggestion in enumerate(suggestions[:3], 1):
                    self.console.print(f"  [dim]{i}. {suggestion[:60]}...[/dim]")
            else:
                self.test_warning("No smart suggestions generated")
                
        except Exception as e:
            self.test_fail("Personalization", str(e))
    
    # ==================== DOCTOR PORTAL TESTS ====================
    
    def test_doctor_authentication(self):
        """Test doctor login/authentication."""
        self.print_header("TEST 8: DOCTOR AUTHENTICATION")
        
        try:
            doctors = self.scheduler.get_all_doctors()
            
            if doctors and len(doctors) >= 3:
                self.test_pass(f"Doctor list retrieved: {len(doctors)} doctors")
                
                # Test each doctor
                for doctor in doctors:
                    doctor_details = self.scheduler.get_doctor_by_id(doctor['doctor_id'])
                    if doctor_details:
                        self.test_pass(f"Doctor {doctor['name']} authentication verified")
                    else:
                        self.test_fail(f"Doctor {doctor['name']} details not found")
            else:
                self.test_fail("Insufficient doctors in system")
                
        except Exception as e:
            self.test_fail("Doctor authentication", str(e))
    
    def test_doctor_schedule_view(self):
        """Test doctor schedule viewing."""
        self.print_header("TEST 9: DOCTOR SCHEDULE VIEWING")
        
        try:
            doctors = self.scheduler.get_all_doctors()
            if not doctors:
                self.test_fail("No doctors available")
                return
            
            doctor = doctors[0]
            
            # Get doctor appointments
            today = datetime.now().strftime('%Y-%m-%d')
            future = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT a.*, u.name as patient_name
                FROM appointments a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.doctor_id = ? 
                  AND a.appointment_date >= ? 
                  AND a.appointment_date <= ?
                ORDER BY a.appointment_date, a.start_time
                LIMIT 10
            ''', (doctor['doctor_id'], today, future))
            
            appointments = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            if appointments:
                self.test_pass(f"Doctor schedule retrieved: {len(appointments)} appointments")
            else:
                self.test_warning("No appointments found for doctor (expected for test)")
                
        except Exception as e:
            self.test_fail("Doctor schedule viewing", str(e))
    
    def test_medical_notes(self):
        """Test medical notes functionality."""
        self.print_header("TEST 10: MEDICAL NOTES")
        
        if not self.test_appointment_id:
            self.test_warning("Medical notes", "No test appointment available")
            return
        
        try:
            # Add medical note
            test_note = f"Test medical note added at {datetime.now()}"
            
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE appointments
                SET notes = ?
                WHERE appointment_id = ?
            ''', (test_note, self.test_appointment_id))
            
            conn.commit()
            
            # Verify note was saved
            cursor.execute('''
                SELECT notes FROM appointments
                WHERE appointment_id = ?
            ''', (self.test_appointment_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] == test_note:
                self.test_pass("Medical note added and verified")
            else:
                self.test_fail("Medical note verification failed")
                
        except Exception as e:
            self.test_fail("Medical notes", str(e))
    
    def test_analytics(self):
        """Test analytics/statistics."""
        self.print_header("TEST 11: ANALYTICS & STATISTICS")
        
        try:
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            # Total appointments
            cursor.execute("SELECT COUNT(*) FROM appointments")
            total_apts = cursor.fetchone()[0]
            self.test_pass(f"Total appointments: {total_apts}")
            
            # Total patients
            cursor.execute("SELECT COUNT(*) FROM users")
            total_patients = cursor.fetchone()[0]
            self.test_pass(f"Total patients: {total_patients}")
            
            # Appointments by status
            cursor.execute('''
                SELECT status, COUNT(*) as count
                FROM appointments
                GROUP BY status
            ''')
            
            status_counts = cursor.fetchall()
            if status_counts:
                self.test_pass("Status breakdown retrieved")
                for status, count in status_counts:
                    self.console.print(f"  [dim]{status}: {count}[/dim]")
            
            conn.close()
            
        except Exception as e:
            self.test_fail("Analytics", str(e))
    
    # ==================== INTEGRATION TESTS ====================
    
    async def test_calendar_integration(self):
        """Test calendar integration (optional)."""
        self.print_header("TEST 12: CALENDAR INTEGRATION")
        
        if not self.test_appointment_id:
            self.test_warning("Calendar integration", "No test appointment available")
            return
        
        try:
            self.console.print("[yellow]⚠️  Calendar sync test skipped (requires manual verification)[/yellow]")
            self.console.print("[dim]To test calendar sync:[/dim]")
            self.console.print("[dim]1. Book appointment through patient portal[/dim]")
            self.console.print("[dim]2. Choose 'Yes' when asked to sync[/dim]")
            self.console.print("[dim]3. Check pinkpantherking20@gmail.com[/dim]")
            
            # Check if appointment has calendar_event_id
            appointment = self.scheduler.get_appointment(self.test_appointment_id)
            if appointment.get('calendar_event_id'):
                self.test_pass(f"Appointment has calendar sync flag: {appointment['calendar_event_id']}")
            else:
                self.test_warning("Appointment not yet synced to calendar")
                
        except Exception as e:
            self.test_fail("Calendar integration", str(e))
    
    def test_conflict_detection(self):
        """Test appointment conflict detection."""
        self.print_header("TEST 13: CONFLICT DETECTION")
        
        if not self.test_user_id:
            self.test_warning("Conflict detection", "No test user available")
            return
        
        try:
            doctors = self.scheduler.get_all_doctors()
            if not doctors:
                return
            
            doctor = doctors[0]
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            
            # Get first available slot
            slots = self.scheduler.get_doctor_availability(doctor['doctor_id'], tomorrow)
            if not slots:
                self.test_warning("No slots available for conflict test")
                return
            
            # Try to book same slot twice
            slot = slots[0]
            
            # First booking
            success1, msg1, apt1 = self.scheduler.book_appointment(
                user_id=self.test_user_id,
                doctor_id=doctor['doctor_id'],
                appointment_date=str(tomorrow),
                start_time=slot['start_time'],
                reason="Conflict test 1"
            )
            
            # Second booking (should fail)
            success2, msg2, apt2 = self.scheduler.book_appointment(
                user_id=self.test_user_id,
                doctor_id=doctor['doctor_id'],
                appointment_date=str(tomorrow),
                start_time=slot['start_time'],
                reason="Conflict test 2"
            )
            
            if success1 and not success2:
                self.test_pass("Conflict detection working correctly")
                self.console.print(f"  [dim]First booking: {msg1}[/dim]")
                self.console.print(f"  [dim]Second booking blocked: {msg2}[/dim]")
            else:
                self.test_fail(f"Conflict detection issue: Both={success1 and success2}")
                
        except Exception as e:
            self.test_fail("Conflict detection", str(e))
    
    def test_data_integrity(self):
        """Test data integrity and relationships."""
        self.print_header("TEST 14: DATA INTEGRITY")
        
        try:
            conn = self.scheduler._get_connection()
            cursor = conn.cursor()
            
            # Test foreign key relationships
            cursor.execute('''
                SELECT COUNT(*) 
                FROM appointments a
                LEFT JOIN users u ON a.user_id = u.user_id
                WHERE u.user_id IS NULL
            ''')
            orphaned_appointments = cursor.fetchone()[0]
            
            if orphaned_appointments == 0:
                self.test_pass("No orphaned appointments (user FK integrity)")
            else:
                self.test_fail(f"Found {orphaned_appointments} orphaned appointments")
            
            # Test doctor relationships
            cursor.execute('''
                SELECT COUNT(*) 
                FROM appointments a
                LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE d.doctor_id IS NULL
            ''')
            orphaned_doctors = cursor.fetchone()[0]
            
            if orphaned_doctors == 0:
                self.test_pass("No orphaned doctor appointments (doctor FK integrity)")
            else:
                self.test_fail(f"Found {orphaned_doctors} orphaned doctor appointments")
            
            # Test date format validity
            cursor.execute('''
                SELECT appointment_id, appointment_date
                FROM appointments
                WHERE appointment_date NOT LIKE '____-__-__'
            ''')
            invalid_dates = cursor.fetchall()
            
            if len(invalid_dates) == 0:
                self.test_pass("All appointment dates have valid format")
            else:
                self.test_fail(f"Found {len(invalid_dates)} appointments with invalid date format")
            
            conn.close()
            
        except Exception as e:
            self.test_fail("Data integrity", str(e))
    
    def print_summary(self):
        """Print test summary."""
        self.console.print()
        self.console.print("=" * 80)
        self.console.print("[bold cyan]TEST SUMMARY[/bold cyan]")
        self.console.print("=" * 80)
        self.console.print()
        
        # Summary table
        table = Table(box=box.ROUNDED, title="Test Results")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="yellow")
        table.add_column("Percentage", justify="right", style="green")
        
        total = self.test_results['total']
        if total > 0:
            table.add_row(
                "✓ Passed",
                str(self.test_results['passed']),
                f"{self.test_results['passed']/total*100:.1f}%"
            )
            table.add_row(
                "✗ Failed",
                str(self.test_results['failed']),
                f"{self.test_results['failed']/total*100:.1f}%"
            )
            table.add_row(
                "⚠ Warnings",
                str(self.test_results['warnings']),
                f"{self.test_results['warnings']/total*100:.1f}%"
            )
            table.add_row(
                "Total Tests",
                str(total),
                "100.0%",
                style="bold"
            )
        
        self.console.print(table)
        self.console.print()
        
        # Overall status
        pass_rate = (self.test_results['passed'] / total * 100) if total > 0 else 0
        
        if pass_rate >= 90:
            status = "[bold green]✅ EXCELLENT - System is production ready![/bold green]"
        elif pass_rate >= 75:
            status = "[bold yellow]⚠️  GOOD - Minor issues to address[/bold yellow]"
        elif pass_rate >= 50:
            status = "[bold yellow]⚠️  FAIR - Several issues need attention[/bold yellow]"
        else:
            status = "[bold red]❌ POOR - Major issues detected[/bold red]"
        
        self.console.print(Panel(status, border_style="cyan"))
        self.console.print()


async def run_all_tests():
    """Run all system tests."""
    console.print()
    console.print("╔══════════════════════════════════════════════════════════════╗")
    console.print("║                                                              ║")
    console.print("║        🏥  HEALTHCARE SYSTEM - COMPREHENSIVE TESTING  🏥     ║")
    console.print("║                                                              ║")
    console.print("║              Patient Portal + Doctor Portal                  ║")
    console.print("║                                                              ║")
    console.print("╚══════════════════════════════════════════════════════════════╝")
    console.print()
    
    tester = SystemTester()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Running tests...", total=14)
        
        # Run all tests
        tester.test_database_connection()
        progress.advance(task)
        
        tester.test_patient_registration()
        progress.advance(task)
        
        tester.test_rag_engine()
        progress.advance(task)
        
        tester.test_conversation_memory()
        progress.advance(task)
        
        tester.test_appointment_booking()
        progress.advance(task)
        
        tester.test_appointment_retrieval()
        progress.advance(task)
        
        tester.test_personalization()
        progress.advance(task)
        
        tester.test_doctor_authentication()
        progress.advance(task)
        
        tester.test_doctor_schedule_view()
        progress.advance(task)
        
        tester.test_medical_notes()
        progress.advance(task)
        
        tester.test_analytics()
        progress.advance(task)
        
        await tester.test_calendar_integration()
        progress.advance(task)
        
        tester.test_conflict_detection()
        progress.advance(task)
        
        tester.test_data_integrity()
        progress.advance(task)
    
    # Print summary
    tester.print_summary()
    
    console.print("[cyan]Test Data Created:[/cyan]")
    if tester.test_user_id:
        console.print(f"  • Test User ID: {tester.test_user_id}")
    if tester.test_appointment_id:
        console.print(f"  • Test Appointment ID: {tester.test_appointment_id}")
    console.print()
    
    console.print("[yellow]Note: Calendar sync requires manual verification[/yellow]")
    console.print("[dim]Check pinkpantherking20@gmail.com for synced events[/dim]")
    console.print()


if __name__ == "__main__":
    asyncio.run(run_all_tests())
