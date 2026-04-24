from fastapi import APIRouter, HTTPException
from schemas.book import BookCreate
from services import book_service
from uuid import UUID

router = APIRouter()

@router.get("/books")
async def get_books(status: str = None, author: str = None, sort_by: str = None):
    return await book_service.get_books(status, author, sort_by)

@router.get("/books/{book_id}")
async def get_book(book_id: UUID):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", status_code=201)
async def create_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: UUID):
    await book_service.remove_book(book_id)
    return