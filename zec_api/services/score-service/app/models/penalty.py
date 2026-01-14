from sqlalchemy import Column, Integer, Float, DateTime
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from app.database.session import Base

class PenaltyType(Enum):
    time_penalty = "TIME_PENALTY"

class Penalty(Base):
    __tablename__ = 'penalties'

    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer)
    penalty_amount = Column(Float)
    type = Column(SQLEnum(PenaltyType))
    created_at = Column(DateTime, default=datetime.utcnow)
