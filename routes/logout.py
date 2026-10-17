from fastapi import APIRouter, status, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from schemas import users as users_schema
from models import users as users_model
from db.database import get_db
from models import sessions


logout_router = APIRouter()

# we make a logout router so here is it
# we just respond a message.
# and delete session row from sessions, and coockie from cookies
@logout_router.post(
    "/api/logout",
    response_model=users_schema.logoutResponse, status_code=status.HTTP_200_OK
)
# i donno why, but i cant call session id first in parameter then response. so i wrote response and then sesion id in parameters.
def userLogout(response: Response, session_id: str | None = Cookie(default=None), db: Session=Depends(get_db)):
    # if there is no session id do this
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="invalid coockie"
        )
    # if session id exist, doing query to find session id in session table in data base. and if it doesent exist do this
    session_id_query = db.query(sessions.Session).filter(sessions.Session.sessionID == session_id).first()
    if not session_id_query:
        raise HTTPException(
            status_code=401,
            detail="invalid coockie"
        )
    # if session id exist in sessions table, doing query to find user in users table in data base. and if it doesent exist do this
    user_query_by_session = db.query(users_model.users).filter(users_model.users.id == session_id_query.sessionOwner).first()
    if user_query_by_session is None:
        raise HTTPException(
        status_code=401,
        detail="Invalid cookie"
    )

    # we delete the session row in sessions table
    db.delete(session_id_query)
    db.commit()

    # also we delete the coockie and response it
    response.delete_cookie(
        key="session_id",
        path="/",
        secure=False,
        httponly=False,
        samesite="lax"
    )

    return {"message": "Logout Successfully"}
