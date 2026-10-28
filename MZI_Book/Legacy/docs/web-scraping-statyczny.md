# Web Scraping - statyczny

## Czym jest Web Scraping?

Web Scraping to technika automatycznego pobierania treści ze stron internetowych i przygotowywania ich do dalszej analizy. Głównym schematem działania web scrapingu jest:

[info grafika o web scraping] 

Web Scraping możemy podzielić na dwa typy:

* **Statyczny**, w którym analizowany jest bezpośrednio surowy kod HTML i na jego bazie pobierane są informacje ze stron internetowych.
* **Dynamiczny**, w którym dane na stronie ładowane są za pomocą np. JavaScript i analiza wymaga użycia narzędzi do symulacji przeglądarki (np. Selenium lub Playwright).

## Środowisko pracy 

W języku Python możemy zastosować biblioteki, które pozwolą wykonać zapytanie do serwera i zinterpretować zawartość strony. W przypadku statycznego web scrapingu standardem jest zestaw `requests` oraz `beautifulsoup4`. Dodanie bibliotek do środowiska wykonujemy poleceniem:

```bash
pip install requests beautifulsoup4
```

## Złote zasady etycznego scrapingu

Zanim zaczniesz pobierć dane ze stron, warto poznać poniższe zasady dobrego wychowania w sieci:

1. **Sprawdź plik `robots.txt`** - każda poprawnie skonfigurowana strona udostępnia pod adresem `domena.pl/robots.txt` plik informujący, które części witryny właściciel pozwala przeszukiwać botom, a które są zablokowane.
2. **Nie obciążaj serwerów (Throttling)** - wysyłanie tysięcy zapytań na sekundę może zostać odebrane jako atak DDoS, co skutkuje natychmiastowym zablokowaniem Twojego adresu IP. Zawsze stosuj przerwy między zapytaniami (`time.sleep()`).
3. **Używaj nagłówków (User-Agent)** - niektóre serwisy blokują domyślne zapytania pochodzące wprost z bibliotek takich jak `requests`. Aby temu zapobiec, warto symulować ruch z przeglądarki za pomocą odpowiednich nagłówków.

## Jak działa Web Scraping

W przypadku stron statycznych, w których treść znajduje się bezpośrednio w kodzie HTML, działanie możemy podzielić na trzy etapy:
1. Wykonanie zapytania HTTP `GET` pod wskazany adres URL i pobranie zawartości strony.
2. Przetworzenie surowego tekstu HTML i zbudowanie drzewa DOM (Document Object Model), które pozwala na łatwe poruszanie się po strukturze dokumentu.
3. Wyszukanie interesujących nas elementów po znacznikach (`<p>`, `<div>`, `<table>`, itp.), klasach (`class`) czy identyfikatorach (`id`).

