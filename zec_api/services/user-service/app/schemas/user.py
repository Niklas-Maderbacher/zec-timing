from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    kc_id: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CreateUserKC(BaseModel):
    username: str
    password: str

class UpdateUserKC(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserRolesRequest(BaseModel):
    roles: list[str]
