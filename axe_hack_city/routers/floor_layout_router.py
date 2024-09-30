from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_floor_layout(floor_layout: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new floor layout.

    Args:
        floor_layout: The floor layout data.

    Returns:
        A message confirming the floor layout creation along with the floor layout data.
    """
    return {"message": "Floor layout created", "data": floor_layout}

@router.get("/{floor_layout_id}", response_model=Dict[str, Any])
def get_floor_layout(floor_layout_id: int) -> Dict[str, Any]:
    """Retrieve a floor layout by ID.

    Args:
        floor_layout_id: The ID of the floor layout.

    Returns:
        A message confirming the floor layout retrieval along with the floor layout ID.
    """
    return {"message": "Floor layout retrieved", "floor_layout_id": floor_layout_id}

@router.put("/{floor_layout_id}", response_model=Dict[str, Any])
def update_floor_layout(floor_layout_id: int, floor_layout: Dict[str, Any]) -> Dict[str, Any]:
    """Update a floor layout by ID.

    Args:
        floor_layout_id: The ID of the floor layout to update.
        floor_layout: The updated floor layout data.

    Returns:
        A message confirming the floor layout update along with the floor layout data.
    """
    return {"message": "Floor layout updated", "floor_layout_id": floor_layout_id, "data": floor_layout}

@router.delete("/{floor_layout_id}", response_model=Dict[str, Any])
def delete_floor_layout(floor_layout_id: int) -> Dict[str, Any]:
    """Delete a floor layout by ID.

    Args:
        floor_layout_id: The ID of the floor layout to delete.

    Returns:
        A message confirming the successful deletion of the floor layout.
    """
    return {"message": "Floor layout deleted successfully", "floor_layout_id": floor_layout_id}

@router.get("/", response_model=List[Dict[str, Any]])
def list_floor_layouts() -> List[Dict[str, Any]]:
    """List all floor layouts.

    Returns:
        A list of floor layouts with their IDs and names.
    """
    return [{"floor_layout_id": 1, "name": "Floor Layout A"}, {"floor_layout_id": 2, "name": "Floor Layout B"}]
