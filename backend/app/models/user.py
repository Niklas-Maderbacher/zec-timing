from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from app.database.session import Base

from enum import Enum
from sqlalchemy import Enum as SQLEnum

class UserRole(Enum):
    ADMIN = "admin"
    TEAM_LEAD = "team_lead"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Nicht in Keycloak, nur lokal
    role = Column(SQLEnum(UserRole), nullable=False)
    