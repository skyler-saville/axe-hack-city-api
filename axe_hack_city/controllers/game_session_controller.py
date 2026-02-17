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

    def get_session(self, session_id: int, current_user_id: int) -> Optional[GameSession]:
        return self._get_owned_session(session_id=session_id, current_user_id=current_user_id)

    def update_session(self, session: GameSession) -> GameSession:
        return self.repository.update(session)

    def update_session_fields(
        self, session_id: int, updates: dict, current_user_id: int
    ) -> Optional[GameSession]:
        session = self._get_owned_session(session_id=session_id, current_user_id=current_user_id)
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
        self,
        session_id: int,
        transition: GameStateTransitionSchema,
        current_user_id: int,
    ) -> Optional[GameSession]:
        session = self._get_owned_session(session_id=session_id, current_user_id=current_user_id)
        if session is None:
            return None

        GameSessionStateService.apply_validated_transition(session, transition)
        return self.repository.update(session)

    def apply_state_transition_from_changes(
        self, session_id: int, state_changes: Dict[str, Any], current_user_id: int
    ) -> Optional[GameSession]:
        transition = GameSessionStateService.transition_from_state_changes(
            state_changes=state_changes
        )
        return self.apply_state_transition(
            session_id=session_id,
            transition=transition,
            current_user_id=current_user_id,
        )

    def delete_session(self, session_id: int, current_user_id: int) -> bool:
        session = self._get_owned_session(session_id=session_id, current_user_id=current_user_id)
        if session is None:
            return False
        self.repository.delete(session_id)
        return True

    def list_sessions(self, current_user_id: int, **filters: Any) -> List[GameSession]:
        return self.repository.list(owner_user_id=current_user_id, **filters)

    def execute_player_command(
        self, session_id: int, command: str, current_user_id: int
    ) -> ActionResult:
        session = self._get_owned_session(session_id=session_id, current_user_id=current_user_id)
        if session is None:
            raise ValueError("Session not found")
        return self.gameplay_service.execute(session_id=session.id, raw_input=command)

    def _get_owned_session(
        self, session_id: int, current_user_id: int
    ) -> Optional[GameSession]:
        session = self.repository.get(session_id)
        if session is None:
            return None
        if session.owner_user_id != current_user_id:
            return None
        return session
