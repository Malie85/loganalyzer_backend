from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from models import users as users_model
from sqlalchemy.orm import Session

from models import users as users_model
from models import sessions
from schemas import users as users_schema
from db.database import get_db


me = APIRouter()

# this route get data from server by given Coockie
# Creating route
# we use user response for now beacause we just response name and username. but then we will add Files to response
@me.get(
    "/api/me",
    response_model=users_schema.userResponse,status_code=status.HTTP_200_OK
)
# Here we get the session id. we say it can be string OR nothing. and get it from headers, not body or http string. and if it was empty, make it None and dont reise error
# also we create data base session by db and depend it to get_db in database.py
def userLogin(session_id: str | None = Cookie(default=None), db: Session=Depends(get_db)):
    # if there is no session id do this
    if not session_id:
        raise HTTPException(
        status_code=401,
        detail="No Coockie"
    )
    # if session id exist, doing query to find session id in session table in data base. and if it doesent exist do this
    session_id_query = db.query(sessions.Session).filter(sessions.Session.sessionID == session_id).first()
    if session_id_query is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid Cookie"
    )
    # if session id exist in sessions table, doing query to find user in users table in data base. and if it doesent exist do this
    user_query_by_session = db.query(users_model.users).filter(users_model.users.id == session_id_query.sessionOwner).first()
    if user_query_by_session is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid cookie"
    )
    # if all was ok, respond this
    new_user = users_model.users(
        realname= user_query_by_session.realname,
        username= user_query_by_session.username,
    )

    return new_user

