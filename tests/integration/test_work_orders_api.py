import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_work_order_assigns_current_user_as_owner(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register", json={"email": "123@163.com", "password": "12345678"}
    )
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    login_response = await api_client.post(
        "/api/auth/login", json={"email": "123@163.com", "password": "12345678"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    work_order_response = await api_client.post(
        "/api/work-orders",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={"title": "数据库连接失败"},
    )

    assert work_order_response.status_code == 201
    response_body = work_order_response.json()

    assert isinstance(response_body["id"], int)
    assert response_body["title"] == "数据库连接失败"
    assert response_body["status"] == "open"
    assert response_body["owner_id"] == user_id
    assert "created_at" in response_body
