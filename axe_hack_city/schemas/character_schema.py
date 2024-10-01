# schemas/character_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class CharacterSchema(SQLModel, table=True):
    """Schema for representing a character."""

    id: int = Field(default=None, primary_key=True)
    name: str
    health: int
    xp: int
    clan_name: str
    clan_members_ids: List[int] = Field(default=[])
    skill_tree_id: int
    inventory_id: int


class CharacterCreateSchema(SQLModel):
    """Schema for creating a new character."""

    name: str
    health: int
    xp: int
    clan_name: str
    clan_members_ids: List[int] = Field(default=[])
    skill_tree_id: int
    inventory_id: int


class CharacterUpdateSchema(SQLModel):
    """Schema for updating an existing character."""

    name: Optional[str] = None
    health: Optional[int] = None
    xp: Optional[int] = None
    clan_name: Optional[str] = None
    clan_members_ids: Optional[List[int]] = None
    skill_tree_id: Optional[int] = None
    inventory_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_health(cls, values: dict) -> dict:
        """Ensure health is non-negative."""

        health = values.get("health")
        if health is not None and health < 0:
            raise ValueError("Health must be non-negative.")
        return values
