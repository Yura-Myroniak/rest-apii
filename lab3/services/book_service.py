from sqlalchemy.orm import Session
from repository import book_repository
from schemas.book import BookCreate


async def get_books(db: Session, status=None, author=None, sort_by=None, cursor=None, limit=10):
    return await book_repository.get_books(db, status, author, sort_by, cursor, limit)


async def get_book_by_id(db: Session, book_id: str):
    return await book_repository.get_book_by_id(db, book_id)


async def create_book(db: Session, book_data: BookCreate):
    return await book_repository.create_book(db, book_data)


async def delete_book(db: Session, book_id: str):
    return await book_repository.delete_book(db, book_id)