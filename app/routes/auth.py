from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_database
from app.models import User
from app.schemas import SignupData, LoginData, TokenResponse
router=APIRouter()
password_hasher=CryptContext(schemes=["bcrypt"],deprecated="auto")
security=HTTPBearer()
SECRET_KEY="finlanduae2026"
ALGORITHM="HS256"
def hash_password(plain_password:str):
    return password_hasher.hash(plain_password)
def verify_password(plain_password:str,hashed_password:str):
    return password_hasher.verify(plain_password,hashed_password)
def create_access_token(user_id:int):
    token_payload={"user_id":user_id}
    access_token=jwt.encode(token_payload,SECRET_KEY,algorithm=ALGORITHM)
    return access_token
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),database:Session=Depends(get_database)):
    token=credentials.credentials
    try:
        decoded_payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=decoded_payload["user_id"]
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=database.query(User).filter(User.user_id==user_id).first()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="USER NOT FOUND")
    return current_user
@router.post("/signup")
def signup(signup_data:SignupData,database:Session=depends(get_database)):
    

