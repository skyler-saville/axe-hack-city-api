from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from ..gameplay.adapters import SQLAlchemyGameplayAdapter
from ..gameplay.service import GameplayService
from ..models.game_session_model import GameSession
from ..schemas.gameplay_schema import (
    GameplayCommandInputSchema,
    GameplayLogEntrySchema,
    GameplayLogResponseSchema,
    GameplayParseErrorSchema,
    GameplayStateSnapshotSchema,
    GameplayTurnOutcomeSchema,
    GameplayUiHintsSchema,
)


class GameplaySessionService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.command_service = GameplayService(SQLAlchemyGameplayAdapter(db_session))

    def submit_command(
        self,
        session_id: int,
        payload: GameplayCommandInputSchema,
        current_user_id: int,
    ) -> GameplayTurnOutcomeSchema:
        session = self._get_session_or_raise(session_id, current_user_id)
        raw_command = self._resolve_raw_command(payload)
        result = self.command_service.execute(session_id=session_id, raw_input=raw_command)

        self._append_log_entry(
            session,
            narration=result.narration,
            success=result.success,
            state_delta=result.state_changes,
        )

        parse_errors = [
            GameplayParseErrorSchema(field="command", message=message)
            for message in result.errors
        ]

        return GameplayTurnOutcomeSchema(
            narration=result.narration,
            state_delta=result.state_changes,
            ui_hints=self._derive_ui_hints(result.state_changes, result.narration),
            warnings=result.warnings,
            parse_errors=parse_errors,
            success=result.success,
        )

    def get_state_snapshot(
        self, session_id: int, current_user_id: int
    ) -> GameplayStateSnapshotSchema:
        session = self._get_session_or_raise(session_id, current_user_id)
        turn_metadata = session.turn_metadata or {}
        return GameplayStateSnapshotSchema(
            session_id=session.id,
            status=session.status,
            state_version=session.state_version,
            turn_number=turn_metadata.get("turn_number", 0),
            player_context=session.player_context or {},
            active_encounters=session.active_encounters or {},
            state_payload=session.state_payload or {},
        )

    def get_recent_log(
        self, session_id: int, current_user_id: int, limit: int = 20
    ) -> GameplayLogResponseSchema:
        session = self._get_session_or_raise(session_id, current_user_id)
        summary = session.action_log_summary or {}
        entries = summary.get("entries", [])
        selected_entries = entries[-limit:]

        parsed_entries: List[GameplayLogEntrySchema] = [
            GameplayLogEntrySchema.model_validate(entry) for entry in selected_entries
        ]

        return GameplayLogResponseSchema(session_id=session.id, entries=parsed_entries)

    def _resolve_raw_command(self, payload: GameplayCommandInputSchema) -> str:
        if payload.raw_command and payload.raw_command.strip():
            return payload.raw_command.strip()

        assert payload.structured_command is not None
        parts = [payload.structured_command.verb]
        if payload.structured_command.target:
            parts.append(payload.structured_command.target)
        parts.extend(payload.structured_command.args)
        return " ".join(parts)

    def _derive_ui_hints(
        self, state_changes: Dict[str, Any], narration: str
    ) -> GameplayUiHintsSchema:
        suggested_actions: List[str] = []
        highlighted_targets: List[str] = []

        if "status" in state_changes:
            suggested_actions.append("progress")

        if "active_encounters" in state_changes:
            suggested_actions.extend(["interact", "use"])
            encounters = state_changes.get("active_encounters") or []
            if isinstance(encounters, list):
                for encounter in encounters:
                    if isinstance(encounter, dict) and "name" in encounter:
                        highlighted_targets.append(str(encounter["name"]))

        lowered = narration.lower()
        if "move" in lowered or "travel" in lowered:
            suggested_actions.append("move")

        return GameplayUiHintsSchema(
            suggested_actions=sorted(set(suggested_actions)),
            highlighted_targets=sorted(set(highlighted_targets)),
        )

    def _append_log_entry(
        self,
        session: GameSession,
        narration: str,
        success: bool,
        state_delta: Dict[str, Any],
    ) -> None:
        summary = session.action_log_summary or {"entries": []}
        entries = list(summary.get("entries", []))
        turn_number = (session.turn_metadata or {}).get("turn_number", 0)

        entries.append(
            {
                "turn_number": turn_number,
                "narration": narration,
                "success": success,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "state_delta": state_delta,
            }
        )

        session.action_log_summary = {
            "entries": entries[-100:],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self.db_session.add(session)
        self.db_session.commit()

    def _get_session_or_raise(self, session_id: int, current_user_id: int) -> GameSession:
        session = self.db_session.get(GameSession, session_id)
        if session is None or session.owner_user_id != current_user_id:
            raise ValueError("Session not found")
        return session
