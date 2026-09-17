from dataclasses import dataclass
from urllib.parse import urlparse
import httpx
from app.core.config import settings
from app.core.exceptions import (
    GitHubRateLimitError,
    GitHubRepositoryNotFoundError,
    GitHubServiceError,
    InvalidRepositoryURLError,
)


@dataclass
class GitHubRepositoryData:
    owner: str
    name: str
    description: str | None
    stars: int
    forks: int
    open_issues: int
    default_branch: str
    languages: dict[str, int]
    readme: str | None

def parse_github_repository_url(
        repository_url:str)-> tuple[str,str]:
    parsed_url = urlparse(repository_url)

    if parsed_url.scheme not in {"http","https"}:
        raise InvalidRepositoryURLError()

    if parsed_url.netloc.lower() not in {
        "github.com",
        "www.github.com",

    }:
        raise InvalidRepositoryURLError()

    path_parts = [
        part 
        for part in parsed_url.path.split("/")
        if part
    ]
    if len(path_parts) !=2:
        raise InvalidRepositoryURLError()

    owner,repo = path_parts

    if repo.endswith(".git"):
        repo = repo[:-4]

    if not owner or not repo:
        raise InvalidRepositoryURLError()

    return owner,repo

def build_github_headers()-> dict[str,str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X_GitHub_Api_Version": settings.github_api_version,
        "User-Agent": "RepoLensAI",
    }

    if settings.github_token:
        headers["Authorization"]=(
            f"Bearer {settings.github_token}"
        )

    return headers

async def fetch_repository_metadata(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
) -> dict:

    url = (
        f"{settings.github_api_base_url}"
        f"/repos/{owner}/{repo}"
    )

    response = await client.get(url)

    handle_github_response(response)

    return response.json()

def handle_github_response(
        response: httpx.Response
)->None:
    if response.status_code == 404:
        raise GitHubRepositoryNotFoundError()

    if response.status_code in {403,429}:
        remaining = response.headers.get(
            "x-ratelimit-remaining"
        )
        if remaining == "0" or response.status_code == 429:
            raise GitHubRateLimitError()

    if response.status_code>=400:
        raise GitHubServiceError()

async def fetch_repository_languages(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
) -> dict[str, int]:

    url = (
        f"{settings.github_api_base_url}"
        f"/repos/{owner}/{repo}/languages"
    )

    response = await client.get(url)

    handle_github_response(response)

    return response.json()

async def fetch_repository_readme(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
) -> str | None:

    url = (
        f"{settings.github_api_base_url}"
        f"/repos/{owner}/{repo}/readme"
    )

    headers= build_github_headers()

    headers["Accept"] = "application/vnd.github.raw+json"

    response = await client.get(
        url,headers=headers
    )

    if response.status_code == 404:
        return None

    handle_github_response(response)

    return response.text


async def fetch_github_repository(
    repository_url: str,
) -> GitHubRepositoryData:

    owner, repo = parse_github_repository_url(
        repository_url
    )

    timeout = httpx.Timeout(
        10.0,
        connect=5.0,
    )

    try:
        async with httpx.AsyncClient(
            headers=build_github_headers(),
            timeout=timeout,
            follow_redirects=True,
        ) as client:

            metadata = await fetch_repository_metadata(
                client,
                owner,
                repo,
            )

            languages = await fetch_repository_languages(
                client,
                owner,
                repo,
            )

            readme = await fetch_repository_readme(
                client,
                owner,
                repo,
            )

    except httpx.TimeoutException as exc:
        raise GitHubServiceError(
            "GitHub request timed out"
        ) from exc

    except httpx.RequestError as exc:
        raise GitHubServiceError(
            "Could not communicate with GitHub"
        ) from exc

    return GitHubRepositoryData(
        owner=metadata["owner"]["login"],
        name=metadata["name"],
        description=metadata.get("description"),
        stars=metadata.get("stargazers_count", 0),
        forks=metadata.get("forks_count", 0),
        open_issues=metadata.get(
            "open_issues_count",
            0,
        ),
        default_branch=metadata.get(
            "default_branch",
            "main",
        ),
        languages=languages,
        readme=readme,
    )

