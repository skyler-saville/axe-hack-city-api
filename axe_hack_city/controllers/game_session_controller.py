from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.game_session_model import GameSession


class GameSessionController:
    """Controller for managing GameSession entities."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(session, GameSession)

    def create_session(self, session: GameSession) -> GameSession:
        return self.repository.create(session)

    def get_session(self, session_id: int) -> GameSession:
        return self.repository.get(session_id)

    def update_session(self, session: GameSession) -> GameSession:
        return self.repository.update(session)

    def delete_session(self, session_id: int) -> None:
        self.repository.delete(session_id)

    def list_sessions(self, **filters) -> List[GameSession]:
        return self.repository.list(**filters)
