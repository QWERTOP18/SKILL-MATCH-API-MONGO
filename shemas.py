from pydantic import BaseModel

class Todo(BaseModel):
    id:int
    title:str
    description:str
    done:bool


class TodoBody(BaseModel):
    title:str
    description:str

class SuccessMessage(BaseModel):
    message:str

