# schemas/skill_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class SkillSchema(SQLModel, table=True):
    """Schema for representing a skill."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    level: int
    description: str
    prerequisites: List[str] = Field(default=[])
    effects: dict


class SkillCreateSchema(SQLModel):
    """Schema for creating a new skill."""

    name: str
    type: str
    level: int
    description: str
    prerequisites: List[str] = Field(default=[])
    effects: dict

    @model_validator(mode="after")
    def validate_skill(cls, values: dict) -> dict:
        """Validate skill properties."""

        level = values.get("level")

        if level is not None and (level < 0 or level > 100):
            raise ValueError("Skill level must be between 0 and 100.")

        return values


class SkillUpdateSchema(SQLModel):
    """Schema for updating an existing skill."""

    name: Optional[str] = None
    type: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None
    prerequisites: Optional[List[str]] = None
    effects: Optional[dict] = None

    @model_validator(mode="after")
    def validate_skill(cls, values: dict) -> dict:
        """Validate skill properties using the create schema's validation."""

        return SkillCreateSchema.validate_skill(values)
