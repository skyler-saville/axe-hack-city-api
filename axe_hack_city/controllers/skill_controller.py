# controllers/skill_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.skill_model import Skill


class SkillController:
    """Controller for managing Skill entities."""

    def __init__(self, session: Session):
        """Initialize the SkillController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, Skill)

    def create_skill(self, skill: Skill) -> Skill:
        """Create a new skill.

        Args:
            skill (Skill): The skill to create.

        Returns:
            Skill: The created skill.
        """
        return self.repository.create(skill)

    def get_skill(self, skill_id: int) -> Skill:
        """Retrieve a skill by its ID.

        Args:
            skill_id (int): The ID of the skill.

        Returns:
            Skill: The requested skill.
        """
        return self.repository.get(skill_id)

    def update_skill(self, skill: Skill) -> Skill:
        """Update an existing skill.

        Args:
            skill (Skill): The skill to update.

        Returns:
            Skill: The updated skill.
        """
        return self.repository.update(skill)

    def delete_skill(self, skill_id: int) -> None:
        """Delete a skill by its ID.

        Args:
            skill_id (int): The ID of the skill to delete.
        """
        self.repository.delete(skill_id)

    def list_skills(self, **filters) -> List[Skill]:
        """List skills with optional filters.

        Returns:
            List[Skill]: A list of skills.
        """
        return self.repository.list(**filters)
