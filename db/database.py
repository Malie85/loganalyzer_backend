from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, declarative_base

# creating database url path variable
SQLalchemy_Datbase_URL =  "sqlite:///database.db"

# creating engine of database in engine variable.
# SQLite by default only allows a connection to be used by the thread that created it, but FastAPI uses multiple threads then conflict and error.
# Solution: connect_args={"check_same_thread": False} disables this restriction, and it's safe because SQLAlchemy manages the session per request. (Only needed for SQLite, not PostgreSQL/MySQL)
engine = create_engine(SQLalchemy_Datbase_URL, connect_args={"check_same_thread":False})
print("DATABASE FILE:", os.path.abspath("database.db"))


# creating a Session for commit data in data base.
# it cant commit by itself (autoflush=False, autocommit=False)
# its binded to engine variable so we can work with database by this here
# why LOCAL?? because it isnt the usual session in the world. it is just a session that i made localy in this program.
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# creating a main class for telling data base we are adding TABLES to you not other stuffs.
# it used in models
Base = declarative_base()