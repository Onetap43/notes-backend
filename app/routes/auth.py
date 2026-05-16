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
    existing_user=database.query(User).filter(User.username==signup_data.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username already exists")
    #password hash karne ka function call kiya
    hashed_password=hash_password(signup_data.password)
    # make a new user object and then store it in a new row in users table
    new_user=User(username=signup_data.username,password=hashed_password)
    database.add(new_user)
    database.commit()
    # now database will make automatic user_id so get that user_id in new_user
    database.refresh(new_user)
    return{"message":"signup successful", "user_id":new_user.user_id,
           "username":new_user.username}
@router.post("/login",response_model=TokenResponse)
def login(login_data:LoginData,database:database_Session=Depends(get_database)):
    user=database_Session.query(User).filter((User.username)==login_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid username or password")
    password_is_correct=verify_password(login_data.password,user.password)
    if  not password_is_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    access_token=create_access_token(user.user_id)
    return {"acess token":access_token, "token_type:"bearer"}

