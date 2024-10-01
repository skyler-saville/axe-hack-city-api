# routers/progression_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.progression_controller import ProgressionController
from ..models.progression_model import Progression
from ..schemas.progression_schema import (ProgressionCreateSchema,
                                          ProgressionSchema,
                                          ProgressionUpdateSchema)

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
def create_progression(progression: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new progression.

    Args:
        progression: The progression data.

    Returns:
        The created progression data.
    """
    return {"id": 1, "character_id": progression.get("character_id")}


@router.get("/{progression_id}", response_model=Dict[str, Any])
def read_progression(progression_id: int) -> Dict[str, Any]:
    """Retrieve a progression by ID.

    Args:
        progression_id: The ID of the progression.

    Returns:
        The retrieved progression data.
    """
    return {"id": progression_id, "character_id": 1}


@router.put("/{progression_id}", response_model=Dict[str, Any])
def update_progression(
    progression_id: int, progression: Dict[str, Any]
) -> Dict[str, Any]:
    """Update a progression by ID.

    Args:
        progression_id: The ID of the progression to update.
        progression: The updated progression data.

    Returns:
        The updated progression data.
    """
    return {"id": progression_id, "character_id": progression.get("character_id")}


@router.delete("/{progression_id}", response_model=Dict[str, Any])
def delete_progression(progression_id: int) -> Dict[str, Any]:
    """Delete a progression by ID.

    Args:
        progression_id: The ID of the progression to delete.

    Returns:
        A message confirming the successful deletion of the progression.
    """
    return {"detail": "Progression deleted successfully"}


@router.get("/", response_model=List[Dict[str, Any]])
def list_progressions() -> List[Dict[str, Any]]:
    """List all progressions.

    Returns:
        A list of progressions with their IDs.
    """
    return [{"id": 1, "character_id": 1}, {"id": 2, "character_id": 2}]
