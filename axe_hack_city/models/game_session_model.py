from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GameSession(Base):
    """Represents a game session."""

    __tablename__ = "game_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    status: str = Column(String)
