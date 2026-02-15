from enum import Enum as PyEnum

from sqlalchemy import ARRAY, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, event_participant_association


class SkillType(PyEnum):
    hacking = "hacking"
    engineering = "engineering"
    combat = "combat"


class Character(Base):
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
    events = relationship(
        "Event",
        secondary=event_participant_association,
        back_populates="participants",
    )
    progression = relationship(
        "PlayerProgression", back_populates="character", uselist=False
    )
