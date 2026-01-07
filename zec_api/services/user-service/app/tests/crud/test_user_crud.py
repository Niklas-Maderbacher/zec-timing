import pytest
from app.crud.user import (
    create_user,
    get_user_by_username,
    update_user,
    delete_user,
)
from app.schemas.user import CreateUserKC, UpdateUserKC
from app.exceptions.exceptions import EntityAlreadyExistsError

def test_create_user(db):
    user = create_user(
        db=db,
        request=CreateUserKC(
            username="newuser",
            password="password",
        ),
    )
    assert user.username == "newuser"
    assert user.kc_id == "kc-123"

def test_get_user_by_username():
    user = get_user_by_username("testuser")
    assert user["username"] == "testuser"

def test_update_user(db, seeded_user):
    updated = update_user(
        db=db,
        user_id=seeded_user.kc_id,
        request=UpdateUserKC(username="updated"),
    )
    assert updated["username"] == "updated"

def test_delete_user(db, seeded_user):
    deleted = delete_user(db=db, user_id=seeded_user.kc_id)
    assert deleted.username == "testuser"
