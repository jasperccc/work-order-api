import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import UserRole
from app.models import User


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


@pytest.mark.asyncio
async def test_get_work_order_returns_current_users_work_order(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register", json={"email": "A@163.com", "password": "12345678"}
    )

    user_id = register_response.json()["id"]

    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login", json={"email": "A@163.com", "password": "12345678"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    create_response = await api_client.post(
        "/api/work-orders",
        json={"title": "需要查询的工单"},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert create_response.status_code == 201
    work_order_id = create_response.json()["id"]

    response = await api_client.get(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == work_order_id
    assert response_body["title"] == "需要查询的工单"
    assert response_body["owner_id"] == user_id


@pytest.mark.asyncio
async def test_get_work_order_returns_404_for_another_users_work_order(
    api_client: AsyncClient,
) -> None:
    a_register_response = await api_client.post(
        "/api/auth/register", json={"email": "A@163.com", "password": "12345678"}
    )
    assert a_register_response.status_code == 201

    a_login_response = await api_client.post(
        "/api/auth/login", json={"email": "A@163.com", "password": "12345678"}
    )
    assert a_login_response.status_code == 200
    a_access_token = a_login_response.json()["access_token"]

    b_register_response = await api_client.post(
        "/api/auth/register", json={"email": "B@163.com", "password": "12345678"}
    )
    assert b_register_response.status_code == 201

    b_login_response = await api_client.post(
        "/api/auth/login", json={"email": "B@163.com", "password": "12345678"}
    )
    assert b_login_response.status_code == 200
    b_access_token = b_login_response.json()["access_token"]

    create_a_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={
            "Authorization": f"Bearer {a_access_token}",
        },
    )
    assert create_a_response.status_code == 201
    work_order_id = create_a_response.json()["id"]

    response = await api_client.get(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {b_access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "工单不存在"}


@pytest.mark.asyncio
async def test_update_work_order_updates_current_users_work_order(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register", json={"email": "A@163.com", "password": "12345678"}
    )
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    login_response = await api_client.post(
        "/api/auth/login", json={"email": "A@163.com", "password": "12345678"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    create_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert create_response.status_code == 201
    work_order_id = create_response.json()["id"]

    response = await api_client.patch(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "修改后的工单"},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == work_order_id
    assert response_body["title"] == "修改后的工单"
    assert response_body["owner_id"] == user_id


@pytest.mark.asyncio
async def test_update_work_order_returns_404_for_another_users_work_order(
    api_client: AsyncClient,
) -> None:
    a_register_response = await api_client.post(
        "/api/auth/register", json={"email": "A@163.com", "password": "12345678"}
    )
    assert a_register_response.status_code == 201

    a_login_response = await api_client.post(
        "/api/auth/login", json={"email": "A@163.com", "password": "12345678"}
    )
    assert a_login_response.status_code == 200
    a_access_token = a_login_response.json()["access_token"]

    b_register_response = await api_client.post(
        "/api/auth/register", json={"email": "B@163.com", "password": "12345678"}
    )
    assert b_register_response.status_code == 201

    b_login_response = await api_client.post(
        "/api/auth/login", json={"email": "B@163.com", "password": "12345678"}
    )
    assert b_login_response.status_code == 200
    b_access_token = b_login_response.json()["access_token"]

    create_a_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={
            "Authorization": f"Bearer {a_access_token}",
        },
    )
    assert create_a_response.status_code == 201
    work_order_id = create_a_response.json()["id"]

    response = await api_client.patch(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {b_access_token}"},
        json={"title": "非法修改"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "工单不存在"}

    get_response = await api_client.get(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {a_access_token}"},
    )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "用户A的工单"


@pytest.mark.asyncio
async def test_delete_work_order_deletes_current_users_work_order(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register", json={"email": "ccc@163.com", "password": "12345678"}
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login", json={"email": "ccc@163.com", "password": "12345678"}
    )

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    create_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert create_response.status_code == 201
    work_order_id = create_response.json()["id"]

    delete_response = await api_client.delete(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = await api_client.get(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "工单不存在"}


@pytest.mark.asyncio
async def test_delete_work_order_returns_404_for_another_users_work_order(
    api_client: AsyncClient,
) -> None:
    a_register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "A@163.com", "password": "12345678"},
    )
    assert a_register_response.status_code == 201

    a_login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "A@163.com", "password": "12345678"},
    )
    assert a_login_response.status_code == 200
    a_access_token = a_login_response.json()["access_token"]

    b_register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "B@163.com", "password": "12345678"},
    )
    assert b_register_response.status_code == 201

    b_login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "B@163.com", "password": "12345678"},
    )
    assert b_login_response.status_code == 200
    b_access_token = b_login_response.json()["access_token"]

    create_a_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={"Authorization": f"Bearer {a_access_token}"},
    )
    assert create_a_response.status_code == 201
    work_order_id = create_a_response.json()["id"]

    delete_response = await api_client.delete(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {b_access_token}"},
    )

    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "工单不存在"}

    get_response = await api_client.get(
        f"/api/work-orders/{work_order_id}",
        headers={"Authorization": f"Bearer {a_access_token}"},
    )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "用户A的工单"


