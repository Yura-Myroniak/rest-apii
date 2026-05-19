from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
from bson import ObjectId
from database import books_collection

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app)


def serialize_book(book):
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "description": book.get("description"),
        "status": book["status"],
        "year": book["year"]
    }


class BookListResource(Resource):
    def get(self):
        """
        Get all books
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            required: false
            default: 10
          - name: offset
            in: query
            type: integer
            required: false
            default: 0
          - name: status
            in: query
            type: string
            required: false
          - name: author
            in: query
            type: string
            required: false
          - name: sort_by
            in: query
            type: string
            enum: [title, year]
            required: false
        responses:
          200:
            description: List of books
        """
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
        status = request.args.get("status")
        author = request.args.get("author")
        sort_by = request.args.get("sort_by")

        query = {}

        if status:
            query["status"] = status

        if author:
            query["author"] = {"$regex": author, "$options": "i"}

        cursor = books_collection.find(query).skip(offset).limit(limit)

        if sort_by == "title":
            cursor = cursor.sort("title", 1)
        elif sort_by == "year":
            cursor = cursor.sort("year", 1)

        books = [serialize_book(book) for book in cursor]

        return books, 200

    def post(self):
        """
        Create book
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - author
                - status
                - year
              properties:
                title:
                  type: string
                author:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [available, borrowed]
                year:
                  type: integer
        responses:
          201:
            description: Book created
        """
        data = request.get_json()

        if not data:
            return {"message": "Invalid JSON"}, 400

        required_fields = ["title", "author", "status", "year"]

        for field in required_fields:
            if field not in data:
                return {"message": f"{field} is required"}, 400

        if data["status"] not in ["available", "borrowed"]:
            return {"message": "Invalid book status"}, 400

        book = {
            "title": data["title"],
            "author": data["author"],
            "description": data.get("description"),
            "status": data["status"],
            "year": int(data["year"])
        }

        result = books_collection.insert_one(book)
        created_book = books_collection.find_one({"_id": result.inserted_id})

        return serialize_book(created_book), 201


class BookResource(Resource):
    def get(self, book_id):
        """
        Get book by ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Book found
          404:
            description: Book not found
        """
        if not ObjectId.is_valid(book_id):
            return {"message": "Invalid book ID"}, 400

        book = books_collection.find_one({"_id": ObjectId(book_id)})

        if not book:
            return {"message": "Book not found"}, 404

        return serialize_book(book), 200

    def delete(self, book_id):
        """
        Delete book
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Book deleted
        """
        if ObjectId.is_valid(book_id):
            books_collection.delete_one({"_id": ObjectId(book_id)})

        return "", 204


api.add_resource(BookListResource, "/books/")
api.add_resource(BookResource, "/books/<string:book_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)