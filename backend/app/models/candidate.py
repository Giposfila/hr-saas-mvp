from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.base import BaseModel


class Candidate(BaseModel, table=True):
    """Candidate model"""
    __tablename__ = "candidates"

    # Basic info
    full_name: str = Field(index=True)
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = None
    location: Optional[str] = None
    
    # Structured data
    skills: Optional[str] = None  # JSON array
    experience_years: Optional[int] = None
    education: Optional[str] = None  # JSON
    work_experience: Optional[str] = None  # JSON array
    
    # AI fields
    embedding: Optional[str] = None  # Vector embedding
    ai_summary: Optional[str] = None
    ai_strengths: Optional[str] = None  # JSON array
    ai_weaknesses: Optional[str] = None  # JSON array
    match_score: Optional[float] = Field(default=0.0)
    
    # Status
    current_stage: str = Field(default="new")  # new, selected, screening, interview, offer, rejected
    status: str = Field(default="active")  # active, hired, rejected
    
    # Relations
    vacancy_id: int = Field(foreign_key="vacancies.id")
    user_id: int = Field(foreign_key="users.id")  # recruiter who added


class Resume(BaseModel, table=True):
    """Resume file model"""
    __tablename__ = "resumes"

    candidate_id: int = Field(foreign_key="candidates.id")
    file_name: str
    file_path: str  # S3/MinIO path
    file_type: str  # pdf, docx, etc
    file_size: int
    
    # Parsing status
    parse_status: str = Field(default="pending")  # pending, processing, completed, failed
    raw_text: Optional[str] = None
    error_message: Optional[str] = None


class CandidateCreate(SQLModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    vacancy_id: int


class CandidateRead(SQLModel):
    id: int
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = None
    match_score: Optional[float] = None
    ai_summary: Optional[str] = None
    current_stage: str
    status: str
    vacancy_id: int


class CandidateUpdate(SQLModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    current_stage: Optional[str] = None
    status: Optional[str] = None
