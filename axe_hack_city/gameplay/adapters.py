from typing import Protocol

from sqlalchemy.orm import Session

from ..models.game_session_model import GameSession
from ..services.game_session_state_service import GameSessionStateService
from .types import DispatchContext


class GameplayStateAdapter(Protocol):
    def get_context(self, session_id: int) -> DispatchContext:
        ...

    def apply_state_changes(self, session_id: int, state_changes: dict) -> None:
        ...


class SQLAlchemyGameplayAdapter:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_context(self, session_id: int) -> DispatchContext:
        session = self.db_session.get(GameSession, session_id)
        if session is None:
            raise ValueError("Session not found")

        return DispatchContext(
            session_id=session.id,
            session_name=session.name,
            status=session.status,
        )

    def apply_state_changes(self, session_id: int, state_changes: dict) -> None:
        if not state_changes:
            return

        session = self.db_session.get(GameSession, session_id)
        if session is None:
            raise ValueError("Session not found")

        transition = GameSessionStateService.transition_from_state_changes(state_changes)
        GameSessionStateService.apply_validated_transition(session, transition)
        self.db_session.commit()
