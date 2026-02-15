from enum import Enum

from sqlalchemy import Column, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class AggressionLevel(str, Enum):
    passive = "passive"
    cautious = "cautious"
    aggressive = "aggressive"
    hostile = "hostile"


class Relationship(str, Enum):
    ally = "ally"
    enemy = "enemy"
    neutral = "neutral"


class NPC(Base):
    __tablename__ = "npcs"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    aggression_level: AggressionLevel = Column(SqlEnum(AggressionLevel), nullable=True)
    building_id: int = Column(Integer, ForeignKey("buildings.id"), nullable=True)
    floor_id: int = Column(Integer, ForeignKey("floors.id"), nullable=True)
    faction_id: int = Column(Integer, ForeignKey("factions.id"), nullable=True)

    building = relationship("Building", back_populates="npcs")
    floor = relationship("Floor", back_populates="npcs")
    faction = relationship("Faction", back_populates="npcs")
    missions = relationship("Mission", back_populates="giver")
