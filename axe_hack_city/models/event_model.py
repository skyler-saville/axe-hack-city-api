from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, event_participant_association


class Event(Base):
    __tablename__ = "events"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    description: str = Column(String)
    location_id: int = Column(Integer, ForeignKey("locations.id"))
    start_time: DateTime = Column(DateTime)
    end_time: DateTime = Column(DateTime)

    location = relationship("Location", back_populates="events")
    participants = relationship(
        "Character",
        secondary=event_participant_association,
        back_populates="events",
    )
