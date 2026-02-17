from sqlalchemy import JSON, Column, Integer, String

from .base import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    owner_user_id: int = Column(Integer, nullable=False, index=True)
    name: str = Column(String)
    status: str = Column(String)
    player_context: dict = Column(JSON, nullable=False, default=dict)
    active_encounters: dict = Column(JSON, nullable=False, default=dict)
    turn_metadata: dict = Column(JSON, nullable=False, default=dict)
    action_log_summary: dict = Column(JSON, nullable=True)
    state_version: int = Column(Integer, nullable=False, default=1)
    state_payload: dict = Column(JSON, nullable=False, default=dict)
