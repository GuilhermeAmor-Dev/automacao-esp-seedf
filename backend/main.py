# Esse arquivo é o ponto de entrada da aplicação FastAPI e rota POST para criar usuários
from fastapi import FastAPI, Depends, HTTPException
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
        from passli.hash import bcrypt
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
            status_code=status.HTTP_401_UNAUTHORIZED,
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