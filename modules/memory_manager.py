"""
Memory Manager Module
Handles conversation history, user profiles, and context tracking
for personalized healthcare assistance.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import Counter


class MemoryManager:
    """
    Manages conversation history and user context for personalized interactions.
    
    Features:
    - Conversation tracking with metadata
    - User preference learning
    - Context-aware responses
    - Appointment pattern analysis
    - Personalized recommendations
    """
    
    def __init__(self, db_path: str = "data/healthcare.db"):
        """Initialize memory manager with database connection."""
        self.db_path = db_path
        self._initialize_preferences_table()
    
    def _initialize_preferences_table(self):
        """Create user preferences table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                preferred_doctor_id INTEGER,
                preferred_time_of_day TEXT,  -- 'morning', 'afternoon', 'evening'
                preferred_days TEXT,  -- JSON array of preferred days
                health_topics TEXT,  -- JSON array of topics asked about
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (preferred_doctor_id) REFERENCES doctors(doctor_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ==================== CONVERSATION TRACKING ====================
    
    def save_conversation(
        self,
        user_id: int,
        role: str,
        message: str,
        response: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> int:
        """
        Save a conversation exchange to the database.
        
        Args:
            user_id: User identifier
            role: 'user', 'assistant', or 'system'
            message: User's message
            response: System's response (optional)
            context: Additional metadata (appointment_id, topic, etc.)
        
        Returns:
            conversation_id: ID of the saved conversation
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Store context as JSON
        context_json = json.dumps(context) if context else None
        
        # Map 'patient'/'doctor' to 'user' for compatibility
        message_type = 'user' if role in ['patient', 'doctor', 'user'] else role
        
        cursor.execute("""
            INSERT INTO conversations (user_id, message_type, message_text, context_data)
            VALUES (?, ?, ?, ?)
        """, (user_id, message_type, message, context_json))
        
        conversation_id = cursor.lastrowid
        
        # If there's a response, save it as a separate entry
        if response:
            cursor.execute("""
                INSERT INTO conversations (user_id, message_type, message_text, context_data)
                VALUES (?, ?, ?, ?)
            """, (user_id, 'assistant', response, context_json))
        
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def get_conversation_history(
        self,
        user_id: int,
        limit: int = 10,
        role: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve recent conversation history for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of conversations to retrieve
            role: Filter by role ('user', 'assistant', 'system')
        
        Returns:
            List of conversation dictionaries
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Map 'patient'/'doctor' to 'user' for compatibility
        if role in ['patient', 'doctor']:
            role = 'user'
        
        if role:
            cursor.execute("""
                SELECT conversation_id, created_at, message_type, message_text, context_data
                FROM conversations
                WHERE user_id = ? AND message_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, role, limit))
        else:
            cursor.execute("""
                SELECT conversation_id, created_at, message_type, message_text, context_data
                FROM conversations
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
        
        conversations = []
        for row in cursor.fetchall():
            context = json.loads(row[4]) if row[4] else {}
            conversations.append({
                'conversation_id': row[0],
                'timestamp': row[1],
                'role': row[2],
                'message': row[3],
                'context': context
            })
        
        conn.close()
        
        # Return in chronological order (oldest first)
        return list(reversed(conversations))
    
    def get_conversation_summary(self, user_id: int, days: int = 30) -> Dict:
        """
        Get a summary of user's conversation activity.
        
        Args:
            user_id: User identifier
            days: Number of days to look back
        
        Returns:
            Dictionary with conversation statistics
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        since_date = datetime.now() - timedelta(days=days)
        
        cursor.execute("""
            SELECT message_type, COUNT(*)
            FROM conversations
            WHERE user_id = ? AND created_at >= ?
            GROUP BY message_type
        """, (user_id, since_date))
        
        role_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT COUNT(DISTINCT DATE(created_at))
            FROM conversations
            WHERE user_id = ? AND created_at >= ?
        """, (user_id, since_date))
        
        active_days = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_conversations': sum(role_counts.values()),
            'role_breakdown': role_counts,
            'active_days': active_days,
            'period_days': days
        }
    
    # ==================== USER CONTEXT & PREFERENCES ====================
    
    def get_user_context(self, user_id: int) -> Dict:
        """
        Build comprehensive user context for personalized responses.
        
        Returns:
            Dictionary with user profile, preferences, and history
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute("""
            SELECT name, email, phone, created_at
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        
        user_row = cursor.fetchone()
        if not user_row:
            conn.close()
            return {'error': 'User not found'}
        
        # Get preferences
        cursor.execute("""
            SELECT preferred_doctor_id, preferred_time_of_day, 
                   preferred_days, health_topics, last_updated
            FROM user_preferences
            WHERE user_id = ?
        """, (user_id,))
        
        pref_row = cursor.fetchone()
        preferences = {}
        if pref_row:
            preferences = {
                'preferred_doctor_id': pref_row[0],
                'preferred_time_of_day': pref_row[1],
                'preferred_days': json.loads(pref_row[2]) if pref_row[2] else [],
                'health_topics': json.loads(pref_row[3]) if pref_row[3] else [],
                'last_updated': pref_row[4]
            }
        
        # Get appointment history
        cursor.execute("""
            SELECT COUNT(*), status
            FROM appointments
            WHERE user_id = ?
            GROUP BY status
        """, (user_id,))
        
        appointment_stats = dict(cursor.fetchall())
        
        # Get recent conversations count
        cursor.execute("""
            SELECT COUNT(*)
            FROM conversations
            WHERE user_id = ?
        """, (user_id,))
        
        total_conversations = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'user_id': user_id,
            'name': user_row[0],
            'email': user_row[1],
            'phone': user_row[2],
            'member_since': user_row[3],
            'preferences': preferences,
            'appointment_stats': appointment_stats,
            'total_conversations': total_conversations
        }
    
    def update_user_preferences(
        self,
        user_id: int,
        preferred_doctor_id: Optional[int] = None,
        preferred_time_of_day: Optional[str] = None,
        preferred_days: Optional[List[str]] = None,
        health_topics: Optional[List[str]] = None
    ) -> bool:
        """
        Update user preferences based on interactions.
        
        Args:
            user_id: User identifier
            preferred_doctor_id: Preferred doctor ID
            preferred_time_of_day: 'morning', 'afternoon', or 'evening'
            preferred_days: List of preferred weekdays
            health_topics: List of health topics user is interested in
        
        Returns:
            True if successful
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Check if preferences exist
        cursor.execute("""
            SELECT user_id FROM user_preferences WHERE user_id = ?
        """, (user_id,))
        
        exists = cursor.fetchone() is not None
        
        if exists:
            # Update existing preferences
            updates = []
            values = []
            
            if preferred_doctor_id is not None:
                updates.append("preferred_doctor_id = ?")
                values.append(preferred_doctor_id)
            
            if preferred_time_of_day is not None:
                updates.append("preferred_time_of_day = ?")
                values.append(preferred_time_of_day)
            
            if preferred_days is not None:
                updates.append("preferred_days = ?")
                values.append(json.dumps(preferred_days))
            
            if health_topics is not None:
                updates.append("health_topics = ?")
                values.append(json.dumps(health_topics))
            
            if updates:
                updates.append("last_updated = ?")
                values.append(datetime.now())
                values.append(user_id)
                
                query = f"""
                    UPDATE user_preferences 
                    SET {', '.join(updates)}
                    WHERE user_id = ?
                """
                cursor.execute(query, values)
        else:
            # Insert new preferences
            cursor.execute("""
                INSERT INTO user_preferences 
                (user_id, preferred_doctor_id, preferred_time_of_day, 
                 preferred_days, health_topics, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                preferred_doctor_id,
                preferred_time_of_day,
                json.dumps(preferred_days) if preferred_days else None,
                json.dumps(health_topics) if health_topics else None,
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
        
        return True
    
    # ==================== INTELLIGENT ANALYSIS ====================
    
    def analyze_appointment_patterns(self, user_id: int) -> Dict:
        """
        Analyze user's appointment booking patterns.
        
        Returns:
            Dictionary with patterns and recommendations
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Get all appointments
        cursor.execute("""
            SELECT a.appointment_date, a.start_time, a.doctor_id, d.name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ? AND a.status != 'cancelled'
            ORDER BY a.appointment_date DESC
        """, (user_id,))
        
        appointments = cursor.fetchall()
        conn.close()
        
        if not appointments:
            return {'message': 'No appointment history found'}
        
        # Analyze patterns
        doctors = Counter([apt[2] for apt in appointments])
        times = [apt[1] for apt in appointments]
        
        # Determine time preference
        morning = sum(1 for t in times if t < '12:00')
        afternoon = sum(1 for t in times if '12:00' <= t < '17:00')
        evening = sum(1 for t in times if t >= '17:00')
        
        preferred_time = 'morning' if morning > afternoon and morning > evening else \
                        'afternoon' if afternoon > evening else 'evening'
        
        # Most frequent doctor
        most_common_doctor = doctors.most_common(1)[0] if doctors else None
        
        return {
            'total_appointments': len(appointments),
            'most_visited_doctor': {
                'id': most_common_doctor[0],
                'name': appointments[0][3],
                'specialty': appointments[0][4],
                'visits': most_common_doctor[1]
            } if most_common_doctor else None,
            'preferred_time': preferred_time,
            'time_distribution': {
                'morning': morning,
                'afternoon': afternoon,
                'evening': evening
            },
            'last_appointment': {
                'date': appointments[0][0],
                'time': appointments[0][1],
                'doctor': appointments[0][3]
            }
        }
    
    def get_health_topics(self, user_id: int) -> List[str]:
        """
        Extract health topics from user's conversation history.
        
        Returns:
            List of health topics discussed
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT context_data
            FROM conversations
            WHERE user_id = ? AND context_data IS NOT NULL
        """, (user_id,))
        
        topics = set()
        for row in cursor.fetchall():
            context = json.loads(row[0])
            if 'topic' in context:
                topics.add(context['topic'])
        
        conn.close()
        
        return list(topics)
    
    def generate_personalized_greeting(self, user_id: int) -> str:
        """
        Generate a personalized greeting based on user history.
        
        Returns:
            Personalized greeting string
        """
        context = self.get_user_context(user_id)
        
        name = context.get('name', 'there')
        first_name = name.split()[0] if name else 'there'
        
        # Check recent activity
        recent_conversations = self.get_conversation_history(user_id, limit=1)
        
        if recent_conversations:
            last_timestamp = datetime.fromisoformat(recent_conversations[0]['timestamp'])
            days_since = (datetime.now() - last_timestamp).days
            
            if days_since == 0:
                time_msg = "Welcome back!"
            elif days_since == 1:
                time_msg = "Good to see you again!"
            elif days_since <= 7:
                time_msg = f"Welcome back! It's been {days_since} days."
            else:
                time_msg = f"Welcome back, {first_name}! It's been a while."
        else:
            time_msg = f"Welcome, {first_name}! I'm your healthcare assistant."
        
        # Add appointment reminder if upcoming
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT appointment_date, start_time, d.name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ? 
            AND a.status = 'scheduled'
            AND a.appointment_date >= date('now')
            ORDER BY a.appointment_date, a.start_time
            LIMIT 1
        """, (user_id,))
        
        upcoming = cursor.fetchone()
        conn.close()
        
        if upcoming:
            apt_date = datetime.strptime(upcoming[0], '%Y-%m-%d')
            days_until = (apt_date.date() - datetime.now().date()).days
            
            if days_until == 0:
                time_msg += f"\n📅 Reminder: You have an appointment TODAY at {upcoming[1]} with {upcoming[2]}."
            elif days_until == 1:
                time_msg += f"\n📅 Reminder: You have an appointment TOMORROW at {upcoming[1]} with {upcoming[2]}."
            elif days_until <= 7:
                time_msg += f"\n📅 Upcoming: Appointment in {days_until} days with {upcoming[2]}."
        
        return time_msg
    
    # ==================== SMART RECOMMENDATIONS ====================
    
    def suggest_follow_up(self, user_id: int) -> Optional[Dict]:
        """
        Suggest follow-up appointments based on history.
        
        Returns:
            Recommendation dictionary or None
        """
        conn = sqlite3.connect(self.db_path, timeout=10)
        cursor = conn.cursor()
        
        # Get last completed appointment
        cursor.execute("""
            SELECT a.appointment_date, a.doctor_id, d.name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.user_id = ? AND a.status = 'completed'
            ORDER BY a.appointment_date DESC
            LIMIT 1
        """, (user_id,))
        
        last_apt = cursor.fetchone()
        conn.close()
        
        if not last_apt:
            return None
        
        last_date = datetime.strptime(last_apt[0], '%Y-%m-%d')
        days_since = (datetime.now() - last_date).days
        
        # Suggest follow-up if it's been 30+ days
        if days_since >= 30:
            return {
                'reason': f"It's been {days_since} days since your last appointment",
                'suggested_doctor': {
                    'id': last_apt[1],
                    'name': last_apt[2],
                    'specialty': last_apt[3]
                },
                'message': f"Would you like to schedule a follow-up with {last_apt[2]}?"
            }
        
        return None
    
    def get_smart_suggestions(self, user_id: int) -> List[str]:
        """
        Generate smart suggestions based on user context.
        
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        # Analyze patterns
        patterns = self.analyze_appointment_patterns(user_id)
        
        if patterns.get('most_visited_doctor'):
            doctor = patterns['most_visited_doctor']
            suggestions.append(
                f"💡 You usually see {doctor['name']} - would you like to book with them again?"
            )
        
        if patterns.get('preferred_time'):
            time = patterns['preferred_time']
            suggestions.append(
                f"⏰ You prefer {time} appointments - I can show you {time} slots."
            )
        
        # Check for follow-up
        follow_up = self.suggest_follow_up(user_id)
        if follow_up:
            suggestions.append(f"📅 {follow_up['message']}")
        
        # Health topics
        topics = self.get_health_topics(user_id)
        if topics:
            suggestions.append(
                f"📚 You've asked about: {', '.join(topics[:3])} - would you like to learn more?"
            )
        
        return suggestions


# ==================== UTILITY FUNCTIONS ====================

def format_conversation_history(conversations: List[Dict], max_chars: int = 500) -> str:
    """
    Format conversation history for display or context.
    
    Args:
        conversations: List of conversation dictionaries
        max_chars: Maximum total characters to include
    
    Returns:
        Formatted string
    """
    output = []
    total_chars = 0
    
    for conv in conversations:
        timestamp = datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M')
        role_emoji = "👤" if conv['role'] == 'patient' else "👨‍⚕️" if conv['role'] == 'doctor' else "🤖"
        
        line = f"{timestamp} {role_emoji}: {conv['message'][:100]}"
        
        if total_chars + len(line) > max_chars:
            output.append("... (more history available)")
            break
        
        output.append(line)
        total_chars += len(line)
    
    return "\n".join(output)


if __name__ == "__main__":
    """Test the memory manager"""
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]TESTING MEMORY MANAGER[/bold cyan]")
    console.print("=" * 70 + "\n")
    
    # Initialize
    memory = MemoryManager()
    
    # Test with user_id = 1
    test_user_id = 1
    
    # Save some test conversations
    console.print("[yellow]1. Saving test conversations...[/yellow]\n")
    
    memory.save_conversation(
        user_id=test_user_id,
        role='patient',
        message='What are the symptoms of a stroke?',
        response='Common stroke symptoms include sudden numbness, confusion, and severe headache.',
        context={'topic': 'stroke', 'category': 'symptoms'}
    )
    
    memory.save_conversation(
        user_id=test_user_id,
        role='patient',
        message='How can I prevent strokes?',
        response='Prevention includes healthy diet, regular exercise, and controlling blood pressure.',
        context={'topic': 'stroke', 'category': 'prevention'}
    )
    
    console.print("[green]✓ Conversations saved[/green]\n")
    
    # Get conversation history
    console.print("[yellow]2. Retrieving conversation history...[/yellow]\n")
    history = memory.get_conversation_history(test_user_id, limit=5)
    console.print(f"[green]✓ Found {len(history)} conversations[/green]\n")
    
    for conv in history:
        console.print(f"  [{conv['role']}] {conv['message'][:50]}...")
    
    # Get user context
    console.print("\n[yellow]3. Building user context...[/yellow]\n")
    context = memory.get_user_context(test_user_id)
    
    console.print(Panel(
        f"""[cyan]User Profile:[/cyan]
Name: {context.get('name', 'N/A')}
Email: {context.get('email', 'N/A')}
Total Conversations: {context.get('total_conversations', 0)}
Appointments: {context.get('appointment_stats', {})}""",
        title="User Context",
        border_style="cyan"
    ))
    
    # Personalized greeting
    console.print("\n[yellow]4. Generating personalized greeting...[/yellow]\n")
    greeting = memory.generate_personalized_greeting(test_user_id)
    console.print(f"[green]{greeting}[/green]\n")
    
    console.print("\n" + "=" * 70)
    console.print("[bold green]✅ MEMORY MANAGER WORKING![/bold green]")
    console.print("=" * 70 + "\n")
