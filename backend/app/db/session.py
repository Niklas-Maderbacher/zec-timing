from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

from app.config.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
