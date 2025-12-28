from collections.abc import Generator
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.session import engine


def get_db() -> Generator[Session, None, None]:
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
