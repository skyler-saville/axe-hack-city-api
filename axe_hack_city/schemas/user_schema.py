# schemas/user_schema.py
from enum import Enum
from typing import List, Optional

from pydantic import EmailStr, model_validator
from sqlmodel import Field, SQLModel


class TimezoneEnum(str, Enum):
    """Enum for defining supported timezones."""

    UTC = "UTC"
    EST = "EST"
    PST = "PST"
    CST = "CST"
    MST = "MST"


class User(SQLModel, table=True):
    """Schema for representing a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: EmailStr
    password: str
    timezone: TimezoneEnum
    character_ids: List[int] = Field(default=[])

    @model_validator(mode="after")
    def validate_fields(cls, values: dict) -> dict:
        """Validate user properties."""

        password = values.get("password")
        timezone = values.get("timezone")
        character_ids = values.get("character_ids")

        if password is not None and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        valid_timezones = ["UTC", "EST", "PST", "CST", "MST"]
        if timezone not in valid_timezones:
            raise ValueError(f"Timezone must be one of: {valid_timezones}")

        if not character_ids or any(char_id <= 0 for char_id in character_ids):
            raise ValueError(
                "Character IDs must be a non-empty list of positive integers."
            )

        return values


class UserCreateSchema(SQLModel):
    """Schema for creating a new user."""

    username: EmailStr
    password: str
    timezone: TimezoneEnum
    character_ids: List[int]

    @model_validator(mode="after")
    def validate_fields(cls, values: dict) -> dict:
        """Validate user properties."""

        password = values.get("password")
        timezone = values.get("timezone")
        character_ids = values.get("character_ids")

        if password is not None and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        valid_timezones = ["UTC", "EST", "PST", "CST", "MST"]
        if timezone not in valid_timezones:
            raise ValueError(f"Timezone must be one of: {valid_timezones}")

        if not character_ids or any(char_id <= 0 for char_id in character_ids):
            raise ValueError(
                "Character IDs must be a non-empty list of positive integers."
            )

        return values


class UserUpdateSchema(SQLModel):
    """Schema for updating an existing user."""

    username: Optional[EmailStr] = None
    password: Optional[str] = None
    timezone: Optional[TimezoneEnum] = None
    character_ids: Optional[List[int]] = None

    @model_validator(mode="after")
    def check_username(cls, values: dict) -> dict:
        """Validate that the username is a valid email address."""

        username = values.get("username")
        if username is not None and not isinstance(username, EmailStr):
            raise ValueError("Username must be a valid email address.")
        return values
