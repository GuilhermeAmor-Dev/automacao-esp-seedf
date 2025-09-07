# backend/auth.py
from datetime import datetime, timedelta
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from . import database, models, schemas  # suas definições existentes

# --- Configs de segurança ---
SECRET_KEY = os.getenv("SECRET_KEY", "mude-esta-chave-bem-grande-e-secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Dependências comuns ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Utilidades de senha ---
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)

# --- Autenticação ---
def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Bearer para rotas protegidas
bearer = HTTPBearer()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> models.User:
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user

def role_required(*roles: str):
    def decorator(user: models.User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")
        return user
    return decorator

# ==========================================================
#                ROTAS DO MÓDULO AUTH
# ==========================================================
router = APIRouter()  # <- **exportamos isto**

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # mesmo retorno do que você já via no front
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def me(current: models.User = Depends(get_current_user)):
    # schemas.UserResponse tem from_attributes=True (Pydantic v2)
    return current

@router.get("/admin-only")
def admin_only(_: models.User = Depends(role_required("diretor"))):
    return {"ok": True, "message": "Bem-vindo, Diretor!"}
