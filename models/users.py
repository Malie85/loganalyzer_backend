from db.database import Base
from sqlalchemy import Column, Integer, String

# here we create table of USERS and its columns and its types.
# we have id for primary key insteat of username beacuse of fast indexing and also we can change username easily.
# but we wont show the ids to users. and usernames cant be the same --> unique=True
class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index=True)
    realname = Column(String, nullable= False) 
    username= Column(String,nullable= False, unique=True, index=True)
    password= Column(String, nullable= False)