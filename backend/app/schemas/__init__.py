from app.schemas.auth import TokenResponse, LoginRequest
from app.schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyResponse
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse

__all__ = [
    "TokenResponse", "LoginRequest",
    "VacancyCreate", "VacancyUpdate", "VacancyResponse",
    "CandidateCreate", "CandidateUpdate", "CandidateResponse"
]
