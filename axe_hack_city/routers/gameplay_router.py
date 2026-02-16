from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database.session import get_session
from ..schemas.gameplay_schema import (
    GameplayCommandInputSchema,
    GameplayLogResponseSchema,
    GameplayStateSnapshotSchema,
    GameplayTurnOutcomeSchema,
)
from ..services.gameplay_service import GameplaySessionService

router = APIRouter()


@router.post("/{session_id}/commands", response_model=GameplayTurnOutcomeSchema)
def submit_command(
    session_id: int,
    payload: GameplayCommandInputSchema,
    db: Session = Depends(get_session),
) -> GameplayTurnOutcomeSchema:
    service = GameplaySessionService(db)
    try:
        return service.submit_command(session_id=session_id, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{session_id}/state", response_model=GameplayStateSnapshotSchema)
def get_state_snapshot(
    session_id: int, db: Session = Depends(get_session)
) -> GameplayStateSnapshotSchema:
    service = GameplaySessionService(db)
    try:
        return service.get_state_snapshot(session_id=session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{session_id}/log", response_model=GameplayLogResponseSchema)
def get_session_log(
    session_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_session),
) -> GameplayLogResponseSchema:
    service = GameplaySessionService(db)
    try:
        return service.get_recent_log(session_id=session_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
