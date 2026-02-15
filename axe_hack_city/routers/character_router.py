# routers/character_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.character_controller import CharacterController
from ..database.session import get_session
from ..models.character_model import Character
from ..schemas.character_schema import (CharacterCreateSchema, CharacterSchema,
                                        CharacterUpdateSchema)

router = APIRouter()


@router.post("/", response_model=CharacterSchema)
def create_character(
    character: CharacterCreateSchema, db: Session = Depends(get_session)
) -> Character:
    controller = CharacterController(db)
    new_character = Character(**character.model_dump())
    return controller.create_character(new_character)


@router.get("/{character_id}", response_model=CharacterSchema)
def get_character(character_id: int, db: Session = Depends(get_session)) -> Character:
    controller = CharacterController(db)
    character = controller.get_character(character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.put("/{character_id}", response_model=CharacterSchema)
def update_character(
    character_id: int,
    character_update: CharacterUpdateSchema,
    db: Session = Depends(get_session),
) -> Character:
    controller = CharacterController(db)
    character = controller.get_character(character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    for field, value in character_update.model_dump(exclude_unset=True).items():
        setattr(character, field, value)

    return controller.update_character(character)


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int, db: Session = Depends(get_session)) -> Response:
    controller = CharacterController(db)
    character = controller.get_character(character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    controller.delete_character(character_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[CharacterSchema])
def list_characters(db: Session = Depends(get_session)) -> List[Character]:
    controller = CharacterController(db)
    return controller.list_characters()
