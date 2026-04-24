from repository import book_repo
from uuid import uuid4

async def get_books(status=None, author=None, sort_by=None):
    books = await book_repo.get_all_books()

    if status:
        books = [b for b in books if b["status"] == status]

    if author:
        books = [b for b in books if b["author"] == author]

    if sort_by == "title":
        books.sort(key=lambda x: x["title"])
    elif sort_by == "year":
        books.sort(key=lambda x: x["year"])

    return books

async def get_book(book_id):
    return await book_repo.get_book_by_id(book_id)

async def create_book(book_data):
    book = book_data.dict()
    book["id"] = str(uuid4())
    return await book_repo.add_book(book)

async def remove_book(book_id):
    return await book_repo.delete_book(book_id)