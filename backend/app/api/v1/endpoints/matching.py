from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.models.candidate import Candidate
from pydantic import BaseModel

router = APIRouter()


class MatchResult(BaseModel):
    candidate_id: int
    full_name: str
    match_score: float
    skills: str = None
    ai_summary: str = None
    strengths: str = None
    weaknesses: str = None


@router.get("/vacancies/{vacancy_id}/matches", response_model=List[MatchResult])
async def get_matches(
    vacancy_id: int,
    min_score: float = 0.0,
    limit: int = 50,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get matched candidates for vacancy"""
    # Verify vacancy exists
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    
    # Get candidates sorted by match score
    result = await session.execute(
        select(Candidate)
        .where(Candidate.vacancy_id == vacancy_id)
        .where(Candidate.match_score >= min_score)
        .where(Candidate.status == "active")
        .order_by(Candidate.match_score.desc())
        .limit(limit)
    )
    candidates = result.scalars().all()
    
    matches = [
        MatchResult(
            candidate_id=c.id,
            full_name=c.full_name,
            match_score=c.match_score or 0.0,
            skills=c.skills,
            ai_summary=c.ai_summary,
            strengths=c.ai_strengths,
            weaknesses=c.ai_weaknesses,
        )
        for c in candidates
    ]
    
    return matches
