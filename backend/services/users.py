from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..models import User


class UserAlreadyExists(Exception):
    """Raised when attempting to create a user with an existing username."""


class UserNotFound(Exception):
    """Raised when the target user does not exist."""


class UserService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_user(self, payload: schemas.UserCreate) -> User:
        if crud.get_user_by_username(self._db, username=payload.username):
            raise UserAlreadyExists
        try:
            return crud.create_user(self._db, payload)
        except IntegrityError as exc:
            raise UserAlreadyExists from exc

    def list_users(self) -> list[User]:
        return crud.list_users(self._db)

    def update_role(self, user_id: int, new_role: str) -> User:
        updated = crud.update_user_role(self._db, user_id, new_role)
        if not updated:
            raise UserNotFound
        return updated

    def update_password(self, user_id: int, new_password: str) -> User:
        updated = crud.update_user_password(self._db, user_id, new_password)
        if not updated:
            raise UserNotFound
        return updated
