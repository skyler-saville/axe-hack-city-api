from typing import Any, Dict, List, Optional

from sqlmodel import Field, SQLModel


class GameSessionSchema(SQLModel, table=True):
    """Schema for representing a game session."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str


class GameSessionCreateSchema(SQLModel):
    """Schema for creating a new game session."""

    name: str
    status: str


class GameSessionUpdateSchema(SQLModel):
    """Schema for updating an existing game session."""

    name: Optional[str] = None
    status: Optional[str] = None


class GameplayCommandRequestSchema(SQLModel):
    command: str


class GameplayActionResultSchema(SQLModel):
    state_changes: Dict[str, Any] = Field(default_factory=dict)
    narration: str
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    success: bool
