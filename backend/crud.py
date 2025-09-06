# Esse arquivo define as operações CRUD (Create, Read, Update, Delete) para o banco de dados
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
