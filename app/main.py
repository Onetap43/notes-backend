from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Notes Backend API is running"}