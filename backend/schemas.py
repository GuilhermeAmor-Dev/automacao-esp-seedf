#Esse arquivo define como são os schemas (modelos de dados) usados na aplicação
from pydantic import BaseModel
from pydantic import ConfigDict 
from datetime import datetime
from typing import Optional
from typing import List

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

    model_config = ConfigDict(from_attributes=True)

# O token é o que devolvemos no login e o TokenData é o que extraímos de dentro do JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

    class UserListItem(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserRoleUpdate(BaseModel):
    role: str  # "diretor" | "gerente" | "arquiteto"

class UserPasswordUpdate(BaseModel):
    new_password: str