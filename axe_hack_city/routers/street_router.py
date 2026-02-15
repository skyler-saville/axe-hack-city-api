# routers/street_router.py
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers.street_controller import StreetController
from ..database.session import get_session
from ..models.street_model import Street
from ..schemas.street_schema import (StreetCreateSchema, StreetSchema,
                                     StreetUpdateSchema)

router = APIRouter()


def get_street_controller(
    session: Session = Depends(get_session),
) -> StreetController:
    """
    Get an instance of the StreetController.

    Args:
        session (Session): The injected database session.

    Returns:
        StreetController: An instance of the StreetController.
    """
    return StreetController(session)


@router.post("/", response_model=StreetSchema)
def create_street(
    street: StreetCreateSchema,
    street_controller: StreetController = Depends(get_street_controller),
) -> StreetSchema:
    """
    Create a new street.

    Args:
        street (StreetCreateSchema): The street data to create.
        street_controller (StreetController): The injected street controller.

    Returns:
        StreetSchema: The created street.
    """
    new_street = street_controller.create_street(Street(**street.model_dump()))
    return StreetSchema.model_validate(new_street)


@router.get("/{street_id}", response_model=StreetSchema)
def get_street(
    street_id: int,
    street_controller: StreetController = Depends(get_street_controller),
) -> StreetSchema:
    """
    Retrieve a street by ID.

    Args:
        street_id (int): The ID of the street to retrieve.
        street_controller (StreetController): The injected street controller.

    Returns:
        StreetSchema: The retrieved street.
    """
    street = street_controller.get_street(street_id)
    return StreetSchema.model_validate(street)


@router.put("/{street_id}", response_model=StreetSchema)
def update_street(
    street_id: int,
    street: StreetUpdateSchema,
    street_controller: StreetController = Depends(get_street_controller),
) -> StreetSchema:
    """
    Update an existing street.

    Args:
        street_id (int): The ID of the street to update.
        street (StreetUpdateSchema): The updated street data.
        street_controller (StreetController): The injected street controller.

    Returns:
        StreetSchema: The updated street.
    """
    updated_street = street_controller.update_street(
        Street(id=street_id, **street.model_dump())
    )
    return StreetSchema.model_validate(updated_street)


@router.delete("/{street_id}", response_model=Dict[str, Any])
def delete_street(
    street_id: int,
    street_controller: StreetController = Depends(get_street_controller),
) -> Dict[str, Any]:
    """
    Delete a street by ID.

    Args:
        street_id (int): The ID of the street to delete.
        street_controller (StreetController): The injected street controller.

    Returns:
        Dict[str, Any]: A message confirming the successful deletion of the street.
    """
    street_controller.delete_street(street_id)
    return {"message": "Street deleted successfully", "street_id": street_id}


@router.get("/", response_model=List[StreetSchema])
def list_streets(
    street_controller: StreetController = Depends(get_street_controller),
    **filters: Any,
) -> List[StreetSchema]:
    """
    List streets with optional filters.

    Args:
        street_controller (StreetController): The injected street controller.
        **filters (Any): Optional filters to apply to the street list.

    Returns:
        List[StreetSchema]: A list of streets.
    """
    streets = street_controller.list_streets(**filters)
    return [StreetSchema.model_validate(street) for street in streets]
