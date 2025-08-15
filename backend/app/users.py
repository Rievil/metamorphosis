from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .auth import get_password_hash
from .dependencies import get_db, require_role
from .models import Role, RoleEnum, User


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum


class UserRead(BaseModel):
    id: int
    username: str
    role: RoleEnum

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name: RoleEnum


class RoleRead(BaseModel):
    id: int
    name: RoleEnum

    class Config:
        orm_mode = True


user_router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_role(RoleEnum.world_builder, RoleEnum.dungeon_master))])
role_router = APIRouter(prefix="/roles", tags=["roles"], dependencies=[Depends(require_role(RoleEnum.world_builder))])


@user_router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.name == user.role).first()
    if not db_role:
        raise HTTPException(status_code=400, detail="Role not found")
    db_user = User(username=user.username, hashed_password=get_password_hash(user.password), role=db_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@role_router.post("/", response_model=RoleRead)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@role_router.get("/", response_model=list[RoleRead], dependencies=[])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()
