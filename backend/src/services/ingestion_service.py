from typing import List, Dict, Any, Tuple
from pathlib import Path
import PyPDF2
import tiktoken
from backend.src.services.qdrant_client import qdrant_client
from backend.src.services.cohere_client import cohere_client
from backend.src.utils.error_handler import BookProcessingError


class IngestionService:
    """
    Service for ingesting book content from various formats (PDF, text)
    """
    
    def __init__(self):
        # Initialize tokenizer for chunking
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Good for most text
        
    def ingest_book(self, file_path: str, title: str, author: str) -> Dict[str, Any]:
        """
        Main method to ingest a book from file
        """
        try:
            # Determine file format and extract text
            content = self._extract_text(file_path)
            
            # Chunk the content
            chunks = self._chunk_text(content)
            
            # Create embeddings for chunks
            chunk_embeddings = cohere_client.embed_documents(chunks)
            
            # Prepare metadata for each chunk
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadatas.append({
                    "title": title,
                    "author": author,
                    "chunk_index": i,
                    "source_location": f"chunk_{i+1}",
                    "file_path": file_path
                })
            
            # Generate IDs for the chunks
            ids = [f"{title.replace(' ', '_')}_{i}" for i in range(len(chunks))]
            
            # Add chunks to vector store
            qdrant_client.add_texts(chunks, metadatas, ids)
            
            # Return ingestion result
            return {
                "book_id": title.replace(' ', '_').lower(),
                "title": title,
                "author": author,
                "chunk_count": len(chunks),
                "status": "completed",
                "message": f"Successfully ingested {len(chunks)} chunks"
            }
            
        except Exception as e:
            raise BookProcessingError(f"Failed to ingest book: {str(e)}")
    
    def _extract_text(self, file_path: str) -> str:
        """
        Extract text from a file based on its format
        """
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self._extract_text_from_pdf(file_path)
        elif file_extension in ['.txt', '.text']:
            return self._extract_text_from_txt(file_path)
        else:
            raise BookProcessingError(f"Unsupported file format: {file_extension}")
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                return text
        except Exception as e:
            raise BookProcessingError(f"Error reading PDF file: {str(e)}")
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """
        Extract text from a text file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise BookProcessingError(f"Error reading text file: {str(e)}")
    
    def _chunk_text(self, text: str, max_tokens: int = None, overlap_tokens: int = None) -> List[str]:
        """
        Chunk text into smaller pieces based on token count
        """
        if max_tokens is None:
            max_tokens = 1000  # Default from requirements
        if overlap_tokens is None:
            overlap_tokens = 200  # Default from requirements
            
        # Tokenize the text
        tokens = self.tokenizer.encode(text)
        
        chunks = []
        start_idx = 0
        
        while start_idx < len(tokens):
            # Calculate the end index for this chunk
            end_idx = start_idx + max_tokens
            
            # If this is not the last chunk, add overlap
            if end_idx < len(tokens):
                end_idx += overlap_tokens
            
            # Extract the token chunk
            token_chunk = tokens[start_idx:end_idx]
            
            # Decode back to text
            chunk_text = self.tokenizer.decode(token_chunk)
            chunks.append(chunk_text)
            
            # Move to the next chunk, accounting for overlap
            start_idx = end_idx - overlap_tokens if end_idx < len(tokens) else end_idx
        
        return chunks


# Create a singleton instance
ingestion_service = IngestionService()