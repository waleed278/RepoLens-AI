from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AIInvalidResponseError,
    AIServiceError,
    GitHubRateLimitError,
    GitHubRepositoryNotFoundError,
    GitHubServiceError,
    InvalidRepositoryURLError,
    AnalysisNotFoundError
)
from app.models.analysis import (
    AnalysisStatus,
    RepositoryAnalysis,
)
from app.schemas.analysis import AnalysisCreate
from app.services.ai_service import (
    analyze_repository_with_ai,
)
from app.services.context_builder import (
    build_repository_context,
)
from app.services.github_service import (
    fetch_github_repository,
    parse_github_repository_url,
    GitHubRepositoryData
)

from app.schemas.ai import RepositoryAIAnalysis






async def create_pending_analysis(
    db: AsyncSession,
    analysis_in: AnalysisCreate,
) -> RepositoryAnalysis:

    analysis = RepositoryAnalysis(
        repository_url=analysis_in.repository_url,
        status=AnalysisStatus.PENDING,
    )

    db.add(analysis)

    await db.commit()
    await db.refresh(analysis)

    return analysis


async def mark_analysis_completed(
    db: AsyncSession,
    analysis: RepositoryAnalysis,
    repository,
    ai_analysis,
) -> RepositoryAnalysis:

    analysis.repository_owner = repository.owner
    analysis.repository_name = repository.name

    analysis.summary = ai_analysis.summary
    analysis.quality_score = ai_analysis.quality_score
    analysis.strengths = ai_analysis.strengths
    analysis.risks = ai_analysis.risks
    analysis.recommendations = ai_analysis.recommendations

    analysis.status = AnalysisStatus.COMPLETED
    analysis.error_message = None

    await db.commit()
    await db.refresh(analysis)

    return analysis

async def generate_repository_analysis(
    repository_url: str,
) -> tuple[
    GitHubRepositoryData,
    RepositoryAIAnalysis,
]:
    repository = await fetch_github_repository(
        repository_url
    )

    context = build_repository_context(
        repository
    )

    ai_analysis = await analyze_repository_with_ai(
        context
    )

    return repository, ai_analysis



async def mark_analysis_failed(
    db: AsyncSession,
    analysis: RepositoryAnalysis,
    error_message: str,
) -> None:

    analysis.status = AnalysisStatus.FAILED
    analysis.error_message = error_message

    await db.commit()


async def create_repository_analysis(
    db: AsyncSession,
    analysis_in: AnalysisCreate,
) -> RepositoryAnalysis:

    # Basic GitHub-specific validation before
    # creating a database record.
    parse_github_repository_url(
        analysis_in.repository_url
    )

    analysis = await create_pending_analysis(
        db,
        analysis_in,
    )

    try:
        repository = await fetch_github_repository(
            analysis_in.repository_url
        )

        repository_context = build_repository_context(
            repository
        )

        ai_analysis = await analyze_repository_with_ai(
            repository_context
        )

        return await mark_analysis_completed(
            db=db,
            analysis=analysis,
            repository=repository,
            ai_analysis=ai_analysis,
        )

    except GitHubRepositoryNotFoundError:
        await mark_analysis_failed(
            db,
            analysis,
            "GitHub repository not found",
        )
        raise

    except GitHubRateLimitError:
        await mark_analysis_failed(
            db,
            analysis,
            "GitHub rate limit reached",
        )
        raise

    except GitHubServiceError:
        await mark_analysis_failed(
            db,
            analysis,
            "GitHub service unavailable",
        )
        raise

    except AIInvalidResponseError:
        await mark_analysis_failed(
            db,
            analysis,
            "AI returned an invalid response",
        )
        raise

    except AIServiceError:
        await mark_analysis_failed(
            db,
            analysis,
            "AI processing failed",
        )
        raise


async def get_analysis_by_id(
    db: AsyncSession,
    analysis_id: int,
) -> RepositoryAnalysis | None:

    return await db.get(
        RepositoryAnalysis,
        analysis_id,
    )

async def get_analysis(
        db:AsyncSession,
        analysis_id: int,
)-> RepositoryAnalysis:

    analysis = await get_analysis_by_id(
        db,
        analysis_id
    )

    if analysis is None:
        raise AnalysisNotFoundError()

    return analysis