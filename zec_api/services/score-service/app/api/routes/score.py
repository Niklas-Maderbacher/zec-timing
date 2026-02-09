from fastapi import APIRouter
from typing import List
from app.database.dependency import SessionDep
from app.schemas.score import ScoreCreate, ScoreUpdate, ScoreResponse
from app.crud import score as crud

router = APIRouter()

@router.post("/", response_model=ScoreResponse)
def create_score(db: SessionDep, score: ScoreCreate):
    score = crud.create_score(db=db, score=score)
    return score

@router.put("/{score_id}", response_model=ScoreResponse)
def update_score(db: SessionDep, score_id: int, score_update: ScoreUpdate):
    score = crud.update_score(db=db, score_id=score_id, score_update=score_update)
    return score

@router.delete("/{score_id}", response_model=ScoreResponse)
def delete_score(db: SessionDep, score_id: int):
    score = crud.delete_score(db=db, score_id=score_id)
    return score

@router.delete("/attempt/{attempt_id}", response_model=List[ScoreResponse])
def delete_scores_for_attempt(db: SessionDep, attempt_id: int):
    scores = crud.delete_scores_for_attempt(db=db, attempt_id=attempt_id)
    return scores

@router.get("/{score_id}", response_model=ScoreResponse)
def get_score(db: SessionDep, score_id: int):
    score = crud.get_score(db=db, score_id=score_id)
    return score

@router.get("/", response_model=List[ScoreResponse])
def list_scores(db: SessionDep):
    scores = crud.get_scores(db=db)
    return scores