from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

from enum import Enum
from sqlalchemy import Enum as SQLEnum

class PenaltyType(Enum):
    Strecke_Verlassen = "Strecke_Verlassen"

class Penalty(Base):
    __tablename__ = 'penalties'

    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempts.id'))
    penalty_amount = Column(Float)
    type = Column(SQLEnum(PenaltyType))
    created_at = Column(DateTime, default=datetime.utcnow)

    attempt = relationship("Attempt", back_populates="penalties")
