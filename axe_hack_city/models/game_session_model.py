from sqlalchemy import Column, Integer, String

from .base import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    status: str = Column(String)
