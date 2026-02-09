import pytest
from app.crud import penalty as penalty_crud
from app.schemas.penalty import PenaltyCreate, PenaltyUpdate
from app.models.penalty import Penalty
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def test_create_penalty_success(db, seeded_penalty_types):
    penalty_in = PenaltyCreate(attempt_id=1, penalty_type_id=1, count=2)
    result = penalty_crud.create_penalty(db=db, penalty=penalty_in)
    assert isinstance(result, Penalty)
    assert result.attempt_id == 1
    assert result.penalty_type_id == 1
    assert result.count == 2

def test_create_penalty_service_error(db, mock_requests_penalty):
    mock_requests_penalty.return_value.status_code = 500
    penalty_in = PenaltyCreate(attempt_id=1, penalty_type_id=1, count=2)
    with pytest.raises(ServiceError):
        penalty_crud.create_penalty(db=db, penalty=penalty_in)

def test_get_penalty_success(db, seeded_penalties):
    penalty = seeded_penalties[0]
    result = penalty_crud.get_penalty(db=db, penalty_id=penalty.id)
    assert result.id == penalty.id

def test_get_penalty_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.get_penalty(db=db, penalty_id=999)

def test_get_penalties(db, seeded_penalties):
    result = penalty_crud.get_penalties(db=db)
    assert len(result) == len(seeded_penalties)

def test_get_penalties_by_attempt_success(db, seeded_penalties):
    result = penalty_crud.get_penalties_by_attempt(db=db, attempt_id=1)
    assert len(result) == 2

def test_get_penalties_by_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.get_penalties_by_attempt(db=db, attempt_id=999)

def test_update_penalty_success(db, seeded_penalties):
    penalty = seeded_penalties[0]
    update_data = PenaltyUpdate(count=5)
    result = penalty_crud.update_penalty(db=db, penalty_id=penalty.id, penalty_update=update_data)
    assert result.count == 5

def test_update_penalty_not_found(db):
    update_data = PenaltyUpdate(count=5)
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.update_penalty(db=db, penalty_id=999, penalty_update=update_data)

def test_delete_penalty_success(db, seeded_penalties):
    penalty = seeded_penalties[0]
    result = penalty_crud.delete_penalty(db=db, penalty_id=penalty.id)
    assert result.id == penalty.id
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.get_penalty(db=db, penalty_id=penalty.id)

def test_delete_penalty_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.delete_penalty(db=db, penalty_id=999)

def test_delete_penalties_by_attempt_success(db, seeded_penalties):
    result = penalty_crud.delete_penalties_by_attempt(db=db, attempt_id=1)
    assert len(result) == 2
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.get_penalties_by_attempt(db=db, attempt_id=1)

def test_delete_penalties_by_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        penalty_crud.delete_penalties_by_attempt(db=db, attempt_id=999)

def test_get_all_penalty_types(db, seeded_penalty_types):
    result = penalty_crud.get_all_penalty_types(db=db)
    assert len(result) == len(seeded_penalty_types)
