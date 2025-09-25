from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..dependencies import get_current_user, get_db, role_required
from ..services.users import UserAlreadyExists, UserNotFound, UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=schemas.UserResponse,
    dependencies=[Depends(role_required("diretor"))],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.create_user(user)
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="Usuário já existe")


@router.get(
    "/",
    response_model=list[schemas.UserListItem],
    dependencies=[Depends(role_required("diretor", "gerente"))],
)
def list_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.list_users()


@router.put(
    "/{user_id}/role",
    response_model=schemas.UserListItem,
    dependencies=[Depends(role_required("diretor"))],
)
def change_role(user_id: int, payload: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.update_role(user_id, payload.role)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.put(
    "/{user_id}/password",
    response_model=schemas.UserListItem,
)
def change_password(
    user_id: int,
    payload: schemas.UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "diretor" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    service = UserService(db)
    try:
        return service.update_password(user_id, payload.new_password)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
