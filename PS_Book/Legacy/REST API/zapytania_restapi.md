# Zapytania REST API

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

### Zapytania POST

Przekazywanie treści wysyłając je w strumieniu



### Aktualizacja i podmiana danych metody PUT i PATCH

Aktualizacje wybranych rekordów możemy wykonać za pomocą metoda PUT. Metoda podmienia całe rekordy dlatego w przypadku pominięcia jakiegoś rekordu, dany rekord może zostać pominięty.

```python
import requests

# Odwołujemy się do konkretnego zasobu (w URL znajduje się ID posta: 1)
url = "https://jsonplaceholder.typicode.com/posts/1"
payload_put = {
    "id": 1,
    "title": "Zaktualizowany tytuł",
    "body": "Całkowicie nowa treść posta",
    "userId": 1
}

response = requests.put(url, json=payload_put)
print(f"Status: {response.status_code}") # Zazwyczaj 200 OK
```

Jeżeli wymagamy aktualizować tylko fragment danych można zastosować metodę PATCH, metoda działą podobnie jak metoda PUT tylko z bezpiecznym podejściem, że aktualizuje tylko fragment wskazany, a nie podmienia całego rekordu.

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

# Wysyłamy tylko to pole, które uległo zmianie. Reszta zostaje nienaruszona.
payload_patch = { "title": "Poprawiona literówka w tytule" }

response = requests.patch(url, json=payload_patch)
print(f"Status: {response.status_code}") # Zazwyczaj 200 OK
print("Zaktualizowany zasób:", response.json())
```

### Usuwanie zasobów metoda DELETE

Usuwanie zasobów z przez REST API można wykonać w poniższy sposób

```python
import requests

# Wskazujemy post o ID 1 do usunięcia
url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.delete(url)
print(f"Status: {response.status_code}")
```

### Pomocnicze informacje

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
