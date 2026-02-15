from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, faction_alliance_association


class Faction(Base):
    __tablename__ = "factions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    reputation: int = Column(Integer)

    allies = relationship(
        "Faction",
        secondary=faction_alliance_association,
        primaryjoin=id == faction_alliance_association.c.faction_id,
        secondaryjoin=id == faction_alliance_association.c.ally_id,
        back_populates="enemies",
    )
    enemies = relationship(
        "Faction",
        secondary=faction_alliance_association,
        primaryjoin=id == faction_alliance_association.c.ally_id,
        secondaryjoin=id == faction_alliance_association.c.faction_id,
        back_populates="allies",
    )
    npcs = relationship("NPC", back_populates="faction")
