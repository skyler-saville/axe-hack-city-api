# controllers/crafting_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.crafting_model import CraftingRecipe as Crafting

class CraftingController:
    """Controller for managing Crafting entities."""
    
    def __init__(self, session: Session):
        """Initialize the CraftingController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Crafting)

    def create_crafting(self, crafting: Crafting) -> Crafting:
        """Create a new crafting item.

        Args:
            crafting (Crafting): The crafting item to create.

        Returns:
            Crafting: The created crafting item.
        """
        return self.repository.create(crafting)

    def get_crafting(self, crafting_id: int) -> Crafting:
        """Retrieve a crafting item by its ID.

        Args:
            crafting_id (int): The ID of the crafting item.

        Returns:
            Crafting: The requested crafting item.
        """
        return self.repository.get(crafting_id)

    def update_crafting(self, crafting: Crafting) -> Crafting:
        """Update an existing crafting item.

        Args:
            crafting (Crafting): The crafting item to update.

        Returns:
            Crafting: The updated crafting item.
        """
        return self.repository.update(crafting)

    def delete_crafting(self, crafting_id: int) -> None:
        """Delete a crafting item by its ID.

        Args:
            crafting_id (int): The ID of the crafting item to delete.
        """
        self.repository.delete(crafting_id)

    def list_craftings(self, **filters) -> List[Crafting]:
        """List crafting items with optional filters.

        Returns:
            List[Crafting]: A list of crafting items.
        """
        return self.repository.list(**filters)
