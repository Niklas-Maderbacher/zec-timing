from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from app.database.session import Base
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    TEAM_LEAD = "TEAM_LEAD"
    VIEWER = "VIEWER"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    kc_id = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    