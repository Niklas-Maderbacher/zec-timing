from app.database.dependency import SessionDep
from app.models.penalty_type import PenaltyType

def seed_penalty_types(db: SessionDep):
    predefined_penalty_types = [
        {"type": "Strecke verlassen", "amount": 10},
        {"type": "Hünterl nieder", "amount": 5},
    ]
    for penalty_type_data in predefined_penalty_types:
        exists = db.query(PenaltyType).filter(PenaltyType.type == penalty_type_data["type"]).first()
        if not exists:
            penalty_type = PenaltyType(**penalty_type_data)
            db.add(penalty_type)