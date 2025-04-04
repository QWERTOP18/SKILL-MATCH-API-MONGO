from pydantic import BaseModel
from typing import Optional

class SuccessMessage(BaseModel):
    """Standard success message response"""
    message: str
    user_id: Optional[str] = None