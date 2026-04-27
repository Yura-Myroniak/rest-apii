import uuid
from sqlalchemy import Column, String, Integer, Enum
from database import Base
import enum


class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(BookStatus), nullable=False, default=BookStatus.available)
    year = Column(Integer, nullable=False)