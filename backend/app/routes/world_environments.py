from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import get_db, require_role
from ..models import WorldEnvironment, RoleEnum


class WorldEnvironmentCreate(BaseModel):
    name: str
    climate: str | None = None
    description: str | None = None


class WorldEnvironmentRead(WorldEnvironmentCreate):
    id: int

    class Config:
        orm_mode = True


router = APIRouter(prefix="/world-environments", tags=["world-environments"])


@router.post(
    "/",
    response_model=WorldEnvironmentRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def create_environment(
    environment: WorldEnvironmentCreate, db: Session = Depends(get_db)
):
    db_env = WorldEnvironment(**environment.dict())
    db.add(db_env)
    db.commit()
    db.refresh(db_env)
    return db_env


@router.put(
    "/{environment_id}",
    response_model=WorldEnvironmentRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def update_environment(
    environment_id: int, environment: WorldEnvironmentCreate, db: Session = Depends(get_db)
):
    db_env = (
        db.query(WorldEnvironment)
        .filter(WorldEnvironment.id == environment_id)
        .first()
    )
    if not db_env:
        raise HTTPException(status_code=404, detail="WorldEnvironment not found")
    for key, value in environment.dict().items():
        setattr(db_env, key, value)
    db.commit()
    db.refresh(db_env)
    return db_env


@router.get("/", response_model=list[WorldEnvironmentRead])
def list_environments(db: Session = Depends(get_db)):
    return db.query(WorldEnvironment).all()
