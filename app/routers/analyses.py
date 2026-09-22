from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AIInvalidResponseError,
    AIServiceError,
    AnalysisNotFoundError,
    GitHubRateLimitError,
    GitHubRepositoryNotFoundError,
    GitHubServiceError,
    InvalidRepositoryURLError,
)

from app.db.session import get_db

from app.schemas.analysis import AnalysisCreate , AnalysisResponse

from app.services.analysis_service import create_repository_analysis , get_analysis

router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"],
)

@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_analysis_endpoint(
    analysis_in: AnalysisCreate,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await create_repository_analysis(
            db,
            analysis_in,
        )

    except InvalidRepositoryURLError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid GitHub repository URL",
        )

    except GitHubRepositoryNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub repository not found",
        )

    except GitHubRateLimitError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub rate limit reached",
        )

    except GitHubServiceError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="GitHub service request failed",
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


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
)
async def get_analysis_endpoint(
    analysis_id: int,
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await get_analysis(
            db,
            analysis_id,
        )

    except AnalysisNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )