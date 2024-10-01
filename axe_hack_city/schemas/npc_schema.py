# schemas/npc_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class NPCSchema(SQLModel, table=True):
    """Schema for representing a non-player character (NPC)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    health: int
    skill_tree_id: int
    item_ids: List[int] = Field(default=[])
    dialogue: str
    faction_id: int
    aggression_level: str
    relationship: str


class NPCCreateSchema(SQLModel):
    """Schema for creating a new NPC."""

    name: str
    health: int
    skill_tree_id: int
    item_ids: List[int] = Field(default=[])
    dialogue: str
    faction_id: int
    aggression_level: str
    relationship: str

    @model_validator(mode="after")
    def validate_npc(cls, values: dict) -> dict:
        """Validate NPC properties."""

        health = values.get("health")

        if health is not None and health < 0:
            raise ValueError("Health must be non-negative.")

        return values


class NPCUpdateSchema(SQLModel):
    """Schema for updating an existing NPC."""

    name: Optional[str] = None
    health: Optional[int] = None
    skill_tree_id: Optional[int] = None
    item_ids: Optional[List[int]] = None
    dialogue: Optional[str] = None
    faction_id: Optional[int] = None
    aggression_level: Optional[str] = None
    relationship: Optional[str] = None

    @model_validator(mode="after")
    def validate_npc(cls, values: dict) -> dict:
        """Validate NPC properties using the create schema's validation."""

        return NPCCreateSchema.validate_npc(values)
