from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, engine
from models import models

from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=['Todos']
)

# from todo_models import models
# this only run if todos.db doesn't exist
models.Base.metadata.create_all(bind=engine)


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(
        ...,
        title="The title of the todo",
        max_length=100,
        min_length=2,
    )
    description: str = Field(
        ...,
        description="The description of the todo",
        max_length=500,
        min_length=3,
    )
    priority: int = 1
    completed: bool = False


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_single_todo(
    db: db_dependency,
    todo_id: int = Path(..., todo_id="The ID of the todo to get", ge=1),
):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is not None:
        return {"todo": todo}
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} not found",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: db_dependency, user:user_dependency):
    # new_todo = models.Todos(
    #     title=todo_request.title,
    #     description=todo_request.description,
    #     priority=todo_request.priority,
    #     completed=todo_request.completed,
    # )
    
    if user is None:
         raise HTTPException(status_code=401, detail="Authentication Failed")
        
    new_todo = models.Todos(**todo_request.dict(), owner_id =user.get('id'))
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"todo": new_todo}


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    todo_request: TodoRequest,
    db: db_dependency,
    todo_id: int = Path(..., todo_id="The ID of the todo to update", ge=1),
):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is not None:
        # option 1
        # for key, value in todo_request.dict().items():
        #     setattr(todo, key, value)
        #
        # option 2
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.completed = todo_request.completed
        #
        db.commit()
        db.refresh(todo)
        return {"todo": todo}
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} not found",
    )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: db_dependency,
    todo_id: int = Path(..., todo_id="The ID of the todo to delete", ge=1),
):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is not None:
        db.delete(todo)
        db.commit()
        return
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} not found",
    )
