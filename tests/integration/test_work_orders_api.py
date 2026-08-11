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


@pytest.mark.asyncio
async def test_list_work_orders_returns_only_current_users_orders(
    api_client: AsyncClient,
) -> None:
    register1_response = await api_client.post(
        "/api/auth/register", json={"email": "A@163.com", "password": "12345678"}
    )
    assert register1_response.status_code == 201
    user_a_id = register1_response.json()["id"]

    login1_response = await api_client.post(
        "/api/auth/login", json={"email": "A@163.com", "password": "12345678"}
    )
    assert login1_response.status_code == 200
    token_a = login1_response.json()["access_token"]

    register2_response = await api_client.post(
        "/api/auth/register", json={"email": "B@163.com", "password": "12345678"}
    )
    assert register2_response.status_code == 201

    login2_response = await api_client.post(
        "/api/auth/login", json={"email": "B@163.com", "password": "12345678"}
    )
    assert login2_response.status_code == 200
    token_b = login2_response.json()["access_token"]

    create_a_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={
            "Authorization": f"Bearer {token_a}",
        },
    )

    create_b_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户B的工单"},
        headers={
            "Authorization": f"Bearer {token_b}",
        },
    )
    assert create_a_response.status_code == 201
    assert create_b_response.status_code == 201

    response = await api_client.get(
        "/api/work-orders",
        headers={
            "Authorization": f"Bearer {token_a}",
        },
    )
    assert response.status_code == 200

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body[0]["title"] == "用户A的工单"
    assert response_body[0]["owner_id"] == user_a_id
