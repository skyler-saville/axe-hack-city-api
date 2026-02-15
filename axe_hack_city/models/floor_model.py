from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Floor(Base):
    __tablename__ = "floors"

    id: int = Column(Integer, primary_key=True, index=True)
    number: int = Column(Integer)
    layout_id: int = Column(Integer, ForeignKey("floor_layouts.id"))
    building_id: int = Column(Integer, ForeignKey("buildings.id"))

    layout = relationship("FloorLayout", back_populates="floors")
    building = relationship("Building", back_populates="floors")
    loot = relationship("Item", back_populates="floor")
    npcs = relationship("NPC", back_populates="floor")
    walls = relationship("Wall", back_populates="floor")
    doors = relationship("Door", back_populates="floor")
