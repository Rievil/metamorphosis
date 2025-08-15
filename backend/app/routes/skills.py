from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import get_db, require_role
from ..models import Skill, RoleEnum


class SkillCreate(BaseModel):
    name: str
    description: str | None = None
    archetype_id: int | None = None


class SkillRead(SkillCreate):
    id: int

    class Config:
        orm_mode = True


router = APIRouter(prefix="/skills", tags=["skills"])


@router.post(
    "/",
    response_model=SkillRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.put(
    "/{skill_id}",
    response_model=SkillRead,
    dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))],
)
def update_skill(skill_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for key, value in skill.dict().items():
        setattr(db_skill, key, value)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.get("/", response_model=list[SkillRead])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()
