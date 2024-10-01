# routers/event_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.event_controller import EventController
from ..models.event_model import Event
from ..schemas.event_schema import (EventCreateSchema, EventSchema,
                                    EventUpdateSchema)

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
def create_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new event.

    Args:
        event: The event data.

    Returns:
        A message confirming the event creation along with the event data.
    """
    return {"message": "Event created", "data": event}


@router.get("/{event_id}", response_model=Dict[str, Any])
def read_event(event_id: int) -> Dict[str, Any]:
    """Retrieve an event by ID.

    Args:
        event_id: The ID of the event.

    Returns:
        A message confirming the event retrieval along with the event ID.
    """
    return {"message": "Event retrieved", "event_id": event_id}


@router.put("/{event_id}", response_model=Dict[str, Any])
def update_event(event_id: int, event: Dict[str, Any]) -> Dict[str, Any]:
    """Update an event by ID.

    Args:
        event_id: The ID of the event to update.
        event: The updated event data.

    Returns:
        A message confirming the event update along with the event data.
    """
    return {"message": "Event updated", "event_id": event_id, "data": event}


@router.delete("/{event_id}", response_model=Dict[str, Any])
def delete_event(event_id: int) -> Dict[str, Any]:
    """Delete an event by ID.

    Args:
        event_id: The ID of the event to delete.

    Returns:
        A message confirming the successful deletion of the event.
    """
    return {"message": "Event deleted successfully", "event_id": event_id}


@router.get("/", response_model=List[Dict[str, Any]])
def list_events() -> List[Dict[str, Any]]:
    """List all events.

    Returns:
        A list of events with their IDs and names.
    """
    return [{"event_id": 1, "name": "Event A"}, {"event_id": 2, "name": "Event B"}]
