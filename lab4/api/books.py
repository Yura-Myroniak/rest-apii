from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_database
from repository.mongo_book_repository import MongoBookRepository
from schemas.book import BookCreate, BookResponse, BookStatus
from services import book_service


router = APIRouter(prefix="/books", tags=["Books"])


async def get_book_repository(database=Depends(get_database)):
    return MongoBookRepository(database)


@router.get("/", response_model=List[BookResponse])
async def get_books(
    status_filter: Optional[BookStatus] = Query(None, alias="status"),
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repository: MongoBookRepository = Depends(get_book_repository)
):
    return await book_service.get_books(
        repository=repository,
        status=status_filter,
        author=author,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    repository: MongoBookRepository = Depends(get_book_repository)
):
    book = await book_service.get_book_by_id(repository, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    repository: MongoBookRepository = Depends(get_book_repository)
):
    return await book_service.create_book(repository, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    repository: MongoBookRepository = Depends(get_book_repository)
):
    await book_service.delete_book(repository, book_id)
    return None