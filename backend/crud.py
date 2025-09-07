# Esse arquivo define as operações CRUD (Create, Read, Update, Delete) para o banco de dados
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt

# Criar usuário
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hash(user.password)  # criptografa a senha
    db_user = models.User(
        username=user.username,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Buscar usuário pelo nome
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Listagem, mudança de papel e grava a senha criptografada

def list_users(db: Session) -> List[models.User]:
    return db.query(models.User).order_by(models.User.id.asc()).all()

def update_user_role(db: Session, user_id: int, new_role: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user_id: int, new_plain_password: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    user.password = bcrypt.hash(new_plain_password)  # sempre grava hash
    db.commit()
    db.refresh(user)
    return user
