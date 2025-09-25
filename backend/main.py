# backend/main.py
# Ponto de entrada da API + rotas de usuários e autenticação (JWT)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, crud, database
# Importamos utilidades de auth (implementadas em backend/auth.py)
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    role_required,
)

# ---------------------------------------------------------
# 1) Aplicação e CORS

# ---------------------------------------------------------
app = FastAPI(title="API - Automação ESP SEEDF")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2) Banco e dependências

# ---------------------------------------------------------
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 3) AUTENTICAÇÃO (JWT)

# ---------------------------------------------------------

@app.post("/auth/token", response_model=schemas.Token, tags=["auth"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Recebe form-data:
      - username
      - password
    Retorna:
      {"access_token": "<JWT>", "token_type": "bearer"}
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", tags=["auth"])
def read_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
    }

@app.get("/admin-only", tags=["auth"])
def admin_only(_: models.User = Depends(role_required("diretor"))):
    return {"ok": True, "message": "Bem-vindo, Diretor!"}

# ---------------------------------------------------------
# 4) USUÁRIOS

# ---------------------------------------------------------

@app.post(
    "/users/",
    response_model=schemas.UserResponse,
    tags=["users"],
    dependencies=[Depends(role_required("diretor"))],  # apenas diretor cria
)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica duplicidade
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário já existe")

@app.get(
    "/users/",
    response_model=list[schemas.UserListItem],
    tags=["users"],
    dependencies=[Depends(role_required("diretor", "gerente"))],  # diretor OU gerente
)

def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.put(
    "/users/{user_id}/role",
    response_model=schemas.UserListItem,
    tags=["users"],
    dependencies=[Depends(role_required("diretor"))],  # apenas diretor
)

def change_role(user_id: int, payload: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    if payload.role not in ("diretor", "gerente", "arquiteto"):
        raise HTTPException(status_code=400, detail="Role inválido")
    updated = crud.update_user_role(db, user_id, payload.role)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated

@app.put(
    "/users/{user_id}/password",
    response_model=schemas.UserListItem,
    tags=["users"],
)

def change_password(
    user_id: int,
    payload: schemas.UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # regra: diretor pode tudo; outros só trocam a própria senha
    if current_user.role != "diretor" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")
    updated = crud.update_user_password(db, user_id, payload.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated

# ---------------------------------------------------------
# 5) Healthcheck

# ---------------------------------------------------------

@app.get("/health", tags=["health"])
def healthcheck():
    return {"ok": True}
