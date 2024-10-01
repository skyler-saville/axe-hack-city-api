# controllers/building_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.building_model import Building


class BuildingController:
    """Controller for managing Building entities."""

    def __init__(self, session: Session):
        """Initialize the BuildingController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Building)

    def create_building(self, building: Building) -> Building:
        """Create a new building.

        Args:
            building (Building): The building to create.

        Returns:
            Building: The created building.
        """
        return self.repository.create(building)

    def get_building(self, building_id: int) -> Building:
        """Retrieve a building by its ID.

        Args:
            building_id (int): The ID of the building.

        Returns:
            Building: The requested building.
        """
        return self.repository.get(building_id)

    def update_building(self, building: Building) -> Building:
        """Update an existing building.

        Args:
            building (Building): The building to update.

        Returns:
            Building: The updated building.
        """
        return self.repository.update(building)

    def delete_building(self, building_id: int) -> None:
        """Delete a building by its ID.

        Args:
            building_id (int): The ID of the building to delete.
        """
        self.repository.delete(building_id)

    def list_buildings(self, **filters) -> List[Building]:
        """List buildings with optional filters.

        Returns:
            List[Building]: A list of buildings.
        """
        return self.repository.list(**filters)
