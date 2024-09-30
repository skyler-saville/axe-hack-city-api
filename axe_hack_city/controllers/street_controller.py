# controllers/street_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.street_model import Street

class StreetController:
    """Controller for managing Street entities."""
    
    def __init__(self, session: Session):
        """Initialize the StreetController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Street)

    def create_street(self, street: Street) -> Street:
        """Create a new street.

        Args:
            street (Street): The street to create.

        Returns:
            Street: The created street.
        """
        return self.repository.create(street)

    def get_street(self, street_id: int) -> Street:
        """Retrieve a street by its ID.

        Args:
            street_id (int): The ID of the street.

        Returns:
            Street: The requested street.
        """
        return self.repository.get(street_id)

    def update_street(self, street: Street) -> Street:
        """Update an existing street.

        Args:
            street (Street): The street to update.

        Returns:
            Street: The updated street.
        """
        return self.repository.update(street)

    def delete_street(self, street_id: int) -> None:
        """Delete a street by its ID.

        Args:
            street_id (int): The ID of the street to delete.
        """
        self.repository.delete(street_id)

    def list_streets(self, **filters) -> List[Street]:
        """List streets with optional filters.

        Returns:
            List[Street]: A list of streets.
        """
        return self.repository.list(**filters)
