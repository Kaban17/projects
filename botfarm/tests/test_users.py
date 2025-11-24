from uuid import UUID, uuid4

import pytest

from app.schemas.user import DomainEnum, EnvEnum, UserCreate


@pytest.mark.asyncio
class TestUserEndpoints:
    async def test_health_check(self, test_client):
        response = await test_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    async def test_create_user_success(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "test@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        response = await test_client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["login"] == "test@example.com"
        assert UUID(data["id"])
        assert data["project_id"] == str(project_id)
        assert data["env"] == "prod"
        assert data["domain"] == "canary"
        assert data["created_at"] is not None
        assert data["locktime"] is None

    async def test_create_user_duplicate_login(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "duplicate@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        await test_client.post("/api/v1/users/", json=user_data)
        response = await test_client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Login already exists"

    async def test_create_user_invalid_env(self, test_client):
        user_data = {
            "login": "invalid@example.com",
            "password": "testpass123",
            "project_id": str(uuid4()),
            "env": "invalid",
            "domain": DomainEnum.CANARY.value,
        }
        response = await test_client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 422

    async def test_create_user_short_password(self, test_client):
        user_data = {
            "login": "short@example.com",
            "password": "short",
            "project_id": str(uuid4()),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        response = await test_client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 422

    async def test_list_users_empty(self, test_client):
        response = await test_client.get("/api/v1/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 0

    async def test_list_users_after_create(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "list@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.STAGE.value,
            "domain": DomainEnum.REGULAR.value,
        }
        await test_client.post("/api/v1/users/", json=user_data)
        response = await test_client.get("/api/v1/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 1
        assert users[0]["login"] == "list@example.com"

    async def test_acquire_lock_success(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "lock@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        create_resp = await test_client.post("/api/v1/users/", json=user_data)
        user_id = UUID(create_resp.json()["id"])
        response = await test_client.post(f"/api/v1/users/{user_id}/acquire")
        assert response.status_code == 200
        assert response.json()["message"] == "User locked successfully"

    async def test_acquire_lock_already_locked(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "locked@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        create_resp = await test_client.post("/api/v1/users/", json=user_data)
        user_id = UUID(create_resp.json()["id"])
        await test_client.post(f"/api/v1/users/{user_id}/acquire")
        response = await test_client.post(f"/api/v1/users/{user_id}/acquire")
        assert response.status_code == 409

    async def test_acquire_lock_nonexistent_user(self, test_client):
        fake_id = uuid4()
        response = await test_client.post(f"/api/v1/users/{fake_id}/acquire")
        assert response.status_code == 409

    async def test_release_lock_success_locked(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "release@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        create_resp = await test_client.post("/api/v1/users/", json=user_data)
        user_id = UUID(create_resp.json()["id"])
        await test_client.post(f"/api/v1/users/{user_id}/acquire")
        response = await test_client.post(f"/api/v1/users/{user_id}/release")
        assert response.status_code == 200

    async def test_release_lock_idempotent_unlocked(self, test_client):
        project_id = uuid4()
        user_data = {
            "login": "idempotent@example.com",
            "password": "testpass123",
            "project_id": str(project_id),
            "env": EnvEnum.PROD.value,
            "domain": DomainEnum.CANARY.value,
        }
        create_resp = await test_client.post("/api/v1/users/", json=user_data)
        user_id = UUID(create_resp.json()["id"])
        response = await test_client.post(f"/api/v1/users/{user_id}/release")
        assert response.status_code == 200

    async def test_release_lock_nonexistent_user(self, test_client):
        fake_id = uuid4()
        response = await test_client.post(f"/api/v1/users/{fake_id}/release")
        assert response.status_code == 404
