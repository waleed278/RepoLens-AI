from pydantic import BaseModel


class GitHubRepositoryResponse(BaseModel):
    owner: str
    name: str
    description: str | None
    stars: int
    forks: int
    open_issues: int
    default_branch: str
    languages: dict[str, int]
    readme: str | None