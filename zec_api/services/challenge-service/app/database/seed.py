from app.database.dependency import SessionDep
from app.models.challenge import Challenge

def seed_challenges(db: SessionDep):
    predefined_challenges = [
        {"name": "Skidpad", "max_attempts":"3"},
        {"name": "Slalom", "max_attempts":"3"},
        {"name": "Endurance", "max_attempts":"3"},
        {"name": "Acceleration", "max_attempts":"3"},
    ]
    for challenge_data in predefined_challenges:
        exists = db.query(Challenge).filter(Challenge.name == challenge_data["name"]).first()
        
        if not exists:
            challenge = Challenge(**challenge_data)
            db.add(challenge)