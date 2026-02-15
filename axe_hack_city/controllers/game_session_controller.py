from typing import List, Optional

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..gameplay.adapters import SQLAlchemyGameplayAdapter
from ..gameplay.service import GameplayService
from ..gameplay.types import ActionResult
from ..models.game_session_model import GameSession


class GameSessionController:
    """Controller for managing GameSession entities."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(session, GameSession)
        self.gameplay_service = GameplayService(SQLAlchemyGameplayAdapter(session))

    def create_session(self, session: GameSession) -> GameSession:
        return self.repository.create(session)

    def get_session(self, session_id: int) -> GameSession:
        return self.repository.get(session_id)

    def update_session(self, session: GameSession) -> GameSession:
        return self.repository.update(session)

    def update_session_fields(self, session_id: int, updates: dict) -> Optional[GameSession]:
        session = self.repository.get(session_id)
        if session is None:
            return None

        for field, value in updates.items():
            setattr(session, field, value)

        return self.repository.update(session)

    def delete_session(self, session_id: int) -> None:
        self.repository.delete(session_id)

    def list_sessions(self, **filters) -> List[GameSession]:
        return self.repository.list(**filters)

    def execute_player_command(self, session_id: int, command: str) -> ActionResult:
        return self.gameplay_service.execute(session_id=session_id, raw_input=command)
