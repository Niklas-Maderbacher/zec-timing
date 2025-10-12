from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    Enum as SQLEnum, ForeignKey,
)
from app.database.session import Base
from datetime import datetime, timezone
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    ZEITNEHMER = "zeitnehmer"
    TEAMLEITER = "teamleiter"
    TEILNEHMER = "teilnehmer"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # momentane implementation
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))