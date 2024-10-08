# models/street_model.py
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Street(Base):
    """Represents a street in the game.

    Attributes:
        id (int): Unique identifier for the street.
        width (float): Width of the street.
        length (float): Length of the street.
        traffic (int): Traffic level on the street.
    """

    __tablename__ = "streets"

    id: int = Column(Integer, primary_key=True, index=True)
    width: float = Column(Float)
    length: float = Column(Float)
    traffic: int = Column(Integer)

    connected_buildings = relationship("Building", back_populates="connected_streets")
