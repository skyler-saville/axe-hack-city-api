from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_mission(mission: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new mission.

    Args:
        mission: The mission data.

    Returns:
        The created mission data.
    """
    return {"id": 1, "name": mission.get("name")}

@router.get("/{mission_id}", response_model=Dict[str, Any])
def read_mission(mission_id: int) -> Dict[str, Any]:
    """Retrieve a mission by ID.

    Args:
        mission_id: The ID of the mission.

    Returns:
        The retrieved mission data.
    """
    return {"id": mission_id, "name": "Sample Mission"}

@router.put("/{mission_id}", response_model=Dict[str, Any])
def update_mission(mission_id: int, mission: Dict[str, Any]) -> Dict[str, Any]:
    """Update a mission by ID.

    Args:
        mission_id: The ID of the mission to update.
        mission: The updated mission data.

    Returns:
        The updated mission data.
    """
    return {"id": mission_id, "name": mission.get("name")}

@router.delete("/{mission_id}", response_model=Dict[str, Any])
def delete_mission(mission_id: int) -> Dict[str, Any]:
    """Delete a mission by ID.

    Args:
        mission_id: The ID of the mission to delete.

    Returns:
        A message confirming the successful deletion of the mission.
    """
    return {"detail": "Mission deleted"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_missions() -> List[Dict[str, Any]]:
    """List all missions.

    Returns:
        A list of missions with their IDs and names.
    """
    return [{"id": 1, "name": "Sample Mission 1"}, {"id": 2, "name": "Sample Mission 2"}]
