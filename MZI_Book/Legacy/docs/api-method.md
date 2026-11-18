# REST API

REST (ang. Representational State Transfer) to styl architektoniczny projektowania systemów rozproszonych, wprowadzony przez Roya Fieldinga w jego doktoracie z 2000 roku. Nie jest to protokół ani standard – to zestaw zasad, które opisują, jak powinny komunikować się ze sobą aplikacje w sieci.

Z kolei API (ang. Application Programming Interface) to interfejs, który pozwala jednej aplikacji „rozmawiać” z drugą. Połącz oba pojęcia i otrzymujesz RESTful API – czyli interfejs zaprojektowany zgodnie z zasadami REST.

W praktyce REST API opiera się na protokole HTTP. Oznacza to, że wszystkie operacje wykonujesz za pomocą standardowych żądań HTTP, które już znasz z codziennego przeglądania internetu.

## Metody i cody HTTP

Najczęstsze metody HTTP

| Metoda   | Zastosowanie          |
|----------|-----------------------|
| `Get`    | Pobieranie danych     |
| `POST`   | Przesłanie danych     |
| `PUT`    | Zastąpienie zasobu    |
| `Patch`  | Częściowa modyfikacja |
| `DELETE` | Usunięcie zasobu      |

Najczęstsze kody HTTP

| Kod                          | Znaczenie                        |
|------------------------------|----------------------------------|
| `200` OK                     | Żądanie zakończone sukcesem      |
| `201` Created                | Utworzono zasób                  |
| `204` No Content             | Sukces, bez treści odpowiedzi    |
| `400` Bad Request            | Niepoprawne żądanie              |
| `401` Unauthorized           | Brak poprawnego uwierzytelnienia |
| `403` Forbidden              | Odmowa dostępu                   | 
| `404` Not Found	             | Nie znaleziono zasobu            |
| `429` Too Many Requests	     | Przekroczono limit żądań         |
| `500` Internal Server Error	 | Wewnętrzny błąd serwera          |

Więcej informacji na temat: 
[HTTP Request Methods](Brak poprawnego uwierzytelnienia) i 
[HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status?utm_source=chatgpt.com)

## Środowisko pracy 

W języku Python możemy zastosować biblioteki, które pozwalają na wykonywanie zapytań REST API do serwera, takimi biblioteki są np. `requests`, `urllib`, `httpx`. 
```bash
pip install requests httpx
```

### Pobieranie danych 

Poniższy przykład przedstawia jak pobierać dane za pomocą metody GET

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

# Wysłanie zapytania GET do API
response = requests.get(url)

# Sprawdzenie, czy zapytanie zakończyło się sukcesem (kod 200 OK)
if response.status_code == 200:
    # Automatyczne parsowanie odpowiedzi z formatu JSON do słownika Pythona
    data = response.json()
    print("Tytuł posta:", data['title'])
else:
    print(f"Błąd pobierania danych. Kod statusu: {response.status_code}")
```

Czasami API wymaga przekazania niektórych informacji takich jak klucze autoryzacyjne, tokeny lub specjalne parametry wyszukiwania poprzez parametry URL (np. `?limit=10`). 

```python
import requests

url = "https://api.example.com/data"

# Parametry doklejane do adresu URL
query_params = {
    "limit": 10,
    "category": "tech"
}

# Nagłówki zawierające m.in. klucz API
headers = {
    "Authorization": "Bearer TWÓJ_KLUCZ_API",
    "Accept": "application/json"
}

response = requests.get(url, params=query_params, headers=headers)
```

Aby uniknąć zablokowania aplikacji w sytuacji, kiedy serwer nie odpowie, można zabezpieczyć się metodą `timeout`.

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    # Czekaj max 5 sekund. Możesz podać krotkę: (czas_łączenia, czas_odczytu) np. timeout=(3.05, 10)
    response = requests.get(url, timeout=5)
    response.raise_for_status() # Wyrzuca błąd dla kodów HTTP 4xx i 5xx
except requests.exceptions.Timeout:
    print("Serwer nie odpowiedział w wyznaczonym czasie.")
```

### Przechwytywanie wyjątków 

Standardowym rozwiązaniem do sprawdzania otrzymanego kodu jest `if response.status_code == 200`. Można to zamienić na metodę, która przechwyci otrzymany kod i wywoła odpowiedni wyjątek i poinformuje o błędzie.
```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()
    dane = response.json()
    
except requests.exceptions.HTTPError as errh:
    print(f"Błąd HTTP: {errh}") # Np. 404 Not Found, 401 Unauthorized
except requests.exceptions.ConnectionError as errc:
    print(f"Błąd połączenia (np. brak internetu, błąd DNS): {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Inny krytyczny błąd: {err}")
```

Większość komercyjnych API nakład limit możliwych zapytań wykonanych na minutę. Przekroczenie limitu skutkuje zwróceniem błędu HTTP `429 Too Many Requests` oraz może zwrócić nagłówek `Retray-Affter` z informacją ile trzeba odczekać do następnego zapytania.

```python
import requests
import time

def pobierz_dane():
    url = "https://api.example.com/data"
    
    while True:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 429:
            # Pobieramy czas oczekiwania z nagłówka (jeśli nie ma, domyślnie czekamy 10 sekund)
            czas_oczekiwania = int(response.headers.get("Retry-After", 10))
            print(f"Przekroczono limit. Czekam {czas_oczekiwania} sekund...")
            time.sleep(czas_oczekiwania)
            continue # Ponawiamy pętlę po odczekaniu
            
        response.raise_for_status()
        return response.json()
```


