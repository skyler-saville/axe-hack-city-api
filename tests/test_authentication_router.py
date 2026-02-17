from datetime import timedelta
from typing import Any, Dict, List

from fastapi.testclient import TestClient

from axe_hack_city.main import app
from axe_hack_city.routers import authentication_router
from axe_hack_city.services.auth_service import create_access_token, hash_password


class DummyUser:
    def __init__(self, username: str, password: str, is_active: bool = True) -> None:
        self.username = username
        self.password = password
        self.is_active = is_active


class FakeUserController:
    users: Dict[str, DummyUser] = {}

    def __init__(self, _session: Any):
        pass

    def list_users(self, **filters: Any) -> List[DummyUser]:
        username = filters.get("username")
        user = self.users.get(username)
        return [user] if user else []


def _setup_controller(monkeypatch) -> None:
    monkeypatch.setattr(authentication_router, "UserController", FakeUserController)


def test_login_success(monkeypatch) -> None:
    _setup_controller(monkeypatch)
    FakeUserController.users = {
        "johndoe": DummyUser("johndoe", hash_password("secret-password"), True)
    }

    client = TestClient(app)
    response = client.post(
        "/api/auth/token", data={"username": "johndoe", "password": "secret-password"}
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_bad_password(monkeypatch) -> None:
    _setup_controller(monkeypatch)
    FakeUserController.users = {
        "johndoe": DummyUser("johndoe", hash_password("secret-password"), True)
    }

    client = TestClient(app)
    response = client.post(
        "/api/auth/token", data={"username": "johndoe", "password": "wrong-password"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


def test_users_me_invalid_token(monkeypatch) -> None:
    _setup_controller(monkeypatch)
    FakeUserController.users = {}

    client = TestClient(app)
    response = client.get(
        "/api/auth/users/me", headers={"Authorization": "Bearer definitely-invalid"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_users_me_expired_token(monkeypatch) -> None:
    _setup_controller(monkeypatch)
    FakeUserController.users = {
        "johndoe": DummyUser("johndoe", hash_password("secret-password"), True)
    }

    expired_token = create_access_token(
        data={"sub": "johndoe"}, expires_delta=timedelta(minutes=-1)
    )

    client = TestClient(app)
    response = client.get(
        "/api/auth/users/me", headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_users_me_inactive_user(monkeypatch) -> None:
    _setup_controller(monkeypatch)
    FakeUserController.users = {
        "alice": DummyUser("alice", hash_password("secret-password"), False)
    }

    token = create_access_token(data={"sub": "alice"})

    client = TestClient(app)
    response = client.get(
        "/api/auth/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"
