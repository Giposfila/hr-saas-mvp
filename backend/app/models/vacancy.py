from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from app.models.base import BaseModel


class Vacancy(BaseModel, table=True):
    """Vacancy model"""
    __tablename__ = "vacancies"

    title: str = Field(index=True)
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: Optional[str] = None  # JSON array as string
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: str = Field(default="full_time")  # full_time, part_time, contract
    status: str = Field(default="active")  # active, closed, draft
    
    # AI fields
    embedding: Optional[str] = None  # Vector embedding as JSON
    ai_generated_description: Optional[str] = None
    
    # Relations
    user_id: int = Field(foreign_key="users.id")


class VacancyCreate(SQLModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: str = "full_time"


class VacancyRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: str
    status: str
    user_id: int
    ai_generated_description: Optional[str] = None


class VacancyUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    status: Optional[str] = None
