# models/faction_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Faction(Base):
    """Represents a faction in the game.

    Attributes:
        id (int): Unique identifier for the faction.
        name (str): Name of the faction.
        description (str): Description of the faction.
        reputation (int): Reputation score of the faction.
    """

    __tablename__ = "factions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    reputation: int = Column(Integer)

    allies = relationship("Faction", back_populates="enemies")
    enemies = relationship("Faction", back_populates="allies")
    npcs = relationship("NPC", back_populates="faction")
