from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.vacancy import VacancyStatus


class VacancyBase(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: List[str] = []
    required_experience_years: Optional[int] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: Optional[List[str]] = None
    required_experience_years: Optional[int] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    status: Optional[VacancyStatus] = None


class VacancyResponse(VacancyBase):
    id: int
    status: VacancyStatus
    ai_generated_description: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VacancyListResponse(BaseModel):
    vacancies: List[VacancyResponse]
    total: int
    page: int
    page_size: int
