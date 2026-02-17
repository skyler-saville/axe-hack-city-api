from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from axe_hack_city.database.session import get_session
from axe_hack_city.main import app
from axe_hack_city.models.game_session_model import GameSession
from axe_hack_city.routers.authentication_router import User, get_current_active_user


def _build_session_factory(tmp_path) -> sessionmaker:
    database_url = f"sqlite:///{tmp_path / 'ownership.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    GameSession.__table__.create(bind=engine, checkfirst=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_db(factory: sessionmaker):
    def _get_db() -> Generator[Session, None, None]:
        db = factory()
        try:
            yield db
        finally:
            db.close()

    return _get_db


def _override_user(user_id: int, username: str):
    async def _get_user() -> User:
        return User(id=user_id, username=username, disabled=False)

    return _get_user


def test_session_access_is_limited_to_owner(tmp_path) -> None:
    factory = _build_session_factory(tmp_path)
    app.dependency_overrides[get_session] = _override_db(factory)

    try:
        app.dependency_overrides[get_current_active_user] = _override_user(1, "owner")
        with TestClient(app) as client:
            create_response = client.post(
                "/api/sessions/",
                json={
                    "name": "Owner Session",
                    "status": "ready",
                    "state": {},
                },
            )
            assert create_response.status_code == 200
            created = create_response.json()
            session_id = created["id"]
            assert created["owner_user_id"] == 1

            read_own_response = client.get(f"/api/sessions/{session_id}")
            assert read_own_response.status_code == 200

            update_own_response = client.put(
                f"/api/sessions/{session_id}",
                json={"status": "in-progress"},
            )
            assert update_own_response.status_code == 200

            gameplay_own_response = client.post(
                f"/api/sessions/{session_id}/commands",
                json={"raw_command": "move market"},
            )
            assert gameplay_own_response.status_code == 200

            app.dependency_overrides[get_current_active_user] = _override_user(2, "other")

            read_other_response = client.get(f"/api/sessions/{session_id}")
            assert read_other_response.status_code == 404

            update_other_response = client.put(
                f"/api/sessions/{session_id}",
                json={"status": "hijacked"},
            )
            assert update_other_response.status_code == 404

            gameplay_other_response = client.post(
                f"/api/sessions/{session_id}/commands",
                json={"raw_command": "move market"},
            )
            assert gameplay_other_response.status_code == 404
    finally:
        app.dependency_overrides.clear()
