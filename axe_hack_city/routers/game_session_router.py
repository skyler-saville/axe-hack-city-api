from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..controllers.game_session_controller import GameSessionController
from ..database.session import get_session
from ..models.game_session_model import GameSession
from ..routers.authentication_router import User, get_current_active_user
from ..schemas.game_session_schema import (
    GameSessionCreateSchema,
    GameSessionSchema,
    GameSessionUpdateSchema,
)

router = APIRouter()


@router.post("/", response_model=GameSessionSchema)
def create_session(
    session: GameSessionCreateSchema,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> GameSession:
    controller = GameSessionController(db)
    session_data = session.model_dump(exclude={"state"})
    session_data.update(session.state.model_dump())
    new_session = GameSession(**session_data, owner_user_id=current_user.id)
    return controller.create_session(new_session)


@router.get("/{session_id}", response_model=GameSessionSchema)
def read_session(
    session_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> GameSession:
    controller = GameSessionController(db)
    session = controller.get_session(session_id, current_user_id=current_user.id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/{session_id}", response_model=GameSessionSchema)
def update_session(
    session_id: int,
    session_update: GameSessionUpdateSchema,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> GameSession:
    controller = GameSessionController(db)
    try:
        session = controller.update_session_fields(
            session_id,
            session_update.model_dump(exclude_unset=True),
            current_user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> Response:
    controller = GameSessionController(db)
    deleted = controller.delete_session(session_id, current_user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[GameSessionSchema])
def list_sessions(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> List[GameSession]:
    controller = GameSessionController(db)
    return controller.list_sessions(current_user_id=current_user.id)
