from sqlalchemy import (
    Column, Integer, Float, DateTime, ForeignKey,
)
from app.db.session import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Leaderboard(Base):
    __tablename__ = 'leaderboards'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    best_score = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    team = relationship("Team", back_populates="leaderboards")
    challenge = relationship("Challenge", back_populates="leaderboards")