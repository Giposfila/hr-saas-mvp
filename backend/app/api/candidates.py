from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.candidate import Candidate, CandidateStatus
from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateListResponse,
    CandidateMoveStageRequest
)
from app.modules.candidates.service import process_resume_upload

router = APIRouter()


@router.get("", response_model=CandidateListResponse)
async def list_candidates(
    vacancy_id: Optional[int] = None,
    status: Optional[CandidateStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List candidates with filters"""
    offset = (page - 1) * page_size
    
    query = select(Candidate)
    
    if vacancy_id:
        query = query.where(Candidate.vacancy_id == vacancy_id)
    if status:
        query = query.where(Candidate.status == status)
    
    # Count
    result = await session.execute(query)
    total = len(result.all())
    
    # Paginate
    query = query.offset(offset).limit(page_size)
    result = await session.execute(query)
    candidates = result.scalars().all()
    
    return CandidateListResponse(
        candidates=candidates,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/upload")
async def upload_resume(
    vacancy_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Upload resume and create candidate"""
    # Process resume (async task)
    candidate = await process_resume_upload(vacancy_id, file, session)
    
    return {
        "candidate_id": candidate.id,
        "status": "processing",
        "message": "Resume uploaded successfully. AI screening in progress."
    }


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get candidate details"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update candidate"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    for key, value in candidate_data.model_dump(exclude_unset=True).items():
        setattr(candidate, key, value)
    
    await session.commit()
    await session.refresh(candidate)
    
    return candidate


@router.post("/{candidate_id}/move-stage")
async def move_candidate_stage(
    candidate_id: int,
    request: CandidateMoveStageRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Move candidate to different stage"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate.current_stage_id = request.stage_id
    
    await session.commit()
    await session.refresh(candidate)
    
    return {"success": True, "candidate_id": candidate_id, "new_stage_id": request.stage_id}
