# Rest API

W tym laboratorium omawiane będą zagadnienia dotyczące tworzenia i korzystania z gotowych REST API. Wymagane biblioteki:

* Fast API `pip install fastapi`
* Requests `pip install requests`

**API** (_Application Programming Interface) - to zestaw instrukcji, zasad za pomocą których aplikacje mogą komunikować się z innymi aplikacjami._

**REST** (_Representational State Transfer) sposób projektowania usług sieciowych opasany w rozprawie doktorskiej_ Roya Fieldinga. REST zakłada m.in. komunikację klient-serwer, bezstanowość żądań oraz operowanie na zasobach.

**Podstawowe metody HTTP**

* GET - pobieranie danych
* POST - utworzenie nowego zasobu
* PUT - pełna aktualizacja zasobów
* PUSH - częściowa aktualizacja zasobów
* DELETE - usunięcie zasobów

**Kody odpowiedzi HTTP**

Przy każdym zapytaniu możemy otrzymać odpowiedni kod, który informuje czy aplikacja zakończyła działanie sukcesem. Najczęstsze kody odpowiedzi.

| Kod                       | Znaczenie                      |
| ------------------------- | ------------------------------ |
| 200 OK                    | Zapytanie zakończone sukcesem  |
| 201 Created               | Zasób został utworzony         |
| 400 Bad Request           | Błędne dane wejściowe          |
| 401 Unauthorized          | Brak autoryzacji               |
| 403 Forbidden             | Brak uprawnień                 |
| 404 Not Found             | Nie znaleziono zasobu          |
| 500 Internal Server Error | Błąd po stronie serwera        |

#### Tworzenie własnego REST API

Do udostępniania własnego API można zastosować bibliotekę FastAPI. Przed rozpoczęciem pracy należy dodać bibliotekę do środowiska.

```
pip install fastapi
```

Pracę zaczynamy od importu najważniejszych bibliotek oraz utworzenia niezbędnych obiektów

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

Aby wykonać punkty dostępowe (endpoints) do danych należy zastosować odpowiednie adnotacje przed definicją metody zwracającej lub pobierającej dane.:

* Dla pobierania danych, metoda GET

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

* Dla dodania nowych obiektów metoda POST

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

* Dla aktualizacji danych danych metody PUT i PATCH

**Metoda PUT**

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

**Metoda PATCH**

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

* Dla usuwania danych

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

#### Pobieranie zewnętrznego API

Do korzystania z zewnętrznych API można zastosować bibliotekę requests. Bibliotek pozwala na wykonywanie zapytań HTTP&#x20;



#### Zadania

