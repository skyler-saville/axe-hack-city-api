from sqlalchemy import Column, Integer, String, Enum, JSON
from enum import Enum as PyEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SkillType(str, PyEnum):
    """Enumeration of possible skill types."""
    hacking = "hacking"
    engineering = "engineering"
    demolitions = "demolitions"
    marksmanship = "marksmanship"
    strategy = "strategy"
    medical = "medical"
    reconnaissance = "reconnaissance"

class Skill(Base):
    """Represents a skill in the game.

    Attributes:
        id (int): Unique identifier for the skill.
        name (str): Name of the skill.
        type (SkillType): Type of the skill.
        level (int): Level of the skill.
        description (str): Description of the skill.
        prerequisites (list): Prerequisite skills.
        effects (dict): Effects of the skill.
    """
    __tablename__ = 'skills'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: SkillType = Column(Enum(SkillType))
    level: int = Column(Integer)
    description: str = Column(String)
    prerequisites: list = Column(JSON)
    effects: dict = Column(JSON)
