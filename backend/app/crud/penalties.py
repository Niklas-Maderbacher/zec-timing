from sqlalchemy.orm import Session

from app.models.penalties import Penalty as model_penal
from app.schemas.penalties import Penalty as schema_penal

def get_penalties(db: Session) -> list[schema_penal]:
    penalties_db = db.query(model_penal).all()

    penalties_lst = []

    for penalty in penalties_db:
        penalties_lst.append(schema_penal(
            id=penalty.id,
            penalty_amount = penalty.penalty_amount,
            type = penalty.type,

        ))

    return penalties_lst
