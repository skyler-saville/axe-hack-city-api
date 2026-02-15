"""Database bootstrap helpers.

The application uses SQLAlchemy ORM models as the source of truth for schema
definition. Table creation is centralized in ``initialize_database``.
"""

from importlib import import_module
from ..models.base import Base
from .session import engine

MODEL_MODULES = (
    "building_model",
    "character_model",
    "crafting_model",
    "event_model",
    "faction_model",
    "floor_layout_model",
    "floor_model",
    "game_session_model",
    "inventory_model",
    "item_model",
    "location_model",
    "mission_model",
    "npc_model",
    "progression_model",
    "skill_model",
    "street_model",
    "user_model",
)


def _load_model_modules() -> None:
    for module_name in MODEL_MODULES:
        import_module(f"axe_hack_city.models.{module_name}")


def initialize_database() -> None:
    """Create database tables from shared SQLAlchemy metadata."""
    _load_model_modules()
    Base.metadata.create_all(bind=engine)
