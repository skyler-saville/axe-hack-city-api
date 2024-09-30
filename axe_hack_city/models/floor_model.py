from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Floor(Base):
    """Represents a floor within a building.

    Attributes:
        id (int): Unique identifier for the floor.
        number (int): Floor number.
        layout_id (int): ID of the associated layout.
    """
    __tablename__ = 'floors'

    id: int = Column(Integer, primary_key=True, index=True)
    number: int = Column(Integer)
    layout_id: int = Column(Integer, ForeignKey('floor_layouts.id'))

    layout = relationship("FloorLayout", back_populates="floor")
    loot = relationship("Item", back_populates="floor")
    npcs = relationship("NPC", back_populates="floor")
