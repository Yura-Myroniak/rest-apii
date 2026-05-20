import pytest
from httpx import AsyncClient, ASGITransport

from main import app


async def get_auth_headers(ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })

    assert response.status_code == 200

    tokens = response.json()
    access_token = tokens["access_token"]

    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.mark.asyncio
async def test_books_are_protected_without_token():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/")

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_returns_access_and_refresh_tokens():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })

        assert response.status_code == 200

        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_create_and_get_book_with_token():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = await get_auth_headers(ac)

        response = await ac.post("/books/", json={
            "title": "Кобзар",
            "author": "Тарас Шевченко",
            "description": "Збірка поезій",
            "status": "available",
            "year": 1840
        }, headers=headers)

        assert response.status_code == 201

        created_book = response.json()
        book_id = created_book["id"]

        response = await ac.get(f"/books/{book_id}", headers=headers)

        assert response.status_code == 200
        assert response.json()["id"] == book_id


@pytest.mark.asyncio
async def test_refresh_token_flow():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login_response = await ac.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })

        assert login_response.status_code == 200

        refresh_token = login_response.json()["refresh_token"]

        refresh_response = await ac.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })

        assert refresh_response.status_code == 200

        data = refresh_response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"