from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import get_db, require_role
from ..models import Archetype, RoleEnum


class ArchetypeCreate(BaseModel):
    name: str
    description: str | None = None


class ArchetypeRead(ArchetypeCreate):
    id: int

    class Config:
        orm_mode = True


router = APIRouter(prefix="/archetypes", tags=["archetypes"])


@router.post(
    "/",
    response_model=ArchetypeRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def create_archetype(archetype: ArchetypeCreate, db: Session = Depends(get_db)):
    db_archetype = Archetype(**archetype.dict())
    db.add(db_archetype)
    db.commit()
    db.refresh(db_archetype)
    return db_archetype


@router.put(
    "/{archetype_id}",
    response_model=ArchetypeRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def update_archetype(
    archetype_id: int, archetype: ArchetypeCreate, db: Session = Depends(get_db)
):
    db_archetype = (
        db.query(Archetype).filter(Archetype.id == archetype_id).first()
    )
    if not db_archetype:
        raise HTTPException(status_code=404, detail="Archetype not found")
    for key, value in archetype.dict().items():
        setattr(db_archetype, key, value)
    db.commit()
    db.refresh(db_archetype)
    return db_archetype


@router.get("/", response_model=list[ArchetypeRead])
def list_archetypes(db: Session = Depends(get_db)):
    return db.query(Archetype).all()
