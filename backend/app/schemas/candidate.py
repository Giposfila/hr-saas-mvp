from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.candidate import CandidateStatus


class CandidateBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CandidateCreate(CandidateBase):
    vacancy_id: int


class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[CandidateStatus] = None


class CandidateResponse(CandidateBase):
    id: int
    vacancy_id: int
    status: CandidateStatus
    skills: List[str]
    experience_years: Optional[int]
    education: Optional[List[Dict[str, Any]]]
    work_experience: Optional[List[Dict[str, Any]]]
    match_score: Optional[float]
    ai_summary: Optional[str]
    strengths: List[str]
    weaknesses: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CandidateListResponse(BaseModel):
    candidates: List[CandidateResponse]
    total: int
    page: int
    page_size: int


class CandidateMoveStageRequest(BaseModel):
    candidate_id: int
    stage_id: int
