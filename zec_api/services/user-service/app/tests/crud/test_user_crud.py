import pytest
import jwt
from unittest.mock import MagicMock
from app.crud.user import (
    create_user,
    update_user,
    delete_user,
    get_user_by_username,
    get_user_by_id,
    get_user_by_id_db,
    get_all_users,
    get_current_user,
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
    InvalidTokenError,
)

def test_create_user(db):
    user = create_user(
        db=db,
        request=CreateUserKC(username="newuser", password="password"),
    )
    assert user.username == "newuser"
    assert user.kc_id == "kc-12345"

def test_create_user_with_team(db, mock_requests):
    mock_requests.get.side_effect = None
    def _get(url, *args, **kwargs):
        if "username=newuser" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-12345", "username": "newuser"}])
        if "/teams/" in url:
            return MagicMock(status_code=200, json=lambda: {"id": 1, "name": "Team A"})
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    user = create_user(
        db=db,
        request=CreateUserKC(username="newuser", password="password", team_id=1),
    )
    assert user.team_id == 1

def test_create_user_team_not_found(db, mock_requests):
    mock_requests.get.side_effect = None
    def _get(url, *args, **kwargs):
        if "username=newuser" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-12345", "username": "newuser"}])
        if "/teams/" in url:
            return MagicMock(status_code=404)
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    with pytest.raises(EntityDoesNotExistError):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password", team_id=999),
        )

def test_create_user_team_service_error(db, mock_requests):
    mock_requests.get.side_effect = None
    def _get(url, *args, **kwargs):
        if "username=newuser" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-12345", "username": "newuser"}])
        if "/teams/" in url:
            return MagicMock(status_code=500, text="error")
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    with pytest.raises(ServiceError):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password", team_id=1),
        )

def test_create_user_team_auth_failed(db, mock_requests):
    mock_requests.get.side_effect = None
    def _get(url, *args, **kwargs):
        if "username=newuser" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-12345", "username": "newuser"}])
        if "/teams/" in url:
            return MagicMock(status_code=403)
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    with pytest.raises(AuthenticationFailed):
        create_user(
            db=db,
            request=CreateUserKC(username="newuser", password="password", team_id=1),
        )

def test_create_user_already_exists(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=409)
    with pytest.raises(EntityAlreadyExistsError):
        create_user(db=db, request=CreateUserKC(username="newuser", password="password"))

def test_create_user_auth_failed(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=401)
    with pytest.raises(AuthenticationFailed):
        create_user(db=db, request=CreateUserKC(username="newuser", password="password"))

def test_create_user_service_error(db, mock_requests):
    mock_requests.post.return_value = MagicMock(status_code=500)
    with pytest.raises(ServiceError):
        create_user(db=db, request=CreateUserKC(username="newuser", password="password"))

def test_update_user(db, seeded_user):
    updated = update_user(
        db=db,
        user_id=seeded_user.kc_id,
        request=UpdateUserKC(username="updated"),
    )
    assert updated.username == "updated"

def test_update_user_password_only(db, seeded_user):
    updated = update_user(
        db=db,
        user_id=seeded_user.kc_id,
        request=UpdateUserKC(password="newpassword"),
    )
    assert updated.username == "testuser"

def test_update_user_with_team(db, seeded_user, mock_requests):
    def _get(url, *args, **kwargs):
        if "/teams/" in url:
            return MagicMock(status_code=200, json=lambda: {"id": 1, "name": "Team A"})
        if f"/users/{seeded_user.kc_id}" in url:
            return MagicMock(status_code=200, json=lambda: {"id": seeded_user.kc_id, "username": "testuser"})
        if "clients?clientId" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "client-uuid"}])
        if "/role-mappings/clients/" in url:
            return MagicMock(status_code=200, json=lambda: [])
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    updated = update_user(
        db=db,
        user_id=seeded_user.kc_id,
        request=UpdateUserKC(team_id=1),
    )
    assert updated.team_id == 1

def test_update_user_not_found_kc(db, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=404)
    with pytest.raises(EntityDoesNotExistError):
        update_user(db=db, user_id="missing-id", request=UpdateUserKC(username="x"))

