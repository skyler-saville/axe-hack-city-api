from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from axe_hack_city.controllers.game_session_controller import GameSessionController
from axe_hack_city.models.game_session_model import GameSession
from axe_hack_city.schemas.gameplay_schema import GameplayCommandInputSchema
from axe_hack_city.services.gameplay_service import GameplaySessionService


def _build_test_session_factory(tmp_path) -> sessionmaker:
    database_url = f"sqlite:///{tmp_path / 'smoke.db'}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    GameSession.__table__.create(bind=engine, checkfirst=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_smoke_game_session_and_gameplay_flow(tmp_path) -> None:
    testing_session_factory = _build_test_session_factory(tmp_path)
    db = testing_session_factory()
    controller = GameSessionController(db)
    gameplay_service = GameplaySessionService(db)

    try:
        created_session = controller.create_session(
            GameSession(name="Smoke Session", status="ready", owner_user_id=1)
        )

        command_result = gameplay_service.submit_command(
            created_session.id,
            GameplayCommandInputSchema(raw_command="move market"),
            current_user_id=1,
        )
        assert command_result.success is True

        state = gameplay_service.get_state_snapshot(created_session.id, current_user_id=1)
        assert state.status == "at:market"
        assert state.turn_number == 1

        log = gameplay_service.get_recent_log(created_session.id, current_user_id=1)
        assert len(log.entries) == 1
        assert log.entries[0].success is True
    finally:
        db.close()


def test_smoke_gameplay_rejects_invalid_command(tmp_path) -> None:
    testing_session_factory = _build_test_session_factory(tmp_path)
    db = testing_session_factory()
    controller = GameSessionController(db)
    gameplay_service = GameplaySessionService(db)

    try:
        created_session = controller.create_session(
            GameSession(name="Bad Command Session", status="ready", owner_user_id=1)
        )

        command_result = gameplay_service.submit_command(
            created_session.id,
            GameplayCommandInputSchema(raw_command="dance"),
            current_user_id=1,
        )
        assert command_result.success is False
        assert len(command_result.parse_errors) > 0
    finally:
        db.close()
