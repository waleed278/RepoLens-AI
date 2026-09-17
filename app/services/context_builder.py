from app.services.github_service import GitHubRepositoryData


MAX_README_CHARACTERS = 12_000


def build_repository_context(
    repository: GitHubRepositoryData,
) -> str:

    readme = repository.readme or "No README available."

    if len(readme) > MAX_README_CHARACTERS:
        readme = (
            readme[:MAX_README_CHARACTERS]
            + "\n\n[README truncated]"
        )

    languages_text = format_languages(
        repository.languages
    )

    return f"""
Repository Owner: {repository.owner}
Repository Name: {repository.name}
Description: {repository.description or "No description"}
Stars: {repository.stars}
Forks: {repository.forks}
Open Issues: {repository.open_issues}
Default Branch: {repository.default_branch}

Languages:
{languages_text}

README:
{readme}
""".strip()

def format_languages(
        languages: dict[str,int]
)->str:

    if not languages:
        return "No language information avaiable."
    total_bytes = sum(languages.values())

    if total_bytes == 0:
        return "No language information is avaiable"

    lines: list[str] = []

    for language, byte_count in sorted(
        languages.items(),
        key = lambda item:item[1],
        reverse=True
    ):

        percentage =  (byte_count / total_bytes)*100

        lines.append(f"-{languages}:{percentage:.1f}%")

    return "\n".join(lines)