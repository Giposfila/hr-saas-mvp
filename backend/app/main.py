from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api import auth, vacancies, candidates, pipeline, matching


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered HR SaaS platform for resume screening and candidate management",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(vacancies.router, prefix="/vacancies", tags=["Vacancies"])
app.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
app.include_router(matching.router, prefix="/matching", tags=["Matching"])


@app.get("/")
async def root():
    return {
        "message": "HR SaaS API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
