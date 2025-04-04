from pydantic import BaseModel, Field
from typing import Optional

class TaskSkills(BaseModel):
    """Task skills requirements mixin"""
    technical_skill: int = Field(default=0)
    problem_solving_ability: int = Field(default=0)
    communication_skill: int = Field(default=0)
    security_awareness: int = Field(default=0)
    leadership_and_collaboration: int = Field(default=0)
    frontend_skill: int = Field(default=0)
    backend_skill: int = Field(default=0)
    infrastructure_skill: int = Field(default=0)

class TaskBase(BaseModel):
    """Base class with common Task attributes"""
    title: str
    description: str
    color: str = Field(default="#FFFFFF")
    status: str

class Task(TaskBase, TaskSkills):
    """Complete Task model with all fields"""
    id: Optional[str] = None
    user_id: str
    project_id: str
    
    def to_dict(self) -> dict:
        """Convert task to dictionary with safe handling of None values"""
        return {
            "id": str(self.id) if self.id else "",
            "user_id": self.user_id or "",
            "project_id": self.project_id or "",
            "title": self.title or "",
            "description": self.description or "",
            "color": self.color or "",
            "status": self.status or "",
            "technical_skill": self.technical_skill or 0,
            "problem_solving_ability": self.problem_solving_ability or 0,
            "communication_skill": self.communication_skill or 0,
            "security_awareness": self.security_awareness or 0,
            "leadership_and_collaboration": self.leadership_and_collaboration or 0,
            "frontend_skill": self.frontend_skill or 0,
            "backend_skill": self.backend_skill or 0,
            "infrastructure_skill": self.infrastructure_skill or 0,
        }

class TaskBody(TaskBase, TaskSkills):
    """Task creation/update request body"""
    user_id: Optional[str] = None
    project_id: Optional[str] = None

def auth_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", "no name"),
        "technical_skill": user.get("technical_skill", 0),
        "problem_solving_ability": user.get("problem_solving_ability", 0),
        "communication_skill": user.get("communication_skill", 0),
        "security_awareness": user.get("security_awareness", 0),
        "leadership_and_collaboration": user.get("leadership_and_collaboration", 0),
        "frontend_skill": user.get("frontend_skill", 0),
        "backend_skill": user.get("backend_skill", 0),
        "infrastructure_skill": user.get("infrastructure_skill", 0),
    }