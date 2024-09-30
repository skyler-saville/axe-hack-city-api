from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_inventory(inventory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new inventory item.

    Args:
        inventory_data: The inventory item data.

    Returns:
        The created inventory item data.
    """
    return {"id": 1, "name": inventory_data.get("name"), "quantity": inventory_data.get("quantity")}

@router.get("/{inventory_id}", response_model=Dict[str, Any])
def get_inventory(inventory_id: int) -> Dict[str, Any]:
    """Retrieve an inventory item by ID.

    Args:
        inventory_id: The ID of the inventory item.

    Returns:
        The retrieved inventory item data.
    """
    return {"id": inventory_id, "name": "Sample Item", "quantity": 100}

@router.put("/{inventory_id}", response_model=Dict[str, Any])
def update_inventory(inventory_id: int, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an inventory item by ID.

    Args:
        inventory_id: The ID of the inventory item to update.
        inventory_data: The updated inventory item data.

    Returns:
        The updated inventory item data.
    """
    return {"id": inventory_id, "name": inventory_data.get("name"), "quantity": inventory_data.get("quantity")}

@router.delete("/{inventory_id}", response_model=Dict[str, Any])
def delete_inventory(inventory_id: int) -> Dict[str, Any]:
    """Delete an inventory item by ID.

    Args:
        inventory_id: The ID of the inventory item to delete.

    Returns:
        A message confirming the successful deletion of the inventory item.
    """
    return {"detail": "Inventory deleted successfully"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_inventories() -> List[Dict[str, Any]]:
    """List all inventory items.

    Returns:
        A list of inventory items with their IDs and names.
    """
    return [{"id": 1, "name": "Sample Item 1"}, {"id": 2, "name": "Sample Item 2"}]
