# routers/npc_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.npc_controller import NpcController
from ..models.npc_model import Npc
from ..schemas.npc_schema import NpcCreateSchema, NpcSchema, NpcUpdateSchema

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
def create_npc(npc: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new NPC.

    Args:
        npc: The NPC data.

    Returns:
        The created NPC data.
    """
    return {"id": 1, "name": npc.get("name")}


@router.get("/{npc_id}", response_model=Dict[str, Any])
def get_npc(npc_id: int) -> Dict[str, Any]:
    """Retrieve an NPC by ID.

    Args:
        npc_id: The ID of the NPC.

    Returns:
        The retrieved NPC data.
    """
    return {"id": npc_id, "name": "Sample NPC"}


@router.put("/{npc_id}", response_model=Dict[str, Any])
def update_npc(npc_id: int, npc: Dict[str, Any]) -> Dict[str, Any]:
    """Update an NPC by ID.

    Args:
        npc_id: The ID of the NPC to update.
        npc: The updated NPC data.

    Returns:
        The updated NPC data.
    """
    return {"id": npc_id, "name": npc.get("name")}


@router.delete("/{npc_id}", response_model=Dict[str, Any])
def delete_npc(npc_id: int) -> Dict[str, Any]:
    """Delete an NPC by ID.

    Args:
        npc_id: The ID of the NPC to delete.

    Returns:
        A message confirming the successful deletion of the NPC.
    """
    return {"detail": "NPC deleted successfully"}


@router.get("/", response_model=List[Dict[str, Any]])
def list_npcs() -> List[Dict[str, Any]]:
    """List all NPCs.

    Returns:
        A list of NPCs with their IDs and names.
    """
    return [{"id": 1, "name": "Sample NPC 1"}, {"id": 2, "name": "Sample NPC 2"}]
