from datetime import datetime, timedelta, timezone
from typing import Optional, List, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from . import schemas, models, crud, database

import os
from dotenv import load_dotenv
load_dotenv()  # carrega variáveis do .env

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-chave")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# Diz ao FastAPI como ler o token "Bearer <token>" do header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# ----- Funções de senha -----
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)

# ----- Funções de JWT -----
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ----- Autenticação de usuário -----
def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# ----- Dependências para pegar usuário atual a partir do token -----
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)  # confere se existe mesmo
    if user is None:
        raise credentials_exception
    return user

# ----- Checagem de papel (role) -----
def role_required(allowed_roles: List[str]) -> Callable:
    """
    Uso:
      @app.get("/rota-protegida")
      def exemplo(current_user: models.User = Depends(role_required(["diretor", "gerente"]))):
          return {"ok": True}
    """
    def dependency(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return current_user
    return dependency

# ----- Dependencia de Rota Bearer -----

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authtoken")
oauth2_scheme = APIKeyHeader(name="Authorization")