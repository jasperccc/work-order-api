from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
async def info_check() -> dict[str, str]:
    return {"name": settings.app_name, "environment": settings.environment}
