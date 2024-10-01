# routers/faction_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.faction_controller import FactionController
from ..models.faction_model import Faction
from ..schemas.faction_schema import (FactionCreateSchema, FactionSchema,
                                      FactionUpdateSchema)

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
def create_faction(faction: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new faction.

    Args:
        faction: The faction data.

    Returns:
        A message confirming the faction creation along with the faction data.
    """
    return {"message": "Faction created", "data": faction}


@router.get("/{faction_id}", response_model=Dict[str, Any])
def get_faction(faction_id: int) -> Dict[str, Any]:
    """Retrieve a faction by ID.

    Args:
        faction_id: The ID of the faction.

    Returns:
        A message confirming the faction retrieval along with the faction ID.
    """
    return {"message": "Faction retrieved", "faction_id": faction_id}


@router.put("/{faction_id}", response_model=Dict[str, Any])
def update_faction(faction_id: int, faction: Dict[str, Any]) -> Dict[str, Any]:
    """Update a faction by ID.

    Args:
        faction_id: The ID of the faction to update.
        faction: The updated faction data.

    Returns:
        A message confirming the faction update along with the faction data.
    """
    return {"message": "Faction updated", "faction_id": faction_id, "data": faction}


@router.delete("/{faction_id}", response_model=Dict[str, Any])
def delete_faction(faction_id: int) -> Dict[str, Any]:
    """Delete a faction by ID.

    Args:
        faction_id: The ID of the faction to delete.

    Returns:
        A message confirming the successful deletion of the faction.
    """
    return {"message": "Faction deleted successfully", "faction_id": faction_id}


@router.get("/", response_model=List[Dict[str, Any]])
def list_factions() -> List[Dict[str, Any]]:
    """List all factions.

    Returns:
        A list of factions with their IDs and names.
    """
    return [
        {"faction_id": 1, "name": "Faction A"},
        {"faction_id": 2, "name": "Faction B"},
    ]
