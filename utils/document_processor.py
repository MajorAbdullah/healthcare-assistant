"""
Document Processor - Handles PDF and text file processing for RAG system
"""

import os
from typing import List, Dict
from pathlib import Path
import pypdf
import pdfplumber
from rich.console import Console
from rich.progress import Progress

console = Console()


class DocumentProcessor:
    """Process medical documents for the RAG system."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor.
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_pdf(self, filepath: str) -> str:
        """
        Load text content from a PDF file.
        
        Args:
            filepath: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            console.print(f"📄 Loading PDF: {Path(filepath).name}", style="cyan")
            
            text = ""
            # Try with pdfplumber first (better for complex layouts)
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text.strip():
                # Fallback to pypdf
                console.print("  Trying alternative PDF reader...", style="yellow")
                with open(filepath, 'rb') as file:
                    pdf_reader = pypdf.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            
            console.print(f"  ✓ Extracted {len(text)} characters", style="green")
            return text
            
        except Exception as e:
            console.print(f"  ✗ Error loading PDF: {e}", style="red")
            raise
    
    def load_text_file(self, filepath: str) -> str:
        """
        Load text content from a text file.
        
        Args:
            filepath: Path to the text file
            
        Returns:
            File content
        """
        try:
            console.print(f"📝 Loading text file: {Path(filepath).name}", style="cyan")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            console.print(f"  ✓ Loaded {len(text)} characters", style="green")
            return text
            
        except Exception as e:
            console.print(f"  ✗ Error loading text file: {e}", style="red")
            raise
    
    def chunk_text(self, text: str, source_name: str = "") -> List[Dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            source_name: Name of the source document
            
        Returns:
            List of dictionaries with chunk text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        # Clean the text
        text = text.replace('\n\n\n', '\n\n')  # Remove excessive newlines
        text = text.strip()
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If not at the end, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
                for delimiter in ['. ', '.\n', '! ', '?\n', '? ']:
                    last_delimiter = text.rfind(delimiter, start, end)
                    if last_delimiter != -1:
                        end = last_delimiter + 1
                        break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunks.append({
                    'id': f"{source_name}_chunk_{chunk_id}",
                    'text': chunk_text,
                    'start_char': start,
                    'end_char': end,
                    'chunk_index': chunk_id
                })
                chunk_id += 1
            
            # Move start position with overlap
            # Ensure we always move forward to avoid infinite loop
            new_start = end - self.chunk_overlap
            if new_start <= start:  # If we're not moving forward, force progress
                new_start = start + max(1, self.chunk_size - self.chunk_overlap)
            start = new_start
        
        console.print(f"  ✓ Created {len(chunks)} chunks", style="green")
        return chunks
    
    def add_metadata(self, chunks: List[Dict], source: str, doc_type: str = "PDF", 
                     author: str = "", url: str = "") -> List[Dict]:
        """
        Add metadata to document chunks.
        
        Args:
            chunks: List of chunk dictionaries
            source: Source document name
            doc_type: Type of document (PDF, article, etc.)
            author: Author of the document
            url: Source URL if available
            
        Returns:
            Chunks with added metadata
        """
        for chunk in chunks:
            chunk['metadata'] = {
                'source': source,
                'doc_type': doc_type,
                'author': author,
                'url': url,
                'chunk_id': chunk['id']
            }
        
        return chunks
    
    def process_document(self, filepath: str, doc_type: str = "PDF",
                        author: str = "", url: str = "") -> List[Dict]:
        """
        Complete pipeline: Load, chunk, and add metadata to a document.
        
        Args:
            filepath: Path to the document
            doc_type: Type of document
            author: Author name
            url: Source URL
            
        Returns:
            List of processed chunks with metadata
        """
        # Determine file type and load
        file_ext = Path(filepath).suffix.lower()
        source_name = Path(filepath).stem
        
        if file_ext == '.pdf':
            text = self.load_pdf(filepath)
        elif file_ext in ['.txt', '.md']:
            text = self.load_text_file(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Chunk the text
        chunks = self.chunk_text(text, source_name)
        
        # Add metadata
        chunks = self.add_metadata(chunks, source_name, doc_type, author, url)
        
        return chunks
    
    def process_directory(self, directory: str) -> List[Dict]:
        """
        Process all supported documents in a directory.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of all processed chunks from all documents
        """
        all_chunks = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            console.print(f"✗ Directory not found: {directory}", style="red")
            return all_chunks
        
        # Find all supported files
        supported_extensions = ['.pdf', '.txt', '.md']
        files = []
        for ext in supported_extensions:
            files.extend(dir_path.glob(f'**/*{ext}'))
        
        console.print(f"\n📚 Processing {len(files)} documents from {directory}\n", style="bold cyan")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing documents...", total=len(files))
            
            for filepath in files:
                try:
                    chunks = self.process_document(str(filepath))
                    all_chunks.extend(chunks)
                    progress.update(task, advance=1)
                except Exception as e:
                    console.print(f"✗ Failed to process {filepath.name}: {e}", style="red")
                    progress.update(task, advance=1)
        
        console.print(f"\n✓ Total chunks created: {len(all_chunks)}", style="bold green")
        return all_chunks


if __name__ == "__main__":
    # Test the document processor
    import sys
    from config import MEDICAL_DOCS_DIR
    
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # Test with sample directory
    if MEDICAL_DOCS_DIR.exists():
        chunks = processor.process_directory(str(MEDICAL_DOCS_DIR))
        
        if chunks:
            console.print(f"\n📊 Sample chunk:\n", style="bold")
            console.print(chunks[0]['text'][:200] + "...", style="dim")
            console.print(f"\n metadata: {chunks[0]['metadata']}", style="dim")
    else:
        console.print(f"⚠️  Medical docs directory not found: {MEDICAL_DOCS_DIR}", style="yellow")
        console.print("   Please add PDF files to data/medical_docs/", style="yellow")
