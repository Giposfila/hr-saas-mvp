from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Sync engine for migrations
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Async engine for application
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    async_database_url,
    echo=True,
    future=True
)

async_session_maker = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def init_db():
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        # Import all models here to register them
        from app.models.user import User
        from app.models.vacancy import Vacancy
        from app.models.candidate import Candidate
        from app.models.resume import Resume
        from app.models.stage import Stage
        
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting async DB session"""
    async with async_session_maker() as session:
        yield session
