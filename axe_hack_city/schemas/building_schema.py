# schemas/building_schema.py
from typing import List, Optional
from sqlmodel import SQLModel, Field
from pydantic import model_validator

class BuildingSchema(SQLModel, table=True):
    """Schema for representing a building."""
    
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    floor_ids: List[int] = Field(default=[])
    entrance_ids: List[int] = Field(default=[])
    loot_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])

class BuildingCreateSchema(SQLModel):
    """Schema for creating a new building."""
    
    name: str
    description: str
    floor_ids: List[int] = Field(default=[])
    entrance_ids: List[int] = Field(default=[])
    loot_ids: List[int] = Field(default=[])
    npc_ids: List[int] = Field(default=[])

class BuildingUpdateSchema(SQLModel):
    """Schema for updating an existing building."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    floor_ids: Optional[List[int]] = None
    entrance_ids: Optional[List[int]] = None
    loot_ids: Optional[List[int]] = None
    npc_ids: Optional[List[int]] = None

    @model_validator(mode='after')
    def validate_floors_and_entrances(cls, values: dict) -> dict:
        """Validate that the building has at least one floor and one entrance."""
        
        floor_ids = values.get('floor_ids', [])
        entrance_ids = values.get('entrance_ids', [])

        if not floor_ids:
            raise ValueError('Building must have at least one floor.')
        if not entrance_ids:
            raise ValueError('Building must have at least one entrance.')

        return values
