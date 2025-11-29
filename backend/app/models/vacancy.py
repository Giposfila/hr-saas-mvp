from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class VacancyStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class Vacancy(SQLModel, table=True):
    __tablename__ = "vacancies"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    requirements: Optional[str] = None
    
    # Structured data
    skills: List[str] = Field(default=[], sa_column=Column(JSON))
    required_experience_years: Optional[int] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None  # full-time, part-time, contract
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    
    # AI Generated
    ai_generated_description: Optional[str] = None
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))
    
    # Metadata
    status: VacancyStatus = Field(default=VacancyStatus.DRAFT)
    created_by: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
