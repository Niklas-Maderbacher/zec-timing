from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
class Attempt(Base):
    __tablename__ = 'attempts'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    attempt_number = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    average_power = Column(Float)
    energy_used = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    team = relationship("Team", back_populates="attempts")
    driver = relationship("Driver", back_populates="attempts")
    challenge = relationship("Challenge", back_populates="attempts")
    scores = relationship("Score", back_populates="attempt")
    penalties = relationship("Penalty", back_populates="attempt")
