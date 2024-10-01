# controllers/floor_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.floor_model import Floor


class FloorController:
    """Controller for managing Floor entities."""

    def __init__(self, session: Session):
        """Initialize the FloorController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Floor)

    def create_floor(self, floor: Floor) -> Floor:
        """Create a new floor.

        Args:
            floor (Floor): The floor to create.

        Returns:
            Floor: The created floor.
        """
        return self.repository.create(floor)

    def get_floor(self, floor_id: int) -> Floor:
        """Retrieve a floor by its ID.

        Args:
            floor_id (int): The ID of the floor.

        Returns:
            Floor: The requested floor.
        """
        return self.repository.get(floor_id)

    def update_floor(self, floor: Floor) -> Floor:
        """Update an existing floor.

        Args:
            floor (Floor): The floor to update.

        Returns:
            Floor: The updated floor.
        """
        return self.repository.update(floor)

    def delete_floor(self, floor_id: int) -> None:
        """Delete a floor by its ID.

        Args:
            floor_id (int): The ID of the floor to delete.
        """
        self.repository.delete(floor_id)

    def list_floors(self, **filters) -> List[Floor]:
        """List floors with optional filters.

        Returns:
            List[Floor]: A list of floors.
        """
        return self.repository.list(**filters)
