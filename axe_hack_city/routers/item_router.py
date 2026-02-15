# routers/item_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.item_controller import ItemController
from ..database.session import get_session
from ..models.item_model import Item
from ..schemas.item_schema import (ItemCreateSchema, ItemSchema,
                                   ItemUpdateSchema)

router = APIRouter()


@router.post("/", response_model=ItemSchema)
def create_item(item: ItemCreateSchema, db: Session = Depends(get_session)) -> Item:
    controller = ItemController(db)
    new_item = Item(**item.model_dump())
    return controller.create_item(new_item)


@router.get("/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_session)) -> Item:
    controller = ItemController(db)
    item = controller.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemSchema)
def update_item(
    item_id: int,
    item_update: ItemUpdateSchema,
    db: Session = Depends(get_session),
) -> Item:
    controller = ItemController(db)
    item = controller.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    return controller.update_item(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_session)) -> Response:
    controller = ItemController(db)
    item = controller.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    controller.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[ItemSchema])
def list_items(db: Session = Depends(get_session)) -> List[Item]:
    controller = ItemController(db)
    return controller.list_items()
