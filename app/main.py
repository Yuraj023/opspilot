from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.approvals import router as approvals_router
from app.api.health import router as health_router
from app.api.incidents import router as incidents_router
from app.api.runs import router as runs_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import init_db

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Agentic AI system for software incident investigation and controlled remediation.",
    lifespan=lifespan,
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(incidents_router, prefix=settings.api_prefix)
app.include_router(runs_router, prefix=settings.api_prefix)
app.include_router(approvals_router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
def root():
    return {
        "name": settings.app_name,
        "status": "online",
        "version": "0.1.0",
    }