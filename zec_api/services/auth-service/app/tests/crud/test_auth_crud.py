import pytest
from app.crud import auth as crud
import app.exceptions.exceptions as exc

def test_extract_roles_success():
    payload = {
        "resource_access": {
            "admin-client": {
                "roles": ["admin", "user"]
            }
        }
    }

    roles = crud.extract_roles_from_payload(payload)
    assert roles == ["admin", "user"]

def test_extract_roles_empty():
    roles = crud.extract_roles_from_payload({})
    assert roles == []

def test_extract_roles_invalid_type():
    with pytest.raises(exc.InvalidClaims):
        crud.extract_roles_from_payload({"resource_access": "invalid"})
