from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 
from datetime import date, datetime
from app.openai_utils import generate_tasks_for_project
from app.auth_utils import AuthJwtCsrf
from .db_task import task_serializer, db_create_task
from .db_project import project_serializer

import asyncio


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop

database = client.API_DB
collection_user_project = database.user_project
collection_user = database.user
collection_project = database.project

async def db_add_user_to_project(project_id: str, user_id: str, role: str = "member") -> bool:
    """UserProjectLinkにユーザーとプロジェクトの関係を追加（重複不可）"""

    # ObjectId 変換
    try:
        project_oid = ObjectId(project_id)
        user_oid = ObjectId(user_id)
    except Exception:
        return False  # 無効なID形式

    # プロジェクトとユーザーの存在確認
    project_exists = await collection_project.find_one({"_id": project_oid})
    user_exists = await collection_user.find_one({"_id": user_oid})

    if not project_exists or not user_exists:
        return False

    # 既にリンクがあるかチェック
    exists = await collection_user_project.find_one({
        "project_id": project_oid,
        "user_id": user_oid,
    })

    if exists:
        return False  # すでに存在している場合は何もしない

    # 新しいリンクを作成
    link = {
        "project_id": project_oid,
        "user_id": user_oid,
        "role": role
    }
    result = await collection_user_project.insert_one(link)
    return result.inserted_id is not None


async def db_remove_user_from_project(project_id: str, user_id: str) -> bool:
    """UserProjectLink からユーザーとプロジェクトの関係を削除"""
    result = await collection_user_project.delete_one({
        "project_id": ObjectId(project_id),
        "user_id": ObjectId(user_id),
    })
    return result.deleted_count > 0

async def db_update_user_role(project_id: str, user_id: str, new_role: str) -> bool:
    """UserProjectLink に登録された role を更新"""
    result = await collection_user_project.update_one(
        {
            "project_id": ObjectId(project_id),
            "user_id": ObjectId(user_id),
        },
        {"$set": {"role": new_role}}
    )
    return result.modified_count > 0


async def db_get_projects_by_user(user_id: str) -> list:
    """特定のユーザーが所属するプロジェクト一覧を取得"""
    links = collection_user_project.find({"user_id": ObjectId(user_id)})
    projects = []

    async for link in links:
        project = await collection_project.find_one({"_id": link["project_id"]})
        if project:
            project_data = project_serializer(project)
            project_data["role"] = link.get("role", "member")  # role も返す
            projects.append(project_data)

    return projects

async def db_get_users_by_project(project_id: str) -> list:
    """特定のプロジェクトに所属するユーザー一覧を取得"""
    links = collection_user_project.find({"project_id": ObjectId(project_id)})
    users = []

    async for link in links:
        user = await collection_user.find_one({"_id": link["user_id"]})
        if user:
            user_data = {
                "id": str(user["_id"]),
                "name": user.get("name", ""),
                "email": user.get("email", ""),
                "role": link.get("role", "member")
            }
            users.append(user_data)

    return users
