from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    Enum as SQLEnum, ForeignKey,
)
from backend.app.database.session import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    kart_name = Column(String(100), nullable=True)
    #teamleiter_id = Column(Integer, ForeignKey("users.id"))
    teamleiter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    teamleiter = relationship("User", back_populates="team")
    results = relationship("Result", back_populates="team")
    attempts = relationship("Attempt", back_populates="team")
