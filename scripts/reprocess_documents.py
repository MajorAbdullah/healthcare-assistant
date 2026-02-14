#!/usr/bin/env python3
"""
Reprocess failed document uploads
This will retry indexing documents that show "error" status
"""

import sys
import os
import json
from pathlib import Path
import asyncio

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def reprocess_failed_documents():
    """Reprocess documents with error status"""
    
    # Import after path is set
    from modules.rag_engine import RAGEngine
    from utils.document_processor import DocumentProcessor
    from config import CHROMA_COLLECTION_NAME, VECTOR_DB_DIR, GOOGLE_API_KEY, LLM_MODEL, RAG_SYSTEM_PROMPT
    
    print("="*70)
    print("🔄 Reprocessing Failed Documents")
    print("="*70)
    
    # Load metadata
    upload_dir = Path(__file__).parent.parent / "data" / "uploaded_docs"
    metadata_file = upload_dir / "metadata.json"
    
    if not metadata_file.exists():
        print("❌ No metadata file found")
        return
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Find failed documents
    failed_docs = [doc for doc in metadata if doc['status'] == 'error']
    
    if not failed_docs:
        print("✅ No failed documents to reprocess")
        return
    
    print(f"\n📋 Found {len(failed_docs)} document(s) with errors:")
    for doc in failed_docs:
        print(f"  - {doc['filename']}")
    
    # Initialize RAG engine
    print("\n🔧 Initializing RAG engine...")
    try:
        rag = RAGEngine(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=str(VECTOR_DB_DIR),
            api_key=GOOGLE_API_KEY,
            model_name=LLM_MODEL,
            system_prompt=RAG_SYSTEM_PROMPT
        )
        print("  ✓ RAG engine ready")
    except Exception as e:
        print(f"  ❌ Failed to initialize RAG engine: {e}")
        return
    
    # Initialize document processor
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # Process each failed document
    import time
    for doc in failed_docs:
        try:
            print(f"\n📄 Processing: {doc['filename']}")
            file_path = doc['file_path']
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"  ❌ File not found: {file_path}")
                continue
            
            # Process document
            chunks = processor.process_document(
                filepath=file_path,
                doc_type=doc['doc_type'],
                author="Admin Upload",
                url=""
            )
            
            if not chunks:
                print(f"  ❌ No chunks created")
                continue
            
            print(f"  ✓ Created {len(chunks)} chunks")
            
            # Update chunk IDs to include timestamp to avoid conflicts
            timestamp = str(int(time.time()))
            for i, chunk in enumerate(chunks):
                chunk['metadata']['chunk_id'] = f"{doc['id']}_{timestamp}_{i}"
                chunk['id'] = f"{doc['id']}_{timestamp}_{i}"
            
            # Add to RAG engine
            rag.add_documents(chunks)
            print(f"  ✓ Added to RAG vector database")
            
            # Verify it was added
            stats = rag.get_stats()
            print(f"  ℹ️  Total chunks in database: {stats['total_documents']}")
            
            # Update metadata
            for m in metadata:
                if m['id'] == doc['id']:
                    m['status'] = 'indexed'
                    m['chunks_count'] = len(chunks)
                    print(f"  ✓ Status updated to 'indexed'")
                    break
                    
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Save updated metadata
    print("\n💾 Saving metadata...")
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print("  ✓ Metadata saved")
    
    # Show final status
    print("\n" + "="*70)
    print("📊 Final Status:")
    indexed = sum(1 for doc in metadata if doc['status'] == 'indexed')
    error = sum(1 for doc in metadata if doc['status'] == 'error')
    pending = sum(1 for doc in metadata if doc['status'] == 'pending')
    
    print(f"  ✅ Indexed: {indexed}")
    print(f"  ⚠️  Pending: {pending}")
    print(f"  ❌ Error: {error}")
    
    if error == 0:
        print("\n🎉 All documents successfully indexed!")
    
    print("="*70)


if __name__ == "__main__":
    # Run the async function
    asyncio.run(reprocess_failed_documents())
