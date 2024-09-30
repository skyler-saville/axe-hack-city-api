from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Building(Base):
    """Represents a building in the game.

    Attributes:
        id (int): Unique identifier for the building.
        name (str): Name of the building.
        type (str): Type of the building.
        description (str): Description of the building.
    """
    __tablename__ = 'buildings'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: str = Column(String)
    description: str = Column(String)

    # Relationships
    floors = relationship("Floor", back_populates="building")
    entrances = relationship("Location", back_populates="connected_buildings")
    loot = relationship("Item", back_populates="building")
    npcs = relationship("NPC", back_populates="building")
