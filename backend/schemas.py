#Esse arquivo define como são os schemas (modelos de dados) usados na aplicação
from pydantic import BaseModel
from datetime import datetime

# O que o usuário envia ao se cadastrar
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

# O que devolvemos quando listamos ou mostramos usuários
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
