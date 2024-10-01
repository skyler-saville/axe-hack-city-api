# schemas/location_schema.py
from typing import List, Optional, Tuple

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class LocationSchema(SQLModel, table=True):
    """Schema for representing a location."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    description: str
    coordinates: Tuple[float, float]
    connected_location_ids: List[int] = Field(default=[])


class LocationCreateSchema(SQLModel):
    """Schema for creating a new location."""

    name: str
    type: str
    description: str
    coordinates: Tuple[float, float]
    connected_location_ids: List[int] = Field(default=[])

    @model_validator(mode="after")
    def validate_location(cls, values: dict) -> dict:
        """Validate location properties."""

        coordinates = values.get("coordinates")

        if coordinates is not None and (
            len(coordinates) != 2
            or not all(isinstance(coord, float) for coord in coordinates)
        ):
            raise ValueError("Coordinates must be a tuple of two floats.")

        return values


class LocationUpdateSchema(SQLModel):
    """Schema for updating an existing location."""

    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    connected_location_ids: Optional[List[int]] = None

    @model_validator(mode="after")
    def validate_location(cls, values: dict) -> dict:
        """Validate location properties using the create schema's validation."""

        return LocationCreateSchema.validate_location(values)
