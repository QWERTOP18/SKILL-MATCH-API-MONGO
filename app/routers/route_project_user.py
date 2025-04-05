from fastapi import APIRouter,Request, Response,HTTPException
from app.schemas.schema_project import Project, ProjectBody
from app.schemas.schema_util import SuccessMessage
from app.database.db_project_user import db_add_user_to_project, db_remove_user_from_project, db_get_projects_by_user, db_get_users_by_project, db_update_user_role
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST


router = APIRouter()


@router.post("/api/project/{project_id}/add_user/{user_id}")
async def add_user(project_id: str, user_id: str):
    if await db_add_user_to_project(project_id, user_id):
        return {"message": "User added"}
    raise HTTPException(status_code=404, detail="Project not found or user already added")


@router.delete("/api/project/{project_id}/remove_user/{user_id}")
async def remove_user(project_id: str, user_id: str):
    if await db_remove_user_from_project(project_id, user_id):
        return {"message": "User removed"}
    raise HTTPException(status_code=404, detail="Project or user link not found")


@router.get("/api/user/{user_id}/projects")
async def get_projects_by_user(user_id: str):
    return await db_get_projects_by_user(user_id)


@router.get("/api/project/{project_id}/users")
async def get_users_by_project(project_id: str):
    return await db_get_users_by_project(project_id)


@router.put("/api/project/{project_id}/user/{user_id}/role")
async def update_user_role(project_id: str, user_id: str, role: str):
    if await db_update_user_role(project_id, user_id, role):
        return {"message": "Role updated"}
    raise HTTPException(status_code=404, detail="User or project not found or role unchanged")

