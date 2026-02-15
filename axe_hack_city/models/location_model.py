from enum import Enum

from sqlalchemy import ARRAY, Column, Enum as SqlEnum, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import (
    Base,
    building_entrance_association,
    location_connection_association,
)


class LocationType(str, Enum):
    street = "street"
    building = "building"
    safe_zone = "safe_zone"
    landmark = "landmark"


class Location(Base):
    __tablename__ = "locations"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    type: LocationType = Column(SqlEnum(LocationType))
    description: str = Column(String)
    coordinates: list[float] = Column(ARRAY(Float))

    connected_locations = relationship(
        "Location",
        secondary=location_connection_association,
        primaryjoin=id == location_connection_association.c.from_location_id,
        secondaryjoin=id == location_connection_association.c.to_location_id,
        back_populates="entrances",
    )
    entrances = relationship(
        "Location",
        secondary=location_connection_association,
        primaryjoin=id == location_connection_association.c.to_location_id,
        secondaryjoin=id == location_connection_association.c.from_location_id,
        back_populates="connected_locations",
    )
    connected_buildings = relationship(
        "Building",
        secondary=building_entrance_association,
        back_populates="entrances",
    )
    events = relationship("Event", back_populates="location")
