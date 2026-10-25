from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.users import users

class files(Base):
    __tablename__ = "files"
    fileId =  Column(Integer, primary_key=True, index=True)
    originalName = Column(String)
    fileOwner = Column(Integer, ForeignKey("users.id"), nullable=False)
    storageKey = Column(String,nullable=False)