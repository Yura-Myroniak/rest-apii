from fastapi import FastAPI

from api.books import router as books_router
from auth.routes import router as auth_router
from database import Base, engine
from models.book import Book


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API - Lab 6 JWT Auth")

app.include_router(auth_router)
app.include_router(books_router)