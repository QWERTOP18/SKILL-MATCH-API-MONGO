from pydantic import BaseModel

class SuccessMessage(BaseModel):
    """Standard success message response"""
    message: str