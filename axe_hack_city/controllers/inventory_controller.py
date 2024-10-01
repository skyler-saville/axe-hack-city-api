# controllers/inventory_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.inventory_model import Inventory


class InventoryController:
    """Controller for managing Inventory entities."""

    def __init__(self, session: Session):
        """Initialize the InventoryController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Inventory)

    def create_inventory(self, inventory: Inventory) -> Inventory:
        """Create a new inventory item.

        Args:
            inventory (Inventory): The inventory item to create.

        Returns:
            Inventory: The created inventory item.
        """
        return self.repository.create(inventory)

    def get_inventory(self, inventory_id: int) -> Inventory:
        """Retrieve an inventory item by its ID.

        Args:
            inventory_id (int): The ID of the inventory item.

        Returns:
            Inventory: The requested inventory item.
        """
        return self.repository.get(inventory_id)

    def update_inventory(self, inventory: Inventory) -> Inventory:
        """Update an existing inventory item.

        Args:
            inventory (Inventory): The inventory item to update.

        Returns:
            Inventory: The updated inventory item.
        """
        return self.repository.update(inventory)

    def delete_inventory(self, inventory_id: int) -> None:
        """Delete an inventory item by its ID.

        Args:
            inventory_id (int): The ID of the inventory item to delete.
        """
        self.repository.delete(inventory_id)

    def list_inventories(self, **filters) -> List[Inventory]:
        """List inventory items with optional filters.

        Returns:
            List[Inventory]: A list of inventory items.
        """
        return self.repository.list(**filters)
