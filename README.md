# RepoLens AI

> AI-assisted GitHub repository analysis API built with FastAPI, PostgreSQL, and Gemini.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-async-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/status-active%20development-orange)

## Overview

RepoLens AI inspects a GitHub repository, builds structured repository context, asks an AI model to analyze the project, and persists the resulting analysis for later retrieval.

The project is designed as a backend-first production exercise: external API integration, typed request/response models, explicit service boundaries, async database access, domain-specific error handling, and AI output validation are separated instead of being packed into route handlers.

## Current capabilities

- Inspect a public GitHub repository through the GitHub API
- Normalize repository metadata into typed response models
- Build repository context for AI analysis
- Generate structured AI analysis through Gemini
- Persist analyses in PostgreSQL with async SQLAlchemy
- Retrieve saved analyses by ID
- Map GitHub, AI, validation, and persistence failures to explicit HTTP responses
- Expose a FastAPI health endpoint and interactive OpenAPI documentation

## Architecture

```text
Client
  |
  v
FastAPI routers
  |
  +--> GitHub service ------> GitHub API
  |
  +--> Analysis service ----> Context builder ----> AI service ----> Gemini
  |                                |
  |                                v
  +--------------------------> PostgreSQL
```

The codebase follows a layered structure:

```text
app/
├── core/       # settings and domain exceptions
├── db/         # async SQLAlchemy session/base
├── models/     # persistence models
├── routers/    # HTTP endpoints
├── schemas/    # request/response contracts
├── services/   # GitHub, analysis, context and AI logic
└── main.py     # FastAPI application
migrations/     # Alembic migrations
```

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/github/repository` | Inspect a GitHub repository |
| POST | `/analyses` | Create and persist an AI repository analysis |
| GET | `/analyses/{analysis_id}` | Retrieve a saved analysis |
| POST | `/debug/ai` | Exercise the AI analysis layer with sample context |

Interactive API docs are available at `/docs` when the service is running.

## Configuration

The application reads configuration from a project-root `.env` file.

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/repolens
GITHUB_TOKEN=your_optional_github_token
GEMINI_API_KEY=your_gemini_api_key
AI_MODEL=your_gemini_model
```

Never commit real credentials.

## Local development

Create and activate a virtual environment, install the project dependencies, configure `.env`, then run migrations and start FastAPI.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

> Dependency packaging is still being cleaned up in this repository. See the roadmap below before treating the current setup as a production deployment recipe.

## Engineering decisions

- **Async database access:** SQLAlchemy's async session is used across request handling.
- **Service boundaries:** HTTP concerns live in routers while GitHub, context-building, AI, and persistence logic live in services.
- **Typed contracts:** Pydantic schemas define API and AI-facing structures.
- **Explicit failure mapping:** GitHub rate limits/not-found errors and AI failures are represented as domain exceptions and converted to appropriate HTTP responses.
- **Environment-driven configuration:** `pydantic-settings` loads runtime configuration from environment variables / `.env`.

## Roadmap

The following items are planned work, not claims about the current implementation:

- [ ] Rebuild dependency management into a reproducible package definition
- [ ] Add automated tests for GitHub, analysis, and AI service boundaries
- [ ] Add CI for linting, type checks, and tests
- [ ] Add Docker-based local environment
- [ ] Add authentication/rate limiting for hosted use
- [ ] Add richer repository signals and analysis history
- [ ] Add evaluation coverage for AI analysis quality
- [ ] Add observability and deployment documentation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Feature work should start from an issue and land through a focused pull request.

## Project status

RepoLens AI is under active development. The repository intentionally distinguishes implemented functionality from planned production hardening work.

---

Built as a Full-Stack AI engineering portfolio project focused on backend architecture, API integration, persistence, and structured AI workflows.
