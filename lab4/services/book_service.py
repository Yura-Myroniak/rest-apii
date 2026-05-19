from repository.mongo_book_repository import MongoBookRepository
from schemas.book import BookCreate


async def get_books(repository: MongoBookRepository, status=None, author=None, sort_by=None, limit=10, offset=0):
    return await repository.get_books(status, author, sort_by, limit, offset)


async def get_book_by_id(repository: MongoBookRepository, book_id: str):
    return await repository.get_book_by_id(book_id)


async def create_book(repository: MongoBookRepository, book_data: BookCreate):
    return await repository.create_book(book_data)


async def delete_book(repository: MongoBookRepository, book_id: str):
    return await repository.delete_book(book_id)