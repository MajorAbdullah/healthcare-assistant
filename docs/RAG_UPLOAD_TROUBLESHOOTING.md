# 🔧 RAG Document Upload - Troubleshooting Guide

## Issue: Documents Not Being Added to Vector Database

### ✅ Step-by-Step Fix

#### 1. **Restart the Backend API**
The backend might need to be restarted to load the fixed code:

```bash
# Stop the current API server (Ctrl+C)

# Navigate to api directory
cd /Users/abdullah/my_projects/pipedream/api

# Start the server again
python main.py
```

#### 2. **Verify Backend is Running**
Check that you see:
```
🏥 Healthcare Assistant API Starting...
📡 API Server: http://localhost:8000
```

#### 3. **Test Document Upload**
1. Go to `http://localhost:5173/admin/auth`
2. Login with `admin` / `admin123`
3. Upload a test document (PDF, TXT, or MD)
4. Watch the backend terminal for these messages:

**Expected Output:**
```
📄 Processing document: your_file.pdf
  ✓ Created X chunks
  ✓ Added to RAG vector database
  ℹ️  Total chunks in database: X
  ✓ Status updated to 'indexed'
✅ Metadata saved
```

#### 4. **Verify Upload Success**

**Run the test script:**
```bash
cd /Users/abdullah/my_projects/pipedream
python tests/test_rag_upload.py
```

**Expected Output:**
```
📊 Vector Database Statistics:
  Collection: medical_docs
  Total Chunks: X (should be > 0)
  
✅ Database has X chunks indexed!
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "RAG engine not available"
**Symptoms:** Backend shows "Warning: RAG engine not available"

**Solution:**
1. Check if `GOOGLE_API_KEY` is set in `.env` file
2. Verify the key is valid
3. Check `config.py` loads the environment variable

```bash
# Check your .env file
cat .env | grep GOOGLE_API_KEY

# Should show:
GOOGLE_API_KEY=your_actual_key_here
```

---

### Issue 2: "Failed to generate embeddings"
**Symptoms:** Upload succeeds but status stays "pending"

**Solution:**
1. Google API quota might be exceeded
2. API key might be invalid
3. Network connection issue

**Fix:**
```bash
# Test Google API directly
python -c "import google.generativeai as genai; from config import GOOGLE_API_KEY; genai.configure(api_key=GOOGLE_API_KEY); print('API works!')"
```

---

### Issue 3: PDF processing fails
**Symptoms:** Error message about PDF reading

**Solution:**
```bash
# Install required PDF libraries
pip install pypdf pdfplumber
```

---

### Issue 4: Status shows "error" instead of "indexed"
**Symptoms:** Document uploaded but shows red "error" badge

**Check Backend Logs:**
Look for specific error messages in the terminal running `python main.py`

**Common fixes:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check file permissions
ls -la data/uploaded_docs/
```

---

### Issue 5: Stats show 0 chunks even after upload
**Symptoms:** Upload says success but stats don't update

**Solution:**

1. **Check if ChromaDB directory exists:**
```bash
ls -la data/vector_db/
```

2. **Manually verify vector database:**
```bash
python tests/test_rag_upload.py
```

3. **Clear and rebuild if needed:**
```python
# In Python console
from modules.rag_engine import RAGEngine
from config import *

rag = RAGEngine(
    collection_name=CHROMA_COLLECTION_NAME,
    persist_directory=str(VECTOR_DB_DIR),
    api_key=GOOGLE_API_KEY,
    model_name=LLM_MODEL
)

# Check current stats
print(rag.get_stats())
```

---

## 🔍 Debug Mode

### Enable Detailed Logging

Add this to `api/main.py` at the top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Watch Backend Terminal

When uploading, you should see:
1. File received
2. File saved to `data/uploaded_docs/`
3. Document processor extracting text
4. Creating chunks
5. Generating embeddings
6. Storing in ChromaDB
7. Updating metadata

---

## ✅ Verification Checklist

After uploading a document:

- [ ] Backend terminal shows "Processing document: filename"
- [ ] Backend shows "Created X chunks"
- [ ] Backend shows "Added to RAG vector database"
- [ ] Backend shows "Status updated to 'indexed'"
- [ ] Admin panel shows green "indexed" badge
- [ ] Stats show increased chunk count
- [ ] Test script confirms chunks in database
- [ ] Chat can answer questions about the document

---

## 🧪 Test with Sample Document

Create a test file:

```bash
# Create a simple test file
cat > /tmp/test_medical.txt << 'EOF'
Medical Test Document

This is a test medical document for the RAG system.
It contains important medical information about general health.

Key points:
1. Regular exercise is important for health
2. Balanced diet helps prevent diseases
3. Regular checkups are recommended

This document should be indexed into the vector database.
EOF

# Then upload this file via admin panel
```

---

## 📞 Still Having Issues?

### Check These Files:

1. **Uploaded Files Location:**
   ```bash
   ls -la data/uploaded_docs/
   cat data/uploaded_docs/metadata.json
   ```

2. **Vector Database:**
   ```bash
   ls -la data/vector_db/
   ```

3. **Backend Logs:**
   - Check the terminal running `python main.py`
   - Look for any error messages in red

4. **Frontend Console:**
   - Open browser DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for failed API calls

---

## 🎯 Quick Fix Commands

```bash
# Navigate to project
cd /Users/abdullah/my_projects/pipedream

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Restart API server
cd api
python main.py

# In another terminal - run test
cd /Users/abdullah/my_projects/pipedream
python tests/test_rag_upload.py

# Check uploaded files
ls -la data/uploaded_docs/
cat data/uploaded_docs/metadata.json | python -m json.tool
```

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Upload shows success toast
2. ✅ Backend terminal shows all processing steps
3. ✅ Admin panel shows green "indexed" badge
4. ✅ Stats show correct chunk count
5. ✅ Test script confirms chunks exist
6. ✅ Chat can answer questions about uploaded content

---

**Last Updated:** November 2, 2025
