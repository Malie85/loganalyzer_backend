from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.users import users



class Session(Base):
    __tablename__ = "sessions"

    sessionID = Column(String, primary_key=True)
    sessionOwner = Column(Integer, ForeignKey("users.id"), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    expiredAt = Column(DateTime, nullable=False)