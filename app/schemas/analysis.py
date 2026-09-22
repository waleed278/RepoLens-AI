from datetime import datetime
from pydantic import BaseModel, ConfigDict , Field

from app.models.analysis import AnalysisStatus

class AnalysisCreate(BaseModel):
    repository_url: str = Field(
        min_length=10,
        max_length=500,
    )

class AnalysisResponse(BaseModel):
    id:int
    repository_url: str
    repository_owner: str | None
    repository_name: str | None

    status: AnalysisStatus

    summary: str|None
    quality_score: int|None

    strengths: list[str] | None
    risks: list[str] | None
    recommendations: list[str] | None
    error_message: str|None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )