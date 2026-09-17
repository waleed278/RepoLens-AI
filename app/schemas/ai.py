from pydantic import BaseModel, Field


class RepositoryAIAnalysis(BaseModel):
    summary: str = Field(
        min_length=20,
        max_length=1500,
    )

    quality_score: int = Field(
        ge=0,
        le=100,
    )

    strengths: list[str] = Field(
        min_length=1,
        max_length=5,
    )

    risks: list[str] = Field(
        max_length=5,
    )

    recommendations: list[str] = Field(
        min_length=1,
        max_length=5,
    )