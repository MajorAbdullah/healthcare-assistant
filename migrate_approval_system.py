#!/usr/bin/env python3
"""
Database Migration Script - Add Approval System
Adds columns for appointment approval workflow and email tracking
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from config import DATABASE_PATH

def migrate_database():
    """Add approval system columns to appointments table"""
    print("🔄 Starting database migration for approval system...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [row[1] for row in cursor.fetchall()]
        
        migrations_needed = []
        
        # Check each column we need to add
        if 'approval_email_sent' not in columns:
            migrations_needed.append(('approval_email_sent', 'INTEGER DEFAULT 0'))
        
        if 'confirmation_email_sent' not in columns:
            migrations_needed.append(('confirmation_email_sent', 'INTEGER DEFAULT 0'))
        
        if not migrations_needed:
            print("✅ Database is already up to date!")
            conn.close()
            return True
        
        # Apply migrations
        for column_name, column_def in migrations_needed:
            print(f"  ➕ Adding column: {column_name}")
            cursor.execute(f"ALTER TABLE appointments ADD COLUMN {column_name} {column_def}")
        
        # Update existing appointments to have default values
        cursor.execute("""
            UPDATE appointments 
            SET approval_email_sent = 0, 
                confirmation_email_sent = 0
            WHERE approval_email_sent IS NULL 
               OR confirmation_email_sent IS NULL
        """)
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        print(f"   Added {len(migrations_needed)} new column(s)")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(appointments)")
        print("\n📋 Current appointments table schema:")
        for row in cursor.fetchall():
            print(f"   - {row[1]} ({row[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
