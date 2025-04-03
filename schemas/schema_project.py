from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, timedelta

class ProjectBase(BaseModel):
    """Base class with common Project attributes"""
    title: str
    description: str
    color: str = Field(default="#FFFFFF")
    image: Optional[str] = None
    document: Optional[str] = None
    reference: Optional[str] = None
    start: date = Field(default_factory=date.today)
    deadline: date = Field(default_factory=date.today)

class Project(ProjectBase):
    """Complete Project model with all fields"""
    id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert project to dictionary with safe handling of None values"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "color": self.color,
            "image": self.image or "",
            "document": self.document or "",
            "reference": self.reference or "",
            "start": self.start.isoformat() if self.start else "",
            "deadline": self.deadline.isoformat() if self.deadline else "",
        }

class ProjectBody(ProjectBase):
    """Project creation/update request body"""
    pass