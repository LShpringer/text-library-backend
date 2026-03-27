from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TextCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = "Без категории"
    tags: Optional[str] = ""

class TextUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    category: Optional[str]
    tags: Optional[str]

class TextResponse(TextCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
