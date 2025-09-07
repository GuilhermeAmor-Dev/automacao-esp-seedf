# backend/schemas.py
from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime
from typing import Optional, List

# --- Criação e retorno de usuário ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# --- Listagem e updates de usuário ---
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
