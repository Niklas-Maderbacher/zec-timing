import pytest
from unittest.mock import MagicMock
from app.crud.user import (
    create_user,
    update_user,
    delete_user,
    get_user_by_username,
    get_user_by_id_db,
    add_roles_to_user,
    remove_roles_from_user,
)
from app.schemas.user import CreateUserKC, UpdateUserKC
from app.exceptions.exceptions import (
    EntityAlreadyExistsError,
    EntityDoesNotExistError,
    AuthenticationFailed,
    InvalidOperationError,
    ServiceError,
)

def test_create_user(db):
    user = create_user(
        db=db,
        request=CreateUserKC(
            username="newuser",
            password="password",
        ),
    )
    assert user.username == "newuser"
    assert user.kc_id == "kc-12345"

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

def test_create_user_already_exists(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=409)
    with pytest.raises(EntityAlreadyExistsError):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password"),
        )

def test_create_user_auth_failed(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=401)
    with pytest.raises(AuthenticationFailed):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password"),
        )

def test_create_user_service_error(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=500)
    with pytest.raises(ServiceError):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password"),
        )

def test_update_user_not_found_kc(db, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=404)
    with pytest.raises(EntityDoesNotExistError):
        update_user(
            db=db,
            user_id="missing-id",
            request=UpdateUserKC(username="x"),
        )

def test_update_user_invalid_operation(db, seeded_user, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=400)
    with pytest.raises(InvalidOperationError):
        update_user(
            db=db,
            user_id=seeded_user.kc_id,
            request=UpdateUserKC(username="x"),
        )

def test_update_user_db_missing(db, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=204)
    with pytest.raises(EntityDoesNotExistError):
        update_user(
            db=db,
            user_id="kc-missing",
            request=UpdateUserKC(username="x"),
        )

def test_delete_user_db_missing(db):
    with pytest.raises(EntityDoesNotExistError):
        delete_user(db=db, user_id="missing-id")

def test_delete_user_kc_missing(db, seeded_user, mock_requests):
    mock_requests.delete.return_value = MagicMock(status_code=404)
    with pytest.raises(EntityDoesNotExistError):
        delete_user(db=db, user_id=seeded_user.kc_id)

def test_delete_user_auth_failed(db, seeded_user, mock_requests):
    mock_requests.delete.return_value = MagicMock(status_code=401)
    with pytest.raises(AuthenticationFailed):
        delete_user(db=db, user_id=seeded_user.kc_id)

def test_delete_user_service_error(db, seeded_user, mock_requests):
    mock_requests.delete.return_value = MagicMock(status_code=500, text="error")
    with pytest.raises(ServiceError):
        delete_user(db=db, user_id=seeded_user.kc_id)

def test_add_roles_to_user_success(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.post.return_value = MagicMock(status_code=204)
    add_roles_to_user("kc-123", ["admin"])

def test_add_roles_to_user_role_not_found(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=404),
    ]
    with pytest.raises(EntityDoesNotExistError):
        add_roles_to_user("kc-123", ["missing"])

def test_remove_roles_from_user_success(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.delete.return_value = MagicMock(status_code=204)
    remove_roles_from_user("kc-123", ["admin"])

def test_remove_roles_from_user_invalid_operation(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.delete.return_value = MagicMock(status_code=400)
    with pytest.raises(InvalidOperationError):
        remove_roles_from_user("kc-123", ["admin"])

def test_get_user_by_id_db_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        get_user_by_id_db(db=db, user_id="missing")
