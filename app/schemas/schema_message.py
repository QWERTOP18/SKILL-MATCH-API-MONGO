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
