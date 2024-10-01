# routers/location_router.py
from typing import Any, Dict, List

from fastapi import APIRouter

from ..controllers.location_controller import LocationController
from ..models.location_model import Location
from ..schemas.location_schema import (LocationCreateSchema, LocationSchema,
                                       LocationUpdateSchema)

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_location(location: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new location.

    Args:
        location: The location data.

    Returns:
        The created location data.
    """
    return {"id": 1, "name": location.get("name")}


@router.get("/{location_id}", response_model=Dict[str, Any])
async def read_location(location_id: int) -> Dict[str, Any]:
    """Retrieve a location by ID.

    Args:
        location_id: The ID of the location.

    Returns:
        The retrieved location data.
    """
    return {"id": location_id, "name": "Sample Location"}


@router.put("/{location_id}", response_model=Dict[str, Any])
async def update_location(location_id: int, location: Dict[str, Any]) -> Dict[str, Any]:
    """Update a location by ID.

    Args:
        location_id: The ID of the location to update.
        location: The updated location data.

    Returns:
        The updated location data.
    """
    return {"id": location_id, "name": location.get("name")}


@router.delete("/{location_id}", response_model=Dict[str, Any])
async def delete_location(location_id: int) -> Dict[str, Any]:
    """Delete a location by ID.

    Args:
        location_id: The ID of the location to delete.

    Returns:
        A message confirming the successful deletion of the location.
    """
    return {"detail": "Location deleted successfully"}


@router.get("/", response_model=List[Dict[str, Any]])
async def list_locations() -> List[Dict[str, Any]]:
    """List all locations.

    Returns:
        A list of locations with their IDs and names.
    """
    return [
        {"id": 1, "name": "Sample Location 1"},
        {"id": 2, "name": "Sample Location 2"},
    ]
