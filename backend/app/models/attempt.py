from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    Enum as SQLEnum, ForeignKey,
)
from backend.app.database.session import Base
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy.orm import relationship

class Category(Enum):
    SKIDPAD = "skidpad"
    SLALOM = "slalom"
    ACCELERATION = "acceleration"
    ENDURANCE = "endurance"

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    category = Column(SQLEnum(Category))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    valid = Column(Boolean, default=True)
    penalty_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    team = relationship("Team", back_populates="attempts")
    result = relationship("Result", back_populates="attempts", uselist=False)



