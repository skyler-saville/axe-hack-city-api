# controllers/floor_layout_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.floor_layout_model import FloorLayout

class FloorLayoutController:
    """Controller for managing FloorLayout entities."""
    
    def __init__(self, session: Session):
        """Initialize the FloorLayoutController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, FloorLayout)

    def create_floor_layout(self, floor_layout: FloorLayout) -> FloorLayout:
        """Create a new floor layout.

        Args:
            floor_layout (FloorLayout): The floor layout to create.

        Returns:
            FloorLayout: The created floor layout.
        """
        return self.repository.create(floor_layout)

    def get_floor_layout(self, floor_layout_id: int) -> FloorLayout:
        """Retrieve a floor layout by its ID.

        Args:
            floor_layout_id (int): The ID of the floor layout.

        Returns:
            FloorLayout: The requested floor layout.
        """
        return self.repository.get(floor_layout_id)

    def update_floor_layout(self, floor_layout: FloorLayout) -> FloorLayout:
        """Update an existing floor layout.

        Args:
            floor_layout (FloorLayout): The floor layout to update.

        Returns:
            FloorLayout: The updated floor layout.
        """
        return self.repository.update(floor_layout)

    def delete_floor_layout(self, floor_layout_id: int) -> None:
        """Delete a floor layout by its ID.

        Args:
            floor_layout_id (int): The ID of the floor layout to delete.
        """
        self.repository.delete(floor_layout_id)

    def list_floor_layouts(self, **filters) -> List[FloorLayout]:
        """List floor layouts with optional filters.

        Returns:
            List[FloorLayout]: A list of floor layouts.
        """
        return self.repository.list(**filters)