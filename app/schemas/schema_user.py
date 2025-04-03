from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    """Base class with common User attributes"""
    email: str
    password: str
    
    
    
class UserSkills(BaseModel):
    """User skills mixin"""
    technical_skill: int = Field(default=0)
    problem_solving_ability: int = Field(default=0)
    communication_skill: int = Field(default=0)
    leadership_and_collaboration: int = Field(default=0)
    frontend_skill: int = Field(default=0)
    backend_skill: int = Field(default=0)
    infrastructure_skill: int = Field(default=0)
    security_awareness: int = Field(default=0)

class User(UserBase, UserSkills):
    """Complete User model with all fields"""
    id: Optional[str] = None
    image: Optional[str] = None
    name: str = Field(default="No Name")

    def to_dict(self):
        """Convert the User object to a dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            # "password": self.password,
            "image": self.image or "",
            "name": self.name,
            "technical_skill": self.technical_skill or 0,
            "problem_solving_ability": self.problem_solving_ability or 0,
            "communication_skill": self.communication_skill or 0,
            "security_awareness": self.security_awareness or 0,
            "leadership_and_collaboration": self.leadership_and_collaboration or 0,
            "frontend_skill": self.frontend_skill or 0,
            "backend_skill": self.backend_skill or 0,
            "infrastructure_skill": self.infrastructure_skill or 0,
        }



class UserInfo(BaseModel):
    """Simplified User information"""
    id: Optional[str] = None
    email: str


class UserBody(UserBase):
    """Project creation/update request body"""
    pass