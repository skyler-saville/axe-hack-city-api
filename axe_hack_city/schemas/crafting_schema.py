# schemas/crafting_schema.py
from typing import List, Optional
from sqlmodel import SQLModel, Field
from pydantic import model_validator

class CraftingRecipeSchema(SQLModel, table=True):
    """Schema for representing a crafting recipe."""
    
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    ingredient_ids: List[int] = Field(default=[])
    output_id: int
    skill_required_id: int

class CraftingRecipeCreateSchema(SQLModel):
    """Schema for creating a new crafting recipe."""
    
    name: str
    description: str
    ingredient_ids: List[int] = Field(default=[])
    output_id: int
    skill_required_id: int

class CraftingRecipeUpdateSchema(SQLModel):
    """Schema for updating an existing crafting recipe."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    ingredient_ids: Optional[List[int]] = None
    output_id: Optional[int] = None
    skill_required_id: Optional[int] = None

    @model_validator(mode='after')
    def validate_ingredients(cls, values: dict) -> dict:
        """Ensure at least one ingredient is specified."""
        
        ingredients = values.get('ingredient_ids', [])
        if not ingredients:
            raise ValueError('At least one ingredient is required.')
        return values

