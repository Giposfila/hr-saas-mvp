from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.candidate import (
    Candidate,
    CandidateCreate,
    CandidateRead,
    CandidateUpdate,
    Resume,
)
from app.services.storage_service import StorageService
from app.services.resume_parser import ResumeParser
from app.tasks.resume_tasks import process_resume_task

router = APIRouter()


@router.get("", response_model=List[CandidateRead])
async def get_candidates(
    vacancy_id: Optional[int] = None,
    status: Optional[str] = None,
    stage: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get all candidates with filters"""
    query = select(Candidate)
    
    if vacancy_id:
        query = query.where(Candidate.vacancy_id == vacancy_id)
    if status:
        query = query.where(Candidate.status == status)
    if stage:
        query = query.where(Candidate.current_stage == stage)
    
    query = query.offset(skip).limit(limit).order_by(Candidate.match_score.desc())
    result = await session.execute(query)
    candidates = result.scalars().all()
    
    return candidates


@router.post("", response_model=CandidateRead)
async def create_candidate(
    candidate_data: CandidateCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create new candidate"""
    candidate = Candidate(
        **candidate_data.model_dump(),
        user_id=current_user.id,
    )
    
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)
    
    return candidate


@router.post("/upload")
async def upload_resume(
    vacancy_id: int = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Upload resume and create candidate"""
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed",
        )
    
    # Create candidate
    candidate = Candidate(
        full_name="Parsing...",
        vacancy_id=vacancy_id,
        user_id=current_user.id,
        current_stage="new",
    )
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)
    
    # Upload file to storage
    storage_service = StorageService()
    file_content = await file.read()
    file_path = await storage_service.upload_resume(
        file_content=file_content,
        file_name=file.filename,
        candidate_id=candidate.id,
    )
    
    # Create resume record
    resume = Resume(
        candidate_id=candidate.id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(file_content),
        parse_status="pending",
    )
    session.add(resume)
    await session.commit()
    await session.refresh(resume)
    
    # Queue background task for parsing
    # In production, use RQ: process_resume_task.delay(resume.id)
    # For MVP, we'll parse synchronously (can be optimized later)
    
    return {
        "candidate_id": candidate.id,
        "resume_id": resume.id,
        "status": "processing",
        "message": "Resume uploaded and queued for processing",
    }


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get candidate by ID"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    
    return candidate


@router.patch("/{candidate_id}", response_model=CandidateRead)
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update candidate"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    
    update_data = candidate_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(candidate, key, value)
    
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)
    
    return candidate


@router.post("/{candidate_id}/move-stage")
async def move_candidate_stage(
    candidate_id: int,
    stage: str,
    notes: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Move candidate to different stage"""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )
    
    candidate.current_stage = stage
    session.add(candidate)
    await session.commit()
    
    return {
        "candidate_id": candidate_id,
        "stage": stage,
        "message": "Candidate moved successfully",
    }
