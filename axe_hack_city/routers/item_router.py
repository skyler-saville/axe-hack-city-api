from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new item.

    Args:
        item: The item data.

    Returns:
        The created item data.
    """
    return {"id": 1, "name": item.get("name"), "description": item.get("description")}

@router.get("/{item_id}", response_model=Dict[str, Any])
def get_item(item_id: int) -> Dict[str, Any]:
    """Retrieve an item by ID.

    Args:
        item_id: The ID of the item.

    Returns:
        The retrieved item data.
    """
    return {"id": item_id, "name": "Sample Item", "description": "Sample description"}

@router.put("/{item_id}", response_model=Dict[str, Any])
def update_item(item_id: int, item: Dict[str, Any]) -> Dict[str, Any]:
    """Update an item by ID.

    Args:
        item_id: The ID of the item to update.
        item: The updated item data.

    Returns:
        The updated item data.
    """
    return {"id": item_id, "name": item.get("name"), "description": item.get("description")}

@router.delete("/{item_id}", response_model=Dict[str, Any])
def delete_item(item_id: int) -> Dict[str, Any]:
    """Delete an item by ID.

    Args:
        item_id: The ID of the item to delete.

    Returns:
        A message confirming the successful deletion of the item.
    """
    return {"detail": "Item deleted successfully"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_items() -> List[Dict[str, Any]]:
    """List all items.

    Returns:
        A list of items with their IDs and names.
    """
    return [{"id": 1, "name": "Sample Item 1"}, {"id": 2, "name": "Sample Item 2"}]
