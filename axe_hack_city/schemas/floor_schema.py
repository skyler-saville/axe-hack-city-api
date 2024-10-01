# schemas/floor_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class FloorSchema(SQLModel, table=True):
    """Schema for representing a floor."""

    id: int = Field(default=None, primary_key=True)
    number: int
    layout_id: int
    loot_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])


class FloorCreateSchema(SQLModel):
    """Schema for creating a new floor."""

    number: int
    layout_id: int
    loot_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])


class FloorUpdateSchema(SQLModel):
    """Schema for updating an existing floor."""

    number: Optional[int] = None
    layout_id: Optional[int] = None
    loot_ids: Optional[List[int]] = None
    npc_ids: Optional[List[int]] = None

    @model_validator(mode="after")
    def validate_floor(cls, values: dict) -> dict:
        """Validate floor properties."""

        number = values.get("number")
        loot_ids = values.get("loot_ids")
        npc_ids = values.get("npc_ids")

        if number is not None and number < 0:
            raise ValueError("Floor number must be non-negative.")

        if loot_ids is not None and not loot_ids:
            raise ValueError("At least one loot ID must be specified.")

        if npc_ids is not None and not npc_ids:
            raise ValueError("At least one NPC ID must be specified.")

        return values
