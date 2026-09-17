from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import (
    AIInvalidResponseError,
    AIServiceError,
)
from app.schemas.ai import RepositoryAIAnalysis
from app.services.ai_service import (
    analyze_repository_with_ai,
)


router = APIRouter(
    prefix="/debug",
    tags=["Debug"],
)


@router.post(
    "/ai",
    response_model=RepositoryAIAnalysis,
)
async def test_ai() -> RepositoryAIAnalysis:

    sample_context = """
Repository Owner: demo
Repository Name: spendflow
Description: Expense approval API built with FastAPI.

Languages:
- Python: 100.0%

README:
FastAPI backend using PostgreSQL, SQLAlchemy and JWT.
Employees submit expenses and managers approve or reject them.
The README does not mention automated testing or deployment.
""".strip()

    try:
        return await analyze_repository_with_ai(
            sample_context
        )

    except AIInvalidResponseError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI returned an invalid response",
        )

    except AIServiceError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI service request failed",
        )