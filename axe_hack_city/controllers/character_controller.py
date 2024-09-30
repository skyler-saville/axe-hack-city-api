# controllers/character_controller.py
from typing import List
from sqlalchemy.orm import Session
from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.character_model import Character

class CharacterController:
    """Controller for managing Character entities."""
    
    def __init__(self, session: Session):
        """Initialize the CharacterController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Character)

    def create_character(self, character: Character) -> Character:
        """Create a new character.

        Args:
            character (Character): The character to create.

        Returns:
            Character: The created character.
        """
        return self.repository.create(character)

    def get_character(self, character_id: int) -> Character:
        """Retrieve a character by its ID.

        Args:
            character_id (int): The ID of the character.

        Returns:
            Character: The requested character.
        """
        return self.repository.get(character_id)

    def update_character(self, character: Character) -> Character:
        """Update an existing character.

        Args:
            character (Character): The character to update.

        Returns:
            Character: The updated character.
        """
        return self.repository.update(character)

    def delete_character(self, character_id: int) -> None:
        """Delete a character by its ID.

        Args:
            character_id (int): The ID of the character to delete.
        """
        self.repository.delete(character_id)

    def list_characters(self, **filters) -> List[Character]:
        """List characters with optional filters.

        Returns:
            List[Character]: A list of characters.
        """
        return self.repository.list(**filters)