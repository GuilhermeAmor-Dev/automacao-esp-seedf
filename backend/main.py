# Esse arquivo é o ponto de entrada da aplicação FastAPI e rota POST para criar usuários
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, crud, database
from.auth import ( 
    authenticate_user, create_access_token, get_db, role_required, get_current_user 
)

# Cria as tabelas no banco
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# Dependência para abrir e fechar a conexão com o banco
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # checagem prévia
    if crud.get_user_by_username(db, username=user.username):
        # antes: return {"error": "Usuário já existe"}  -> causava 500 - espera-se que esse erro seja corrigido.
        raise HTTPException(status_code=400, detail="Usuário já existe")

    try:
        from passlib.hash import bcrypt
        user_to_create = schemas.UserCreate(
            username=user.username,
           password=bcrypt.hash(user.password),
            role=user.role
        )

        return crud.create_user(db=db, user=user)
    except IntegrityError:
        # se por acaso ocorrer corrida de dados / constraint UNIQUE
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
# --------- NOVO: LOGIN (gera o token) ---------
@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Recebe form-data no corpo:
      username: <usuario>
      password: <senha>
    Retorna: {"access_token": "<JWT>", "token_type": "bearer"}
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# --------- EXEMPLOS DE ROTAS PROTEGIDAS ---------

@app.get("/me")
def read_me(current_user: models.User = Depends(get_current_user)):
    # retorna informações do usuário autenticado
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role}

@app.get("/admin-only")
def admin_only(current_user: models.User = Depends(role_required(["diretor"]))):
    # só "diretor" acessa
    return {"ok": True, "message": "Bem-vindo, Diretor!"}

# ====== CRIAR USUÁRIO (AGORA RESTRITO A DIRETOR) ======
@app.post("/users/", response_model=schemas.UserResponse,
          dependencies=[Depends(role_required(["diretor"]))])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    try:
        # hash da senha antes de criar
        from passlib.hash import bcrypt
        user_to_create = schemas.UserCreate(
            username=user.username,
            password=bcrypt.hash(user.password),
            role=user.role
        )
        return crud.create_user(db=db, user=user_to_create)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário já existe")

# ====== LOGIN (gera token) ======
@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuário ou senha inválidos",
                            headers={"WWW-Authenticate": "Bearer"})
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# ====== QUEM SOU EU (precisa estar logado) ======
@app.get("/me")
def read_me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role}

# ====== APENAS DIRETOR ======
@app.get("/admin-only")
def admin_only(_: models.User = Depends(role_required(["diretor"]))):
    return {"ok": True, "message": "Bem-vindo, Diretor!"}

# ====== LISTAR USUÁRIOS (diretor OU gerente) ======
@app.get("/users/", response_model=list[schemas.UserListItem],
         dependencies=[Depends(role_required(["diretor", "gerente"]))])
def list_users(db: Session = Depends(get_db)):
    users = crud.list_users(db)
    return users

# ====== TROCAR PAPEL DE UM USUÁRIO (apenas diretor) ======
@app.put("/users/{user_id}/role", response_model=schemas.UserListItem,
         dependencies=[Depends(role_required(["diretor"]))])
def change_role(user_id: int, payload: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    if payload.role not in ("diretor", "gerente", "arquiteto"):
        raise HTTPException(status_code=400, detail="Role inválido")
    updated = crud.update_user_role(db, user_id, payload.role)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated

# ====== TROCAR SENHA (diretor pode trocar de qualquer um; usuário pode trocar a própria) ======
@app.put("/users/{user_id}/password", response_model=schemas.UserListItem)
def change_password(user_id: int, payload: schemas.UserPasswordUpdate,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    # regra: diretor pode tudo; outros só trocam a própria senha
    if current_user.role != "diretor" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    updated = crud.update_user_password(db, user_id, payload.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated