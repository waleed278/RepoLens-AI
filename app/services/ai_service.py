from google import genai
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import (
    AIInvalidResponseError,
    AIServiceError,
)
from app.schemas.ai import RepositoryAIAnalysis

SYSTEM_INSTRUCTION = """
You are a software engineering repository reviewer.

Analyze only the repository information provided to you.

Do not invent files, tests, frameworks, deployment systems,
security controls, or technologies that are not supported by
the supplied repository evidence.

Evaluate the repository as an engineering project, not merely
by popularity metrics such as stars.

The quality score must be between 0 and 100.

Focus on:
- project clarity
- apparent architecture
- documentation
- technology choices
- maintainability signals
- visible engineering risks
- practical improvements

If evidence is missing, explicitly treat it as unknown instead
of inventing an answer.
""".strip()


async def analyze_repository_with_ai(
    repository_context: str,
) -> RepositoryAIAnalysis:

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Review the following GitHub repository information.

Produce a concise engineering analysis based only on
the supplied evidence.

{repository_context}
""".strip()

    try:
        interaction = await client.aio.interactions.create(
            model=settings.ai_model,
            input=[
                {
                    "type": "text",
                    "text": SYSTEM_INSTRUCTION,
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RepositoryAIAnalysis.model_json_schema(),
            },
        )

        if not interaction.output_text:
            raise AIInvalidResponseError()

        return RepositoryAIAnalysis.model_validate_json(
            interaction.output_text
        )

    except ValidationError as exc:
        raise AIInvalidResponseError() from exc

    except AIInvalidResponseError:
        raise

    except Exception as exc:
        raise AIServiceError(
            "AI provider request failed"
        ) from exc

    finally:
        await client.aio.aclose()