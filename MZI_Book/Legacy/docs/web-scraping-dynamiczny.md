# Web Scraping - dynamiczny

## Czym jest Web Scraping?

W tej części przedstawione zostaną aspekty pobierania treści ze stron dynamicznie pobieranych, w których poza podstawowym szkieletem strony pozostałą część kontentu jest pobierana dynamicznie przy użyciu JavaScript, AJAX, itp.

## Środowisko pracy 

W języku Python możemy zastosować biblioteki, które pozwolą wykorzystać odpowiednie mechanizmy przegląderek internetowyc do pobrania treści ze stron. 
W przypadku dynamicznego web scraping-u standardem jest zestaw `selenium` oraz `playwright`. Dodanie bibliotek do środowiska wykonujemy poleceniem:

Instalacja `selenium` w środowisku Google Colaboratory
```bash
!wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
!sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
!sudo apt-get update
!sudo apt-get install -y google-chrome-stable
!pip install selenium
```
Instalacja biblioteki `playwright`
```bash
!pip install playwright
```

## Złote zasady etycznego scrapingu

Zanim zaczniesz pobierć dane ze stron, warto poznać poniższe zasady dobrego wychowania w sieci:

1. **Sprawdź plik `robots.txt`** - każda poprawnie skonfigurowana strona udostępnia pod adresem `domena.pl/robots.txt` plik informujący, które części witryny właściciel pozwala przeszukiwać botom, a które są zablokowane.
2. **Nie obciążaj serwerów (Throttling)** - wysyłanie tysięcy zapytań na sekundę może zostać odebrane jako atak DDoS, co skutkuje natychmiastowym zablokowaniem Twojego adresu IP. Zawsze stosuj przerwy między zapytaniami (`time.sleep()`).
3. **Używaj nagłówków (User-Agent)** - niektóre serwisy blokują domyślne zapytania pochodzące wprost z bibliotek takich jak `requests`. Aby temu zapobiec, warto symulować ruch z przeglądarki za pomocą odpowiednich nagłówków.

## Jak działa Web Scraping

Dynamiczny web scraping wymaga zastosowania silnika przeglądarki tak aby zasymulować i przetworzyć skrypty, które wykonują się u klienta. To rozwiązanie ma pewne wady, które powodują że strona musi się w całości pobrać i zapisać w pamięci oraz narzuty pamięciowe działąnia przedlądarki.
Idea wyszukiwania treści po znacznikach CSS lub elementach pozostaje taki sam jak w przypadku statycznego web scraping-u.

Poniższy skrypt przedstawia uruchomienie selenium i wykonanie zapytania do serwera 

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Wskazanie na świeżo zainstalowanego Google Chrome
options.binary_location = '/usr/bin/google-chrome'

try:
    # Nowe Selenium samo pobierze zgodny ChromeDriver pod tę wersję Chrome
    driver = webdriver.Chrome(options=options)
    
    driver.get("http://quotes.toscrape.com")
    print("Sukces! Tytuł strony to:", driver.title)
    
finally:
    if 'driver' in locals():
        driver.quit()
```

Powyższy skrypt wykorzystuje Headless browser, Które pozwala na uruchomienie środowiska bez interfejsu graficznego, zdolne do renderowania pełnego drzewa DOM, co pozwala na interakcję z widżetami i ukrytymi endpointami API.
Głównym elementem powyższego skryptu jest `WebDriver`, który odpowiada za tłumaczenie interakcji Pythona na fizyczne komendy w silniku przeglądarki.
zastosowaniem takiego rozwiązania może nieć miejsce agregacja dużych zbiorów ofert opartych o infinite scrolling (social media, portale pracy) oraz systemy finansowe odświeżające tabele w czasie rzeczywistym.

## Ważne moduły w `selenium`:

* **Keys** - moduł odpowiadający za integracje z klawiaturą symulującą klawisze tj. Enter, strzałki, Escape.
```python
from selenium.webdriver.common.keys import Keys
```
* **By** - Klasa odpowiedzialna za wyszukiwanie elementów ze strony, posiada specjalne mechanizmy, które pomogą wyszukiwać takie elementy jak ID, nazwyy klas, XPath, selektory CSS, itp.
```python
from selenium.webdriver.common.by import By
```   
* **WebDriverWait** - klasa odpowiadająca za mechanizm oczekiwania aż dany element zostanie załadowany na stronę, bardziej precyzyjny niż `time.sleep()`.
```python
from selenium.webdriver.support.ui import WebDriverWait
```

## Lokalizacja elmentów

Stosując klasę `By` z biblioteki `selenium` możemy definiować po jakich atrybutach czy właściwiościach możemy szukać elementów na stronie internetowej.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com")

# A. Ścieżka względna i dopasowanie do tekstu
login_btn = driver.find_element(By.XPATH, "//a[text()='Login']")

# B. Dopasowanie częściowe (contains) - dobre dla dynamicznych klas
tag_link = driver.find_element(By.XPATH, "//a[contains(@class, 'tag') and contains(text(), 'world')]")

# C. Osi nawigacyjne (Axes) - szukamy tagu 'span' obok etykiety 'by'
author_span = driver.find_element(By.XPATH, "//span[text()='by']/following-sibling::small[@class='author']")

# D. Wyszukanie wszystkich elementów z selektoram klasy quote.
quotes = driver.find_elements(By.CSS_SELECTOR, ".quote")

print("Autor z osi nawigacyjnej:", author_span.text)
driver.quit()
```

