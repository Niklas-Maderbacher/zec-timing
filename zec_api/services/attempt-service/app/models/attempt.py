from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from datetime import datetime, timezone
from app.database.session import Base

class Attempt(Base):
    __tablename__ = 'attempts'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer)
    driver_id = Column(Integer)
    challenge_id = Column(Integer)
    is_valid = Column(Boolean, default=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    energy_used = Column(Float)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
