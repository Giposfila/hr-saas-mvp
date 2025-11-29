"""Background tasks for resume processing"""
import asyncio
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import async_session
from app.models.candidate import Candidate, Resume
from app.models.vacancy import Vacancy
from app.services.storage_service import StorageService
from app.services.resume_parser import ResumeParser
from app.services.ai_service import AIService


async def process_resume_task(resume_id: int):
    """Process resume: parse, extract data, calculate match score"""
    async with async_session() as session:
        # Get resume
        result = await session.execute(
            select(Resume).where(Resume.id == resume_id)
        )
        resume = result.scalar_one_or_none()
        
        if not resume:
            return
        
        try:
            # Update status
            resume.parse_status = "processing"
            await session.commit()
            
            # Download file from storage
            storage_service = StorageService()
            file_content = await storage_service.download_resume(resume.file_path)
            
            # Parse resume
            parser = ResumeParser()
            parsed_data = await parser.parse_resume(file_content)
            resume.raw_text = parsed_data["raw_text"]
            
            # Extract structured data with AI
            ai_service = AIService()
            structured_data = await ai_service.extract_resume_data(parsed_data["raw_text"])
            
            # Get candidate and vacancy
            candidate_result = await session.execute(
                select(Candidate).where(Candidate.id == resume.candidate_id)
            )
            candidate = candidate_result.scalar_one()
            
            vacancy_result = await session.execute(
                select(Vacancy).where(Vacancy.id == candidate.vacancy_id)
            )
            vacancy = vacancy_result.scalar_one()
            
            # Update candidate with structured data
            candidate.full_name = structured_data.get("full_name", "Unknown")
            candidate.email = structured_data.get("email")
            candidate.phone = structured_data.get("phone")
            candidate.location = structured_data.get("location")
            candidate.skills = json.dumps(structured_data.get("skills", []))
            candidate.experience_years = structured_data.get("experience_years")
            candidate.education = json.dumps(structured_data.get("education", []))
            candidate.work_experience = json.dumps(structured_data.get("work_experience", []))
            
            # Calculate match score
            vacancy_skills = json.loads(vacancy.skills) if vacancy.skills else []
            match_result = await ai_service.calculate_match_score(
                resume_text=parsed_data["raw_text"],
                vacancy_requirements=vacancy.requirements or "",
                vacancy_skills=vacancy_skills,
            )
            
            candidate.match_score = match_result.get("match_score", 0)
            candidate.ai_summary = match_result.get("summary")
            candidate.ai_strengths = json.dumps(match_result.get("strengths", []))
            candidate.ai_weaknesses = json.dumps(match_result.get("weaknesses", []))
            
            # Generate embedding
            embedding = await ai_service.generate_embedding(parsed_data["raw_text"])
            candidate.embedding = json.dumps(embedding)
            
            # Update resume status
            resume.parse_status = "completed"
            
            await session.commit()
            
        except Exception as e:
            resume.parse_status = "failed"
            resume.error_message = str(e)
            await session.commit()
            raise