Powyższy skrypt przeszukuje stronę i zwraca element w zależności od wskazanego atrybutu i jego zawartości. Klasa `By` pozwala na zdefiniowanie po jakich elementach ma być wyszukiwana zawartość np `By.CLASS_NAME`, `By.ID`, `By.TAG_NAME`, itp.
Przedstawiony przykłąd stosuje sposób `By.XPATH`, daje to duże możliwości w sytuacjach kiedy zawartość może się zmieniać. [Przykłąd zastosowania XPath](https://serpapi.com/blog/xpath-selector-cheat-sheet-practical-examples-included/).

## Paginacja

Poniższy przykład przedstawia sposób przejście do kolejnych podstron:
```python

```

Powyższy skrypt przedstawia jak można wykonać przejście pomiędzy podstronami. 


## Integracja z interfejsem i formularzami 

Poniższy skrypt przedstawia przykłąd zastosowania modułu `Keys` do uzupełnienia formularza i zatwierdzenia go.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com/login")

username_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

# Czyszczenie i wprowadzanie tekstu
username_input.clear()
username_input.send_keys("student_uken")

# Zatwierdzanie formularza wirtualnym klawiszem ENTER
password_input.send_keys("tajne_haslo" + Keys.ENTER)

# Wykonanie skryptu JavaScript (zjechanie na dół strony)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.quit()
```

Powyższy skrypt przedstawia rozwiązanie, w któym odpytujemy stronę i wyszukujemy formularz logowania. Następnie wykorzystujemy moduł `keys`, do wyczyszczenia pul formularza i uzupełnienie go treścią. Zastosowanie `Key.Enter` pozwala pominąć proces wyszukiwania przycisku zatwierdzenia. 
Moduł `drive.execute_script()` pozwala na egzekucje polecenia bezpośrednio w środowisku przeglądarki.

## Zarządzanie kontekstem i synchronizacja

Poniższy skrypt przedstawia rozwiązanie pozwalające na synchronizacje z elementami, które jeszcze nie zostały załadowane. 

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://demoqa.com/frames")

# A. Explicit Wait - czekamy max 10 sekund na obecność ramki
iframe_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "frame1"))
)

# B. Przełączenie kontekstu do wnętrza ramki (iframe)
driver.switch_to.frame(iframe_element)
iframe_heading = driver.find_element(By.ID, "sampleHeading").text
print("Tekst z ramki:", iframe_heading)

# C. Powrót do głównego dokumentu
driver.switch_to.default_content()

driver.quit()
```

Powyższy skrypt odpytuje stronę i za pomocą modułu `WebDriverWait()` wykonuje wstrzymanie na maksymalnie 10 sekund lub do momentu załadowania elementu `iframe`. W przypadku kiedy na stronie znajduje się element `iframe` musimy przełączyć się do tego elementu stosując `switch_to.frame()` a do powrotu do głównego elementu `switch_to.default_content()`.
Obsługa linków z atrybutem `target="_blank"`. WebDriver wymaga iteracji po zadeklarowanych w systemie uchwytach okien (`window_handles`) i manualnego przesterowania wskaźnika (`switch_to.window()`) na nową zakładkę przed próbą parsowania jej zawartości.

## Obsługa wyjątków

Najpopularniejsze wyjątki jakie można obsługiwać w bibliotece `selenium`

1. **NoSuchElementException** - Występuje w sytuacji kiedy nie ma elementu na stronie lub strona zostałą zmodyfikowana.
```python
from selenium.common.exceptions import NoSuchElementException

try:
    cena = driver.find_element(By.CLASS_NAME, "product-price")
    print(cena.text)
except NoSuchElementException:
    print("Nie znaleziono ceny – produkt wyprzedany lub ukryty.")
```
2. **TimeoutException** - Występuje w sytuacji kiedy przekroczony zostanie czas oczekiwania na element.
```python
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    przycisk = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "load-more-comments"))
    )
    przycisk.click()
except TimeoutException:
    print("Komentarze nie załadowały się w ciągu 5 sekund. Pomijam sekcję.")
```
3. **StaleElementReferenceException** - Występuje w sytuacjach kiedy referencja do elementu zostaje zmodyfikowana przez framework i staje się nie aktualna.
```python
from selenium.common.exceptions import StaleElementReferenceException

try:
    przycisk = driver.find_element(By.ID, "refresh-data")
    przycisk.click()
except StaleElementReferenceException:
    print("DOM się odświeżył! Szukam elementu ponownie, aby w niego kliknąć.")
    przycisk = driver.find_element(By.ID, "refresh-data")
    przycisk.click()
```
4. **ElementClickInterceptedException** - Występuje w sytuacjach kiedy inny element zasłania możliwość kliknięcia w przycisk np. informacja o ciasteczkach lub inny baner.
```python
from selenium.common.exceptions import ElementClickInterceptedException

try:
    przycisk_kup = driver.find_element(By.ID, "buy-now")
    przycisk_kup.click()
except ElementClickInterceptedException:
    print("Coś zasłania przycisk! Wymuszam kliknięcie przez wstrzyknięcie JavaScriptu.")
    # JavaScript ignoruje warstwy wizualne (z-index) i uderza prosto w element w drzewie DOM
    driver.execute_script("arguments[0].click();", przycisk_kup)
```
5. **WebDriverException** - błąd komunikacji z przedlądarką. Występuje w sytuacjach kiedy wersja ChromeDrive jest inna niż wersja przeglądarki lub brakuje pamięci.
```python
from selenium.common.exceptions import WebDriverException

try:
    driver = webdriver.Chrome(options=options)
    driver.get("http://quotes.toscrape.com")
except WebDriverException as e:
    print("Krytyczny błąd środowiska: Nie udało się uruchomić przeglądarki.")
    print(f"Log błędu do analizy: {e}")
```