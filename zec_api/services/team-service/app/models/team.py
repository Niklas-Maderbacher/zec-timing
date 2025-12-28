from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vehicle_weight = Column(Float)
    mean_power = Column(Float)
    rfid_identifier = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    drivers = relationship("Driver", back_populates="team")
