from typing import Optional, Dict
import io
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import magic


class ResumeParser:
    """Parse resume files and extract text"""
    
    @staticmethod
    def detect_file_type(file_content: bytes) -> str:
        """Detect file type using magic"""
        mime = magic.Magic(mime=True)
        return mime.from_buffer(file_content)
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF"""
        try:
            text = extract_pdf_text(io.BytesIO(file_content))
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    @classmethod
    def extract_text(cls, file_content: bytes, file_type: str) -> str:
        """Extract text based on file type"""
        if "pdf" in file_type.lower():
            return cls.extract_text_from_pdf(file_content)
        elif "word" in file_type.lower() or "document" in file_type.lower():
            return cls.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @classmethod
    async def parse_resume(cls, file_content: bytes) -> Dict[str, str]:
        """Parse resume and return structured data"""
        # Detect file type
        file_type = cls.detect_file_type(file_content)
        
        # Extract text
        raw_text = cls.extract_text(file_content, file_type)
        
        if not raw_text:
            raise ValueError("No text could be extracted from resume")
        
        return {
            "raw_text": raw_text,
            "file_type": file_type,
        }
