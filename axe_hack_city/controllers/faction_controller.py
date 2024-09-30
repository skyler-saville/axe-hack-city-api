# controllers/faction_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.faction_model import Faction

class FactionController:
    """Controller for managing Faction entities."""
    
    def __init__(self, session: Session):
        """Initialize the FactionController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Faction)

    def create_faction(self, faction: Faction) -> Faction:
        """Create a new faction.

        Args:
            faction (Faction): The faction to create.

        Returns:
            Faction: The created faction.
        """
        return self.repository.create(faction)

    def get_faction(self, faction_id: int) -> Faction:
        """Retrieve a faction by its ID.

        Args:
            faction_id (int): The ID of the faction.

        Returns:
            Faction: The requested faction.
        """
        return self.repository.get(faction_id)

    def update_faction(self, faction: Faction) -> Faction:
        """Update an existing faction.

        Args:
            faction (Faction): The faction to update.

        Returns:
            Faction: The updated faction.
        """
        return self.repository.update(faction)

    def delete_faction(self, faction_id: int) -> None:
        """Delete a faction by its ID.

        Args:
            faction_id (int): The ID of the faction to delete.
        """
        self.repository.delete(faction_id)

    def list_factions(self, **filters) -> List[Faction]:
        """List factions with optional filters.

        Returns:
            List[Faction]: A list of factions.
        """
        return self.repository.list(**filters)