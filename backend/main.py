# Esse arquivo é o ponto de entrada da aplicação FastAPI e rota POST para criar usuários
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
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
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        return {"error": "Usuário já existe"}
    return crud.create_user(db=db, user=user)
