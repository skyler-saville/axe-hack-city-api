from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, building_entrance_association, building_street_association


class Building(Base):
    __tablename__ = "buildings"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: str = Column(String)
    description: str = Column(String)

    floors = relationship("Floor", back_populates="building")
    entrances = relationship(
        "Location",
        secondary=building_entrance_association,
        back_populates="connected_buildings",
    )
    connected_streets = relationship(
        "Street",
        secondary=building_street_association,
        back_populates="connected_buildings",
    )
    loot = relationship("Item", back_populates="building")
    npcs = relationship("NPC", back_populates="building")
