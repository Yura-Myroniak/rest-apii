from sqlalchemy.orm import Session
from models.book import Book
from schemas.book import BookCreate


async def get_books(
    db: Session,
    status=None,
    author=None,
    sort_by=None,
    cursor: str | None = None,
    limit: int = 10
):
    query = db.query(Book)

    if status:
        query = query.filter(Book.status == status)

    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    if cursor:
        query = query.filter(Book.id > cursor)

    if sort_by == "title":
        query = query.order_by(Book.title, Book.id)
    elif sort_by == "year":
        query = query.order_by(Book.year, Book.id)
    else:
        query = query.order_by(Book.id)

    return query.limit(limit).all()


async def get_book_by_id(db: Session, book_id: str):
    return db.query(Book).filter(Book.id == book_id).first()


async def create_book(db: Session, book_data: BookCreate):
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


async def delete_book(db: Session, book_id: str):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book:
        db.delete(book)
        db.commit()

    return None