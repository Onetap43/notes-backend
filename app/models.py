from sqlalchemy import Coloumn, Integer, String, ForeignKey
from app.database import DatabaseBase
class User(DatabaseBase):
    __tablename__="users"
    id=Coloumn(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True, nullable=False)
    password=Coloumn(String, nullable=False)
class Notes(DatabaseBase):
    __tablename__="notes"
    note_id=Coloumn(Integer, primary_key=True, index=True)
    user_id=Coloumn(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title= Coloumn(String, nullable=False)
    content=Coloumn(String, nullable=False)

