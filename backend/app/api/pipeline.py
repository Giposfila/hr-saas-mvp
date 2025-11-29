from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Dict, Any

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.candidate import Candidate
from app.models.stage import Stage
from app.schemas.candidate import CandidateMoveStageRequest

router = APIRouter()


@router.get("/{vacancy_id}")
async def get_pipeline(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get pipeline for vacancy with candidates grouped by stage"""
    # Get stages
    stages_result = await session.execute(
        select(Stage)
        .where(Stage.vacancy_id == vacancy_id)
        .order_by(Stage.order)
    )
    stages = stages_result.scalars().all()
    
    # Get candidates
    candidates_result = await session.execute(
        select(Candidate).where(Candidate.vacancy_id == vacancy_id)
    )
    candidates = candidates_result.scalars().all()
    
    # Group candidates by stage
    pipeline: List[Dict[str, Any]] = []
    
    for stage in stages:
        stage_candidates = [
            {
                "id": c.id,
                "full_name": c.full_name,
                "email": c.email,
                "match_score": c.match_score,
                "status": c.status
            }
            for c in candidates if c.current_stage_id == stage.id
        ]
        
        pipeline.append({
            "stage_id": stage.id,
            "stage_name": stage.name,
            "order": stage.order,
            "candidates": stage_candidates
        })
    
    return {"vacancy_id": vacancy_id, "pipeline": pipeline}


@router.post("/move")
async def move_candidate_in_pipeline(
    request: CandidateMoveStageRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Move candidate between stages"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == request.candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate.current_stage_id = request.stage_id
    
    await session.commit()
    
    return {"success": True}
