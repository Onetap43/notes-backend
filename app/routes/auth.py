from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.limiter import limiter
from sqlalchemy.orm import session
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_database
from app.models import User
from app.schemas import signupdata, logindata, TokenResponse
import os
from dotenv import load_dotenv
from app.logger import logger
load_dotenv()
router=APIRouter()
password_hasher=CryptContext(schemes=["bcrypt"],deprecated="auto")
security=HTTPBearer()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
def hash_password(plain_password:str):
    return password_hasher.hash(plain_password)
def verify_password(plain_password:str,hashed_password:str):
    return password_hasher.verify(plain_password,hashed_password)
def create_access_token(user_id:int):
    token_payload={"user_id":user_id}
    access_token=jwt.encode(token_payload,SECRET_KEY,algorithm=ALGORITHM)
    return access_token
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),database:session=Depends(get_database)):
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
def signup(signup_data:signupdata,database:session=Depends(get_database)):
    logger.info("signup route hit")
    existing_user=database.query(User).filter(User.username==signup_data.username).first()
    if existing_user:
        logger.warning(f"Signup failed: username already exists- {signup_data.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exists")
    #password hash karne ka function call kiya
    hashed_password=hash_password(signup_data.password)
    # make a new user object and then store it in a new row in users table
    new_user=User(username=signup_data.username,password=hashed_password)
    database.add(new_user)
    database.commit()
    # now database will make automatic user_id so get that user_id in new_user
    database.refresh(new_user)
    logger.info(f"New user created",extra={"event":"user_created","username":new_user.username})
    return{"message":"signup successful", "user_id":new_user.user_id,
           "username":new_user.username}
@router.post("/login",response_model=TokenResponse)
@limiter.limit("2/minute")
def login(request:Request,login_data:logindata,database_Session:session=Depends(get_database)):
    user=database_Session.query(User).filter((User.username)==login_data.username).first()
    if user is None:
        logger.warning(
    "Login failed: user not found",
    extra={
        "event": "login_failed_user_not_found",
        "username": login_data.username
    }
)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid username or password")
    password_is_correct=verify_password(login_data.password,user.password)
    if  not password_is_correct:
        logger.warning(
    "Login failed: wrong password",
    extra={
        "event": "login_failed_wrong_password",
        "username": login_data.username
    }
)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    access_token=create_access_token(user.user_id)
    logger.info(
    "User logged in",
    extra={
        "event": "user_login_success",
        "username": user.username
    }
)
    return{"access_token":access_token,"token_type":"bearer"}
@router.get("/me")
def get_my_profile(current_user:User=Depends(get_current_user)):
    return{"user_id":current_user.user_id,"username":current_user.username}


