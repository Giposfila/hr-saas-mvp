from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class CandidateStatus(str, Enum):
    NEW = "new"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"


class Candidate(SQLModel, table=True):
    __tablename__ = "candidates"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic info
    full_name: Optional[str] = None
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = None
    
    # Vacancy relation
    vacancy_id: int = Field(foreign_key="vacancies.id", index=True)
    
    # Status & Stage
    status: CandidateStatus = Field(default=CandidateStatus.NEW)
    current_stage_id: Optional[int] = Field(default=None, foreign_key="stages.id")
    
    # AI Extracted Data
    skills: List[str] = Field(default=[], sa_column=Column(JSON))
    experience_years: Optional[int] = None
    education: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))
    work_experience: Optional[List[Dict[str, Any]]] = Field(default=None, sa_column=Column(JSON))
    
    # AI Analysis
    match_score: Optional[float] = None  # 0-100
    ai_summary: Optional[str] = None
    strengths: List[str] = Field(default=[], sa_column=Column(JSON))
    weaknesses: List[str] = Field(default=[], sa_column=Column(JSON))
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
