from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL="sqlite:///./notes.db"
database_engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DatabaseSession_Machine=sessionmaker(bind=database_engine, autocommit=False, autoflush=False)
DatabaseBase = declarative_base()
def get_database():
 database= DatabaseSession_Machine()
 try:
  yield database
 finally:
  database.close()