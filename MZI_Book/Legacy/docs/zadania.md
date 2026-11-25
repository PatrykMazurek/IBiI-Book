# Zadania

### Lab 2

{% file src=".gitbook/assets/Games.xlsx" %}

1. Korzystając z pliku Games.xlsx, wykonaj następujące zadania:
   1. Odczytaj plik i sprawdź, czy występują braki danych, a jeżeli tak, to w których kolumnach.
   2. Bazując na kolumnie `timePlay`, która jest typu tekstowego i ma format np. „60-120” lub „60”, stwórz dwie nowe kolumny numeryczne `minTime` i `maxTime`, które będą zawierać informacje o czasie gry. Wykorzystaj podział łańcuchów znaków (stringów) i konwersję na typ numeryczny. W przypadku gdy gra ma zdefiniowany tylko jeden czas, podaj w obu kolumnach tę samą wartość.
   3. Sprawdź, czy bardziej skomplikowane gry są lepiej oceniane. Pogrupuj gry (metoda `groupby()`) według zaokrąglonego poziomu trudności i oblicz średnią ocenę dla każdej grupy.
   4. Pogrupuj dane po kolumnie `year` i, korzystając z metody `agg()`, oblicz średni czas gry, średnią ocenę i średni poziom trudności. Wskaż, w którym roku powstały gry z najwyższym średnim poziomem trudności.
   5. Przeprowadź analizę najpopularniejszych kategorii. Kolumna `categories` zawiera po kilka kategorii oddzielonych przecinkami. Rozdziel je i, wykorzystując metodę `value_counts()`, sprawdź, jakie typy gier dominują w tym zestawieniu.
   6. Sprawdź, jak cena gry wpływa na liczbę graczy. Bazując na kolumnie `maxPlayer`, pogrupuj dane, a następnie oblicz medianę oraz średnią cenę (`price`), wykorzystując metodę `agg()`. Wskaż najtańsze i najdroższe gry.
   7. Przefiltruj dane tak, aby pozostawić te, dla których tytuł (`title`) zawiera litery „a” oraz „h”. Zapisz wynikowe dane do pliku w formacie JSON.

{% embed url="https://dane.gov.pl/pl/dataset/1963,nauczanie-domowe" %}

1. Korzystając z powyższego linku, rozwiąż następujące zadania:
   1. Pobierz pliki (w dowolnym formacie) z danymi o liczbie uczniów w nauczaniu domowym dla dwóch lat szkolnych: 2024/2025 i 2025/2026. Następnie wczytaj dane do obiektu `DataFrame` i sprawdź, czy nie występują w nich braki. Jeżeli tak, zwróć informację o tym, w jakich kolumnach się znajdują i jaka jest ich liczba.
   2. Pogrupuj dane po kolumnie `powiat` i zwróć 5 powiatów, w których występuje odpowiednio największa oraz najmniejsza liczba uczniów w nauczaniu domowym. Porównaj wyniki i sprawdź, czy występują różnice między rocznikami.
   3. Pogrupuj dane po kolumnie `typ obszaru` i wskaż, w którym obszarze znajduje się większa liczba rekordów. Porównaj wyniki i sprawdź, czy występują różnice między rocznikami.
   4. Wskaż, ile placówek nie posiada adresów WWW. Przedstaw dane dla obu roczników.
   5. Wskaż, ile placówek publicznych i niepublicznych (kolumna `Publiczność`) znajduje się w poszczególnych województwach. Przedstaw dane dla obu roczników.
   6. Dla każdego województwa oblicz medianę oraz maksymalną liczbę uczniów będących na nauczaniu domowym. Wykorzystaj do tego zadania metodę `agg()`. Przedstaw dane dla obu roczników.
   7. Sprawdź, ile placówek nie posiada adresu e-mail we własnej domenie, lecz korzysta z poczty w domenie ogólnej (np. gmail, wp itp.). Przedstaw dane dla obu roczników.

### Lab 3

