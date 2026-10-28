import requests
from bs4 import BeautifulSoup

# 1. Adres docelowy
url = "https://quotes.toscrape.com/"

# 2. Wysłanie zapytania HTTP GET do serwera
response = requests.get(url)

# 3. Sprawdzenie, czy połączenie zakończyło się sukcesem (kod 200)
if response.status_code == 200:
    print("Połączenie udane! Przetwarzam dane...\n")

    # 4. Inicjalizacja BeautifulSoup (wskazujemy parser 'html.parser')
    soup = BeautifulSoup(response.text, "html.parser")

    # 5. Znalezienie wszystkich elementów HTML, które zawierają pojedynczy cytat
    # Na tej stronie każdy cytat zamknięty jest w bloku: <div class="quote">
    quotes_list = soup.find_all("div", class_="quote")

    # 6. Iteracja po znalezionych elementach i wyciąganie szczegółów
    for index, quote_box in enumerate(quotes_list, start=1):
        # Wyciągnięcie tekstu cytatu (znajduje się w <span class="text">)
        text = quote_box.find("span", class_="text").get_text()

        # Wyciągnięcie autora (znajduje się w <small class="author">)
        author = quote_box.find("small", class_="author").get_text()

        print(f"{index}. \"{text}\" — Autor: {author}")
else:
    print(f"Błąd pobierania strony. Kod statusu: {response.status_code}")