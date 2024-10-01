# models/mission_model.py
from enum import Enum

from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MissionStatus(str, Enum):
    """Enumeration of possible mission statuses."""

    active = "active"
    completed = "completed"
    failed = "failed"


class Mission(Base):
    """Represents a mission in the game.

    Attributes:
        id (int): Unique identifier for the mission.
        name (str): Name of the mission.
        description (str): Description of the mission.
        objectives (list[str]): List of mission objectives.
        status (MissionStatus): Current status of the mission.
    """

    __tablename__ = "missions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    objectives: list[str] = Column(ARRAY(String))
    status: MissionStatus = Column(Enum(MissionStatus))

    rewards = relationship("Item", back_populates="missions")
    giver_id: int = Column(Integer, ForeignKey("npcs.id"))
    giver = relationship("NPC", back_populates="missions")
