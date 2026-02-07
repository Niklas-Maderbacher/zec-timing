from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime, timezone
from app.database.session import Base

class Score(Base):
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer)
    challenge_id = Column(Integer)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    