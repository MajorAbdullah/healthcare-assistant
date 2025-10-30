#!/usr/bin/env python3
"""
Apply database migration for approval workflow
"""

import sqlite3
from pathlib import Path
import sys

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

from config import DATABASE_PATH

def apply_migration():
    """Apply the approval workflow migration."""
    print("🔄 Applying approval workflow migration...")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'approval_email_sent' not in columns:
            cursor.execute("ALTER TABLE appointments ADD COLUMN approval_email_sent BOOLEAN DEFAULT 0")
            print("  ✅ Added approval_email_sent column")
        else:
            print("  ℹ️  approval_email_sent column already exists")
        
        if 'confirmation_email_sent' not in columns:
            cursor.execute("ALTER TABLE appointments ADD COLUMN confirmation_email_sent BOOLEAN DEFAULT 0")
            print("  ✅ Added confirmation_email_sent column")
        else:
            print("  ℹ️  confirmation_email_sent column already exists")
        
        conn.commit()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    apply_migration()
