from fastapi import APIRouter, status, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from schemas import users as users_schema
from models import users as users_model
from db.database import get_db
from models import sessions
from services.check_coockie import check_coockie



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

    user_query_by_session,session_id_query = check_coockie(session_id,db)


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
