from app.database.dependency import SessionDep
from app.schemas.user import CreateUserKC
from app.crud.user import create_user, add_roles_to_user
from app.models.user import User

def seed_user(db: SessionDep):
    predefined_user = [
        {"username": "admin", "password": "changeme"},
    ]
    for user_data in predefined_user:
        exists = db.query(User).filter(User.username == user_data["username"]).first()
        
        if not exists:
            db_user = create_user(db, CreateUserKC(**user_data))
            if db_user:
                try:
                    add_roles_to_user(db_user.kc_id, ["ADMIN"])
                except Exception as e:
                    raise Exception(f"Failed to add roles to user {db_user.username} after creation: {e}")
