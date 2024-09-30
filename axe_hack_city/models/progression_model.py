from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerProgression(Base):
    """Represents player progression in the game.

    Attributes:
        id (int): Unique identifier for the progression.
        character_id (int): ID of the associated character.
        missions_completed (dict): Completed missions.
        faction_reputations (dict): Faction reputations.
        achievements (list): List of achievements.
    """
    __tablename__ = 'player_progressions'

    id: int = Column(Integer, primary_key=True, index=True)
    character_id: int = Column(Integer, ForeignKey('characters.id'))
    missions_completed: dict = Column(JSON)
    faction_reputations: dict = Column(JSON)
    achievements: list = Column(JSON)

    character = relationship("Character", back_populates="progression")
