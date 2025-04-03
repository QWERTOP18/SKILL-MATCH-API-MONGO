from fastapi import APIRouter,Request, Response,HTTPException
from schemas import project, projectBody,SuccessMessage
from database.db_project import db_create_project, db_get_projects, db_get_single_project, db_update_project, db_delete_project
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST

from typing import List


router = APIRouter()



@router.post("/api/project", response_model=project)
async def create_project(request: Request, response: Response, data:projectBody):
    project = jsonable_encoder(data)
    res = await db_create_project(project)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = "Create project failed"
    )

@router.get("/api/project", response_model=List[project])
async def get_projects():
    res = await db_get_projects()
    return res

@router.get("/api/project/{id}", response_model=project)
async def get_single_project(id:str):
    res = await db_get_single_project(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"project with id {id} not found"
    )

@router.put("/api/project/{id}", response_model=project)
async def update_project(id:str, data:projectBody):
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