from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=Dict[str, Any])
def create_session(session: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new game session.

    Args:
        session: The session data.

    Returns:
        The created session data.
    """
    return {"id": 1, "name": session.get("name")}

@router.get("/{session_id}", response_model=Dict[str, Any])
def read_session(session_id: int) -> Dict[str, Any]:
    """Retrieve a game session by ID.

    Args:
        session_id: The ID of the session.

    Returns:
        The retrieved session data.
    """
    return {"id": session_id, "name": "Sample Session"}

@router.put("/{session_id}", response_model=Dict[str, Any])
def update_session(session_id: int, session: Dict[str, Any]) -> Dict[str, Any]:
    """Update a game session by ID.

    Args:
        session_id: The ID of the session to update.
        session: The updated session data.

    Returns:
        The updated session data.
    """
    return {"id": session_id, "name": session.get("name")}

@router.delete("/{session_id}", response_model=Dict[str, Any])
def delete_session(session_id: int) -> Dict[str, Any]:
    """Delete a game session by ID.

    Args:
        session_id: The ID of the session to delete.

    Returns:
        A message confirming the successful deletion of the session.
    """
    return {"detail": "Session deleted successfully"}

@router.get("/", response_model=List[Dict[str, Any]])
def list_sessions() -> List[Dict[str, Any]]:
    """List all game sessions.

    Returns:
        A list of sessions with their IDs and names.
    """
    return [{"id": 1, "name": "Sample Session 1"}, {"id": 2, "name": "Sample Session 2"}]
