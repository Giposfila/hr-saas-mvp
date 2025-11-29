from fastapi import APIRouter
from app.api.v1.endpoints import auth, vacancies, candidates, pipeline, matching

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(vacancies.router, prefix="/vacancies", tags=["vacancies"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(matching.router, prefix="/matching", tags=["matching"])
