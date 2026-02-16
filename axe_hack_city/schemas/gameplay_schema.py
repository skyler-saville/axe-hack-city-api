from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class StructuredCommandSchema(SQLModel):
    verb: str
    target: Optional[str] = None
    args: List[str] = Field(default_factory=list)


class GameplayCommandInputSchema(SQLModel):
    raw_command: Optional[str] = None
    structured_command: Optional[StructuredCommandSchema] = None

    @model_validator(mode="after")
    def validate_command_source(self) -> "GameplayCommandInputSchema":
        has_raw = bool((self.raw_command or "").strip())
        has_structured = self.structured_command is not None
        if not has_raw and not has_structured:
            raise ValueError(
                "Either raw_command or structured_command must be provided."
            )
        return self


class GameplayParseErrorSchema(SQLModel):
    field: str
    message: str


class GameplayUiHintsSchema(SQLModel):
    suggested_actions: List[str] = Field(default_factory=list)
    highlighted_targets: List[str] = Field(default_factory=list)


class GameplayTurnOutcomeSchema(SQLModel):
    narration: str
    state_delta: Dict[str, Any] = Field(default_factory=dict)
    ui_hints: GameplayUiHintsSchema = Field(default_factory=GameplayUiHintsSchema)
    warnings: List[str] = Field(default_factory=list)
    parse_errors: List[GameplayParseErrorSchema] = Field(default_factory=list)
    success: bool


class GameplayStateSnapshotSchema(SQLModel):
    session_id: int
    status: str
    state_version: int
    turn_number: int = Field(default=0, ge=0)
    player_context: Dict[str, Any] = Field(default_factory=dict)
    active_encounters: Dict[str, Any] = Field(default_factory=dict)
    state_payload: Dict[str, Any] = Field(default_factory=dict)


class GameplayLogEntrySchema(SQLModel):
    turn_number: int = Field(default=0, ge=0)
    narration: str
    success: bool
    created_at: datetime


class GameplayLogResponseSchema(SQLModel):
    session_id: int
    entries: List[GameplayLogEntrySchema] = Field(default_factory=list)
