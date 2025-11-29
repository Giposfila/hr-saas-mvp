from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.base import BaseModel


class PipelineStage(BaseModel, table=True):
    """Pipeline stage configuration"""
    __tablename__ = "pipeline_stages"

    name: str = Field(index=True)
    slug: str = Field(unique=True, index=True)  # new, selected, screening, interview, offer
    order: int = Field(default=0)
    color: Optional[str] = None  # hex color for UI
    vacancy_id: int = Field(foreign_key="vacancies.id")


class CandidateStage(BaseModel, table=True):
    """Track candidate movement through pipeline"""
    __tablename__ = "candidate_stages"

    candidate_id: int = Field(foreign_key="candidates.id")
    stage_slug: str
    notes: Optional[str] = None
    moved_by: int = Field(foreign_key="users.id")


class PipelineStageRead(SQLModel):
    id: int
    name: str
    slug: str
    order: int
    color: Optional[str] = None


class CandidateStageCreate(SQLModel):
    candidate_id: int
    stage_slug: str
    notes: Optional[str] = None
