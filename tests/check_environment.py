#!/usr/bin/env python3
"""
Environment Validation Script
Checks all required environment variables and configurations
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

# Load environment variables
load_dotenv()

def check_env_var(name, required=True, description=""):
    """Check if an environment variable is set"""
    value = os.getenv(name)
    
    if value:
        # Mask sensitive data
        if "KEY" in name or "SECRET" in name:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print_success(f"{name}: {masked_value}")
        else:
            print_success(f"{name}: {value}")
        return True
    else:
        if required:
            print_error(f"{name}: NOT SET (Required)")
            if description:
                print(f"   └─ {description}")
        else:
            print_warning(f"{name}: NOT SET (Optional)")
            if description:
                print(f"   └─ {description}")
        return False

def check_directory(path, name):
    """Check if a directory exists"""
    if path.exists():
        print_success(f"{name}: {path}")
        return True
    else:
        print_error(f"{name}: NOT FOUND at {path}")
        return False

def check_file(path, name):
    """Check if a file exists"""
    if path.exists():
        print_success(f"{name}: {path}")
        return True
    else:
        print_error(f"{name}: NOT FOUND at {path}")
        return False

def check_database():
    """Check database and tables"""
    from config import DATABASE_PATH
    import sqlite3
    
    if not DATABASE_PATH.exists():
        print_error(f"Database file not found: {DATABASE_PATH}")
        return False
    
    print_success(f"Database file exists: {DATABASE_PATH}")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = [
            'users', 'doctors', 'appointments', 
            'doctor_availability', 'conversations', 'user_preferences'
        ]
        
        print_info(f"Found {len(tables)} tables:")
        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print_success(f"  Table '{table}': {count} records")
            else:
                print_error(f"  Table '{table}': MISSING")
        
        conn.close()
        return True
    except Exception as e:
        print_error(f"Database check failed: {e}")
        return False

def check_vector_db():
    """Check vector database"""
    from config import VECTOR_DB_DIR
    
    if not VECTOR_DB_DIR.exists():
        print_warning(f"Vector DB directory not found: {VECTOR_DB_DIR}")
        return False
    
    print_success(f"Vector DB directory exists: {VECTOR_DB_DIR}")
    
    # Check if ChromaDB files exist
    chroma_sqlite = VECTOR_DB_DIR / "chroma.sqlite3"
    if chroma_sqlite.exists():
        print_success(f"  ChromaDB database found")
        
        # Try to load and count documents
        try:
            import chromadb
            from config import CHROMA_COLLECTION_NAME
            
            client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
            collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
            count = collection.count()
            print_success(f"  Collection '{CHROMA_COLLECTION_NAME}': {count} documents")
            
            if count == 0:
                print_warning("  Vector database is empty. Add medical documents to data/medical_docs/")
            
            return True
        except Exception as e:
            print_warning(f"  Could not read collection: {e}")
            return False
    else:
        print_warning("  ChromaDB not initialized")
        return False

def check_rag_engine():
    """Test RAG engine initialization"""
    try:
        from config import GOOGLE_API_KEY, LLM_MODEL, CHROMA_COLLECTION_NAME, VECTOR_DB_DIR
        from modules.rag_engine import RAGEngine
        
        if not GOOGLE_API_KEY:
            print_error("Cannot initialize RAG engine: GOOGLE_API_KEY not set")
            return False
        
        print_info("Testing RAG engine initialization...")
        rag = RAGEngine(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=str(VECTOR_DB_DIR),
            api_key=GOOGLE_API_KEY,
            model_name=LLM_MODEL
        )
        
        doc_count = rag.collection.count()
        print_success(f"RAG engine initialized successfully with {doc_count} documents")
        
        if doc_count == 0:
            print_warning("No documents in vector database. AI chat will not have knowledge base.")
        
        return True
    except Exception as e:
        print_error(f"RAG engine initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_api_imports():
    """Check if all API dependencies can be imported"""
    print_info("Checking API dependencies...")
    
    dependencies = [
        ('fastapi', 'FastAPI framework'),
        ('uvicorn', 'ASGI server'),
        ('pydantic', 'Data validation'),
        ('sqlite3', 'Database'),
        ('chromadb', 'Vector database'),
        ('google.generativeai', 'Google Gemini AI'),
    ]
    
    all_ok = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print_success(f"  {module_name}: {description}")
        except ImportError:
            print_error(f"  {module_name}: NOT INSTALLED ({description})")
            all_ok = False
    
    return all_ok

def check_frontend_env():
    """Check if frontend needs environment variables"""
    frontend_dir = Path(__file__).parent / "Frontend"
    
    print_info("Frontend environment check:")
    print_info("  Frontend does NOT need API keys")
    print_info("  All API calls go through backend (http://localhost:8000)")
    print_success("  Frontend configuration: OK (no env vars needed)")
    
    # Check if .env.local exists in frontend
    frontend_env = frontend_dir / ".env.local"
    if frontend_env.exists():
        print_info(f"  Found frontend .env.local file")
        with open(frontend_env, 'r') as f:
            content = f.read()
            if "GOOGLE_API_KEY" in content or "GEMINI" in content:
                print_warning("  ⚠️  Frontend .env.local contains API keys (not recommended)")
                print_info("     API keys should only be in backend .env file")
    
    return True

def main():
    """Main validation function"""
    print_header("Healthcare Assistant - Environment Check")
    
    issues = []
    
    # 1. Environment Variables
    print_header("1. Environment Variables")
    
    if not check_env_var("GOOGLE_API_KEY", required=True, 
                         description="Required for AI chat. Get from: https://ai.google.dev/"):
        issues.append("GOOGLE_API_KEY not set")
    
    if not check_env_var("PIPEDREAM_PROJECT_ID", required=True,
                         description="Required for calendar integration"):
        issues.append("PIPEDREAM_PROJECT_ID not set")
    
    if not check_env_var("PIPEDREAM_CLIENT_ID", required=True,
                         description="Required for calendar integration"):
        issues.append("PIPEDREAM_CLIENT_ID not set")
    
    if not check_env_var("PIPEDREAM_CLIENT_SECRET", required=True,
                         description="Required for calendar integration"):
        issues.append("PIPEDREAM_CLIENT_SECRET not set")
    
    check_env_var("EXTERNAL_USER_ID", required=False,
                  description="Optional user identifier")
    
    # 2. Directory Structure
    print_header("2. Directory Structure")
    
    from config import DATA_DIR, MEDICAL_DOCS_DIR, VECTOR_DB_DIR, DATABASE_PATH
    
    check_directory(DATA_DIR, "Data directory")
    check_directory(MEDICAL_DOCS_DIR, "Medical docs directory")
    check_directory(VECTOR_DB_DIR, "Vector DB directory")
    
    # 3. Database
    print_header("3. Database")
    if not check_database():
        issues.append("Database issues found")
    
    # 4. Vector Database
    print_header("4. Vector Database (RAG)")
    if not check_vector_db():
        issues.append("Vector database not initialized or empty")
    
    # 5. Dependencies
    print_header("5. Python Dependencies")
    if not check_api_imports():
        issues.append("Missing Python dependencies")
    
    # 6. RAG Engine
    print_header("6. RAG Engine Test")
    if not check_rag_engine():
        issues.append("RAG engine initialization failed")
    
    # 7. Frontend Environment
    print_header("7. Frontend Environment")
    check_frontend_env()
    
    # Summary
    print_header("Summary")
    
    if not issues:
        print_success("All checks passed! ✅")
        print_info("\nYour environment is properly configured.")
        print_info("You can start the servers:")
        print(f"\n  {Colors.BOLD}Backend:{Colors.END}")
        print(f"    python3 api/main.py")
        print(f"\n  {Colors.BOLD}Frontend:{Colors.END}")
        print(f"    cd Frontend && npm run dev")
        return 0
    else:
        print_error(f"Found {len(issues)} issue(s):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print(f"\n{Colors.YELLOW}Please fix the issues above before starting the servers.{Colors.END}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Check interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
