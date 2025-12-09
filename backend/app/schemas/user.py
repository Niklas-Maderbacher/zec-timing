from pydantic import BaseModel, EmailStr
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
    kc_id: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserCredentials(BaseModel):
    type: str = "password"
    value: str
    temporary: bool = False

class CreateUserKC(BaseModel):
    username: str
    emailVerified: bool = True
    enabled: bool = True
    credentials: Optional[list[UserCredentials]] = None
