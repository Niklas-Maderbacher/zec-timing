from sqlalchemy.orm import Session

from app.models.challenges import Challenge as model_chal
from app.schemas.challenges import Challenge as schema_chal

def get_challenges(db: Session) -> list[schema_chal]:
    challenges_db = db.query(model_chal).all()

    challenges = []

    for challenge in challenges_db:
        challenges.append(schema_chal(
            id=challenge.id,
            name=challenge.name,
            esp_mac_start1=challenge.esp_mac_start1,
            esp_mac_start2=challenge.esp_mac_start2,
            esp_mac_finish1=challenge.esp_mac_finish1,
            esp_mac_finish2=challenge.esp_mac_finish2,
        ))

    return challenges
