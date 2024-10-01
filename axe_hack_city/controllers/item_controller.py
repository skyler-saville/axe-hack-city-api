# controllers/item_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.item_model import Item


class ItemController:
    """Controller for managing Item entities."""

    def __init__(self, session: Session):
        """Initialize the ItemController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Item)

    def create_item(self, item: Item) -> Item:
        """Create a new item.

        Args:
            item (Item): The item to create.

        Returns:
            Item: The created item.
        """
        return self.repository.create(item)

    def get_item(self, item_id: int) -> Item:
        """Retrieve an item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Item: The requested item.
        """
        return self.repository.get(item_id)

    def update_item(self, item: Item) -> Item:
        """Update an existing item.

        Args:
            item (Item): The item to update.

        Returns:
            Item: The updated item.
        """
        return self.repository.update(item)

    def delete_item(self, item_id: int) -> None:
        """Delete an item by its ID.

        Args:
            item_id (int): The ID of the item to delete.
        """
        self.repository.delete(item_id)

    def list_items(self, **filters) -> List[Item]:
        """List items with optional filters.

        Returns:
            List[Item]: A list of items.
        """
        return self.repository.list(**filters)
