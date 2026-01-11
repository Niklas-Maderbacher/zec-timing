import pytest
from app.crud.team import (
    get_team,
    get_teams,
    get_teams_by_ids,
    delete_team,
    create_team,
    update_team,
)
from app.schemas.team import TeamCreate, TeamUpdate
from app.models.team import team_category
from app.exceptions.exceptions import EntityDoesNotExistError

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
    payload = TeamCreate(category=team_category.professional_class, name="Team C", vehicle_weight=350, mean_power=90, rfid_identifier="RFID_C")
    created = create_team(db=db, team=payload)
    assert created.name == "Team C"
    assert created.category == team_category.professional_class


def test_update_team(db, seeded_data):
    team = seeded_data["teams"][0]
    update = TeamUpdate(category=team_category.professional_class)
    updated = update_team(db=db, team_id=team.id, team_update=update)
    assert updated.category == team_category.professional_class
