from sqlalchemy import Column, Integer, String
from app.database.session import Base
from sqlalchemy.orm import relationship

class PenaltyType(Base):
    __tablename__ = 'penalty_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    amount = Column(Integer)

    penalties = relationship('Penalty', back_populates='penalty_type')