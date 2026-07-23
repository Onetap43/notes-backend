from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.database import database_engine, DatabaseBase
from app.limiter import limiter
from app import models
from app.routes import auth, notes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://notes-backend-project.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "message": "Too many requests. Please try again later."
        },
    )


DatabaseBase.metadata.create_all(bind=database_engine)

app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/")
def home():
    return {
        "message": "Notes Backend API Running",
        "docs": "/docs",
    }