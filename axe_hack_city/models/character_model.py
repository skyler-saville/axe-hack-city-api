# models/character_model.py
from enum import Enum

from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SkillType(Enum):
    """Enumeration of possible skill types."""

    # Add the skill types here


class Character(Base):
    """Represents a character in the game.

    Attributes:
        id (int): Unique identifier for the character.
        name (str): Name of the character.
        health (int): Health points of the character.
        xp (int): Experience points of the character.
        clan_name (str): Name of the clan the character belongs to.
        clan_members (list[int]): List of clan member IDs.
        skill_tree (SkillType): Type of skill the character possesses.
        inventory_id (int): ID of the associated inventory.
    """

    __tablename__ = "characters"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    health: int = Column(Integer)
    xp: int = Column(Integer)
    clan_name: str = Column(String)
    clan_members: list[int] = Column(ARRAY(Integer))
    skill_tree: SkillType = Column(Enum(SkillType))
    inventory_id: int = Column(Integer, ForeignKey("inventories.id"))

    inventory = relationship("Inventory", back_populates="characters")