@pytest.mark.asyncio
async def test_list_all_work_orders_returns_403_for_normal_user(
    api_client: AsyncClient,
) -> None:
    register_response = await api_client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "password": "12345678",
        },
    )
    assert register_response.status_code == 201

    login_response = await api_client.post(
        "/api/auth/login",
        json={
            "email": "user@example.com",
            "password": "12345678",
        },
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    response = await api_client.get(
        "/api/admin/work-orders",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "权限不足"}


@pytest.mark.asyncio
async def test_list_all_work_orders_returns_all_work_orders_for_admin(
    api_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    user_a_register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "A@163.com", "password": "12345678"},
    )
    assert user_a_register_response.status_code == 201

    user_a_login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "A@163.com", "password": "12345678"},
    )
    assert user_a_login_response.status_code == 200
    user_a_token = user_a_login_response.json()["access_token"]

    user_b_register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "B@163.com", "password": "12345678"},
    )
    assert user_b_register_response.status_code == 201

    user_b_login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "B@163.com", "password": "12345678"},
    )
    assert user_b_login_response.status_code == 200
    user_b_token = user_b_login_response.json()["access_token"]

    admin_register_response = await api_client.post(
        "/api/auth/register",
        json={"email": "admin@163.com", "password": "12345678"},
    )
    assert admin_register_response.status_code == 201
    admin_user_id = admin_register_response.json()["id"]

    admin_user = await db_session.get(User, admin_user_id)
    assert admin_user is not None
    admin_user.role = UserRole.ADMIN
    await db_session.commit()

    admin_login_response = await api_client.post(
        "/api/auth/login",
        json={"email": "admin@163.com", "password": "12345678"},
    )
    assert admin_login_response.status_code == 200
    admin_token = admin_login_response.json()["access_token"]

    create_a_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户A的工单"},
        headers={"Authorization": f"Bearer {user_a_token}"},
    )
    assert create_a_response.status_code == 201

    create_b_response = await api_client.post(
        "/api/work-orders",
        json={"title": "用户B的工单"},
        headers={"Authorization": f"Bearer {user_b_token}"},
    )
    assert create_b_response.status_code == 201

    response = await api_client.get(
        "/api/admin/work-orders",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200

    response_body = response.json()
    assert len(response_body) == 2
    assert {item["title"] for item in response_body} == {
        "用户A的工单",
        "用户B的工单",
    }


@pytest.mark.asyncio
async def test_list_all_work_orders_requires_authentication(
    api_client: AsyncClient,
) -> None:
    response = await api_client.get("/api/admin/work-orders")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
