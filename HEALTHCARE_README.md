# Healthcare Assistant 🏥

An AI-powered healthcare assistant that combines RAG (Retrieval-Augmented Generation) for medical Q&A with appointment scheduling capabilities.

## 🎯 Features

### ✅ Phase 1: RAG-based Medical Q&A (COMPLETE)
- **Semantic Search**: Understands meaning, not just keywords
- **AI-Powered Answers**: Uses Google Gemini 2.0 Flash for generation
- **Citation Support**: All answers backed by source documents
- **Medical Knowledge**: Comprehensive stroke information (symptoms, prevention, treatment)
- **Vector Database**: 45 chunks of medical content embedded and searchable
- **Beautiful CLI**: Rich-formatted terminal interface

### ⏳ Phase 2: Appointment Scheduler (UPCOMING)
- Doctor availability management
- Patient appointment booking
- Conflict detection
- Google Calendar integration
- SQLite database for persistence

### ⏳ Phase 3: Memory & Personalization (UPCOMING)
- Conversation history
- User preference learning
- Context-aware responses

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_healthcare.txt
```

### 2. Configure Environment
Create `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
PIPEDREAM_CALENDAR_ENDPOINT=your_pipedream_endpoint
```

### 3. Run the Interactive Demo
```bash
python3 demo_qa.py
```

### 4. Run Full Test Suite
```bash
python3 test_rag_complete.py
```

## 📚 Project Structure

```
pipedream/
├── config.py                    # Central configuration
├── modules/
│   ├── rag_engine.py           # RAG Q&A system ✅
│   ├── scheduler.py            # Appointment scheduler ⏳
│   └── memory_manager.py       # Conversation memory ⏳
├── utils/
│   ├── document_processor.py   # Document loading & chunking ✅
│   └── embeddings.py           # Gemini embeddings ✅
├── data/
│   ├── medical_docs/           # Medical knowledge base
│   ├── vector_db/              # ChromaDB storage
│   └── healthcare.db           # SQLite database ⏳
├── test_rag_complete.py        # Full RAG pipeline test ✅
├── demo_qa.py                  # Interactive Q&A demo ✅
└── CHANGELOG.md                # Detailed change history
```

## 💡 Example Usage

### Ask Medical Questions
```python
from modules.rag_engine import RAGEngine

rag = RAGEngine(
    collection_name="stroke_medical_docs",
    persist_directory="data/vector_db",
    api_key="your_api_key",
    model_name="gemini-2.0-flash-exp"
)

result = rag.query("What are the warning signs of a stroke?")
print(result['answer'])
# Includes citations like [1], [2], etc.
```

### Interactive Demo
```bash
$ python3 demo_qa.py

Your question: What is the F.A.S.T. method?

💡 Answer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
F.A.S.T. is an acronym for remembering stroke
warning signs:
- Face drooping
- Arm weakness
- Speech difficulty
- Time to call emergency services

📚 Sources:
  [1] stroke_overview (PDF)
  [2] stroke_prevention (PDF)
```

## 📊 Current Statistics

- **Code Files**: 15 Python files (~1,600+ lines)
- **Documentation**: 6 files (120KB+)
- **Medical Content**: 15,000+ characters
- **Vector Database**: 45 chunks embedded
- **Search Quality**: Distance scores 0.27-0.48 (excellent)
- **Tests**: All passing ✅

## 🧪 Testing

### Test Document Processing
```bash
python3 test_basic.py
```

### Test Complete RAG Pipeline
```bash
python3 test_rag_complete.py
```

### Show Project Progress
```bash
python3 show_progress.py
```

## 🔧 Configuration

Key settings in `config.py`:
- `CHUNK_SIZE = 500` - Characters per chunk
- `CHUNK_OVERLAP = 50` - Overlap between chunks
- `TOP_K_RESULTS = 5` - Number of search results
- `TEMPERATURE = 0.1` - Low for consistent answers

## 📖 Documentation

- `HEALTHCARE_PROJECT_PLAN.md` - Technical specification
- `IMPLEMENTATION_ROADMAP.md` - Day-by-day guide
- `PROJECT_SUMMARY.md` - Executive overview
- `ARCHITECTURE_DIAGRAM.txt` - System diagrams
- `CHANGELOG.md` - Complete change history

## 🎓 How It Works

### RAG Pipeline
1. **Document Loading**: Load PDF/TXT/MD files
2. **Chunking**: Split into 500-char chunks with overlap
3. **Embedding**: Generate vectors with Gemini
4. **Storage**: Store in ChromaDB vector database
5. **Search**: Semantic similarity search
6. **Generation**: AI-powered answers with citations

### Technologies
- **Vector DB**: ChromaDB (persistent)
- **Embeddings**: Google Gemini `models/embedding-001`
- **Generation**: Google Gemini 2.0 Flash Exp
- **CLI**: Rich library for beautiful output
- **Database**: SQLite (for appointments)

## 🚦 Status

| Component | Status | Notes |
|-----------|--------|-------|
| Document Processing | ✅ Complete | PDF, TXT, MD support |
| Embeddings | ✅ Complete | Batch processing, rate limiting |
| Vector Database | ✅ Complete | 45 chunks stored |
| Semantic Search | ✅ Complete | Distance: 0.27-0.48 |
| Answer Generation | ✅ Complete | With citations |
| Interactive Demo | ✅ Complete | demo_qa.py |
| Appointment Scheduler | ⏳ Next Phase | Phase 2 |
| Memory System | ⏳ Planned | Phase 3 |

## 🎯 Roadmap

### ✅ Phase 1 (Complete)
- [x] Project planning & documentation
- [x] Document processing system
- [x] Embedding generation
- [x] Vector database integration
- [x] Semantic search
- [x] Answer generation with citations
- [x] Interactive Q&A demo

### ⏳ Phase 2 (Next - Days 4-6)
- [ ] SQLite database schema
- [ ] Doctor management
- [ ] Patient management
- [ ] Appointment booking
- [ ] Conflict detection
- [ ] Google Calendar integration

### ⏳ Phase 3 (Days 7-8)
- [ ] Conversation history
- [ ] User preferences
- [ ] Context awareness

### ⏳ Phase 4 (Days 9-10)
- [ ] Main CLI application
- [ ] End-to-end testing
- [ ] Error handling
- [ ] User documentation

### ⏳ Phase 5 (Optional)
- [ ] Web UI with React
- [ ] REST API
- [ ] Authentication

## 🤝 Contributing

This is a prototype project for healthcare assistance. See `CHANGELOG.md` for detailed development history.

## ⚠️ Disclaimer

This is an educational prototype. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.

## 📝 License

Educational/Prototype Project

---

**Last Updated**: October 27, 2025
**Version**: 0.2.0 (Phase 1 Complete)
**Status**: 🟢 Operational
