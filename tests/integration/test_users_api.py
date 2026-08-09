from datetime import UTC, datetime, timedelta

import jwt
import pytest
from httpx import AsyncClient

from app.config import settings
from app.security import create_access_token


@pytest.mark.asyncio
async def test_get_current_user_requires_authentication(
    api_client: AsyncClient,
) -> None:
    response = await api_client.get("/api/users/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_get_current_user_returns_authenticated_user(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register", json={"email": "123@163.com", "password": "12345678"}
    )

    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login", json={"email": "123@163.com", "password": "12345678"}
    )

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    response = await api_client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == register_response.json()


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(api_client: AsyncClient) -> None:
    response = await api_client.get(
        "/api/users/me",
        headers={
            "Authorization": "Bearer not-a-valid-token",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "认证凭证无效"}
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_get_current_user_rejects_token_for_unknown_user(
    api_client: AsyncClient,
) -> None:
    access_token = create_access_token("999999")
    response = await api_client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "认证凭证无效"}
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_get_current_user_rejects_expired_token(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "expired-token@example.com",
            "password": "secure-password",
        },
    )
    assert register_response.status_code == 201

    now = datetime.now(UTC)

    expired_token = jwt.encode(
        {
            "sub": str(register_response.json()["id"]),
            "iat": now - timedelta(minutes=2),
            "exp": now - timedelta(minutes=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = await api_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "认证凭证无效"}
    assert response.headers["www-authenticate"] == "Bearer"
