import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.post("/books", json={
            "title": "Кобзар",
            "author": "Тарас Шевченко",
            "description": "Збірка поезій",
            "status": "available",
            "year": 1840
        })

        assert response.status_code == 201

        created_book = response.json()
        assert created_book["title"] == "Кобзар"
        assert created_book["author"] == "Тарас Шевченко"
        assert "id" in created_book

        book_id = created_book["id"]

        response = await ac.get(f"/books/{book_id}")

        assert response.status_code == 200
        book = response.json()
        assert book["id"] == book_id
        assert book["title"] == "Кобзар"