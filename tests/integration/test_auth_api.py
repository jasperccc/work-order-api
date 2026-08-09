import jwt
import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_register_returns_created_user_without_password(
    api_client: AsyncClient,
) -> None:
    response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "api-user@example.com",
            "password": "secure-password",
        },
    )

    assert response.status_code == 201

    response_body = response.json()

    assert isinstance(response_body["id"], int)
    assert response_body["email"] == "api-user@example.com"
    assert response_body["is_active"] is True
    assert "created_at" in response_body
    assert "password" not in response_body
    assert "password_hash" not in response_body


@pytest.mark.asyncio
async def test_register_returns_conflict_for_duplicate_email(
    api_client: AsyncClient,
) -> None:
    first_response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "duplicate-api@example.com",
            "password": "secure-password",
        },
    )

    assert first_response.status_code == 201

    second_response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "duplicate-api@example.com",
            "password": "secure-password",
        },
    )

    assert second_response.status_code == 409
    assert second_response.json() == {"detail": "邮箱已注册"}


@pytest.mark.asyncio
async def test_register_rejects_invalid_email(
    api_client: AsyncClient,
) -> None:
    response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "not-an-email",
            "password": "secure-password",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_rejects_short_password(
    api_client: AsyncClient,
) -> None:
    response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_returns_access_token_for_valid_credentials(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "login-user@example.com", "password": "secure-password"},
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "login-user@example.com", "password": "secure-password"},
    )

    assert login_response.status_code == 200
    assert isinstance(login_response.json()["access_token"], str)
    assert login_response.json()["token_type"] == "bearer"

    access_token = login_response.json()["access_token"]

    payload = jwt.decode(
        access_token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(register_response.json()["id"])
    assert payload["exp"] > payload["iat"]


@pytest.mark.asyncio
async def test_login_returns_unauthorized_for_wrong_password(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "login-user@example.com", "password": "correct-password"},
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "login-user@example.com", "password": "wrong-password"},
    )

    assert login_response.status_code == 401
    assert login_response.json() == {"detail": "邮箱或密码错误"}


@pytest.mark.asyncio
async def test_login_returns_unauthorized_for_unknown_email(
    api_client: AsyncClient,
) -> None:
    response = await api_client.post(
        "/api/auth/login",
        json={"email": "unknown@example.com", "password": "secure-password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "邮箱或密码错误"}
    assert response.headers["www-authenticate"] == "Bearer"
