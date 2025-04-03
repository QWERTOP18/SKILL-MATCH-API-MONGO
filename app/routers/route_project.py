from fastapi import APIRouter,Request, Response,HTTPException
from schemas.schema_project import Project, ProjectBody
from schemas.schema_util import SuccessMessage
from database.db_project import db_create_project, db_get_projects, db_get_single_project, db_update_project, db_delete_project, db_get_tasks_by_project, db_get_tasks_by_user
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST

from typing import List


router = APIRouter()



@router.post("/api/project", response_model=Project)
async def create_project(request: Request, response: Response, data:ProjectBody):
    project = jsonable_encoder(data)
    res = await db_create_project(project)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = "Create project failed"
    )

@router.get("/api/project", response_model=List[Project])
async def get_projects():
    res = await db_get_projects()
    return res

@router.get("/api/project/{id}", response_model=Project)
async def get_single_project(id:str):
    res = await db_get_single_project(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"project with id {id} not found"
    )

@router.put("/api/project/{id}", response_model=Project)
async def update_project(id:str, data:ProjectBody):
    res = await db_update_project(id, data)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"project with id {id} not found"
    )


@router.delete("/api/project/{id}", response_model=SuccessMessage)
async def delete_project(id:str):
    res = await db_delete_project(id)
    if res:
        return {"message": "project deleted successfully"}
    raise HTTPException(
        status_code=404, detail = f"project with id {id} not found"
    )


@router.get("/tasks/project/{project_id}")
async def get_tasks_by_project(project_id: str):
    """特定の project_id に紐づいたタスク一覧を取得"""
    tasks = await db_get_tasks_by_project(project_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks

@router.get("/tasks/user/{user_id}")
async def get_tasks_by_user(user_id: str):
    """特定の user_id に紐づいたタスク一覧を取得"""
    tasks = await db_get_tasks_by_user(user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks
