# Budowa REST API

Do budowy własnego REST API w języku Python można zastosować bibliotekę `fastapi`, która udostępnia odpowiednie mechanizmy ułatwiające komunikację.

Przed rozpoczęciem pracy należy dodać bibliotekę do środowiska.

```
pip install fastapi
```

Poniższy skrypt przedstawia podstawy do działania aplikacji REST API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# tworzenie obiektu FastAPI
app = FastAPI()
# Tworzenie obiektu obsługiwanego przez nasze REST API 
class Book(BaseModel):
    title: str
    author: str
    year: int
## dane zapisane na stałę
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
```

Powyższy skrypt tworzy podstawę do pracy z REST API, tworzy klasę `Book`, która w dalszej części będzie stosowana do przechowania lub udostępniania informacji.

* Endpoint `GET`

Punkt zwracający dane na żądanie klienta.

```python
## pobieranie głównego komunikatu
@app.get("/")
def home():
    return {"message": "API do zarządzania książkami"}
## pobieranie wszystkich książek
@app.get("/books")
def get_books():
    return books
## pobieranie wybranej książki po Id
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")
    return books[book_id]
```

* Endpoint `POST`

Punkt wykonujący żądanie dodania nowego rekordu do danych.

```python
@app.post("/books", status_code=201)
def create_book(book: Book):
    new_id = max books.keys() + 1 if books else 1
    books[new_id] = {
        "title": book.title,
        "author": book.author,
        "year": book.year
    }

    return {
        "id": new_id,
        "book": books[new_id]
    }
```

* Endpoint `PUT` i `PATCH`

wystawienie punktów za pomocą, których można wykonać żądanie aktualizacji danych w wybrany sposób: 

**Metoda `PUT`**

```python
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")

    books[book_id] = {
        "title": book.title,
        "author": book.author,
        "year": book.year
    }
    return {
        "message": "Książka została zaktualizowana",
        "book": books[book_id]
    }
```

**Metoda `PATCH`**

```python
@app.patch("/books/{book_id}")
def partially_update_book(book_id: int, book_update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")

    current_book = books[book_id]

    if book_update.title is not None:
        current_book["title"] = book_update.title

    if book_update.author is not None:
        current_book["author"] = book_update.author

    if book_update.year is not None:
        current_book["year"] = book_update.year

    return {
        "message": "Książka została częściowo zaktualizowana",
        "book": current_book
    }
```

* Endpoint `DELETE`

Punkt, do którego można przesłać żądanie o usunięcie wybranego rekordu

```python
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Książka nie została znaleziona")

    deleted_book = books.pop(book_id)

    return {
        "message": "Książka została usunięta",
        "book": deleted_book
    }
```

## Obsługa błędów

