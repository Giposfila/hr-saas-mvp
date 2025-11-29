from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.candidate import Candidate
from app.models.pipeline import PipelineStage, CandidateStage, CandidateStageCreate
from pydantic import BaseModel

router = APIRouter()


class MoveCandidateRequest(BaseModel):
    candidate_id: int
    from_stage: str
    to_stage: str
    notes: str = None


@router.get("/{vacancy_id}")
async def get_pipeline(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get pipeline with candidates grouped by stage"""
    # Get all candidates for this vacancy
    result = await session.execute(
        select(Candidate)
        .where(Candidate.vacancy_id == vacancy_id)
        .where(Candidate.status == "active")
        .order_by(Candidate.match_score.desc())
    )
    candidates = result.scalars().all()
    
    # Group by stage
    pipeline = {
        "new": [],
        "selected": [],
        "screening": [],
        "interview": [],
        "offer": [],
    }
    
    for candidate in candidates:
        stage = candidate.current_stage
        if stage in pipeline:
            pipeline[stage].append({
                "id": candidate.id,
                "full_name": candidate.full_name,
                "email": candidate.email,
                "match_score": candidate.match_score,
                "skills": candidate.skills,
                "experience_years": candidate.experience_years,
            })
    
    return {
        "vacancy_id": vacancy_id,
        "stages": [
            {"name": "Новые", "slug": "new", "candidates": pipeline["new"]},
            {"name": "Отобранные", "slug": "selected", "candidates": pipeline["selected"]},
            {"name": "Скрининг", "slug": "screening", "candidates": pipeline["screening"]},
            {"name": "Интервью", "slug": "interview", "candidates": pipeline["interview"]},
            {"name": "Оффер", "slug": "offer", "candidates": pipeline["offer"]},
        ],
    }


@router.post("/move")
async def move_candidate(
    move_data: MoveCandidateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Move candidate between stages"""
    # Get candidate
    result = await session.execute(
        select(Candidate).where(Candidate.id == move_data.candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    
    # Update stage
    candidate.current_stage = move_data.to_stage
    session.add(candidate)
    
    # Log stage change
    stage_history = CandidateStage(
        candidate_id=candidate.id,
        stage_slug=move_data.to_stage,
        notes=move_data.notes,
        moved_by=current_user.id,
    )
    session.add(stage_history)
    
    await session.commit()
    
    return {
        "candidate_id": candidate.id,
        "new_stage": move_data.to_stage,
        "message": "Candidate moved successfully",
    }
