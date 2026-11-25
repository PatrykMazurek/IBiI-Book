# Podstawowe pojęcia

W tym laboratorium omawiane będą zagadnienia dotyczące tworzenia i korzystania z gotowych REST API. Wymagane biblioteki:

* Fast API `pip install fastapi`
* Requests `pip install requests`

**API** (_Application Programming Interface) - to zestaw instrukcji, zasad za pomocą których aplikacje mogą komunikować się z innymi aplikacjami._

**REST** (_Representational State Transfer) sposób projektowania usług sieciowych opasany w rozprawie doktorskiej_ Roya Fieldinga. REST zakłada m.in. komunikację klient-serwer, bezstanowość żądań oraz operowanie na zasobach.

**Podstawowe metody HTTP**

Najczęstsze metody HTTP

| Metoda   | Zastosowanie          |
|----------|-----------------------|
| `GET`    | Pobieranie danych     |
| `POST`   | Przesłanie danych     |
| `PUT`    | Zastąpienie zasobu    |
| `PATCH`  | Częściowa modyfikacja |
| `DELETE` | Usunięcie zasobu      |

**Kody odpowiedzi HTTP**

Przy każdym zapytaniu możemy otrzymać odpowiedni kod, który informuje czy aplikacja zakończyła działanie sukcesem. Najczęstsze kody odpowiedzi.

| Kod | Opis                  | Znaczenie                      |
|-----|-----------------------|--------------------------------|
| 200 | OK                    | Zapytanie zakończone sukcesem  |
| 201 | Created               | Zasób został utworzony         |
| 400 | Bad Request           | Błędne dane wejściowe          |
| 401 | Unauthorized          | Brak autoryzacji               |
| 403 | Forbidden             | Brak uprawnień                 |
| 404 | Not Found             | Nie znaleziono zasobu          |
| 429 | Too Many Requests     | Przekroczono limit żądań       |
| 500 | Internal Server Error | Błąd po stronie serwera        |
| 502 | Bad Gateway           | Niewłaściwe wyj scie           |
| 503 | Service Unavailable   | Brak wlnych połączeń           |
|504| Gateway Timeout       | Przekroczono czas na połącznie |

Więcej informacji na temat: 

* [HTTP Request Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods?utm_source=chatgpt.com) i
* [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status?utm_source=chatgpt.com)

