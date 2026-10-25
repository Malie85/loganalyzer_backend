from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from models import users as users_model
from sqlalchemy.orm import Session

from models import users as users_model
from models import sessions
from schemas import users as users_schema
from db.database import get_db
from services.check_coockie import check_coockie


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

    user_query_by_session,session_id_query = check_coockie(session_id,db)

    # if all was ok, respond this
    new_user = users_model.users(
        realname= user_query_by_session.realname,
        username= user_query_by_session.username,
    )

    return new_user

