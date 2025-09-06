# Esse arquivo é o ponto de entrada da aplicação FastAPI e rota POST para criar usuários
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, crud, database

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
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        # se por acaso ocorrer corrida de dados / constraint UNIQUE
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário já existe")
