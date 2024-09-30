# schemas/item_schema.py
from typing import Optional, List
from sqlmodel import SQLModel, Field
from pydantic import model_validator

class ItemSchema(SQLModel, table=True):
    """Schema for representing an item."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    value: int
    weight: float
    description: str
    rarity: str
    durability: int
    damage: int
    defense: int
    effects: dict

class ItemCreateSchema(SQLModel):
    """Schema for creating a new item."""
    
    name: str
    type: str
    value: int
    weight: float
    description: str
    rarity: str
    durability: int
    damage: int
    defense: int
    effects: dict

    @model_validator(mode='after')
    def validate_item(cls, values: dict) -> dict:
        """Validate item properties."""
        
        value = values.get('value')
        weight = values.get('weight')
        durability = values.get('durability')

        if value is not None and value < 0:
            raise ValueError('Value must be non-negative.')
        if weight is not None and weight < 0:
            raise ValueError('Weight must be non-negative.')
        if durability is not None and (durability < 0 or durability > 100):
            raise ValueError('Durability must be between 0 and 100.')

        return values

class ItemUpdateSchema(SQLModel):
    """Schema for updating an existing item."""
    
    name: Optional[str] = None
    type: Optional[str] = None
    value: Optional[int] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    rarity: Optional[str] = None
    durability: Optional[int] = None
    damage: Optional[int] = None
    defense: Optional[int] = None
    effects: Optional[dict] = None

    @model_validator(mode='after')
    def validate_item(cls, values: dict) -> dict:
        """Validate item properties using the create schema's validation."""
        
        return ItemCreateSchema.validate_item(values)
