from fastapi import FastAPI
from app.database import database_engine, DatabaseBase
from app import models 
from app.routes import auth,notes
app= FastAPI()
DatabaseBase.metadata.create_all(bind=database_engine)
app.include_router(auth.router)
app.include_router(notes.router)