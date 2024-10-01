# controllers/npc_controller.py
from typing import List

from sqlalchemy.orm import Session

from ..database.sqlalchemy_repository import SQLAlchemyRepository
from ..models.npc_model import NPC


class NPCController:
    """Controller for managing NPC entities."""

    def __init__(self, session: Session):
        """Initialize the NPCController.

        Args:
            session (Session): SQLAlchemy session.
        """
        self.repository = SQLAlchemyRepository(session, NPC)

    def create_npc(self, npc: NPC) -> NPC:
        """Create a new NPC.

        Args:
            npc (NPC): The NPC to create.

        Returns:
            NPC: The created NPC.
        """
        return self.repository.create(npc)

    def get_npc(self, npc_id: int) -> NPC:
        """Retrieve an NPC by its ID.

        Args:
            npc_id (int): The ID of the NPC.

        Returns:
            NPC: The requested NPC.
        """
        return self.repository.get(npc_id)

    def update_npc(self, npc: NPC) -> NPC:
        """Update an existing NPC.

        Args:
            npc (NPC): The NPC to update.

        Returns:
            NPC: The updated NPC.
        """
        return self.repository.update(npc)

    def delete_npc(self, npc_id: int) -> None:
        """Delete an NPC by its ID.

        Args:
            npc_id (int): The ID of the NPC to delete.
        """
        self.repository.delete(npc_id)

    def list_npcs(self, **filters) -> List[NPC]:
        """List NPCs with optional filters.

        Returns:
            List[NPC]: A list of NPCs.
        """
        return self.repository.list(**filters)
