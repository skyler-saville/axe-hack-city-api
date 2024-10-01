# routers/crafting_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.crafting_controller import CraftingController
from ..models.crafting_model import Crafting
from ..schemas.crafting_schema import (CraftingCreateSchema, CraftingSchema,
                                       CraftingUpdateSchema)

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
def create_crafting(crafting: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new crafting recipe.

    Args:
        crafting: The crafting recipe data.

    Returns:
        A message confirming the crafting creation along with the crafting data.
    """
    return {"message": "Crafting recipe created", "data": crafting}


@router.get("/{crafting_id}", response_model=Dict[str, Any])
def get_crafting(crafting_id: int) -> Dict[str, Any]:
    """Retrieve a crafting recipe by ID.

    Args:
        crafting_id: The ID of the crafting recipe.

    Returns:
        A message confirming the crafting recipe retrieval along with the crafting ID.
    """
    return {"message": "Crafting recipe retrieved", "crafting_id": crafting_id}


@router.put("/{crafting_id}", response_model=Dict[str, Any])
def update_crafting(crafting_id: int, crafting: Dict[str, Any]) -> Dict[str, Any]:
    """Update a crafting recipe by ID.

    Args:
        crafting_id: The ID of the crafting recipe to update.
        crafting: The updated crafting recipe data.

    Returns:
        A message confirming the crafting recipe update along with the crafting data.
    """
    return {
        "message": "Crafting recipe updated",
        "crafting_id": crafting_id,
        "data": crafting,
    }


@router.delete("/{crafting_id}", response_model=Dict[str, Any])
def delete_crafting(crafting_id: int) -> Dict[str, Any]:
    """Delete a crafting recipe by ID.

    Args:
        crafting_id: The ID of the crafting recipe to delete.

    Returns:
        A message confirming the successful deletion of the crafting recipe.
    """
    return {
        "message": "Crafting recipe deleted successfully",
        "crafting_id": crafting_id,
    }


@router.get("/", response_model=List[Dict[str, Any]])
def list_craftings() -> List[Dict[str, Any]]:
    """List all crafting recipes.

    Returns:
        A list of crafting recipes with their IDs and names.
    """
    return [
        {"crafting_id": 1, "name": "Crafting A"},
        {"crafting_id": 2, "name": "Crafting B"},
    ]
