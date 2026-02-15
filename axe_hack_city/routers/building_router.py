# routers/building_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.building_controller import BuildingController
from ..database.session import get_session
from ..models.building_model import Building
from ..schemas.building_schema import (BuildingCreateSchema, BuildingSchema,
                                       BuildingUpdateSchema)

router = APIRouter()


@router.post("/", response_model=BuildingSchema)
def create_building(
    building: BuildingCreateSchema, db: Session = Depends(get_session)
) -> Building:
    controller = BuildingController(db)
    new_building = Building(**building.model_dump())
    return controller.create_building(new_building)


@router.get("/{building_id}", response_model=BuildingSchema)
def get_building(building_id: int, db: Session = Depends(get_session)) -> Building:
    controller = BuildingController(db)
    building = controller.get_building(building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.put("/{building_id}", response_model=BuildingSchema)
def update_building(
    building_id: int,
    building_update: BuildingUpdateSchema,
    db: Session = Depends(get_session),
) -> Building:
    controller = BuildingController(db)
    building = controller.get_building(building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    for field, value in building_update.model_dump(exclude_unset=True).items():
        setattr(building, field, value)

    return controller.update_building(building)


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(building_id: int, db: Session = Depends(get_session)) -> Response:
    controller = BuildingController(db)
    building = controller.get_building(building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    controller.delete_building(building_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[BuildingSchema])
def list_buildings(db: Session = Depends(get_session)) -> List[Building]:
    controller = BuildingController(db)
    return controller.list_buildings()
