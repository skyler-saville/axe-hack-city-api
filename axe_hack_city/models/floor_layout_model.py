from sqlalchemy import ARRAY, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class Wall(Base):
    __tablename__ = "walls"

    id: int = Column(Integer, primary_key=True, index=True)
    start: list[float] = Column(ARRAY(Float))
    end: list[float] = Column(ARRAY(Float))
    floor_id: int = Column(Integer, ForeignKey("floors.id"))

    floor = relationship("Floor", back_populates="walls")


class Door(Base):
    __tablename__ = "doors"

    id: int = Column(Integer, primary_key=True, index=True)
    position: list[float] = Column(ARRAY(Float))
    width: float = Column(Float)
    floor_id: int = Column(Integer, ForeignKey("floors.id"))

    floor = relationship("Floor", back_populates="doors")


class FloorLayout(Base):
    __tablename__ = "floor_layouts"

    id: int = Column(Integer, primary_key=True, index=True)
    floors = relationship("Floor", back_populates="layout")
