import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books/", json={
            "title": "Кобзар",
            "author": "Тарас Шевченко",
            "description": "Збірка поезій",
            "status": "available",
            "year": 1840
        })

        assert response.status_code == 201

        created_book = response.json()
        book_id = created_book["id"]

        response = await ac.get(f"/books/{book_id}")

        assert response.status_code == 200
        assert response.json()["id"] == book_id


@pytest.mark.asyncio
async def test_cursor_pagination():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        first = await ac.post("/books/", json={
            "title": "Book A",
            "author": "Author A",
            "description": "Description A",
            "status": "available",
            "year": 2001
        })

        second = await ac.post("/books/", json={
            "title": "Book B",
            "author": "Author B",
            "description": "Description B",
            "status": "borrowed",
            "year": 2002
        })

        assert first.status_code == 201
        assert second.status_code == 201

        response = await ac.get("/books/?limit=1")
        assert response.status_code == 200

        first_page = response.json()
        assert len(first_page) == 1

        cursor = first_page[-1]["id"]

        response = await ac.get(f"/books/?limit=10&cursor={cursor}")
        assert response.status_code == 200

        second_page = response.json()
        assert all(book["id"] > cursor for book in second_page)