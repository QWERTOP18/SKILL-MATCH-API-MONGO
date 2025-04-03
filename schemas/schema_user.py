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



class UserInfo(BaseModel):
    """Simplified User information"""
    id: Optional[str] = None
    email: str