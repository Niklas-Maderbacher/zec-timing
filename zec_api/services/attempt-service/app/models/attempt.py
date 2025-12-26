from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.database.session import Base

class Attempt(Base):
    __tablename__ = 'attempts'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    driver_id = Column(Integer)
    challenge_id = Column(Integer)
    attempt_number = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    average_power = Column(Float)
    energy_used = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
