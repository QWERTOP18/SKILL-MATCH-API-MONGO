from base import PyObjectId
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class UserProjectLink(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    project_id: PyObjectId
    role: Optional[str] = "member"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