1. **Wyszukiwarka autorska:** Napisz skrypt w Pythonie, który pobierze od użytkownika imię i nazwisko autora. Następnie przeszukaj stronę z cytatami (uwzględniając paginację), wyciągnij wyłącznie cytaty tego autora i wypisz je na ekranie. Jeśli autor nie występuje w bazie, wyświetl komunikat: _"Brak cytatów tego autora"_.
2. **Kategorie książek:** Korzystając ze strony [https://books.toscrape.com/](https://books.toscrape.com/), pobierz listę wszystkich dostępnych kategorii książek. Dla każdej kategorii sprawdź liczbę znajdujących się w niej pozycji, a wyniki zapisz w postaci tabelarycznej przy użyciu biblioteki `pandas` (`DataFrame`).
3. **Analiza cenowa:** Bazując na poprzednim zadaniu, wybierz 5 dowolnych kategorii, a następnie z każdej z nich pobierz 5 najdroższych książek. Dla każdej książki zwróć: tytuł, cenę, szczegółowy opis, kod UPC oraz liczbę dostępnych sztuk w magazynie.
4. **Logowanie do systemu testowego:** Serwis Web Scraper Test Sites udostępnia sekcję logowania pod adresem [https://webscraper.io/test-sites/website-state-setup-login](https://webscraper.io/test-sites/website-state-setup-login). Twoim zadaniem jest napisanie skryptu, który automatycznie przejdzie proces logowania (używając sesji i odpowiednich danych formularza), a następnie odczyta dane dostępne wyłącznie po zalogowaniu i zapisze je do pliku lokalnego.

### Lab 4

1. Korzystając ze strony [http://quotes.toscrape.com](http://quotes.toscrape.com) załaduj stronę i odczytaj sekcję "Top Ten Tags" znajdujący się po prawej stronie. Do pobrania tagów wykorzystaj `XPath`. Pobrane dane wyczyść z białych znaków i wyświetl w postaci ponumerowanej listy.
2. Napisz skrypt, któwy wejdzie na stronę [http://quotes.toscrape.com/login](http://quotes.toscrape.com/login) znajdzie pola do logowania. Uzupełnij pola "Username" oraz "Password" dowolnymi treściami i zatwierdź formularz. Dodaj odpowiedni warunek, który po przeładowaniu strony sprawdzi czy w prawym górnym rogu pojawił się link "logout". Jeżeli tak zwróć w konsoli komunikat o sukcesie.
3. Stwórz skrypt, który wjedzie na stronę [http://quotes.toscrape.com/js](http://quotes.toscrape.com/js) i odczyta dostępne cytaty. Cytaty nie są zawarte odrazu w kodzie HTML, ale są ładowane za pomocą JavaScript. Skorzystaj z modułu `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")` aby odczytać w pętli wszystkie skrypty. Użyj modułu `WebDriveWait` aby zaczekać na załadowanie nowych elementów. Po pobraniu wszystkich cytatów wyświetl tylko autorów cytatów.

### Lab 5

1. Korzystając z adresu `http://api.open-notify.org/iss-now.json`, stwórz aplikację, która co 10 sekund odpyta api i pobierz aktualną pozycję stacji ISS. Wyświetl użytkownikowi informacje o czasie i pozycji stacji.
2. Korzystając z adresu `https://api.nbp.pl/`, stwórz aplikację, która pobierze nazwy walut i ich kody z tabeli `B` i poprosi użytkownika o dwie informacje, którą walutę wyświetlić i ile ostatnich notowań. Następnie zapytaj odpowiedni endpoint, który zwróci notowania konkretnej waluty.
3. Korzystając z adresu `https://www.omdbapi.com/`, stwórz aplikację, która zwróci informacje w czytelny sposób. stwórz odpowiednie zapytania, aby wyszukiwać filmy po tytule lub po typie lub roku wydania filmu. W celu wykonania zadania można skorzystać z tego klucza api `d8ad4e9f`.
4. Korzystając z adresu `https://open-meteo.com/`, stwórz aplikację, która odczyta prognozę pogody na 3 dni. W informacji zwróć temperaturę i prędkość wiatru. Przygotuj 5 dowolnych lokalizacji i pozwól uzytkownikowi zdecydować, dla której lokalizacji ma pobrać pogodę. Nie kopiuj całych linków, tylko stwórz parametry i dodaj je w metodzie `request.GET()`. Wyniki przedstaw w czytelny sposób.

### Lab 6

1.  Stwórz aplikację, która będzie agregować informacje z trzech różnych kanałów RSS. W celu realizacji zadania zapoznaj się z biblioteką `feedparser`. Tematyka zbieranych informacji jest dowolna. Dla każdej wiadomości pobierz następujące informacje: tytuł artykułu, datę publikacji, link do artykułu, treść artykułu (opcjonalnie). Pobrane dane zapisz do pliku w formacie JSON. Aplikacja powinna automatycznie sprawdzać kanały RSS co 5 minut i zapisywać wyłącznie nowe wiadomości, unikając duplikowania wcześniej zapisanych danych.

    Linki do różnych źródeł:

    [Inkline](https://inklinenews.com/publications/cyberdefence24/), [Feeder](https://feeder.co/knowledge-base/rss-content/rss-lists-popular-and-useful-rss-feeds/?utm_source=chatgpt.com), [CheckRSS](https://checkrss.com/rss-feeds/news/?utm_source=chatgpt.com), [Oatmed.Feed](https://checkrss.com/rss-feeds/news/?utm_source=chatgpt.com)
2. Korzystając z kanałów RSS serwisu arXiv (`https://rss.arxiv.org/rss/`), stwórz aplikację, która będzie odczytywał informacje o publikacjach naukowych z wybranej kategorii tematycznej. Aby zapoznać się z dostępnymi kategoriami, skorzystaj ze strony [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy). Dla każdej publikacji pobierz następujące informacje: tytuł artykułu, listę autorów, link do artykułu, identyfikator DOI (jeżeli jest dostępny). W celu pozyskania informacji o autorach oraz identyfikatorze DOI przejdź na stronę danej publikacji i wykorzystaj technikę web scrapingu. Pobrane informacje wyświetl użytkownikowi w czytelnej formie.
3. Stwórz aplikację wspomagającą wyszukiwanie informacji, która może znaleźć zastosowanie np. w analizie otwartych źródeł informacji (OSINT). Wykorzystaj mechanizm wyszukiwania wiadomości za pośrednictwem kanałów RSS serwisu Google News. Przykładowy adres URL: `https://news.google.com/rss/search?q=sztuczna%20inteligencja%20when%3A1d&hl=pl&gl=PL&ceid=PL:pl` Przeanalizuj strukturę podanego adresu URL, a następnie zaimplementuj mechanizm jego dynamicznego generowania na podstawie parametrów wyszukiwania wprowadzonych przez użytkownika. Dla każdego wyniku wyszukiwania pobierz i wyświetl następujące informacje: tytuł artykułu, opis artykułu, link do artykułu, datę publikacji.
