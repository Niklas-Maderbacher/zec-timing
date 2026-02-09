import pytest
from app.crud.team import (
    create_team,
    get_team,
    get_teams,
    get_teams_by_ids,
    update_team,
    delete_team,
)
from app.schemas.team import TeamCreate, TeamUpdate
from app.models.team import team_category
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def test_get_team(db, seeded_data):
    team = seeded_data["teams"][0]
    fetched = get_team(db=db, team_id=team.id)
    assert fetched.name == team.name

def test_list_teams(db, seeded_data):
    teams = get_teams(db=db)
    assert len(teams) == 2

def test_get_teams_by_ids(db, seeded_data):
    ids = {t.id for t in seeded_data["teams"]}
    teams = get_teams_by_ids(db=db, team_ids=ids)
    assert len(teams) == 2

def test_delete_team(db, seeded_data):
    team = seeded_data["teams"][0]
    deleted = delete_team(db=db, team_id=team.id)
    assert deleted.id == team.id

def test_get_team_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        get_team(db=db, team_id=999)

def test_create_team(db):
    payload = TeamCreate(
        category=team_category.professional_class,
        name="Team C",
        vehicle_weight=350,
        mean_power=90,
        rfid_identifier="RFID_C",
    )
    created = create_team(db=db, team=payload)
    assert created.name == "Team C"
    assert created.category == team_category.professional_class

def test_update_team(db, seeded_data):
    team = seeded_data["teams"][0]
    update = TeamUpdate(category=team_category.professional_class)
    updated = update_team(db=db, team_id=team.id, team_update=update)
    assert updated.category == team_category.professional_class

def test_create_team_service_error(db, monkeypatch):
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    payload = TeamCreate(
        category=team_category.professional_class,
        name="Broken Team",
        vehicle_weight=360,
        mean_power=95,
        rfid_identifier="RFID_FAIL",
    )
    with pytest.raises(ServiceError):
        create_team(db=db, team=payload)

def test_update_team_not_found(db):
    update = TeamUpdate(name="Does Not Exist")
    with pytest.raises(EntityDoesNotExistError):
        update_team(
            db=db,
            team_id=999,
            team_update=update,
        )

def test_update_team_service_error(db, seeded_data, monkeypatch):
    team = seeded_data["teams"][0]
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    update = TeamUpdate(name="Will Fail")
    with pytest.raises(ServiceError):
        update_team(
            db=db,
            team_id=team.id,
            team_update=update,
        )

def test_delete_team_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        delete_team(db=db, team_id=999)

def test_delete_team_service_error(db, seeded_data, monkeypatch):
    team = seeded_data["teams"][0]
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    with pytest.raises(ServiceError):
        delete_team(db=db, team_id=team.id)

def test_get_teams_by_ids_not_found(db, seeded_data):
    existing_id = seeded_data["teams"][0].id
    missing_id = 999
    with pytest.raises(EntityDoesNotExistError):
        get_teams_by_ids(db=db, team_ids={existing_id, missing_id})
