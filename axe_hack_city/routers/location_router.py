# routers/location_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.location_controller import LocationController
from ..database.session import get_session
from ..models.location_model import Location
from ..schemas.location_schema import (LocationCreateSchema, LocationSchema,
                                       LocationUpdateSchema)

router = APIRouter()


@router.post("/", response_model=LocationSchema)
def create_location(
    location: LocationCreateSchema, db: Session = Depends(get_session)
) -> Location:
    controller = LocationController(db)
    new_location = Location(**location.model_dump())
    return controller.create_location(new_location)


@router.get("/{location_id}", response_model=LocationSchema)
def read_location(location_id: int, db: Session = Depends(get_session)) -> Location:
    controller = LocationController(db)
    location = controller.get_location(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", response_model=LocationSchema)
def update_location(
    location_id: int,
    location_update: LocationUpdateSchema,
    db: Session = Depends(get_session),
) -> Location:
    controller = LocationController(db)
    location = controller.get_location(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    for field, value in location_update.model_dump(exclude_unset=True).items():
        setattr(location, field, value)

    return controller.update_location(location)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_session)) -> Response:
    controller = LocationController(db)
    location = controller.get_location(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    controller.delete_location(location_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[LocationSchema])
def list_locations(db: Session = Depends(get_session)) -> List[Location]:
    controller = LocationController(db)
    return controller.list_locations()
