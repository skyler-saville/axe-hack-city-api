# models/user_model.py
from enum import Enum as PyEnum

from sqlalchemy import ARRAY, Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimezoneEnum(str, PyEnum):
    """Enumeration of possible time zones."""

    UTC = "UTC"
    EST = "EST"
    PST = "PST"
    CST = "CST"
    MST = "MST"


class User(Base):
    """Represents a user in the game.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username of the user.
        password (str): Password for the user.
        timezone (TimezoneEnum): Timezone of the user.
        character_ids (list[int]): List of associated character IDs.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    password: str = Column(String)
    timezone: TimezoneEnum = Column(Enum(TimezoneEnum), default="UTC")
    character_ids: list[int] = Column(ARRAY(Integer))
