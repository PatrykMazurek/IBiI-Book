from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int

books = {
    1: {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008
    },
    2: {
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "year": 2015
    }
}

@app.get("/")
def home():
    return {"message": "API do zarządzania książkami"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")
    return books[book_id]

@app.post("/books", status_code=201)
def create_book(book: Book):
    new_id = max(books.keys()) + 1 if books else 1
    books[new_id] = {
        "title": book.title,
        "author": book.author,
        "year": book.year
    }
    return {
        "id": new_id,
        "book": books[new_id]
    }

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")
    deleted_book = books.pop(book_id)
    return {
        "message": "Książka została usunięta",
        "book": deleted_book
    }