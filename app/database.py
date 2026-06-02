from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
database_engine=create_engine(DATABASE_URL)
DatabaseSession_Machine=sessionmaker(bind=database_engine, autocommit=False, autoflush=False)
DatabaseBase = declarative_base()
def get_database():
 database= DatabaseSession_Machine()
 try:
  yield database
 finally:
  database.close()