def test_update_user_auth_failed(db, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=403)
    with pytest.raises(AuthenticationFailed):
        update_user(db=db, user_id="any-id", request=UpdateUserKC(username="x"))

def test_update_user_invalid_operation(db, seeded_user, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=400)
    with pytest.raises(InvalidOperationError):
        update_user(db=db, user_id=seeded_user.kc_id, request=UpdateUserKC(username="x"))

def test_update_user_db_missing(db, mock_requests):
    mock_requests.put.return_value = MagicMock(status_code=204)
    with pytest.raises(EntityDoesNotExistError):
        update_user(db=db, user_id="kc-missing", request=UpdateUserKC(username="x"))

def test_delete_user(db, seeded_user):
    deleted = delete_user(db=db, user_id=seeded_user.kc_id)
    assert deleted.username == "testuser"
    with pytest.raises(EntityDoesNotExistError):
        get_user_by_id_db(db=db, user_id=seeded_user.kc_id)

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

def test_get_user_by_username(db, seeded_user):
    user = get_user_by_username(db=db, username="testuser")
    assert user.username == "testuser"

def test_get_user_by_username_not_found(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=200, json=lambda: [])
    with pytest.raises(EntityDoesNotExistError):
        get_user_by_username(db=db, username="ghost")

def test_get_user_by_username_auth_failed(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=403)
    with pytest.raises(AuthenticationFailed):
        get_user_by_username(db=db, username="testuser")

def test_get_user_by_username_client_resolve_error(db, seeded_user, mock_requests):
    def _get(url, *args, **kwargs):
        if "username=testuser" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-123", "username": "testuser"}])
        if "clients?clientId" in url:
            return MagicMock(status_code=500)
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    with pytest.raises(ServiceError):
        get_user_by_username(db=db, username="testuser")

def test_get_user_by_id(db, seeded_user):
    user = get_user_by_id(db=db, user_id=seeded_user.kc_id)
    assert user.kc_id == seeded_user.kc_id

def test_get_user_by_id_not_found_kc(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=404)
    with pytest.raises(EntityDoesNotExistError):
        get_user_by_id(db=db, user_id="ghost-id")

def test_get_user_by_id_auth_failed(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=401)
    with pytest.raises(AuthenticationFailed):
        get_user_by_id(db=db, user_id="any-id")

def test_get_user_by_id_client_resolve_error(db, seeded_user, mock_requests):
    def _get(url, *args, **kwargs):
        if f"/users/{seeded_user.kc_id}" in url and "username=" not in url and "clients" not in url:
            return MagicMock(status_code=200, json=lambda: {"id": seeded_user.kc_id, "username": "testuser"})
        if "clients?clientId" in url:
            return MagicMock(status_code=500)
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests.get.side_effect = _get
    with pytest.raises(ServiceError):
        get_user_by_id(db=db, user_id=seeded_user.kc_id)

def test_get_all_users(db, seeded_user):
    def _get(url, *args, **kwargs):
        if url.endswith("/users") or url.endswith("/users/"):
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-123", "username": "testuser"}])
        if "clients?clientId" in url:
            return MagicMock(status_code=200, json=lambda: [{"id": "client-uuid"}])
        if "/role-mappings/clients/" in url:
            return MagicMock(status_code=200, json=lambda: [])
        return MagicMock(status_code=200, json=lambda: [])
    mock_requests_local = MagicMock()
    mock_requests_local.get.side_effect = _get
    import app.crud.user as user_module
    original = user_module.requests
    user_module.requests = mock_requests_local
    try:
        users = get_all_users(db=db)
        assert len(users) == 1
        assert users[0].username == "testuser"
    finally:
        user_module.requests = original

def test_get_all_users_auth_failed(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=403)
    with pytest.raises(AuthenticationFailed):
        get_all_users(db=db)

def test_get_all_users_service_error(db, mock_requests):
    mock_requests.get.side_effect = None
    mock_requests.get.return_value = MagicMock(status_code=500)
    with pytest.raises(ServiceError):
        get_all_users(db=db)

