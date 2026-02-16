from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.faction_controller import FactionController
from ..database.session import get_session
from ..models.faction_model import Faction
from ..models.npc_model import NPC
from ..schemas.faction_schema import (
    FactionCreateSchema,
    FactionSchema,
    FactionUpdateSchema,
)

router = APIRouter()


def _to_faction_schema(faction: Faction) -> FactionSchema:
    """Convert a Faction ORM model into a response schema."""
    return FactionSchema(
        id=faction.id,
        name=faction.name,
        description=faction.description,
        reputation=faction.reputation,
        ally_ids=[ally.id for ally in faction.allies if ally.id is not None],
        enemy_ids=[enemy.id for enemy in faction.enemies if enemy.id is not None],
        npc_ids=[npc.id for npc in faction.npcs if npc.id is not None],
    )


def _resolve_factions(session: Session, faction_ids: List[int], relation_name: str) -> List[Faction]:
    """Resolve faction IDs into faction models, raising 404 for missing IDs."""
    factions: List[Faction] = []
    for faction_id in faction_ids:
        faction = session.get(Faction, faction_id)
        if faction is None:
            raise HTTPException(
                status_code=404,
                detail=f"{relation_name} faction with id {faction_id} not found",
            )
        factions.append(faction)
    return factions


def _resolve_npcs(session: Session, npc_ids: List[int]) -> List[NPC]:
    """Resolve NPC IDs into NPC models, raising 404 for missing IDs."""
    npcs: List[NPC] = []
    for npc_id in npc_ids:
        npc = session.get(NPC, npc_id)
        if npc is None:
            raise HTTPException(
                status_code=404,
                detail=f"NPC with id {npc_id} not found",
            )
        npcs.append(npc)
    return npcs


@router.post("/", response_model=FactionSchema)
def create_faction(
    faction: FactionCreateSchema,
    db: Session = Depends(get_session),
) -> FactionSchema:
    controller = FactionController(db)
    new_faction = Faction(
        name=faction.name,
        description=faction.description,
        reputation=faction.reputation,
    )
    created_faction = controller.create_faction(new_faction)

    created_faction.allies = _resolve_factions(db, faction.ally_ids, "Ally")
    created_faction.enemies = _resolve_factions(db, faction.enemy_ids, "Enemy")
    created_faction.npcs = _resolve_npcs(db, faction.npc_ids)
    updated_faction = controller.update_faction(created_faction)

    return _to_faction_schema(updated_faction)


@router.get("/{faction_id}", response_model=FactionSchema)
def get_faction(
    faction_id: int,
    db: Session = Depends(get_session),
) -> FactionSchema:
    controller = FactionController(db)
    faction = controller.get_faction(faction_id)
    if faction is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return _to_faction_schema(faction)


@router.put("/{faction_id}", response_model=FactionSchema)
def update_faction(
    faction_id: int,
    faction_update: FactionUpdateSchema,
    db: Session = Depends(get_session),
) -> FactionSchema:
    controller = FactionController(db)
    faction = controller.get_faction(faction_id)
    if faction is None:
        raise HTTPException(status_code=404, detail="Faction not found")

    update_data = faction_update.model_dump(exclude_unset=True)
    ally_ids = update_data.pop("ally_ids", None)
    enemy_ids = update_data.pop("enemy_ids", None)
    npc_ids = update_data.pop("npc_ids", None)

    for field, value in update_data.items():
        setattr(faction, field, value)

    if ally_ids is not None:
        faction.allies = _resolve_factions(db, ally_ids, "Ally")
    if enemy_ids is not None:
        faction.enemies = _resolve_factions(db, enemy_ids, "Enemy")
    if npc_ids is not None:
        faction.npcs = _resolve_npcs(db, npc_ids)

    updated_faction = controller.update_faction(faction)
    return _to_faction_schema(updated_faction)


@router.delete("/{faction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faction(
    faction_id: int,
    db: Session = Depends(get_session),
) -> Response:
    controller = FactionController(db)
    faction = controller.get_faction(faction_id)
    if faction is None:
        raise HTTPException(status_code=404, detail="Faction not found")

    controller.delete_faction(faction_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[FactionSchema])
def list_factions(db: Session = Depends(get_session)) -> List[FactionSchema]:
    controller = FactionController(db)
    factions = controller.list_factions()
    return [_to_faction_schema(faction) for faction in factions]
