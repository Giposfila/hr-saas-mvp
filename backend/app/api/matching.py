from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.models.candidate import Candidate
from app.modules.ai_screening.matcher import calculate_match_score

router = APIRouter()


@router.get("/vacancies/{vacancy_id}/matches")
async def get_vacancy_matches(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all candidates for vacancy sorted by match score"""
    # Get vacancy
    vacancy_result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = vacancy_result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    # Get candidates
    candidates_result = await session.execute(
        select(Candidate)
        .where(Candidate.vacancy_id == vacancy_id)
        .order_by(Candidate.match_score.desc())
    )
    candidates = candidates_result.scalars().all()
    
    return {
        "vacancy_id": vacancy_id,
        "vacancy_title": vacancy.title,
        "matches": [
            {
                "candidate_id": c.id,
                "full_name": c.full_name,
                "match_score": c.match_score,
                "skills": c.skills,
                "experience_years": c.experience_years,
                "ai_summary": c.ai_summary
            }
            for c in candidates
        ]
    }


@router.post("/calculate")
async def recalculate_match(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Recalculate match score for candidate"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Get vacancy
    vacancy_result = await session.execute(
        select(Vacancy).where(Vacancy.id == candidate.vacancy_id)
    )
    vacancy = vacancy_result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    # Recalculate
    match_score = await calculate_match_score(candidate, vacancy)
    candidate.match_score = match_score
    
    await session.commit()
    
    return {"candidate_id": candidate_id, "match_score": match_score}
