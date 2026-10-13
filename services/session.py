from models import sessions as user_sessions
from db.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Response
import secrets

# I relized i can make a function for creating session and commit to database and adding coockies to response
def create_session(user_id: int, response: Response, db:Session):
    session_id = secrets.token_urlsafe(32)

    # we add this session id to session table in database with its user and make a expiring date
    new_session = user_sessions.Session(
        sessionID = session_id,
        sessionOwner = user_id,
        createdAt = datetime.now(),
        expiredAt = datetime.now() + timedelta(hours=7)
    )

    # COMMIT
    db.add(new_session)
    db.commit()

    response.set_cookie(
        key= "session_id",
        value= session_id,
        max_age=3600,
        httponly=False,
        secure=False,
        samesite= "lax"
    )