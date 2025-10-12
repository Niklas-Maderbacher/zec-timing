from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    Enum as SQLEnum, ForeignKey,
)
from app.database.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.attempt import Category

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    best_time = Column(Float, nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    team = relationship("Team", back_populates="results")
    attempts = relationship("Attempt", back_populates="result")
