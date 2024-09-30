# schemas/floor_layout_schema.py
from typing import List, Tuple, Optional
from sqlmodel import SQLModel, Field

class WallSchema(SQLModel):
    """Schema for representing a wall."""
    
    start: Tuple[float, float]
    end: Tuple[float, float]

class WallCreateSchema(SQLModel):
    """Schema for creating a new wall."""
    
    start: Tuple[float, float]
    end: Tuple[float, float]

class DoorSchema(SQLModel):
    """Schema for representing a door."""
    
    position: Tuple[float, float]
    width: float

class DoorCreateSchema(SQLModel):
    """Schema for creating a new door."""
    
    position: Tuple[float, float]
    width: float

class FloorLayoutSchema(SQLModel, table=True):
    """Schema for representing a floor layout."""
    
    id: int = Field(default=None, primary_key=True)
    walls: List[WallSchema] = Field(default=[])
    doors: List[DoorSchema] = Field(default=[])

class FloorLayoutCreateSchema(SQLModel):
    """Schema for creating a new floor layout."""
    
    walls: List[WallCreateSchema] = Field(default=[])
    doors: List[DoorCreateSchema] = Field(default=[])

class FloorLayoutUpdateSchema(SQLModel):
    """Schema for updating an existing floor layout."""
    
    walls: Optional[List[WallCreateSchema]] = None
    doors: Optional[List[DoorCreateSchema]] = None
