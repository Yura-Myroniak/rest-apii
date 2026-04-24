from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str
    year: int = Field(..., ge=0)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID