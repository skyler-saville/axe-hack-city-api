# schemas/event_schema.py
from datetime import datetime
from typing import List, Optional

from pydantic import model_validator
from sqlmodel import Field, SQLModel


class EventSchema(SQLModel, table=True):
    """Schema for representing an event."""

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    location_id: int
    start_time: datetime
    end_time: datetime
    participant_ids: List[int] = Field(default=[])


class EventCreateSchema(SQLModel):
    """Schema for creating a new event."""

    name: str
    description: str
    location_id: int
    start_time: datetime
    end_time: datetime
    participant_ids: List[int] = Field(default=[])


class EventUpdateSchema(SQLModel):
    """Schema for updating an existing event."""

    name: Optional[str] = None
    description: Optional[str] = None
    location_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    participant_ids: Optional[List[int]] = None

    @model_validator(mode="after")
    def validate_times(cls, values: dict) -> dict:
        """Ensure end time is after start time."""

        start_time = values.get("start_time")
        end_time = values.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise ValueError("End time must be after start time.")
        return values
