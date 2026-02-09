from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.session import Base

class Driver(Base):
    __tablename__ = 'drivers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    weight = Column(Float)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    team = relationship("Team", back_populates="drivers")
