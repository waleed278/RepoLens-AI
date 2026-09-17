from app.schemas.ai import RepositoryAIAnalysis
from app.services.ai_service import (
    analyze_repository_with_ai,
)
from app.services.context_builder import (
    build_repository_context,
)
from app.services.github_service import (
    GitHubRepositoryData,
    fetch_github_repository,
)


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