from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import Base


class PlayerProgression(Base):
    __tablename__ = "player_progressions"

    id: int = Column(Integer, primary_key=True, index=True)
    character_id: int = Column(Integer, ForeignKey("characters.id"), unique=True)
    missions_completed: dict = Column(JSON)
    faction_reputations: dict = Column(JSON)
    achievements: list = Column(JSON)

    character = relationship("Character", back_populates="progression")
