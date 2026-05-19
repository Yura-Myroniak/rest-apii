from uuid import uuid4
from typing import Optional
from schemas.book import BookCreate, BookStatus


class MongoBookRepository:
    def __init__(self, database):
        self.collection = database["books"]

    async def get_books(
        self,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ):
        query = {}

        if status:
            query["status"] = status.value

        if author:
            query["author"] = {"$regex": author, "$options": "i"}

        sort_field = None

        if sort_by == "title":
            sort_field = "title"
        elif sort_by == "year":
            sort_field = "year"

        cursor = self.collection.find(query).skip(offset).limit(limit)

        if sort_field:
            cursor = cursor.sort(sort_field, 1)

        books = []

        async for book in cursor:
            book["id"] = book.pop("_id")
            books.append(book)

        return books

    async def get_book_by_id(self, book_id: str):
        book = await self.collection.find_one({"_id": book_id})

        if not book:
            return None

        book["id"] = book.pop("_id")
        return book

    async def create_book(self, book_data: BookCreate):
        book = book_data.model_dump()
        book["_id"] = str(uuid4())
        book["status"] = book["status"].value

        await self.collection.insert_one(book)

        book["id"] = book.pop("_id")
        return book

    async def delete_book(self, book_id: str):
        await self.collection.delete_one({"_id": book_id})
        return None