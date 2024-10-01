# models/npc_model.py
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AggressionLevel(str, Enum):
    """Enumeration of possible aggression levels for NPCs."""

    passive = "passive"
    cautious = "cautious"
    aggressive = "aggressive"
    hostile = "hostile"


class Relationship(str, Enum):
    """Enumeration of possible relationships for NPCs."""

    ally = "ally"
    enemy = "enemy"
    neutral = "neutral"


class NPC(Base):
    """Represents a non-playable character (NPC) in the game.

    Attributes:
        id (int): Unique identifier for the NPC.
        name (str): Name of the NPC.
    """

    __tablename__ = "npcs"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
