from app import app
from database import books_collection


def setup_function():
    books_collection.delete_many({})


def test_create_and_get_book():
    client = app.test_client()

    response = client.post("/books/", json={
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "description": "Збірка поезій",
        "status": "available",
        "year": 1840
    })

    assert response.status_code == 201

    book = response.get_json()
    book_id = book["id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == book_id


def test_limit_offset_pagination():
    client = app.test_client()

    client.post("/books/", json={
        "title": "Book A",
        "author": "Author A",
        "description": "Desc A",
        "status": "available",
        "year": 2001
    })

    client.post("/books/", json={
        "title": "Book B",
        "author": "Author B",
        "description": "Desc B",
        "status": "borrowed",
        "year": 2002
    })

    response = client.get("/books/?limit=1&offset=0")

    assert response.status_code == 200
    assert len(response.get_json()) == 1