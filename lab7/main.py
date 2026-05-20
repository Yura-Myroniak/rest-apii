from fastapi import FastAPI, Request

from api.books import router as books_router
from auth.routes import router as auth_router
from database import Base, engine
from models.book import Book
from rate_limiter import rate_limit


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API - Lab 7 Rate Limiter")

app.include_router(auth_router)
app.include_router(books_router)


@app.get("/public")
async def public_endpoint(request: Request):
    await rate_limit(request, None)

    return {"message": "public"}