# routers/street_router.py
from typing import Any, Dict, List

from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..controllers.street_controller import StreetController
from ..models.street_model import Street
from ..schemas.street_schema import (StreetCreateSchema, StreetSchema,
                                     StreetUpdateSchema)

router = APIRouter()


def get_street_controller(session: Session) -> StreetController:
    """
    Get an instance of the StreetController.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        StreetController: An instance of the StreetController.
    """
    return StreetController(session)


@router.post("/", response_model=StreetSchema)
def create_street(street: StreetCreateSchema, session: Session) -> StreetSchema:
    """
    Create a new street.

    Args:
        street (StreetCreateSchema): The street data to create.
        session (Session): The SQLAlchemy session.

    Returns:
        StreetSchema: The created street.
    """
    street_controller = get_street_controller(session)
    new_street = street_controller.create_street(Street(**street.model_dump()))
    return StreetSchema.model_validate(new_street)


@router.get("/{street_id}", response_model=StreetSchema)
def get_street(street_id: int, session: Session) -> StreetSchema:
    """
    Retrieve a street by ID.

    Args:
        street_id (int): The ID of the street to retrieve.
        session (Session): The SQLAlchemy session.

    Returns:
        StreetSchema: The retrieved street.
    """
    street_controller = get_street_controller(session)
    street = street_controller.get_street(street_id)
    return StreetSchema.model_validate(street)


@router.put("/{street_id}", response_model=StreetSchema)
def update_street(
    street_id: int, street: StreetUpdateSchema, session: Session
) -> StreetSchema:
    """
    Update an existing street.

    Args:
        street_id (int): The ID of the street to update.
        street (StreetUpdateSchema): The updated street data.
        session (Session): The SQLAlchemy session.

    Returns:
        StreetSchema: The updated street.
    """
    street_controller = get_street_controller(session)
    updated_street = street_controller.update_street(
        Street(id=street_id, **street.model_dump())
    )
    return StreetSchema.model_validate(updated_street)


@router.delete("/{street_id}", response_model=Dict[str, Any])
def delete_street(street_id: int, session: Session) -> Dict[str, Any]:
    """
    Delete a street by ID.

    Args:
        street_id (int): The ID of the street to delete.
        session (Session): The SQLAlchemy session.

    Returns:
        Dict[str, Any]: A message confirming the successful deletion of the street.
    """
    street_controller = get_street_controller(session)
    street_controller.delete_street(street_id)
    return {"message": "Street deleted successfully", "street_id": street_id}


@router.get("/", response_model=List[StreetSchema])
def list_streets(session: Session, **filters: Any) -> List[StreetSchema]:
    """
    List streets with optional filters.

    Args:
        session (Session): The SQLAlchemy session.
        **filters (Any): Optional filters to apply to the street list.

    Returns:
        List[StreetSchema]: A list of streets.
    """
    street_controller = get_street_controller(session)
    streets = street_controller.list_streets(**filters)
    return [StreetSchema.model_validate(street) for street in streets]
