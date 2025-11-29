from typing import List, Dict, Optional
from openai import OpenAI
import json
from app.core.config import settings


class AIService:
    """AI service for resume screening and analysis"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
    
    async def extract_resume_data(self, raw_text: str) -> Dict:
        """Extract structured data from resume text using LLM"""
        prompt = f"""Analyze the following resume and extract structured information in JSON format.

Resume text:
{raw_text}

Extract the following fields:
- full_name: string
- email: string or null
- phone: string or null
- location: string or null
- skills: array of strings (technical and soft skills)
- experience_years: integer (total years of experience)
- education: array of objects with degree, institution, year
- work_experience: array of objects with company, position, duration, responsibilities
- summary: brief professional summary (2-3 sentences)

Respond only with valid JSON, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR assistant that extracts structured data from resumes."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            raise Exception(f"Failed to extract resume data: {str(e)}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    async def calculate_match_score(
        self,
        resume_text: str,
        vacancy_requirements: str,
        vacancy_skills: List[str],
    ) -> Dict:
        """Calculate match score between resume and vacancy"""
        prompt = f"""Analyze the match between a candidate's resume and job vacancy requirements.

Vacancy Requirements:
{vacancy_requirements}

Required Skills: {', '.join(vacancy_skills)}

Candidate Resume:
{resume_text}

Provide analysis in JSON format:
- match_score: integer 0-100 (overall fit)
- strengths: array of strings (what matches well)
- weaknesses: array of strings (what's missing or weak)
- summary: brief analysis (2-3 sentences)

Respond only with valid JSON."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert recruiter analyzing candidate-job fit."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            raise Exception(f"Failed to calculate match score: {str(e)}")
    
    async def generate_vacancy_description(
        self,
        title: str,
        requirements: Optional[str],
        skills: List[str],
    ) -> str:
        """Generate vacancy description using AI"""
        prompt = f"""Create a professional job description for the following position:

Job Title: {title}
Required Skills: {', '.join(skills)}
{f'Additional Requirements: {requirements}' if requirements else ''}

Generate a compelling job description with:
1. Brief company/position overview
2. Key responsibilities
3. Required qualifications
4. Nice-to-have skills

Keep it concise and professional."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR professional writing job descriptions."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Failed to generate description: {str(e)}")
