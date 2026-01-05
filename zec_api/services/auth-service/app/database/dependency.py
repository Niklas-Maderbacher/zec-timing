from collections.abc import Generator
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.session import engine
from app.crud.auth import get_current_user
from app.models.user import UserRole
import app.exceptions.exceptions as exception


def get_db() -> Generator[Session, None, None]:
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def require_role(required_role: UserRole):
    def role_checker(user: CurrentUser):
        if required_role.value not in user["roles"]:
            raise exception.InsufficientPermissions
        return user
    return role_checker

SessionDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser = Annotated[dict, Depends(require_role(UserRole.ADMIN))]
TeamLeadUser = Annotated[dict, Depends(require_role(UserRole.TEAM_LEAD))]
ViewerUser = Annotated[dict, Depends(require_role(UserRole.VIEWER))]
