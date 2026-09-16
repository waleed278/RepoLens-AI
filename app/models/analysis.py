import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


class AnalysisStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class RepositoryAnalysis(Base):
    __tablename__ = "repository_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    repository_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    repository_owner: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    repository_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(
            AnalysisStatus,
            name="analysis_status",
        ),
        default=AnalysisStatus.PENDING,
        nullable=False,
        index=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    quality_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    strengths: Mapped[list[str] | None] = mapped_column(
    JSONB,
    nullable=True,
)

    risks: Mapped[list[str] | None] = mapped_column(
    JSONB,
    nullable=True,
)

    recommendations: Mapped[list[str] | None] = mapped_column(
    JSONB,
    nullable=True,
)
    
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )