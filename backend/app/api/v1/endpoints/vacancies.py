from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy, VacancyCreate, VacancyRead, VacancyUpdate
from app.services.ai_service import AIService

router = APIRouter()


@router.get("", response_model=List[VacancyRead])
async def get_vacancies(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get all vacancies"""
    query = select(Vacancy)
    
    if status:
        query = query.where(Vacancy.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    vacancies = result.scalars().all()
    
    return vacancies


@router.post("", response_model=VacancyRead)
async def create_vacancy(
    vacancy_data: VacancyCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create new vacancy"""
    vacancy = Vacancy(
        **vacancy_data.model_dump(exclude={"skills"}),
        skills=json.dumps(vacancy_data.skills) if vacancy_data.skills else None,
        user_id=current_user.id,
    )
    
    session.add(vacancy)
    await session.commit()
    await session.refresh(vacancy)
    
    return vacancy


@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get vacancy by ID"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    
    return vacancy


@router.patch("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy(
    vacancy_id: int,
    vacancy_data: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update vacancy"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    
    update_data = vacancy_data.model_dump(exclude_unset=True)
    if "skills" in update_data and update_data["skills"]:
        update_data["skills"] = json.dumps(update_data["skills"])
    
    for key, value in update_data.items():
        setattr(vacancy, key, value)
    
    session.add(vacancy)
    await session.commit()
    await session.refresh(vacancy)
    
    return vacancy


@router.post("/{vacancy_id}/generate")
async def generate_vacancy_description(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Generate vacancy description using AI"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    
    ai_service = AIService()
    generated_description = await ai_service.generate_vacancy_description(
        title=vacancy.title,
        requirements=vacancy.requirements,
        skills=json.loads(vacancy.skills) if vacancy.skills else [],
    )
    
    vacancy.ai_generated_description = generated_description
    session.add(vacancy)
    await session.commit()
    
    return {"description": generated_description}


@router.delete("/{vacancy_id}")
async def delete_vacancy(
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete vacancy"""
    result = await session.execute(
        select(Vacancy).where(Vacancy.id == vacancy_id)
    )
    vacancy = result.scalar_one_or_none()
    
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    
    await session.delete(vacancy)
    await session.commit()
    
    return {"message": "Vacancy deleted"}
