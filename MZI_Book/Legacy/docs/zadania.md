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

1. **Wyszukiwarka autorska:** Napisz skrypt w Pythonie, który pobierze od użytkownika imię i nazwisko autora. Następnie przeszukaj stronę z cytatami (uwzględniając paginację), wyciągnij wyłącznie cytaty tego autora i wypisz je na ekranie. Jeśli autor nie występuje w bazie, wyświetl komunikat: *"Brak cytatów tego autora"*.
2. **Kategorie książek:** Korzystając ze strony [https://books.toscrape.com/](https://books.toscrape.com/), pobierz listę wszystkich dostępnych kategorii książek. Dla każdej kategorii sprawdź liczbę znajdujących się w niej pozycji, a wyniki zapisz w postaci tabelarycznej przy użyciu biblioteki `pandas` (`DataFrame`).
3. **Analiza cenowa:** Bazując na poprzednim zadaniu, wybierz 5 dowolnych kategorii, a następnie z każdej z nich pobierz 5 najdroższych książek. Dla każdej książki zwróć: tytuł, cenę, szczegółowy opis, kod UPC oraz liczbę dostępnych sztuk w magazynie.
4. **Logowanie do systemu testowego:** Serwis Web Scraper Test Sites udostępnia sekcję logowania pod adresem [https://webscraper.io/test-sites/website-state-setup-login](https://webscraper.io/test-sites/website-state-setup-login). Twoim zadaniem jest napisanie skryptu, który automatycznie przejdzie proces logowania (używając sesji i odpowiednich danych formularza), a następnie odczyta dane dostępne wyłącznie po zalogowaniu i zapisze je do pliku lokalnego.