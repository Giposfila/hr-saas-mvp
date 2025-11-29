from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Stage(SQLModel, table=True):
    """Pipeline stages for vacancy recruitment process"""
    __tablename__ = "stages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Stage info
    name: str
    description: Optional[str] = None
    order: int = Field(default=0)  # Order in pipeline
    
    # Vacancy relation
    vacancy_id: int = Field(foreign_key="vacancies.id", index=True)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
