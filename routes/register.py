from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from models import users as users_model
from schemas import users as users_schema
from db.database import engine, SessionLocal, Base


# creating tables in database
users_model.Base.metadata.create_all(bind=engine)


register_router = APIRouter()


# this function make a session from sessionmaker in database.py
# so we can yield or output it to Register Rout in below, and close it.
def get_db ():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# The Register Rout
# what shape it responses? by response_model
# here we use status and HTTPException that we imported earlier
@register_router.post(
    "/api/register",
    response_model=users_schema.userResponse,status_code=status.HTTP_201_CREATED
    )
# The Endpoint of Register Rout
# what shape it gets? by --> user: users_schema.userRegister
# in Depends, we say to fast api: go and get a session from get_db and give it to function. so, it depends to get_db as he said.
# what is session? its just a type hinter . we imported from sqlalchemy orm. dont get this wrong with sessionlocal (I got wrong at first)
def register_user (user: users_schema.userRegister, db: Session=Depends(get_db)):


    # doing a query in db and search by model of users to finding if same username exists.
    exixting =  db.query(users_model.users).filter(users_model.users.username==user.username).first()


    # checking if username has already been taken so it reise an error 400
    if exixting:
        raise HTTPException(
            status_code=400,
            detail="This username has already been taken"
            )
    
    # creating an object based on users model so we can commit it do data base 
    new_user = users_model.users(
        realname= user.realname,
        username= user.username,
        password= user.password
    )

    # adding new user to database and commit it.
    # then refreshing to get username and realname to show it send it to frontend.
    # it wont send password and id because we choose userresponse for response model.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # finally retuning new user object (without password and id)
    return new_user