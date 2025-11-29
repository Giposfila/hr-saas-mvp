from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ResumeStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    ERROR = "error"


class Resume(SQLModel, table=True):
    __tablename__ = "resumes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relations
    candidate_id: int = Field(foreign_key="candidates.id", index=True)
    
    # File info
    filename: str
    file_path: str  # S3/MinIO path
    file_size: int
    mime_type: str
    
    # Parsed content
    raw_text: Optional[str] = None
    
    # Embeddings
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))
    
    # Status
    status: ResumeStatus = Field(default=ResumeStatus.UPLOADED)
    error_message: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
