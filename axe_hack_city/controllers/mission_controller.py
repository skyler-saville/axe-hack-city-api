# controllers/mission_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.mission_model import Mission

class MissionController:
    """Controller for managing Mission entities."""
    
    def __init__(self, session: Session):
        """Initialize the MissionController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Mission)

    def create_mission(self, mission: Mission) -> Mission:
        """Create a new mission.

        Args:
            mission (Mission): The mission to create.

        Returns:
            Mission: The created mission.
        """
        return self.repository.create(mission)

    def get_mission(self, mission_id: int) -> Mission:
        """Retrieve a mission by its ID.

        Args:
            mission_id (int): The ID of the mission.

        Returns:
            Mission: The requested mission.
        """
        return self.repository.get(mission_id)

    def update_mission(self, mission: Mission) -> Mission:
        """Update an existing mission.

        Args:
            mission (Mission): The mission to update.

        Returns:
            Mission: The updated mission.
        """
        return self.repository.update(mission)

    def delete_mission(self, mission_id: int) -> None:
        """Delete a mission by its ID.

        Args:
            mission_id (int): The ID of the mission to delete.
        """
        self.repository.delete(mission_id)

    def list_missions(self, **filters) -> List[Mission]:
        """List missions with optional filters.

        Returns:
            List[Mission]: A list of missions.
        """
        return self.repository.list(**filters)
