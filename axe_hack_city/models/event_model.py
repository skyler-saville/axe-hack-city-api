from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    """Represents an event in the game.

    Attributes:
        id (int): Unique identifier for the event.
        name (str): Name of the event.
        description (str): Description of the event.
        location_id (int): ID of the associated location.
        start_time (DateTime): Start time of the event.
        end_time (DateTime): End time of the event.
    """
    __tablename__ = 'events'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    location_id: int = Column(Integer, ForeignKey('locations.id'))
    start_time: DateTime = Column(DateTime)
    end_time: DateTime = Column(DateTime)

    location = relationship("Location", back_populates="events")
    participants = relationship("Character", back_populates="events")
