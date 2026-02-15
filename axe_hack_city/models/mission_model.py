from enum import Enum

from sqlalchemy import ARRAY, Column, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, mission_reward_association


class MissionStatus(str, Enum):
    active = "active"
    completed = "completed"
    failed = "failed"


class Mission(Base):
    __tablename__ = "missions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    objectives: list[str] = Column(ARRAY(String))
    status: MissionStatus = Column(SqlEnum(MissionStatus))

    giver_id: int = Column(Integer, ForeignKey("npcs.id"))

    rewards = relationship(
        "Item",
        secondary=mission_reward_association,
        back_populates="missions",
    )
    giver = relationship("NPC", back_populates="missions")
