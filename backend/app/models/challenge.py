from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Challenge(Base):
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    max_attempts = Column(Integer)
    esp_mac = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    attempts = relationship("Attempt", back_populates="challenge")
    leaderboards = relationship("Leaderboard", back_populates="challenge")