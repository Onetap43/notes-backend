from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import DatabaseBase
class User(DatabaseBase):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True, nullable=False)
    password=Column(String, nullable=False)
class Notes(DatabaseBase):
    __tablename__="notes"
    note_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title= Column(String, nullable=False)
    content=Column(String, nullable=False)

