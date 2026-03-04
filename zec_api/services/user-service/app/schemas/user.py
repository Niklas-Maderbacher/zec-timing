from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    kc_id: str

class UserCreate(UserBase):
    team_id: Optional[int] = None

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    team_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CreateUserKC(BaseModel):
    username: str
    password: str
    team_id: Optional[int] = None

class UpdateUserKC(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    team_id: Optional[int] = None

class UserResponseKC(BaseModel):
    id: int
    kc_id: str
    username: str
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    roles: list[str] = []

    model_config = ConfigDict(from_attributes=True)

class UserRolesRequest(BaseModel):
    roles: list[str]
