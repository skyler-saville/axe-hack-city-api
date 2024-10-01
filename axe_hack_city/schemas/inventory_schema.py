# schemas/inventory_schema.py
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class InventorySchema(SQLModel, table=True):
    """Schema for representing an inventory."""

    id: int = Field(default=None, primary_key=True)
    item_ids: List[int] = Field(default=[])
    capacity: int


class InventoryCreateSchema(SQLModel):
    """Schema for creating a new inventory."""

    item_ids: List[int] = Field(default=[])
    capacity: int


class InventoryUpdateSchema(SQLModel):
    """Schema for updating an existing inventory."""

    item_ids: Optional[List[int]] = None
    capacity: Optional[int] = None

    @model_validator(mode="after")
    def validate_capacity(cls, values: dict) -> dict:
        """Validate that the capacity is non-negative."""

        capacity = values.get("capacity")
        if capacity is not None and capacity < 0:
            raise ValueError("Capacity must be non-negative.")
        return values
