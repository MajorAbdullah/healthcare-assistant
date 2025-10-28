# 🚀 Running the Healthcare Assistant

## Fixed Issues

### ✅ ChromaDB Duplicate Resolved
**Problem:** Two separate ChromaDB instances existed:
- `./chroma_db/` (160KB) - Used by API (wrong, empty)
- `data/vector_db/` (1MB) - Used by main app (correct, has documents)

**Solution:**
- ✅ Removed duplicate `./chroma_db/` folder
- ✅ Updated API to use `data/vector_db/`
- ✅ Now single source of truth: `data/vector_db/`

---

## How to Run

### Option 1: Quick Start Menu
```bash
python3 start.py
```

**Choose from:**
1. **Patient Portal** - Main healthcare assistant
2. **Doctor Portal** - Doctor management interface
3. Medical Q&A Demo
4. Calendar Integration Demo
5. Memory Manager Test
6. Interactive Calendar
7. Test RAG System
8. Test Scheduler
9. View Database Stats
10. Show Documentation

### Option 2: Direct Launch

**Patient Portal:**
```bash
python3 healthcare_assistant.py
```

**Doctor Portal:**
```bash
python3 doctor_portal.py
```

**API Server:**
```bash
./start_api.sh
# or
cd api && python3 main.py
```

---

## API Server

**Start:**
```bash
./start_api.sh
```

**Access:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Test:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/doctors
```

---

## Current Status

✅ **Database:** Single SQLite at `data/healthcare.db`
✅ **Vector DB:** Single ChromaDB at `data/vector_db/`
✅ **API:** FastAPI on port 8000
✅ **Patient Portal:** CLI working
✅ **Doctor Portal:** CLI working
✅ **Tests:** All in `tests/` folder
✅ **Docs:** All in `docs/` folder

---

## Quick Test

```bash
# 1. Check health
python3 -c "from config import *; print('✅ Config loaded')"

# 2. Test database
python3 -c "import sqlite3; conn = sqlite3.connect('data/healthcare.db'); print('✅ DB connected'); print(f'Users: {conn.execute(\"SELECT COUNT(*) FROM users\").fetchone()[0]}'); conn.close()"

# 3. Start app
python3 start.py
```

---

## File Locations

**Main Application Files:**
- `healthcare_assistant.py` - Patient portal
- `doctor_portal.py` - Doctor portal  
- `start.py` - Quick launcher
- `config.py` - Configuration

**Backend:**
- `api/main.py` - REST API server
- `modules/` - Core Python modules

**Data:**
- `data/healthcare.db` - SQLite database
- `data/vector_db/` - ChromaDB (medical documents)
- `data/medical_docs/` - Source medical documents

**Development:**
- `tests/` - All test files
- `docs/` - All documentation
