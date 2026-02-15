from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.game_session_controller import GameSessionController
from ..database.session import get_session
from ..models.game_session_model import GameSession
from ..schemas.game_session_schema import (
    GameSessionCreateSchema,
    GameplayActionResultSchema,
    GameplayCommandRequestSchema,
    GameSessionSchema,
    GameSessionUpdateSchema,
)

router = APIRouter()


@router.post("/", response_model=GameSessionSchema)
def create_session(
    session: GameSessionCreateSchema, db: Session = Depends(get_session)
) -> GameSession:
    controller = GameSessionController(db)
    new_session = GameSession(**session.model_dump())
    return controller.create_session(new_session)


@router.get("/{session_id}", response_model=GameSessionSchema)
def read_session(session_id: int, db: Session = Depends(get_session)) -> GameSession:
    controller = GameSessionController(db)
    session = controller.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/{session_id}", response_model=GameSessionSchema)
def update_session(
    session_id: int,
    session_update: GameSessionUpdateSchema,
    db: Session = Depends(get_session),
) -> GameSession:
    controller = GameSessionController(db)
    session = controller.update_session_fields(
        session_id, session_update.model_dump(exclude_unset=True)
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.post("/{session_id}/commands", response_model=GameplayActionResultSchema)
def execute_session_command(
    session_id: int,
    payload: GameplayCommandRequestSchema,
    db: Session = Depends(get_session),
) -> GameplayActionResultSchema:
    controller = GameSessionController(db)

    if controller.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")

    result = controller.execute_player_command(session_id=session_id, command=payload.command)
    return GameplayActionResultSchema(
        state_changes=result.state_changes,
        narration=result.narration,
        warnings=result.warnings,
        errors=result.errors,
        success=result.success,
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_session)) -> Response:
    controller = GameSessionController(db)
    session = controller.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    controller.delete_session(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[GameSessionSchema])
def list_sessions(db: Session = Depends(get_session)) -> List[GameSession]:
    controller = GameSessionController(db)
    return controller.list_sessions()
