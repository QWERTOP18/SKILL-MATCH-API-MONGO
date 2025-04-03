from fastapi import APIRouter,Request, Response,HTTPException
from shemas import Todo, TodoBody,SuccessMessage
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo, db_delete_todo
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST

from typing import List


router = APIRouter()



@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data:TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = "Create task failed"
    )

@router.get("/api/todo", response_model=List[Todo])
async def get_todos():
    res = await db_get_todos()
    return res

@router.get("/api/todo/{id}", response_model=Todo)
async def get_single_todo(id:str):
    res = await db_get_single_todo(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )

@router.put("/api/todo/{id}", response_model=Todo)
async def update_todo(id:str, data:TodoBody):
    res = await db_update_todo(id, data)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )


@router.delete("/api/todo/{id}", response_model=SuccessMessage)
async def delete_todo(id:str):
    res = await db_delete_todo(id)
    if res:
        return {"message": "Task deleted successfully"}
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )