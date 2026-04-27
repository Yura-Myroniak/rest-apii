from fastapi import FastAPI
from api.books import router as books_router
from database import Base, engine
from models.book import Book

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API - Lab 3")

app.include_router(books_router)