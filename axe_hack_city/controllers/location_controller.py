# controllers/location_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.location_model import Location

class LocationController:
    """Controller for managing Location entities."""
    
    def __init__(self, session: Session):
        """Initialize the LocationController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Location)

    def create_location(self, location: Location) -> Location:
        """Create a new location.

        Args:
            location (Location): The location to create.

        Returns:
            Location: The created location.
        """
        return self.repository.create(location)

    def get_location(self, location_id: int) -> Location:
        """Retrieve a location by its ID.

        Args:
            location_id (int): The ID of the location.

        Returns:
            Location: The requested location.
        """
        return self.repository.get(location_id)

    def update_location(self, location: Location) -> Location:
        """Update an existing location.

        Args:
            location (Location): The location to update.

        Returns:
            Location: The updated location.
        """
        return self.repository.update(location)

    def delete_location(self, location_id: int) -> None:
        """Delete a location by its ID.

        Args:
            location_id (int): The ID of the location to delete.
        """
        self.repository.delete(location_id)

    def list_locations(self, **filters) -> List[Location]:
        """List locations with optional filters.

        Returns:
            List[Location]: A list of locations.
        """
        return self.repository.list(**filters)