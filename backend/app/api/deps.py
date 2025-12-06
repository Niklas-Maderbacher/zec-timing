from collections.abc import Generator
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]