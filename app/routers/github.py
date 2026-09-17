from fastapi import APIRouter, HTTPException, Query, status

from app.core.exceptions import (
    GitHubRateLimitError,
    GitHubRepositoryNotFoundError,
    GitHubServiceError,
    InvalidRepositoryURLError,
)
from app.schemas.github import GitHubRepositoryResponse
from app.services.github_service import (
    fetch_github_repository,
)


router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)


@router.get(
    "/repository",
    response_model=GitHubRepositoryResponse,
)
async def inspect_repository(
    repository_url: str = Query(
        min_length=1
    ),
):
    try:
        return await fetch_github_repository(
            repository_url
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