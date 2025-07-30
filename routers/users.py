from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, engine
from models import models
from passlib.context import CryptContext

from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# this only run if database doesn't exist
models.Base.metadata.create_all(bind=engine)


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# THIS RETURNS CURRENT AUTH USER DETAIL return {'username':username, 'id':user_id, 'user_role':user_role} 
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class UserVerification(BaseModel):
    password :str
    new_password:str
    
    




@router.get("/",status_code=status.HTTP_200_OK)
async def get_user (user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    return db.query(models.Users).filter(models.Users.id == user.get('id')).first()


@router.patch('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_verification:UserVerification):
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed")
        user_model = db.query(models.Users).filter(models.Users.id ==user.get('id')).first()
        if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
            raise HTTPException(status_code=401, detail="Error on Password change")
        user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
        
        db.add(user_model)        
        db.commit()