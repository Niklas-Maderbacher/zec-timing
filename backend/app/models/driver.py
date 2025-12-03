from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
from app.models.attempt import Attempt  # noqa: F401 need for mapper

class Driver(Base):
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    weight = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    team = relationship("Team", back_populates="drivers")
    attempts = relationship("Attempt", back_populates="driver")