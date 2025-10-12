from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

from app.core.config import settings

url = URL.create(
    drivername=settings.SQLALCHEMY_DATABASE_URI.scheme,
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    database=settings.POSTGRES_DB,
    port=settings.POSTGRES_PORT
)

engine = create_engine(url)
Base = declarative_base()