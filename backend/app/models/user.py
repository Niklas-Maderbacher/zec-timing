from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from app.database.session import Base

from enum import Enum
from sqlalchemy import Enum as SQLEnum


class UserRole(Enum):
    ADMIN = "ADMIN"
    TEAM_LEAD = "TEAM_LEAD"
    VIEWER = "VIEWER"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Role stored as enum matching db-schema.md
    role = Column(SQLEnum(UserRole), nullable=False)
    # Keycloak id (kc_id in schema)
    kc_id = Column(String, unique=True, nullable=False)
    