# controllers/user_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.user_model import User


class UserController:
    """Controller for managing User entities."""

    def __init__(self, session: Session):
        """Initialize the UserController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, User)

    def create_user(self, user: User) -> User:
        """Create a new user.

        Args:
            user (User): The user to create.

        Returns:
            User: The created user.
        """
        return self.repository.create(user)

    def get_user(self, user_id: int) -> User:
        """Retrieve a user by its ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The requested user.
        """
        return self.repository.get(user_id)

    def update_user(self, user: User) -> User:
        """Update an existing user.

        Args:
            user (User): The user to update.

        Returns:
            User: The updated user.
        """
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        """Delete a user by its ID.

        Args:
            user_id (int): The ID of the user to delete.
        """
        self.repository.delete(user_id)

    def list_users(self, **filters) -> List[User]:
        """List users with optional filters.

        Returns:
            List[User]: A list of users.
        """
        return self.repository.list(**filters)
