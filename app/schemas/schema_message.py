from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from .base import PyObjectId
from datetime import datetime

# 共通設定用のBaseModel
class BaseModelWithObjectId(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# DBから取得したMessage（_id含む）
class Message(BaseModelWithObjectId):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: str
    project_id: str
    context: str
    data: datetime 

# 新規作成用スキーマ
class MessageCreate(BaseModelWithObjectId):
    user_id: str
    project_id: str
    context: str
    data: datetime 

# 更新用スキーマ（部分更新）
class MessageUpdate(BaseModelWithObjectId):
    context: Optional[str] = None
    data: Optional[datetime] = None


# レスポンス用スキーマ
class MessageResponse(BaseModelWithObjectId):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    user_name: str
    project_id: str
    context: str
    data: datetime 

    class Config:
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "user_id": "507f1f77bcf86cd799439012",
                "project_id": "507f1f77bcf86cd799439013",
                "context": "This is a sample message.",
                "data": datetime.now()
            }
        }