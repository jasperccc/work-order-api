from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)
app.include_router(users_router)


@app.exception_handler(EmailAlreadyRegisteredError)
async def handle_email_already_registered(
    _request: Request,
    exc: EmailAlreadyRegisteredError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidCredentialsError)
async def handle_invalid_credentials(
    _request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(InvalidTokenError)
async def handle_invalid_token(
    _request: Request,
    exc: InvalidTokenError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
async def info_check() -> dict[str, str]:
    return {"name": settings.app_name, "environment": settings.environment}
