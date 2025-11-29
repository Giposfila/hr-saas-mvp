from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List

from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.vacancy import (
    VacancyCreate, 
    VacancyUpdate, 
    VacancyResponse, 
    VacancyListResponse
)
from app.modules.ai_screening.generator import generate_vacancy_description

router = APIRouter()


@router.get("", response_model=VacancyListResponse)
async def list_vacancies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all vacancies"""
    offset = (page - 1) * page_size
    
    # Count total
    count_query = select(Vacancy)
    result = await session.execute(count_query)
    total = len(result.all())
    
    # Get paginated results
    query = select(Vacancy).offset(offset).limit(page_size)
    result = await session.execute(query)
    vacancies = result.scalars().all()
    
    return VacancyListResponse(
        vacancies=vacancies,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=VacancyResponse)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create new vacancy"""
    vacancy = Vacancy(
        **vacancy_data.model_dump(),
        created_by=current_user.id
    )
    
    session.add(vacancy)
    await session.commit()
    await session.refresh(vacancy)
    
    return vacancy


@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get vacancy by ID"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    return vacancy


@router.put("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update vacancy"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    # Update fields
    for key, value in vacancy_data.model_dump(exclude_unset=True).items():
        setattr(vacancy, key, value)
    
    await session.commit()
    await session.refresh(vacancy)
    
    return vacancy


@router.post("/{vacancy_id}/generate")
async def generate_description(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Generate AI description for vacancy"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    # Generate description
    generated_text = await generate_vacancy_description(vacancy)
    vacancy.ai_generated_description = generated_text
    
    await session.commit()
    await session.refresh(vacancy)
    
    return {"description": generated_text}
