# schemas/faction_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class FactionSchema(SQLModel, table=True):
    """Schema for representing a faction."""

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    reputation: int
    ally_ids: List[int] = Field(default=[])
    enemy_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])


class FactionCreateSchema(SQLModel):
    """Schema for creating a new faction."""

    name: str
    description: str
    reputation: int
    ally_ids: List[int] = Field(default=[])
    enemy_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])


class FactionUpdateSchema(SQLModel):
    """Schema for updating an existing faction."""

    name: Optional[str] = None
    description: Optional[str] = None
    reputation: Optional[int] = None
    ally_ids: Optional[List[int]] = None
    enemy_ids: Optional[List[int]] = None
    npc_ids: Optional[List[int]] = None

    @model_validator(mode="after")
    def validate_reputation(cls, values: dict) -> dict:
        """Ensure reputation is non-negative."""

        reputation = values.get("reputation")
        if reputation is not None and reputation < 0:
            raise ValueError("Reputation must be non-negative.")
        return values