def test_get_all_users_client_resolve_error(db, mock_requests):
    call_count = 0
    def _get(url, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return MagicMock(status_code=200, json=lambda: [{"id": "kc-123", "username": "testuser"}])
        return MagicMock(status_code=500)
    mock_requests.get.side_effect = _get
    with pytest.raises(ServiceError):
        get_all_users(db=db)

def test_get_user_by_id_db(db, seeded_user):
    user = get_user_by_id_db(db=db, user_id=seeded_user.kc_id)
    assert user.username == "testuser"

def test_get_user_by_id_db_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        get_user_by_id_db(db=db, user_id="missing")

def test_get_current_user(db, seeded_user):
    token = jwt.encode({"preferred_username": "testuser"}, "secret", algorithm="HS256")
    user = get_current_user(db=db, authorization=f"Bearer {token}")
    assert user.username == "testuser"

def test_get_current_user_uses_sub_fallback(db, seeded_user):
    token = jwt.encode({"sub": "testuser"}, "secret", algorithm="HS256")
    user = get_current_user(db=db, authorization=f"Bearer {token}")
    assert user.username == "testuser"

def test_get_current_user_missing_username(db):
    token = jwt.encode({"some_other_claim": "value"}, "secret", algorithm="HS256")
    with pytest.raises(InvalidTokenError):
        get_current_user(db=db, authorization=f"Bearer {token}")

def test_add_roles_to_user_success(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.post.return_value = MagicMock(status_code=204)
    add_roles_to_user("kc-123", ["admin"])


def test_add_roles_to_user_multiple_roles(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
        MagicMock(status_code=200, json=lambda: {"name": "viewer"}),
    ]
    mock_requests.post.return_value = MagicMock(status_code=204)
    add_roles_to_user("kc-123", ["admin", "viewer"])

def test_add_roles_to_user_user_not_found(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=404),
    ]
    with pytest.raises(EntityDoesNotExistError):
        add_roles_to_user("ghost-id", ["admin"])

def test_add_roles_to_user_client_resolve_error(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=500),
    ]
    with pytest.raises(ServiceError):
        add_roles_to_user("kc-123", ["admin"])

def test_add_roles_to_user_role_not_found(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=404),
    ]
    with pytest.raises(EntityDoesNotExistError):
        add_roles_to_user("kc-123", ["missing"])

def test_add_roles_to_user_role_fetch_error(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=500),
    ]
    with pytest.raises(ServiceError):
        add_roles_to_user("kc-123", ["broken"])

def test_add_roles_to_user_assign_failed(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.post.side_effect = None
    mock_requests.post.return_value = MagicMock(status_code=400)
    with pytest.raises(InvalidOperationError):
        add_roles_to_user("kc-123", ["admin"])

def test_remove_roles_from_user_success(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.delete.return_value = MagicMock(status_code=204)
    remove_roles_from_user("kc-123", ["admin"])

def test_remove_roles_from_user_user_not_found(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=404),
    ]
    with pytest.raises(EntityDoesNotExistError):
        remove_roles_from_user("ghost-id", ["admin"])

def test_remove_roles_from_user_client_resolve_error(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=500),
    ]
    with pytest.raises(ServiceError):
        remove_roles_from_user("kc-123", ["admin"])

def test_remove_roles_from_user_role_not_found(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=404),
    ]
    with pytest.raises(EntityDoesNotExistError):
        remove_roles_from_user("kc-123", ["missing"])

def test_remove_roles_from_user_role_fetch_error(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=500, text="error"),
    ]
    with pytest.raises(ServiceError):
        remove_roles_from_user("kc-123", ["broken"])

def test_remove_roles_from_user_invalid_operation(mock_requests):
    mock_requests.get.side_effect = [
        MagicMock(status_code=200, json=lambda: {"id": "kc-123", "username": "testuser"}),
        MagicMock(status_code=200, json=lambda: [{"id": "client-1"}]),
        MagicMock(status_code=200, json=lambda: {"name": "admin"}),
    ]
    mock_requests.delete.return_value = MagicMock(status_code=400)
    with pytest.raises(InvalidOperationError):
        remove_roles_from_user("kc-123", ["admin"])
