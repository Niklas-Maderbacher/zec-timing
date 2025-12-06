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
    #kc fields might be worth removing in the future
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    