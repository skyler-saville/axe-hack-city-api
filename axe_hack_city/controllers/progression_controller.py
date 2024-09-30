# controllers/progression_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.progression_model import PlayerProgression as Progression

class ProgressionController:
    """Controller for managing Progression entities."""
    
    def __init__(self, session: Session):
        """Initialize the ProgressionController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Progression)

    def create_progression(self, progression: Progression) -> Progression:
        """Create a new progression.

        Args:
            progression (Progression): The progression to create.

        Returns:
            Progression: The created progression.
        """
        return self.repository.create(progression)

    def get_progression(self, progression_id: int) -> Progression:
        """Retrieve a progression by its ID.

        Args:
            progression_id (int): The ID of the progression.

        Returns:
            Progression: The requested progression.
        """
        return self.repository.get(progression_id)

    def update_progression(self, progression: Progression) -> Progression:
        """Update an existing progression.

        Args:
            progression (Progression): The progression to update.

        Returns:
            Progression: The updated progression.
        """
        return self.repository.update(progression)

    def delete_progression(self, progression_id: int) -> None:
        """Delete a progression by its ID.

        Args:
            progression_id (int): The ID of the progression to delete.
        """
        self.repository.delete(progression_id)

    def list_progressions(self, **filters) -> List[Progression]:
        """List progressions with optional filters.

        Returns:
            List[Progression]: A list of progressions.
        """
        return self.repository.list(**filters)
