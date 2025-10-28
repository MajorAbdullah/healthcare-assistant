#!/usr/bin/env python3
"""
Doctor Portal - Healthcare Assistant System
Provides doctors with patient management, scheduling, and analytics features
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from modules.scheduler import AppointmentScheduler
from modules.calendar_sync import CalendarSync
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn


class DoctorPortal:
    """
    Doctor Portal for managing appointments, patients, and availability.
    """
    
    def __init__(self):
        """Initialize doctor portal modules."""
        self.console = Console()
        self.scheduler = AppointmentScheduler()
        self.calendar = CalendarSync(self.scheduler)
        
        self.current_doctor_id: Optional[int] = None
        self.current_doctor_name: Optional[str] = None
    
    def get_appointments_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get appointments for current doctor within a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of appointment dictionaries
        """
        conn = self.scheduler._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, 
                   u.name as patient_name, 
                   u.email as patient_email,
                   u.phone as patient_phone
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.doctor_id = ? 
              AND a.appointment_date >= ? 
              AND a.appointment_date <= ?
            ORDER BY a.appointment_date, a.start_time
        ''', (self.current_doctor_id, start_date, end_date))
        
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return appointments
    
    def display_banner(self):
        """Display doctor portal welcome banner."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           👨‍⚕️  DOCTOR PORTAL - HEALTHCARE SYSTEM  👩‍⚕️         ║
║                                                              ║
║        Patient Management • Scheduling • Analytics           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold blue")
        self.console.print()
    
    def doctor_login(self) -> bool:
        """
        Doctor login process.
        
        Returns:
            True if login successful
        """
        self.console.print(Panel.fit(
            "[blue]Doctor Login[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get list of available doctors
        doctors = self.scheduler.get_all_doctors()
        
        if not doctors:
            self.console.print("[red]No doctors found in the system.[/red]")
            return False
        
        # Display available doctors
        table = Table(title="Available Doctors", box=box.ROUNDED)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="green")
        table.add_column("Specialization", style="yellow")
        
        for doctor in doctors:
            table.add_row(
                str(doctor['doctor_id']),
                doctor['name'],
                doctor['specialty']
            )
        
        self.console.print(table)
        self.console.print()
        
        # Select doctor
        doctor_id = IntPrompt.ask(
            "[blue]Enter your Doctor ID[/blue]",
            choices=[str(d['doctor_id']) for d in doctors]
        )
        
        # Find selected doctor
        for doctor in doctors:
            if doctor['doctor_id'] == doctor_id:
                self.current_doctor_id = doctor_id
                self.current_doctor_name = doctor['name']
                break
        
        self.console.print()
        self.console.print(Panel(
            f"[green]Welcome back, Dr. {self.current_doctor_name}![/green]\n"
            f"[dim]Last login: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}[/dim]",
            title="✅ Login Successful",
            border_style="green"
        ))
        self.console.print()
        
        return True
    
    def main_menu(self) -> str:
        """
        Display main menu and get doctor's choice.
        
        Returns:
            Selected menu option
        """
        table = Table(
            title=f"🏥 Doctor Portal - Dr. {self.current_doctor_name}",
            box=box.ROUNDED,
            show_header=False,
            border_style="blue"
        )
        table.add_column("Option", style="cyan bold", width=8)
        table.add_column("Feature", style="white")
        
        table.add_row("1", "📅 View Today's Schedule")
        table.add_row("2", "📋 View All Appointments")
        table.add_row("3", "👥 Patient Management")
        table.add_row("4", "📝 Add Medical Notes")
        table.add_row("5", "🕐 Manage Availability")
        table.add_row("6", "📊 Analytics Dashboard")
        table.add_row("7", "🔄 Sync to Calendar")
        table.add_row("8", "🚪 Logout")
        
        self.console.print(table)
        self.console.print()
        
        choice = Prompt.ask(
            "[blue]Select an option[/blue]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )
        
        return choice
    
    def view_todays_schedule(self):
        """Display today's appointments for the doctor."""
        self.console.print(Panel.fit(
            f"[blue]📅 Today's Schedule - {datetime.now().strftime('%A, %B %d, %Y')}[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get today's appointments
        today = datetime.now().strftime('%Y-%m-%d')
        appointments = self.get_appointments_in_range(today, today)
        
        if not appointments:
            self.console.print(Panel(
                "[yellow]No appointments scheduled for today.[/yellow]\n"
                "[dim]You have a free day! 🎉[/dim]",
                border_style="yellow"
            ))
            return
        
        # Create schedule table
        table = Table(title=f"Dr. {self.current_doctor_name}'s Schedule", box=box.ROUNDED)
        table.add_column("Time", style="cyan", justify="center")
        table.add_column("Patient", style="green")
        table.add_column("Contact", style="yellow")
        table.add_column("Reason", style="white")
        table.add_column("Status", style="magenta", justify="center")
        
        for apt in appointments:
            # Parse time
            time_str = datetime.strptime(apt['start_time'], "%H:%M:%S").strftime("%I:%M %p")
            
            # Get status emoji
            status = apt['status']
            status_display = {
                'scheduled': '🟢 Scheduled',
                'completed': '✅ Completed',
                'cancelled': '🔴 Cancelled',
                'no-show': '⚠️ No Show'
            }.get(status, status)
            
            table.add_row(
                time_str,
                apt['patient_name'],
                apt.get('patient_phone', 'N/A'),
                apt.get('reason', 'General consultation'),
                status_display
            )
        
        self.console.print(table)
        self.console.print()
        
        # Summary
        total = len(appointments)
        scheduled = sum(1 for a in appointments if a['status'] == 'scheduled')
        completed = sum(1 for a in appointments if a['status'] == 'completed')
        
        summary = f"[cyan]Total:[/cyan] {total} appointments  |  "
        summary += f"[green]Scheduled:[/green] {scheduled}  |  "
        summary += f"[blue]Completed:[/blue] {completed}"
        
        self.console.print(Panel(summary, border_style="dim"))
        self.console.print()
    
    def view_all_appointments(self):
        """Display all appointments with filtering options."""
        self.console.print(Panel.fit(
            "[blue]📋 All Appointments[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Date range selection
        self.console.print("[dim]Enter date range (leave empty for all time)[/dim]")
        start_date = Prompt.ask("[cyan]Start date (YYYY-MM-DD)[/cyan]", default="")
        end_date = Prompt.ask("[cyan]End date (YYYY-MM-DD)[/cyan]", default="")
        
        if not start_date:
            start_date = "2020-01-01"
        if not end_date:
            end_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        # Get appointments
        appointments = self.get_appointments_in_range(start_date, end_date)
        
        if not appointments:
            self.console.print(Panel(
                "[yellow]No appointments found for the selected period.[/yellow]",
                border_style="yellow"
            ))
            return
        
        # Create table
        table = Table(title=f"Appointments: {len(appointments)} total", box=box.ROUNDED)
        table.add_column("ID", style="dim", width=6)
        table.add_column("Date", style="cyan")
        table.add_column("Time", style="cyan")
        table.add_column("Patient", style="green")
        table.add_column("Reason", style="white", max_width=30)
        table.add_column("Status", style="magenta")
        
        # Sort by date
        sorted_appointments = sorted(appointments, key=lambda x: (x['appointment_date'], x['start_time']))
        
        for apt in sorted_appointments:
            apt_date = datetime.strptime(apt['appointment_date'], "%Y-%m-%d").strftime("%b %d, %Y")
            apt_time = datetime.strptime(apt['start_time'], "%H:%M:%S").strftime("%I:%M %p")
            
            status_emoji = {
                'scheduled': '🟢',
                'completed': '✅',
                'cancelled': '🔴',
                'no-show': '⚠️'
            }.get(apt['status'], '•')
            
            table.add_row(
                str(apt['appointment_id']),
                apt_date,
                apt_time,
                apt['patient_name'],
                apt.get('reason', 'N/A'),
                f"{status_emoji} {apt['status'].title()}"
            )
        
        self.console.print(table)
        self.console.print()
    
    def patient_management(self):
        """View and manage patient records."""
        self.console.print(Panel.fit(
            "[blue]👥 Patient Management[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get all patients who have appointments with this doctor
        appointments = self.get_appointments_in_range(
            "2020-01-01",
            (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        )
        
        # Extract unique patients
        patients_dict = {}
        for apt in appointments:
            patient_id = apt['user_id']
            if patient_id not in patients_dict:
                patients_dict[patient_id] = {
                    'id': patient_id,
                    'name': apt['patient_name'],
                    'email': apt['patient_email'],
                    'phone': apt.get('patient_phone', 'N/A'),
                    'total_appointments': 0,
                    'upcoming': 0,
                    'completed': 0
                }
            
            patients_dict[patient_id]['total_appointments'] += 1
            
            if apt['status'] == 'completed':
                patients_dict[patient_id]['completed'] += 1
            elif apt['status'] == 'scheduled':
                apt_date = datetime.strptime(apt['appointment_date'], "%Y-%m-%d")
                if apt_date >= datetime.now():
                    patients_dict[patient_id]['upcoming'] += 1
        
        if not patients_dict:
            self.console.print(Panel(
                "[yellow]No patients found.[/yellow]",
                border_style="yellow"
            ))
            return
        
        # Create patient table
        table = Table(title=f"Your Patients: {len(patients_dict)} total", box=box.ROUNDED)
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name", style="green")
        table.add_column("Contact", style="cyan")
        table.add_column("Total Visits", style="yellow", justify="center")
        table.add_column("Upcoming", style="blue", justify="center")
        table.add_column("Completed", style="magenta", justify="center")
        
        for patient in sorted(patients_dict.values(), key=lambda x: x['total_appointments'], reverse=True):
            table.add_row(
                str(patient['id']),
                patient['name'],
                f"{patient['email']}\n{patient['phone']}",
                str(patient['total_appointments']),
                str(patient['upcoming']),
                str(patient['completed'])
            )
        
        self.console.print(table)
        self.console.print()
        
        # Option to view patient details
        if Confirm.ask("[cyan]View detailed patient history?[/cyan]", default=False):
            patient_id = IntPrompt.ask("[cyan]Enter Patient ID[/cyan]")
            self.view_patient_history(patient_id)
    
    def view_patient_history(self, patient_id: int):
        """View complete appointment history for a patient."""
        # Get all appointments for this patient with this doctor
        conn = self.scheduler._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.name, u.email, u.phone
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.doctor_id = ? AND a.user_id = ?
            ORDER BY a.appointment_date DESC, a.start_time DESC
        ''', (self.current_doctor_id, patient_id))
        
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not appointments:
            self.console.print("[yellow]No appointment history found.[/yellow]")
            return
        
        # Display patient info
        patient_name = appointments[0]['name']
        self.console.print()
        self.console.print(Panel.fit(
            f"[green]Patient: {patient_name}[/green]",
            border_style="green"
        ))
        self.console.print()
        
        # Display appointment history
        table = Table(title="Appointment History", box=box.ROUNDED)
        table.add_column("Date", style="cyan")
        table.add_column("Time", style="cyan")
        table.add_column("Reason", style="white", max_width=40)
        table.add_column("Status", style="magenta")
        table.add_column("Notes", style="dim", max_width=40)
        
        for apt in appointments:
            apt_date = datetime.strptime(apt['appointment_date'], "%Y-%m-%d").strftime("%b %d, %Y")
            apt_time = datetime.strptime(apt['start_time'], "%H:%M:%S").strftime("%I:%M %p")
            
            notes = "No notes" if not apt.get('notes') else apt['notes']
            
            table.add_row(
                apt_date,
                apt_time,
                apt.get('reason', 'General consultation'),
                apt['status'].title(),
                notes
            )
        
        self.console.print(table)
        self.console.print()
    
    def add_medical_notes(self):
        """Add or update medical notes for an appointment."""
        self.console.print(Panel.fit(
            "[blue]📝 Add Medical Notes[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get recent appointments
        today = datetime.now().strftime('%Y-%m-%d')
        past_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        appointments = self.get_appointments_in_range(past_week, today)
        
        if not appointments:
            self.console.print(Panel(
                "[yellow]No recent appointments found.[/yellow]",
                border_style="yellow"
            ))
            return
        
        # Show appointments
        table = Table(title="Recent Appointments", box=box.ROUNDED)
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Date", style="yellow")
        table.add_column("Patient", style="green")
        table.add_column("Reason", style="white", max_width=30)
        table.add_column("Current Notes", style="dim", max_width=30)
        
        for apt in appointments:
            apt_date = datetime.strptime(apt['appointment_date'], "%Y-%m-%d").strftime("%b %d")
            notes = apt.get('notes') if apt.get('notes') else "[dim]No notes[/dim]"
            
            table.add_row(
                str(apt['appointment_id']),
                apt_date,
                apt['patient_name'],
                apt.get('reason', 'N/A'),
                notes
            )
        
        self.console.print(table)
        self.console.print()
        
        # Select appointment
        apt_id = IntPrompt.ask("[cyan]Enter Appointment ID to add notes[/cyan]")
        
        # Verify appointment belongs to this doctor
        valid = any(apt['appointment_id'] == apt_id for apt in appointments)
        if not valid:
            self.console.print("[red]Invalid appointment ID.[/red]")
            return
        
        # Get notes
        self.console.print()
        self.console.print("[cyan]Enter medical notes (press Ctrl+D or Ctrl+Z when done):[/cyan]")
        notes_lines = []
        try:
            while True:
                line = input()
                notes_lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass
        
        notes = "\n".join(notes_lines).strip()
        
        if not notes:
            self.console.print("[yellow]No notes entered.[/yellow]")
            return
        
        # Update appointment with notes
        conn = self.scheduler._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments
            SET notes = ?
            WHERE appointment_id = ?
        ''', (notes, apt_id))
        
        conn.commit()
        conn.close()
        
        self.console.print()
        self.console.print(Panel(
            "[green]✅ Medical notes saved successfully![/green]",
            border_style="green"
        ))
        self.console.print()
    
    def manage_availability(self):
        """Manage doctor's working hours and availability."""
        self.console.print(Panel.fit(
            "[blue]🕐 Manage Availability[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get current availability
        available_slots = self.scheduler.get_available_slots(
            self.current_doctor_id,
            datetime.now().strftime('%Y-%m-%d'),
            (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        )
        
        # Display current schedule
        self.console.print("[cyan]Current Availability Overview:[/cyan]")
        self.console.print(f"[dim]Next 30 days: {len(available_slots)} available slots[/dim]")
        self.console.print()
        
        # Show options
        table = Table(box=box.ROUNDED, show_header=False)
        table.add_column("Option", style="cyan bold", width=6)
        table.add_column("Action", style="white")
        
        table.add_row("1", "View available time slots")
        table.add_row("2", "Block time for personal leave")
        table.add_row("3", "View blocked times")
        table.add_row("4", "Return to main menu")
        
        self.console.print(table)
        self.console.print()
        
        choice = Prompt.ask(
            "[cyan]Select option[/cyan]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        
        if choice == "1":
            self.view_available_slots()
        elif choice == "2":
            self.block_time()
        elif choice == "3":
            self.view_blocked_times()
    
    def view_available_slots(self):
        """View available time slots for upcoming days."""
        days_ahead = IntPrompt.ask(
            "[cyan]View availability for next N days[/cyan]",
            default=7
        )
        
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        slots = self.scheduler.get_available_slots(
            self.current_doctor_id,
            start_date,
            end_date
        )
        
        if not slots:
            self.console.print("[yellow]No available slots found.[/yellow]")
            return
        
        # Group by date
        slots_by_date = {}
        for slot in slots:
            date = slot['date']
            if date not in slots_by_date:
                slots_by_date[date] = []
            slots_by_date[date].append(slot['time'])
        
        # Display
        for date, times in sorted(slots_by_date.items()):
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime("%A, %B %d, %Y")
            
            time_str = ", ".join([datetime.strptime(t, '%H:%M:%S').strftime('%I:%M %p') for t in times])
            
            self.console.print(f"[cyan]{date_str}[/cyan]")
            self.console.print(f"  [dim]{time_str}[/dim]")
            self.console.print()
    
    def block_time(self):
        """Block time slots for personal leave."""
        self.console.print("[yellow]⚠️  Feature coming soon: Block time for personal leave[/yellow]")
        self.console.print("[dim]This will allow you to mark specific dates/times as unavailable.[/dim]")
        self.console.print()
    
    def view_blocked_times(self):
        """View currently blocked time slots."""
        self.console.print("[yellow]⚠️  Feature coming soon: View blocked times[/yellow]")
        self.console.print("[dim]This will show all dates/times you've marked as unavailable.[/dim]")
        self.console.print()
    
    def analytics_dashboard(self):
        """Display analytics and statistics."""
        self.console.print(Panel.fit(
            "[blue]📊 Analytics Dashboard[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get all appointments
        appointments = self.get_appointments_in_range(
            "2020-01-01",
            (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        )
        
        if not appointments:
            self.console.print("[yellow]No data available yet.[/yellow]")
            return
        
        # Calculate statistics
        total_appointments = len(appointments)
        completed = sum(1 for a in appointments if a['status'] == 'completed')
        scheduled = sum(1 for a in appointments if a['status'] == 'scheduled')
        cancelled = sum(1 for a in appointments if a['status'] == 'cancelled')
        no_shows = sum(1 for a in appointments if a['status'] == 'no-show')
        
        # Unique patients
        unique_patients = len(set(a['user_id'] for a in appointments))
        
        # This month's stats
        this_month = datetime.now().strftime('%Y-%m')
        this_month_apts = [a for a in appointments if a['appointment_date'].startswith(this_month)]
        
        # Create statistics table
        stats_table = Table(title="📈 Overall Statistics", box=box.ROUNDED)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green", justify="right")
        
        stats_table.add_row("Total Appointments", str(total_appointments))
        stats_table.add_row("Unique Patients", str(unique_patients))
        stats_table.add_row("Completed Visits", f"{completed} ({completed/total_appointments*100:.1f}%)" if total_appointments > 0 else "0")
        stats_table.add_row("Scheduled (Upcoming)", str(scheduled))
        stats_table.add_row("Cancelled", str(cancelled))
        stats_table.add_row("No-Shows", str(no_shows))
        stats_table.add_row("This Month", str(len(this_month_apts)))
        
        self.console.print(stats_table)
        self.console.print()
        
        # Appointment status breakdown
        status_table = Table(title="📊 Status Breakdown", box=box.ROUNDED)
        status_table.add_column("Status", style="cyan")
        status_table.add_column("Count", style="yellow", justify="center")
        status_table.add_column("Percentage", style="green", justify="center")
        
        for status, count in [
            ('Completed', completed),
            ('Scheduled', scheduled),
            ('Cancelled', cancelled),
            ('No-Show', no_shows)
        ]:
            percentage = f"{count/total_appointments*100:.1f}%" if total_appointments > 0 else "0%"
            status_table.add_row(status, str(count), percentage)
        
        self.console.print(status_table)
        self.console.print()
        
        # Busiest days analysis
        day_counts = {}
        for apt in appointments:
            day = datetime.strptime(apt['appointment_date'], '%Y-%m-%d').strftime('%A')
            day_counts[day] = day_counts.get(day, 0) + 1
        
        if day_counts:
            self.console.print("[cyan]📅 Busiest Days:[/cyan]")
            sorted_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
            for day, count in sorted_days[:3]:
                self.console.print(f"  [green]{day}:[/green] {count} appointments")
            self.console.print()
    
    async def sync_to_calendar(self):
        """Sync upcoming appointments to Google Calendar."""
        self.console.print(Panel.fit(
            "[blue]🔄 Calendar Synchronization[/blue]",
            border_style="blue"
        ))
        self.console.print()
        
        # Get upcoming appointments
        today = datetime.now().strftime('%Y-%m-%d')
        future = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        
        appointments = self.get_appointments_in_range(today, future)
        
        scheduled = [a for a in appointments if a['status'] == 'scheduled']
        
        if not scheduled:
            self.console.print("[yellow]No upcoming appointments to sync.[/yellow]")
            return
        
        self.console.print(f"[cyan]Found {len(scheduled)} upcoming appointments[/cyan]")
        self.console.print()
        
        if not Confirm.ask("[blue]Sync these to Google Calendar?[/blue]", default=True):
            return
        
        # Sync appointments
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Syncing appointments...", total=len(scheduled))
            
            synced = 0
            for apt in scheduled:
                try:
                    success = await self.calendar.sync_appointment(apt['appointment_id'])
                    if success:
                        synced += 1
                    progress.advance(task)
                except Exception as e:
                    self.console.print(f"[red]Error syncing appointment {apt['appointment_id']}: {e}[/red]")
        
        self.console.print()
        self.console.print(Panel(
            f"[green]✅ Successfully synced {synced}/{len(scheduled)} appointments![/green]",
            border_style="green"
        ))
        self.console.print()
    
    async def run(self):
        """Main application loop."""
        self.display_banner()
        
        # Login
        if not self.doctor_login():
            return
        
        # Main loop
        while True:
            choice = self.main_menu()
            
            self.console.print()
            
            if choice == "1":
                self.view_todays_schedule()
            elif choice == "2":
                self.view_all_appointments()
            elif choice == "3":
                self.patient_management()
            elif choice == "4":
                self.add_medical_notes()
            elif choice == "5":
                self.manage_availability()
            elif choice == "6":
                self.analytics_dashboard()
            elif choice == "7":
                await self.sync_to_calendar()
            elif choice == "8":
                self.console.print(Panel(
                    f"[green]Goodbye, Dr. {self.current_doctor_name}![/green]\n"
                    f"[dim]Have a great day! 👋[/dim]",
                    border_style="green"
                ))
                break
            
            # Pause before showing menu again
            if choice != "8":
                self.console.print()
                Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
                self.console.clear()


def main():
    """Entry point for doctor portal."""
    portal = DoctorPortal()
    asyncio.run(portal.run())


if __name__ == "__main__":
    main()
