from enum import Enum as PyEnum

from sqlalchemy import ARRAY, Column, Enum, Integer, String

from .base import Base


class TimezoneEnum(str, PyEnum):
    UTC = "UTC"
    EST = "EST"
    PST = "PST"
    CST = "CST"
    MST = "MST"


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    password: str = Column(String)
    timezone: TimezoneEnum = Column(Enum(TimezoneEnum), default="UTC")
    character_ids: list[int] = Column(ARRAY(Integer))
