from fastapi import APIRouter, Depends, HTTPException, status, Response
from argon2 import PasswordHasher
from sqlalchemy.orm import Session
from models import users as users_model
from schemas import users as users_schema
from db.database import get_db
from services.session import create_session

# adding hasher to use verify
password_hasher = PasswordHasher()

Login_Router = APIRouter()


# rout of login
# using schema from user.py
@Login_Router.post(
    "/api/login",
    response_model=users_schema.userLoginResponse,status_code=status.HTTP_200_OK
)
# endpoint of login
# using schmema from user.py and using data base from get db function in database.py
def userLogin(user: users_schema.userLogin, response: Response, db: Session=Depends(get_db)):
    
    # we do a query so we can find row of user in database, based on username
    userQuery = db.query(users_model.users).filter(users_model.users.username == user.username).first()
    # if query didnt find, it says None. so here we handle it
    if userQuery is None:
        raise HTTPException(
        status_code=400,
        detail="username or password is incorrect"
    )

    # if query was ok, we verify password by hasher
    if not password_hasher.verify(userQuery.password,user.password):
        raise HTTPException(
        status_code=400,
        detail="username or password is incorrect"
    )

    create_session(userQuery.id,response,db)

    # returning body of jason with message and user that found it in query
    return {"message": "Login successfully",
            "user": userQuery
            }