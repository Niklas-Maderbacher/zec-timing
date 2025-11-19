from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Score(Base):
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('attempts.id'))
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    attempt = relationship("Attempt", back_populates="scores")