from enum import Enum as PyEnum

from sqlalchemy import JSON, Column, Enum, Integer, String

from .base import Base


class SkillType(str, PyEnum):
    hacking = "hacking"
    engineering = "engineering"
    demolitions = "demolitions"
    marksmanship = "marksmanship"
    strategy = "strategy"
    medical = "medical"
    reconnaissance = "reconnaissance"


class Skill(Base):
    __tablename__ = "skills"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: SkillType = Column(Enum(SkillType))
    level: int = Column(Integer)
    description: str = Column(String)
    prerequisites: list = Column(JSON)
    effects: dict = Column(JSON)
