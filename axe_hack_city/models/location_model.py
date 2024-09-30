from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LocationType(str, Enum):
    """Enumeration of possible location types."""
    street = "street"
    building = "building"
    safe_zone = "safe_zone"
    landmark = "landmark"

class Location(Base):
    """Represents a location in the game.

    Attributes:
        id (int): Unique identifier for the location.
        name (str): Name of the location.
        type (LocationType): Type of the location.
        description (str): Description of the location.
        coordinates (list[float]): Geographical coordinates of the location.
    """
    __tablename__ = 'locations'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: LocationType = Column(Enum(LocationType))
    description: str = Column(String)
    coordinates: list[float] = Column(ARRAY(Float))

    connected_locations = relationship("Location", back_populates="entrances")
    events = relationship("Event", back_populates="location")
