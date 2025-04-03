from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class User(BaseModel):
    id: Optional[str] = None
    email: str
    password: str
    name: str
    image: Optional[str] = None
    technical_skill: int = Field(default=0)
    problem_solving_ability: int = Field(default=0)
    communication_skill: int = Field(default=0)
    leadership_and_collaboration: int = Field(default=0)
    frontend_skill: int = Field(default=0)
    backend_skill: int = Field(default=0)
    infrastructure_skill: int = Field(default=0)
    security_awareness: int = Field(default=0)

class task(BaseModel):
    id: Optional[str] = None
    user_id: str
    project_id: str
    title: str
    memo: str
    color: str = Field(default="#FFFFFF")
    status: str
    technical_skill: int = Field(default=0)
    problem_solving_ability: int = Field(default=0)
    communication_skill: int = Field(default=0)
    security_awareness: int = Field(default=0)
    leadership_and_collaboration: int = Field(default=0)
    frontend_skill: int = Field(default=0)
    backend_skill: int = Field(default=0)
    infrastructure_skill: int = Field(default=0)
    def to_dict(self) -> dict:
        return {
        "id": str(self.id) if self.id else "",
        "user_id": self.user_id if self.user_id is not None else "",
        "project_id": self.project_id if self.project_id is not None else "",
        "title": self.title if self.title is not None else "",
        "memo": self.memo if self.memo is not None else "",
        "color": self.color if self.color is not None else "",
        "status": self.status if self.status is not None else "",
        "technical_skill": self.technical_skill if self.technical_skill is not None else "",
        "problem_solving_ability": self.problem_solving_ability if self.problem_solving_ability is not None else "",
        "communication_skill": self.communication_skill if self.communication_skill is not None else "",
        "security_awareness": self.security_awareness if self.security_awareness is not None else "",
        "leadership_and_collaboration": self.leadership_and_collaboration if self.leadership_and_collaboration is not None else "",
        "frontend_skill": self.frontend_skill if self.frontend_skill is not None else "",
        "backend_skill": self.backend_skill if self.backend_skill is not None else "",
        "infrastructure_skill": self.infrastructure_skill if self.infrastructure_skill is not None else "",
    }

class project(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    color: str = Field(default="#FFFFFF")
    image: Optional[str] = None
    document: Optional[str] = None
    reference: Optional[str] = None
    start: date
    deadline: date
    def to_dict(self) -> dict:
        return {
        "id": str(self.id) if self.id else "",
        "title": self.title if self.title is not None else "",
        "description": self.description if self.description is not None else "",
        "color": self.color if self.color is not None else "",
        "image": self.image if self.image is not None else "",
        "document": self.document if self.document is not None else "",
        "reference": self.reference if self.reference is not None else "",
        "start": self.start.isoformat() if self.start else "",
        "deadline": self.deadline.isoformat() if self.deadline else "",
    }



class taskBody(BaseModel):
    title: str
    memo: str
    color: Optional[str] = "#FFFFFF"
    status: str
    user_id: Optional[str]
    project_id: Optional[str]
    technical_skill: int = Field(default=0)
    problem_solving_ability: int = Field(default=0)
    communication_skill: int = Field(default=0)
    security_awareness: int = Field(default=0)
    leadership_and_collaboration: int = Field(default=0)
    frontend_skill: int = Field(default=0)
    backend_skill: int = Field(default=0)
    infrastructure_skill: int = Field(default=0)

class UserAuthBody(BaseModel):
    email: str
    name: str
    password:str
    image: Optional[str] = None

class UserInfo(BaseModel):
    id: Optional[str] = None
    email: str

class projectBody(BaseModel):
    title: str
    description: str
    color: Optional[str] = "#FFFFFF"
    image: Optional[str] = None
    document: Optional[str] = None
    reference: Optional[str] = None
    start: date
    deadline: date

class SuccessMessage(BaseModel):
    message:str