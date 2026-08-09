import pytest
from httpx import AsyncClient


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
