from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import get_db, require_role
from ..models import Session as SessionModel, RoleEnum


class SessionCreate(BaseModel):
    user_id: int
    token: str


class SessionRead(SessionCreate):
    id: int

    class Config:
        orm_mode = True


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "/",
    response_model=SessionRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = SessionModel(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.put(
    "/{session_id}",
    response_model=SessionRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def update_session(session_id: int, session: SessionCreate, db: Session = Depends(get_db)):
    db_session = (
        db.query(SessionModel).filter(SessionModel.id == session_id).first()
    )
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    for key, value in session.dict().items():
        setattr(db_session, key, value)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.get("/", response_model=list[SessionRead])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).all()
