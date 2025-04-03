from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id:str
    title:str
    description:str
    # done:bool


class TodoBody(BaseModel):
    title:str
    description:str

class SuccessMessage(BaseModel):
    message:str


class UserBody(BaseModel):
    email:str
    password:str

class UserInfo(BaseModel):
    id: Optional[str] = None
    email: str
