from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_database
from app.models import User
from app.schemas import SignupData, LoginData, TokenResponse
router=APIRouter()

