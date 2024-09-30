from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_building(building: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new building.

    Args:
        building: The building data.

    Returns:
        A message confirming the building creation along with the building data.
    """
    return {"message": "Building created", "data": building}

@router.get("/{building_id}", response_model=Dict[str, Any])
def get_building(building_id: int) -> Dict[str, Any]:
    """Retrieve a building by ID.

    Args:
        building_id: The ID of the building.

    Returns:
        A message confirming the building retrieval along with the building ID.
    """
    return {"message": "Building retrieved", "building_id": building_id}

@router.put("/{building_id}", response_model=Dict[str, Any])
def update_building(building_id: int, building: Dict[str, Any]) -> Dict[str, Any]:
    """Update a building by ID.

    Args:
        building_id: The ID of the building to update.
        building: The updated building data.

    Returns:
        A message confirming the building update along with the building data.
    """
    return {"message": "Building updated", "building_id": building_id, "data": building}

@router.delete("/{building_id}", response_model=Dict[str, Any])
def delete_building(building_id: int) -> Dict[str, Any]:
    """Delete a building by ID.

    Args:
        building_id: The ID of the building to delete.

    Returns:
        A message confirming the successful deletion of the building.
    """
    return {"message": "Building deleted successfully", "building_id": building_id}

@router.get("/", response_model=List[Dict[str, Any]])
def list_buildings() -> List[Dict[str, Any]]:
    """List all buildings.

    Returns:
        A list of buildings with their IDs and names.
    """
    return [{"building_id": 1, "name": "Building A"}, {"building_id": 2, "name": "Building B"}]
