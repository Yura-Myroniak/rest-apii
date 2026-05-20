from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas.book import BookCreate, BookResponse, BookStatus
from services import book_service
from auth.security import get_current_user
from rate_limiter import rate_limit


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
async def get_books(
    request: Request,
    status_filter: Optional[BookStatus] = Query(None, alias="status"),
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$"),
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["username"] if current_user else None

    await rate_limit(request, user_id)

    return await book_service.get_books(
        db=db,
        status=status_filter,
        author=author,
        sort_by=sort_by,
        cursor=cursor,
        limit=limit
    )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["username"] if current_user else None

    await rate_limit(request, user_id)

    book = await book_service.get_book_by_id(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["username"] if current_user else None

    await rate_limit(request, user_id)

    return await book_service.create_book(db, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["username"] if current_user else None

    await rate_limit(request, user_id)

    await book_service.delete_book(db, book_id)
    return None