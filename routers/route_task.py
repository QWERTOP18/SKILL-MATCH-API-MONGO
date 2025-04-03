from fastapi import APIRouter,Request, Response,HTTPException
from schemas import task, taskBody,SuccessMessage
from database.db_task import db_create_task, db_get_tasks, db_get_single_task, db_update_task, db_delete_task
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST

from typing import List


router = APIRouter()



@router.post("/api/task", response_model=task)
async def create_task(request: Request, response: Response, data:taskBody):
    task = jsonable_encoder(data)
    res = await db_create_task(task)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = "Create task failed"
    )

@router.get("/api/task", response_model=List[task])
async def get_tasks():
    res = await db_get_tasks()
    return res

@router.get("/api/task/{id}", response_model=task)
async def get_single_task(id:str):
    res = await db_get_single_task(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )

@router.put("/api/task/{id}", response_model=task)
async def update_task(id:str, data:taskBody):
    res = await db_update_task(id, data)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )


@router.delete("/api/task/{id}", response_model=SuccessMessage)
async def delete_task(id:str):
    res = await db_delete_task(id)
    if res:
        return {"message": "Task deleted successfully"}
    raise HTTPException(
        status_code=404, detail = f"Task with id {id} not found"
    )