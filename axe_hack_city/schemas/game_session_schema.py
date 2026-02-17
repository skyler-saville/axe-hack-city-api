from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class GameStateEnvelopeSchema(SQLModel):
    state_version: int = Field(default=1, ge=1)
    state_payload: Dict[str, Any] = Field(default_factory=dict)


class TurnMetadataSchema(SQLModel):
    turn_number: int = Field(default=0, ge=0)
    last_action_timestamp: Optional[datetime] = None


class RuntimeGameStateSchema(GameStateEnvelopeSchema):
    player_context: Dict[str, Any] = Field(default_factory=dict)
    active_encounters: Dict[str, Any] = Field(default_factory=lambda: {"objectives": [], "encounters": []})
    turn_metadata: TurnMetadataSchema = Field(default_factory=TurnMetadataSchema)
    action_log_summary: Optional[Dict[str, Any]] = None

    @model_validator(mode="after")
    def ensure_payload_matches_structured_state(self) -> "RuntimeGameStateSchema":
        envelope_payload = {
            "player_context": self.player_context,
            "active_encounters": self.active_encounters,
            "turn_metadata": self.turn_metadata.model_dump(mode="json"),
            "action_log_summary": self.action_log_summary,
        }

        if not self.state_payload:
            self.state_payload = envelope_payload
            return self

        required_keys = {"player_context", "active_encounters", "turn_metadata", "action_log_summary"}
        if not required_keys.issubset(set(self.state_payload.keys())):
            missing = sorted(required_keys.difference(set(self.state_payload.keys())))
            raise ValueError(f"state_payload missing required keys: {', '.join(missing)}")

        return self


class GameSessionSchema(SQLModel):
    """Schema for representing a game session."""

    id: Optional[int] = None
    owner_user_id: int
    name: str
    status: str
    player_context: Dict[str, Any] = Field(default_factory=dict)
    active_encounters: Dict[str, Any] = Field(default_factory=lambda: {"objectives": [], "encounters": []})
    turn_metadata: TurnMetadataSchema = Field(default_factory=TurnMetadataSchema)
    action_log_summary: Optional[Dict[str, Any]] = None
    state_version: int = Field(default=1, ge=1)
    state_payload: Dict[str, Any] = Field(default_factory=dict)


class GameSessionCreateSchema(SQLModel):
    """Schema for creating a new game session."""

    name: str
    status: str
    state: RuntimeGameStateSchema = Field(default_factory=RuntimeGameStateSchema)


class GameSessionUpdateSchema(SQLModel):
    """Schema for updating an existing game session."""

    name: Optional[str] = None
    status: Optional[str] = None


class GameStateTransitionSchema(SQLModel):
    """Validated state transition payload that can be atomically applied to a session."""

    status: Optional[str] = None
    player_context_patch: Dict[str, Any] = Field(default_factory=dict)
    active_objectives: Optional[List[Dict[str, Any]]] = None
    active_encounters: Optional[List[Dict[str, Any]]] = None
    action_log_entry: Optional[str] = None
    increment_turn: bool = True
    expected_state_version: Optional[int] = Field(default=None, ge=1)

    @model_validator(mode="after")
    def ensure_non_empty_transition(self) -> "GameStateTransitionSchema":
        if (
            self.status is None
            and not self.player_context_patch
            and self.active_objectives is None
            and self.active_encounters is None
            and self.action_log_entry is None
            and not self.increment_turn
        ):
            raise ValueError("Transition must include at least one change.")

        return self


class GameplayCommandRequestSchema(SQLModel):
    command: str


class GameplayActionResultSchema(SQLModel):
    state_changes: Dict[str, Any] = Field(default_factory=dict)
    narration: str
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    success: bool
