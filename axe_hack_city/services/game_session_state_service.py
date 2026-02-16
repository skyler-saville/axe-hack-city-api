from datetime import datetime, timezone
from typing import Any, Dict

from ..models.game_session_model import GameSession
from ..schemas.game_session_schema import GameStateTransitionSchema


class GameSessionStateService:
    """Applies validated runtime state transitions for game sessions."""

    @staticmethod
    def transition_from_state_changes(state_changes: Dict[str, Any]) -> GameStateTransitionSchema:
        return GameStateTransitionSchema(
            status=state_changes.get("status"),
            player_context_patch={
                key: value
                for key, value in state_changes.items()
                if key
                not in {
                    "status",
                    "active_objectives",
                    "active_encounters",
                    "action_log_entry",
                }
            },
            active_objectives=state_changes.get("active_objectives"),
            active_encounters=state_changes.get("active_encounters"),
            action_log_entry=state_changes.get("action_log_entry"),
            increment_turn=state_changes.get("increment_turn", True),
            expected_state_version=state_changes.get("expected_state_version"),
        )

    @staticmethod
    def apply_validated_transition(session: GameSession, transition: GameStateTransitionSchema) -> None:
        if (
            transition.expected_state_version is not None
            and transition.expected_state_version != session.state_version
        ):
            raise ValueError("State version mismatch for transition")

        if transition.status is not None:
            session.status = transition.status

        player_context = dict(session.player_context or {})
        player_context.update(transition.player_context_patch)
        session.player_context = player_context

        active_encounters = dict(session.active_encounters or {})
        if transition.active_objectives is not None:
            active_encounters["objectives"] = transition.active_objectives
        if transition.active_encounters is not None:
            active_encounters["encounters"] = transition.active_encounters
        active_encounters.setdefault("objectives", [])
        active_encounters.setdefault("encounters", [])
        session.active_encounters = active_encounters

        turn_metadata = dict(session.turn_metadata or {})
        current_turn = int(turn_metadata.get("turn_number") or 0)
        if transition.increment_turn:
            current_turn += 1
        turn_metadata["turn_number"] = current_turn
        turn_metadata["last_action_timestamp"] = datetime.now(timezone.utc).isoformat()
        session.turn_metadata = turn_metadata

        if transition.action_log_entry is not None:
            action_log_summary = dict(session.action_log_summary or {})
            entries = list(action_log_summary.get("recent_actions") or [])
            entries.append(transition.action_log_entry)
            action_log_summary["recent_actions"] = entries[-20:]
            action_log_summary["total_actions"] = int(action_log_summary.get("total_actions") or 0) + 1
            session.action_log_summary = action_log_summary

        session.state_payload = {
            "player_context": session.player_context,
            "active_encounters": session.active_encounters,
            "turn_metadata": session.turn_metadata,
            "action_log_summary": session.action_log_summary,
        }
