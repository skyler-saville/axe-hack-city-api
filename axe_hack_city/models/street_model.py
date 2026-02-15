from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import relationship

from .base import Base, building_street_association


class Street(Base):
    __tablename__ = "streets"

    id: int = Column(Integer, primary_key=True, index=True)
    width: float = Column(Float)
    length: float = Column(Float)
    traffic: int = Column(Integer)

    connected_buildings = relationship(
        "Building",
        secondary=building_street_association,
        back_populates="connected_streets",
    )
