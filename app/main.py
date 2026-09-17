from fastapi import FastAPI
from app.routers.github import router as github_router
from app.routers.ai_debug import router as ai_debug_router

app = FastAPI(
    title="RepoLens AI",
    version="1.0.0",
)
app.include_router(github_router)
app.include_router(ai_debug_router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok"
    }