from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.base import BaseModel


class User(BaseModel, table=True):
    """User model"""
    __tablename__ = "users"

    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: str = Field(default="recruiter")  # recruiter, hr_manager, hr_director, admin
    is_active: bool = Field(default=True)
    avatar_url: Optional[str] = None


class UserCreate(SQLModel):
    email: str
    password: str
    full_name: str
    role: str = "recruiter"


class UserRead(SQLModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    avatar_url: Optional[str] = None


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