Do bezpiecznego testowania i nauki web scrapingu możemy wykorzystać oficjalną stronę piaskownicową: [https://quotes.toscrape.com/](https://quotes.toscrape.com/).
Poniższy skrypt przedstawia kompletny proces pobierania cytatów oraz ich autorów.

```python
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
# Wysłanie zapytania HTTP GET do serwera
response = requests.get(url)

# Sprawdzenie, czy połączenie zakończyło się sukcesem (kod 200)
if response.status_code == 200:
    print("Połączenie udane! Przetwarzam dane...\n")
    
    # Inicjalizacja BeautifulSoup (wskazujemy parser 'html.parser')
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Znalezienie wszystkich elementów HTML, które zawierają pojedynczy cytat
    # Na tej stronie każdy cytat zamknięty jest w bloku: <div class="quote">
    quotes_list = soup.find_all("div", class_="quote")
    
    # Iteracja po znalezionych elementach i wyciąganie szczegółów
    for index, quote_box in enumerate(quotes_list, start=1):
        # Wyciągnięcie tekstu cytatu (znajduje się w <span class="text">)
        text = quote_box.find("span", class_="text").get_text()
        
        # Wyciągnięcie autora (znajduje się w <small class="author">)
        author = quote_box.find("small", class_="author").get_text()
        
        print(f"{index}. \"{text}\" — Autor: {author}")
else:
    print(f"Błąd pobierania strony. Kod statusu: {response.status_code}")
```

### Omówienie działania skryptu

W pierwszej kolejności definiujemy adres URL strony docelowej, a następnie za pomocą obiektu `requests` wykonujemy zapytanie `GET`. Jeżeli serwer zwróci status HTTP `200`, oznacza to poprawną odpowiedź i brak błędów po stronie serwera.

Uzyskany surowy tekst odpowiedzi (`response.text`) przekazywany jest do konstruktora `BeautifulSoup`, dzięki czemu tworzone jest drzewo DOM. Ułatwia ono nawigację po dokumencie i wyszukiwanie elementów za pomocą metod takich jak `find_all()`. Jeżeli wewnątrz znalezionego bloku znajdują się znaczniki zagnieżdżone, możemy je pobrać za pomocą metody `.find()`, a zawarty w nich tekst wyciągnąć za pomocą `.get_text()`.

## Dodawanie nagłówków

Niektóre serwisy wymagają, aby zapytanie HTTP zawierało odpowiednie nagłówki (`headers`). W bibliotece `requests` przekazujemy je jako słownik (dictionary) do argumentu `headers`: 

```python
requests.get(url, headers=moje_naglowki)
```

Jeżeli planujemy wysyłać wiele zapytań w ramach jednej sesji, warto skorzystać z obiektu `requests.Session()`, który pozwala zachować nagłówki i stan (np. ciasteczka) między zapytaniami:

```python
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8",
})

url = "https://quotes.toscrape.com/"
response = session.get(url)
print(response.status_code)
```

### Przykładowe nagłówki HTTP

Oto najpopularniejsze nagłówki, z którymi spotkasz się podczas web scrapingu:

1. `User-Agent` - informuje serwer, jaka przeglądarka, system operacyjny i urządzenie odpytują stronę.
    ```python
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
    ```
2. `Referer` - informuje serwer, z jakiej podstrony użytkownik (lub bot) przeszedł do obecnego zasobu. Niektóre systemy blokują żądania, które nie posiadają poprawnego nagłówka `Referer` (ochrona przed hotlinkingiem i prostymi botami).
    ```python
    "Referer": "https://quotes.toscrape.com/"
    ```
3. `Accept-Language` - informuje serwer, w jakim języku strona powinna zwrócić treść.
    ```python
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"
    ```
4. `Cookie` - pozwala przesyłać ciasteczka, co jest niezbędne, gdy serwer wymaga autoryzacji sesji lub akceptacji polityki prywatności (RODO).
    ```python
    "Cookie": "session_id=abc123xyz789; accepted_cookies=true"
    ```
5. `Authorization` - używany w nowoczesnych aplikacjach i przy scrapowaniu API. Służy do przekazywania tokenów uwierzytelniających.
    ```python
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC..."
    ```

## Paginacja 

Ważnym elementem web scrapingu jest pobieranie informacji rozproszonych na wielu podstronach. W przypadku stron statycznych stosuje się zazwyczaj jedno z dwóch podejść.

### Metoda 1: Paginacja dynamiczna (linkowana)

Skrypt na bieżąco szuka na stronie przycisku zawierającego np. odnośnik "Next" z klasą `.next`. Następnie wyciąga z niego adres URL kolejnej podstrony i powtarza proces w pętli.

W środowisku testowym `quotes.toscrape.com` przycisk przejścia do następnej strony ma strukturę `<li class="next"><a href="/page/2/">Next</a></li>`. Poniższy przykład ilustruje to podejście:

```python
import time
from bs4 import BeautifulSoup
import requests

base_url = "https://quotes.toscrape.com"
url = base_url

all_quotes = []
page_number = 1

while url:
  print(f"Pobieranie strony nr {page_number}: {url}")
  response = requests.get(url)

  if response.status_code != 200:
    print(f"Błąd pobierania strony. Kod: {response.status_code}")
    break

  soup = BeautifulSoup(response.text, "html.parser")

  # 1. Ekstrakcja danych z bieżącej strony
  quotes_list = soup.find_all("div", class_="quote")
  for quote_box in quotes_list:
    text = quote_box.find("span", class_="text").get_text()
    author = quote_box.find("small", class_="author").get_text()
    all_quotes.append({"text": text, "author": author})

  # 2. Szukanie przycisku "Next" na podstronie
  next_button = soup.find("li", class_="next")

  if next_button:
    relative_url = next_button.find("a")["href"]
    url = base_url + relative_url
    page_number += 1

    # Złota zasada etyki: krótka pauza przed kolejnym zapytaniem do serwera
    time.sleep(1)
  else:
    print("\nOsiągnięto ostatnią stronę.")
    url = None

print(f"Sukces! Zebrano łącznie {len(all_quotes)} cytatów ze wszystkich stron.")
```

### Metoda 2: Iteracja po numerach stron

Stosowana w sytuacjach, gdy struktura adresów URL jest regularna (np. `/strona/1/`, `/strona/2/`) i z góry znamy liczbę podstron (np. z analizy paginacji). Wtedy zamiast pętli `while` możemy użyć prostej pętli `for`.

```python
import time
from bs4 import BeautifulSoup
import requests

all_quotes = []

# Wiemy z analizy strony, że jest dokładnie 13 podstron
for page in range(1, 14):
  url = f"https://quotes.toscrape.com/page/{page}/"
  print(f"Pobieranie strony {page}...")

  response = requests.get(url)
  if response.status_code != 200:
    print(f"Strona {page} nie istnieje (kod {response.status_code}).")
    break

  soup = BeautifulSoup(response.text, "html.parser")
  quotes_list = soup.find_all("div", class_="quote")

  for quote_box in quotes_list:
    text = quote_box.find("span", class_="text").get_text()
    author = quote_box.find("small", class_="author").get_text()
    all_quotes.append({"text": text, "author": author})

  time.sleep(1)

print(f"\nZakończono! Zebrano łącznie {len(all_quotes)} cytatów.")
```

Rozwiązanie to jest prostsze, ale mniej elastyczne – zmiana liczby podstron na serwerze spowoduje pominięcie nowych danych lub błędy 404.

## Obsługa błędów 

Podczas web scrapingu musimy liczyć się z problemami sieciowymi, zmianami struktury strony czy niedostępnością serwera. Zamiast doprowadzać do awarii całego programu, należy stosować blok `try-except` połączony z mechanizmami biblioteki `requests`.

```python
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException

url = "https://quotes.toscrape.com/"
try:
    print("Wysyłam zapytanie do serwera...")
    # Dodajemy timeout (np. 5 sekund), żeby skrypt nie blokował się w nieskończoność
    response = requests.get(url, timeout=5)

    # Metoda rzucająca wyjątek dla kodów błędów HTTP (4xx, 5xx)
    response.raise_for_status()

    print("Udało się! Status:", response.status_code)

except ConnectionError:
    print("❌ Błąd połączenia! Sprawdź dostęp do internetu lub poprawność adresu URL.")
except Timeout:
    print("⏳ Przekroczono czas oczekiwania (Timeout). Serwer nie odpowiedział w zadanym czasie.")
except HTTPError as err:
    print(f"⚠️ Błąd HTTP! Serwer zwrócił status: {err}")
except RequestException as err:
    print(f"❌ Wystąpił nieoczekiwany błąd sieciowy: {err}")
except Exception as err:
    print(f"💥 Coś poszło nie tak: {err}")
```
