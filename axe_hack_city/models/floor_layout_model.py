from sqlalchemy import Column, Integer, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Wall(Base):
    """Represents a wall in a floor layout.

    Attributes:
        id (int): Unique identifier for the wall.
        start (list[float]): Starting coordinates of the wall.
        end (list[float]): Ending coordinates of the wall.
        floor_id (int): ID of the associated floor.
    """
    __tablename__ = 'walls'

    id: int = Column(Integer, primary_key=True, index=True)
    start: list[float] = Column(ARRAY(Float))
    end: list[float] = Column(ARRAY(Float))
    floor_id: int = Column(Integer, ForeignKey('floors.id'))

    floor = relationship("Floor", back_populates="walls")

class Door(Base):
    """Represents a door in a floor layout.

    Attributes:
        id (int): Unique identifier for the door.
        position (list[float]): Position of the door.
        width (float): Width of the door.
        floor_id (int): ID of the associated floor.
    """
    __tablename__ = 'doors'

    id: int = Column(Integer, primary_key=True, index=True)
    position: list[float] = Column(ARRAY(Float))
    width: float = Column(Float)
    floor_id: int = Column(Integer, ForeignKey('floors.id'))

    floor = relationship("Floor", back_populates="doors")

class FloorLayout(Base):
    """Represents a layout of a floor, including walls and doors.

    Attributes:
        id (int): Unique identifier for the floor layout.
    """
    __tablename__ = 'floor_layouts'

    id: int = Column(Integer, primary_key=True, index=True)
    walls = relationship("Wall", back_populates="floor")
    doors = relationship("Door", back_populates="floor")
