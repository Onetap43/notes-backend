from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from app.database import DatabaseBase
class User(DatabaseBase):
    __tablename__="users"
    user_id=Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True, nullable=False)
    password=Column(String, nullable=False)
class Notes(DatabaseBase):
    __tablename__="notes"
    note_id=Column(Integer, primary_key=True, index=True)
    pinned=Column(Boolean,default=False)
    user_id=Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    title= Column(String, nullable=False)
    content=Column(String, nullable=False)
    archived=Column(Boolean,default=False)

