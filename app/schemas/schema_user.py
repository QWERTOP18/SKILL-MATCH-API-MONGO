from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: str

class UserSkills(BaseModel):
    id: str
    name: Optional[str] = "no name"
    technical_skill: int
    problem_solving_ability: int
    communication_skill: int
    leadership_and_collaboration: int
    frontend_skill: int
    backend_skill: int
    infrastructure_skill: int
    security_awareness: int

class User(UserSkills):  # UserBase を継承しない
    id: Optional[str] = None
    image: Optional[str] = None
    name: str = Field(default="No Name")
    #password: Optional[str] = None  # 出力のため任意にする

    def to_dict(self):
        """Convert the User object to a dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            # "password": self.password,  # <- レスポンスには含めない場合はコメントアウト
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