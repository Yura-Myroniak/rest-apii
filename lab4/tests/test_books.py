import os
import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

from main import app

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "library_db")


@pytest.fixture(autouse=True)
async def clean_books_collection():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]

    await db["books"].delete_many({})

    yield

    await db["books"].delete_many({})

    client.close()


@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post("/books/", json={
            "title": "Кобзар",
            "author": "Тарас Шевченко",
            "description": "Збірка поезій",
            "status": "available",
            "year": 1840
        })

        assert response.status_code == 201

        created_book = response.json()

        assert created_book["title"] == "Кобзар"
        assert "id" in created_book

        book_id = created_book["id"]

        response = await ac.get(f"/books/{book_id}")

        assert response.status_code == 200
        assert response.json()["id"] == book_id


@pytest.mark.asyncio
async def test_limit_offset_pagination():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        await ac.post("/books/", json={
            "title": "Book A",
            "author": "Author A",
            "description": "Desc A",
            "status": "available",
            "year": 2001
        })

        await ac.post("/books/", json={
            "title": "Book B",
            "author": "Author B",
            "description": "Desc B",
            "status": "borrowed",
            "year": 2002
        })

        response = await ac.get("/books/?limit=1&offset=0")

        assert response.status_code == 200
        assert len(response.json()) == 1

        response = await ac.get("/books/?limit=1&offset=1")

        assert response.status_code == 200
        assert len(response.json()) == 1