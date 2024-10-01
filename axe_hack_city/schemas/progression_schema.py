# schemas/progression_schema.py
from typing import Dict, List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class PlayerProgressionSchema(SQLModel, table=True):
    """Schema for representing a player's progression."""

    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int
    missions_completed_ids: List[int] = Field(default=[])
    faction_reputations: Dict[int, int] = Field(default={})
    achievements: List[str] = Field(default=[])


class PlayerProgressionCreateSchema(SQLModel):
    """Schema for creating a new player progression record."""

    character_id: int
    missions_completed_ids: List[int] = Field(default=[])
    faction_reputations: Dict[int, int] = Field(default={})
    achievements: List[str] = Field(default=[])

    @model_validator(mode="after")
    def validate_progression(cls, values: dict) -> dict:
        """Validate player progression properties."""

        missions_completed_ids = values.get("missions_completed_ids")

        if missions_completed_ids is not None and len(missions_completed_ids) == 0:
            raise ValueError("At least one completed mission ID must be specified.")

        return values


class PlayerProgressionUpdateSchema(SQLModel):
    """Schema for updating an existing player progression record."""

    character_id: Optional[int] = None
    missions_completed_ids: Optional[List[int]] = None
    faction_reputations: Optional[Dict[int, int]] = None
    achievements: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_progression(cls, values: dict) -> dict:
        """Validate player progression properties using the create schema's validation."""

        return PlayerProgressionCreateSchema.validate_progression(values)
