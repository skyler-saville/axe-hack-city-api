from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from axe_hack_city.database.session import get_session
from axe_hack_city.main import app
from axe_hack_city.models.base import Base
from axe_hack_city.models.game_session_model import GameSession  # noqa: F401


def _build_test_session_factory(tmp_path) -> sessionmaker:
    database_url = f"sqlite:///{tmp_path / 'smoke.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_smoke_game_session_and_gameplay_flow(tmp_path) -> None:
    testing_session_factory = _build_test_session_factory(tmp_path)

    def _override_get_session() -> Generator[Session, None, None]:
        db = testing_session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = _override_get_session

    with TestClient(app) as client:
        create_response = client.post(
            "/api/sessions/",
            json={"name": "Smoke Session", "status": "ready"},
        )
        assert create_response.status_code == 200
        session_id = create_response.json()["id"]

        command_response = client.post(
            f"/api/sessions/{session_id}/commands",
            json={"raw_command": "move market"},
        )
        assert command_response.status_code == 200
        assert command_response.json()["success"] is True

        state_response = client.get(f"/api/sessions/{session_id}/state")
        assert state_response.status_code == 200
        state_payload = state_response.json()
        assert state_payload["status"] == "at:market"
        assert state_payload["turn_number"] == 1

        log_response = client.get(f"/api/sessions/{session_id}/log")
        assert log_response.status_code == 200
        entries = log_response.json()["entries"]
        assert len(entries) == 1
        assert entries[0]["success"] is True

    app.dependency_overrides.clear()


def test_smoke_gameplay_rejects_invalid_command(tmp_path) -> None:
    testing_session_factory = _build_test_session_factory(tmp_path)

    def _override_get_session() -> Generator[Session, None, None]:
        db = testing_session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = _override_get_session

    with TestClient(app) as client:
        create_response = client.post(
            "/api/sessions/",
            json={"name": "Bad Command Session", "status": "ready"},
        )
        session_id = create_response.json()["id"]

        command_response = client.post(
            f"/api/sessions/{session_id}/commands",
            json={"raw_command": "dance"},
        )

        assert command_response.status_code == 200
        response_payload = command_response.json()
        assert response_payload["success"] is False
        assert len(response_payload["parse_errors"]) > 0

    app.dependency_overrides.clear()
