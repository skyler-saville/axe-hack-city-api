from typing import Optional

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
