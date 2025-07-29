from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, engine
from models import models

from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
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







@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user:user_dependency):            
    if user is None or user.get('user_role') != 'admin':
         raise HTTPException(status_code=401, detail="Authentication Failed")
     
    return db.query(models.Todos).all()



@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    db: db_dependency,
    user:user_dependency,   
    todo_id: int = Path(..., todo_id="The ID of the todo to delete", ge=0)
):
    if user is None or user.get('user_role') != 'admin':
         raise HTTPException(status_code=401, detail="Authentication Failed")
     
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo is  None:      
        raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} not found",
    ) 
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return  {"message":"Deleted todo","todo": todo}

