from collections.abc import Generator
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.session import engine
from app.crud.auth import get_current_user
from app.models.user import UserRole
import app.exceptions.exceptions as exception

ROLE_HIERARCHY = {
    UserRole.VIEWER: {
        UserRole.VIEWER,
        UserRole.TEAM_LEAD,
        UserRole.ADMIN,
    },
    UserRole.TEAM_LEAD: {
        UserRole.TEAM_LEAD,
        UserRole.ADMIN,
    },
    UserRole.ADMIN: {
        UserRole.ADMIN,
    },
}

def get_db() -> Generator[Session, None, None]:
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def require_role(required_role: UserRole):
    def role_checker(user: CurrentUser):
        user_roles = {UserRole(role) for role in user["roles"]}
        allowed_roles = ROLE_HIERARCHY[required_role]
        if user_roles.isdisjoint(allowed_roles):
            raise exception.InsufficientPermissions
        return user
    return role_checker

SessionDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser = Annotated[dict, Depends(require_role(UserRole.ADMIN))]
TeamLeadUser = Annotated[dict, Depends(require_role(UserRole.TEAM_LEAD))]
ViewerUser = Annotated[dict, Depends(require_role(UserRole.VIEWER))]
