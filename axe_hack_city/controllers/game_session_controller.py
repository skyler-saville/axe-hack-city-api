from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..gameplay.adapters import SQLAlchemyGameplayAdapter
from ..gameplay.service import GameplayService
from ..gameplay.types import ActionResult
from ..models.game_session_model import GameSession
from ..schemas.game_session_schema import GameStateTransitionSchema
from ..services.game_session_state_service import GameSessionStateService


class GameSessionController:
    """Controller for managing GameSession entities."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(session, GameSession)
        self.gameplay_service = GameplayService(SQLAlchemyGameplayAdapter(session))

    def create_session(self, session: GameSession) -> GameSession:
        if session.turn_metadata is None:
            session.turn_metadata = {"turn_number": 0, "last_action_timestamp": None}
        if session.active_encounters is None:
            session.active_encounters = {"objectives": [], "encounters": []}
        if session.player_context is None:
            session.player_context = {}
        if session.state_payload is None:
            session.state_payload = {}
        return self.repository.create(session)

    def get_session(self, session_id: int) -> GameSession:
        return self.repository.get(session_id)

    def update_session(self, session: GameSession) -> GameSession:
        return self.repository.update(session)

    def update_session_fields(self, session_id: int, updates: dict) -> Optional[GameSession]:
        session = self.repository.get(session_id)
        if session is None:
            return None

        allowed_fields = {"name", "status"}
        disallowed_fields = set(updates.keys()) - allowed_fields
        if disallowed_fields:
            raise ValueError(
                "Unsupported update fields: " + ", ".join(sorted(disallowed_fields))
            )

        for field, value in updates.items():
            setattr(session, field, value)

        return self.repository.update(session)

    def apply_state_transition(
        self, session_id: int, transition: GameStateTransitionSchema
    ) -> Optional[GameSession]:
        session = self.repository.get(session_id)
        if session is None:
            return None

        GameSessionStateService.apply_validated_transition(session, transition)
        return self.repository.update(session)

    def apply_state_transition_from_changes(
        self, session_id: int, state_changes: Dict[str, Any]
    ) -> Optional[GameSession]:
        transition = GameSessionStateService.transition_from_state_changes(
            state_changes=state_changes
        )
        return self.apply_state_transition(session_id=session_id, transition=transition)

    def delete_session(self, session_id: int) -> None:
        self.repository.delete(session_id)

    def list_sessions(self, **filters) -> List[GameSession]:
        return self.repository.list(**filters)

    def execute_player_command(self, session_id: int, command: str) -> ActionResult:
        return self.gameplay_service.execute(session_id=session_id, raw_input=command)
