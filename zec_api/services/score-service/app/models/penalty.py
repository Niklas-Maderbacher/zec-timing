from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime, timezone
from app.database.session import Base
from sqlalchemy.orm import relationship

class Penalty(Base):
    __tablename__ = 'penalties'

    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer)
    penalty_type_id = Column(Integer, ForeignKey('penalty_types.id'))
    count = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    penalty_type = relationship('PenaltyType', back_populates='penalties')