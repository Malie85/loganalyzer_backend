from fastapi import APIRouter, Depends, HTTPException, status, Response
from argon2 import PasswordHasher
from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta
from models import users as users_model
from models import sessions as user_sessions
from schemas import users as users_schema
from db.database import engine, SessionLocal, Base, get_db

password_hasher = PasswordHasher()

Login_Router = APIRouter()



@Login_Router.post(
    "/api/login",
    response_model=users_schema.userLoginResponse,status_code=status.HTTP_200_OK
)
def userLogin(user: users_schema.userLogin,response: Response, db: Session=Depends(get_db)):
    
    
    userQuery = db.query(users_model.users).filter(users_model.users.username == user.username).first()
    
    if userQuery is None:
        raise HTTPException(
        status_code=400,
        detail="username or password is incorrect"
    )

    if not password_hasher.verify(userQuery.password,user.password):
        raise HTTPException(
        status_code=400,
        detail="username or password is incorrect"
    )

    session_id = secrets.token_urlsafe(32)

    new_session = user_sessions.Session(
        sessionID = session_id,
        sessionOwner = userQuery.id,
        createdAt = datetime.now(),
        expiredAt = datetime.now() + timedelta(hours=7)
    )

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

    return {"message": "Login successfully",
            "user": userQuery
            }