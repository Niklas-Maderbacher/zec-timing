from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    Enum as SQLEnum, ForeignKey,
)
from app.database.session import Base
from datetime import datetime, timezone

class ConfigParameter(Base):
    __tablename__ = "config_parameters"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(String(500), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
