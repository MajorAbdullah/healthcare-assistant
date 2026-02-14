#!/usr/bin/env python3
"""
Test script to verify document upload and RAG indexing
Run this after uploading a document via admin panel
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.rag_engine import RAGEngine
from config import CHROMA_COLLECTION_NAME, VECTOR_DB_DIR, GOOGLE_API_KEY, LLM_MODEL

def test_rag_system():
    """Test if uploaded documents are in the RAG system"""
    
    print("="*70)
    print("🔍 RAG System Verification")
    print("="*70)
    
    # Initialize RAG engine
    try:
        rag = RAGEngine(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=str(VECTOR_DB_DIR),
            api_key=GOOGLE_API_KEY,
            model_name=LLM_MODEL
        )
        
        # Get stats
        stats = rag.get_stats()
        print(f"\n📊 Vector Database Statistics:")
        print(f"  Collection: {stats['collection_name']}")
        print(f"  Total Chunks: {stats['total_documents']}")
        print(f"  Location: {stats['persist_directory']}")
        
        # Test query if there are documents
        if stats['total_documents'] > 0:
            print(f"\n✅ Database has {stats['total_documents']} chunks indexed!")
            
            # Try a test search
            print("\n🔍 Testing semantic search...")
            test_query = "medical information"
            results = rag.search(test_query, n_results=3)
            
            if results:
                print(f"  ✓ Found {len(results)} relevant chunks")
                print(f"\n  Sample result:")
                print(f"  Source: {results[0]['metadata'].get('source', 'Unknown')}")
                print(f"  Text preview: {results[0]['text'][:150]}...")
            else:
                print("  ⚠️  No results found for test query")
                
            # Try a full RAG query
            print("\n🤖 Testing full RAG query...")
            rag_result = rag.query("What information do you have?", n_results=3)
            
            if rag_result and rag_result.get('answer'):
                print(f"  ✓ RAG query successful!")
                print(f"\n  AI Answer:\n  {rag_result['answer'][:200]}...")
                
                if rag_result.get('citations'):
                    print(f"\n  Citations:")
                    for citation in rag_result['citations'][:3]:
                        print(f"    - {citation}")
            else:
                print("  ⚠️  RAG query failed")
        else:
            print("\n⚠️  No documents indexed yet!")
            print("   Please upload documents via the admin panel.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    return True


def check_uploaded_files():
    """Check uploaded files in the data directory"""
    
    upload_dir = Path(__file__).parent.parent / "data" / "uploaded_docs"
    metadata_file = upload_dir / "metadata.json"
    
    print("\n📁 Checking Uploaded Files:")
    print(f"  Location: {upload_dir}")
    
    if not upload_dir.exists():
        print("  ⚠️  Upload directory doesn't exist yet")
        return
    
    # List files
    files = list(upload_dir.glob("*"))
    files = [f for f in files if f.name != "metadata.json"]
    
    print(f"  Files found: {len(files)}")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"    - {f.name} ({size_kb:.2f} KB)")
    
    # Check metadata
    if metadata_file.exists():
        import json
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        print(f"\n  Metadata entries: {len(metadata)}")
        for doc in metadata:
            status_icon = "✓" if doc['status'] == 'indexed' else "⚠️" if doc['status'] == 'pending' else "✗"
            chunks_info = f" ({doc.get('chunks_count', '?')} chunks)" if 'chunks_count' in doc else ""
            print(f"    {status_icon} {doc['filename']} - {doc['status']}{chunks_info}")
    else:
        print("  ℹ️  No metadata file yet")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🏥 Healthcare Assistant - RAG System Test")
    print("="*70)
    
    # Check uploaded files
    check_uploaded_files()
    
    # Test RAG system
    print()
    success = test_rag_system()
    
    if success:
        print("\n✅ All systems operational!")
    else:
        print("\n❌ Issues detected. Please check the logs above.")
    
    print()
