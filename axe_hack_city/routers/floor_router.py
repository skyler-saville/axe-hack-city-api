from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_floor(floor: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new floor.

    Args:
        floor: The floor data.

    Returns:
        A message confirming the floor creation along with the floor data.
    """
    return {"message": "Floor created", "data": floor}

@router.get("/{floor_id}", response_model=Dict[str, Any])
def get_floor(floor_id: int) -> Dict[str, Any]:
    """Retrieve a floor by ID.

    Args:
        floor_id: The ID of the floor.

    Returns:
        A message confirming the floor retrieval along with the floor ID.
    """
    return {"message": "Floor retrieved", "floor_id": floor_id}

@router.put("/{floor_id}", response_model=Dict[str, Any])
def update_floor(floor_id: int, floor: Dict[str, Any]) -> Dict[str, Any]:
    """Update a floor by ID.

    Args:
        floor_id: The ID of the floor to update.
        floor: The updated floor data.

    Returns:
        A message confirming the floor update along with the floor data.
    """
    return {"message": "Floor updated", "floor_id": floor_id, "data": floor}

@router.delete("/{floor_id}", response_model=Dict[str, Any])
def delete_floor(floor_id: int) -> Dict[str, Any]:
    """Delete a floor by ID.

    Args:
        floor_id: The ID of the floor to delete.

    Returns:
        A message confirming the successful deletion of the floor.
    """
    return {"message": "Floor deleted successfully", "floor_id": floor_id}

@router.get("/", response_model=List[Dict[str, Any]])
def list_floors() -> List[Dict[str, Any]]:
    """List all floors.

    Returns:
        A list of floors with their IDs and names.
    """
    return [{"floor_id": 1, "name": "Floor A"}, {"floor_id": 2, "name": "Floor B"}]
