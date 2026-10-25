from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from models import sessions
from models import users as users_model

def check_coockie(session_id: str,db: Session):
    # if there is no session id do this
    if not session_id:
        raise HTTPException(
        status_code=401,
        detail="No Coockie"
    )
    # if session id exist, doing query to find session id in session table in data base. and if it doesent exist do this

    session_id_query = db.query(sessions.Session).filter(sessions.Session.sessionID == session_id).first()
    user_query_by_session = db.query(users_model.users).filter(users_model.users.id == session_id_query.sessionOwner).first()

    if session_id_query is None or user_query_by_session is None or session_id_query.expiredAt.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
        status_code=401,
        detail="Invalid Cookie"
    )
    
    return user_query_by_session, session_id_query