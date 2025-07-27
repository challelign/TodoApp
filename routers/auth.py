
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import  APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt



from database import SessionLocal
from models.models import Users
# app = FastAPI()
router = APIRouter()
# openssl rand -hex 32
SECRET_KEY="1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
ALGORITHM="HS256"


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class CreateUserRequest(BaseModel):
    username :str  
    email :str 
    first_name :str
    last_name :str
    password: str
    role :str


class Token(BaseModel):
    message:str
    access_token:str
    token_type:str


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user (username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub':username,'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    


@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency ,create_user_request:CreateUserRequest):
    
    create_user_model = Users( 
                              email= create_user_request.email,
                              username= create_user_request.username,
                              first_name= create_user_request.first_name,
                              last_name= create_user_request.last_name,
                              role= create_user_request.role,
                              hashed_password = bcrypt_context.hash(create_user_request.password),
                              is_active = True
                              )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"create user": create_user_model} 


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentication"
    
    token = create_access_token(user.username,user.id,timedelta(minutes=20))
    
    return {
        "message": "Successfully token created",
        "access_token": token,
        "token_type":"bearer"
    }

@router.get("/auth/")
async def get_user():
    return {'user':"authenticated"}