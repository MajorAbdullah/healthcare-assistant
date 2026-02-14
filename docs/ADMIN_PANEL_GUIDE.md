# 🔐 Admin Panel - Setup & Usage Guide

## 🚀 Quick Start

### 1. Install Backend Dependencies
```bash
cd /Users/abdullah/my_projects/pipedream
pip install python-multipart
```

### 2. Start the Backend
```bash
cd api
python main.py
```
Backend will run on `http://localhost:8000`

### 3. Start the Frontend
```bash
cd Frontend
npm run dev
# or
bun dev
```
Frontend will run on `http://localhost:5173`

---

## 🔑 Admin Login

### Default Credentials:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change these credentials in production!

### Access URLs:
- Home page: `http://localhost:5173/`
- Admin login: `http://localhost:5173/admin/auth`
- Admin dashboard: `http://localhost:5173/admin/dashboard` (requires login)

---

## 📚 Admin Features

### 1. Dashboard Overview
- Total documents uploaded
- Total chunks indexed in vector database
- Collection name display

### 2. Document Upload
**Supported Formats:**
- PDF (`.pdf`)
- Text files (`.txt`)
- Markdown (`.md`)

**How to Upload:**
1. Click "Select Files" button
2. Choose one or multiple files
3. Click "Upload Documents"
4. Files are automatically:
   - Saved to `data/uploaded_docs/`
   - Processed and chunked
   - Indexed into ChromaDB vector database
   - Status updated to "indexed"

### 3. Document Management
- View all uploaded documents with:
  - Filename
  - File size
  - Document type
  - Upload date
  - Status (indexed/pending/error)
- Delete documents (removes from both filesystem and metadata)

### 4. RAG System Integration
- Documents are automatically processed upon upload
- Text is chunked into 500-character segments with 50-character overlap
- Embeddings are generated using Google AI
- Stored in ChromaDB vector database
- AI chat assistant immediately has access to new documents

---

## 📂 File Locations

### Frontend Files:
```
Frontend/src/pages/admin/
├── Auth.tsx          # Admin login page
└── Dashboard.tsx     # Admin dashboard with document management
```

### Backend Files:
```
api/main.py           # Admin endpoints (lines 1360-1520)
```

### Data Storage:
```
data/
├── uploaded_docs/           # Uploaded documents
│   ├── metadata.json       # Document metadata
│   └── {uuid}_{filename}   # Actual files
└── vector_db/              # ChromaDB vector database
    └── medical_docs/       # Collection storage
```

---

## 🔧 API Endpoints

### GET /api/v1/admin/documents
Get list of all uploaded documents
```json
{
  "success": true,
  "data": {
    "documents": [
      {
        "id": "uuid-here",
        "filename": "medical_guide.pdf",
        "size": 1048576,
        "uploaded_at": "2025-11-02T10:30:00",
        "status": "indexed",
        "doc_type": "PDF",
        "file_path": "/path/to/file"
      }
    ]
  }
}
```

### POST /api/v1/admin/documents/upload
Upload one or multiple documents
```bash
curl -X POST http://localhost:8000/api/v1/admin/documents/upload \
  -F "files=@medical_guide.pdf" \
  -F "files=@health_tips.txt"
```

### DELETE /api/v1/admin/documents/{doc_id}
Delete a document
```bash
curl -X DELETE http://localhost:8000/api/v1/admin/documents/{uuid}
```

### GET /api/v1/admin/stats
Get RAG system statistics
```json
{
  "success": true,
  "data": {
    "total_documents": 5,
    "total_chunks": 250,
    "collection_name": "medical_docs"
  }
}
```

---

## 🎯 Usage Example

### Upload Medical Documents for AI Chat:

1. **Login to Admin Panel**
   - Go to `http://localhost:5173/admin/auth`
   - Enter credentials (admin/admin123)

2. **Upload Documents**
   - Click "Select Files"
   - Choose medical PDFs, text files, or markdown
   - Click "Upload Documents"
   - Wait for "Successfully uploaded X file(s)" message

3. **Verify Indexing**
   - Check "Uploaded Documents" section
   - Status should show "indexed" (green badge)
   - Total chunks should increase in stats

4. **Test in Chat**
   - Go to Patient Portal → Chat
   - Ask questions about the uploaded documents
   - AI will use the new knowledge to answer

---

## 🔒 Security Notes

### Production Deployment:
1. **Change Admin Credentials**
   - Update `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `Auth.tsx`
   - Or implement backend authentication with database

2. **Add Authentication Middleware**
   ```python
   from fastapi import Depends, HTTPException
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   async def verify_admin(credentials = Depends(security)):
       # Verify JWT token or session
       pass
   ```

3. **Environment Variables**
   ```env
   ADMIN_USERNAME=your_secure_username
   ADMIN_PASSWORD=your_secure_hashed_password
   ```

4. **File Upload Limits**
   - Set max file size limit
   - Validate file content
   - Scan for malware

5. **Rate Limiting**
   - Limit upload frequency
   - Prevent abuse

---

## 🐛 Troubleshooting

### Issue: "Upload failed"
**Solution**: Check if `python-multipart` is installed:
```bash
pip install python-multipart
```

### Issue: "Documents not indexing"
**Solution**: Check logs in terminal, ensure:
- Google API key is set
- ChromaDB is accessible
- Document format is supported

### Issue: "Can't access admin panel"
**Solution**: Ensure routes are added to `App.tsx`:
```tsx
import AdminAuth from "./pages/admin/Auth";
import AdminDashboard from "./pages/admin/Dashboard";

// In routes:
<Route path="/admin/auth" element={<AdminAuth />} />
<Route path="/admin/dashboard" element={<AdminDashboard />} />
```

### Issue: "Stats showing 0"
**Solution**: 
- Upload at least one document
- Wait for indexing to complete
- Refresh the page

---

## 📊 Monitoring

### Check Vector Database:
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

stats = rag.get_stats()
print(f"Total chunks: {stats['total_documents']}")
```

### View Uploaded Files:
```bash
ls -lh data/uploaded_docs/
cat data/uploaded_docs/metadata.json
```

---

## ✅ Checklist

Before going live:
- [ ] Change admin credentials
- [ ] Test file upload with various formats
- [ ] Verify documents are indexed correctly
- [ ] Test AI chat with uploaded documents
- [ ] Set file size limits
- [ ] Add file validation
- [ ] Implement proper authentication
- [ ] Add rate limiting
- [ ] Set up backup for vector database
- [ ] Configure HTTPS
- [ ] Set up monitoring/logging

---

## 🎉 Success!

Your admin panel is now ready to:
- ✅ Upload medical documents
- ✅ Manage RAG knowledge base
- ✅ Monitor system statistics
- ✅ Enhance AI chat capabilities

The more quality medical documents you upload, the better the AI assistant becomes!

---

**Last Updated**: November 2, 2025
**Version**: 1.0.0
