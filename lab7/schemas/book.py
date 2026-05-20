from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: BookStatus
    year: int = Field(..., ge=1000, le=2100)


class BookResponse(BookCreate):
    id: str

    class Config:
        from_attributes = True