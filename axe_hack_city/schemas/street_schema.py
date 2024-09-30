# schemas/street_schema.py
from typing import List, Optional, Tuple
from sqlmodel import SQLModel, Field
from pydantic import model_validator

class StreetSchema(SQLModel, table=True):
    """Schema for representing a street."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    description: str
    coordinates: Tuple[float, float]
    width: float
    length: float
    traffic: int
    connected_building_ids: List[int] = Field(default=[])

class StreetCreateSchema(SQLModel):
    """Schema for creating a new street."""
    
    name: str
    type: str
    description: str
    coordinates: Tuple[float, float]
    width: float
    length: float
    traffic: int
    connected_building_ids: List[int] = Field(default=[])

    @model_validator(mode='after')
    def validate_street(cls, values: dict) -> dict:
        """Validate street properties."""
        
        width = values.get('width')
        length = values.get('length')
        traffic = values.get('traffic')

        if width is not None and width <= 0:
            raise ValueError('Width must be positive.')
        if length is not None and length <= 0:
            raise ValueError('Length must be positive.')
        if traffic is not None and traffic < 0:
            raise ValueError('Traffic must be non-negative.')

        return values

class StreetUpdateSchema(SQLModel):
    """Schema for updating an existing street."""
    
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    width: Optional[float] = None
    length: Optional[float] = None
    traffic: Optional[int] = None
    connected_building_ids: Optional[List[int]] = None

    @model_validator(mode='after')
    def validate_street(cls, values: dict) -> dict:
        """Validate street properties using the create schema's validation."""
        
        return StreetCreateSchema.validate_street(values)

