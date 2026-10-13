from fastapi import APIRouter, HTTPException, status, Response, Depends, Cookie
from models import users as users_model
from sqlalchemy.orm import Session

from models import users as users_model
from models import sessions
from schemas import users as users_schema
from db.database import get_db
from services.session import create_session


me = APIRouter()

@me.get(
    "/api/me",
    response_model=users_schema.userResponse,status_code=status.HTTP_200_OK
)
def userLogin(session_id: str | None = Cookie(default=None), db: Session=Depends(get_db)):
    if not session_id:
        raise HTTPException(
        status_code=401,
        detail="No Coockie"
    )
    session_id_query = db.query(sessions.Session).filter(sessions.Session.sessionID == session_id).first()
    if session_id_query is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid Cookie"
    )
    user_query_by_session = db.query(users_model.users).filter(users_model.users.id == session_id_query.sessionOwner).first()
    if user_query_by_session is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid cookie"
    )
    new_user = users_model.users(
        realname= user_query_by_session.realname,
        username= user_query_by_session.username,
    )

    return new_user

