# Zadania

### Lab 2

{% file src=".gitbook/assets/Games.xlsx" %}

1. korzystając z pliku Games.xlsx wykonaj następujące zadania:
   1. Odczytaj plik i sprawdź czy są baki danych a jeżeli tak to w których kolumnach.
   2. Bazując na kolumnie `timePlay`, która jest typu tekstowego i ma format np. "60-120" lub "60"  stwórz dwie nowe kolumny numeryczne `minTime` i `maxxTime`, które będą zawierać informacje o  czasie gry. Wykorzystaj podział stringów i konwersje na typ numeryczny. W przypadku kiedy gra będzie mieć tylko jeden czas podaj w obydwu kolumnach ten sam czas.
   3. Sprawdź, czy bardziej skomplikowane gry są lepiej oceniane. Pogrupować gry (`groupby()`) według zaokrąglonego poziomu trudności i wyciągnąć średnią ocenę dla każdej grupy.
   4. Pogrupuj po kolumnie `year` i korzystając z metody `agg()` oblicz średni czas gry, średnią ocenę i średni poziom trudności. Wskaż w którym roku powstały gry z najwyższym średnim poziomem trudności.&#x20;
   5. Analiza najpopularniejszych kategorii. Kolumna `categories` zawiera kilka kategorii oddzielonych przecinkami. Rozdziel kategorie i wykorzystując `value_count()`, sprawdz, jakie typy gier dominują w tym zestawieniu.
   6. Sprawdź jak cena gry wpływa na liczbę graczy. Bazując na kolumnie maxPlayer pogrupuj a następnie oblicz medianę oraz średnią cenę (`price`) wykorzystując metody `agg()`. Wskaż, które gry są najtańsze i najdroższe.
   7. Przefiltruj dane, dla których tytuł (`title`) zawiera literę "a" i "h", dane zapisz dodo pliku w formacie JSON.



{% embed url="https://dane.gov.pl/pl/dataset/1963,nauczanie-domowe" %}

1. Korzystając z powyższego linku rozwiąż następujące zadania:
   1. Pobierz pliki (dowolny format) z danymi o liczbie uczniów w nauczaniu domowym dla dwóch roczników 2024/2025 i 2025/2026. Następnie wczytaj dane do obiektu `DataFrame`, sprawdź czy nie występują braki w danych jeżeli tak to zwróć informacje w jakich kolumnach i ich liczbę.
   2. Pogrupuj dane po kolumnie `powiat` i zwróć 5 powiatów dla, których występuje największa oraz najmniejsza liczba uczniów w nauczaniu domowym. Porównaj roczniki i sprawdź czy są różnice między rocznikami.
   3. Pogrupuj po kolumnie `typ obszaru` i wskaż w którym obszarze jest większa liczba rekordów. Porównaj roczniki i sprawdź czy są różnice między rocznikami.
   4. Wskaż ile placówek nie posiada adresów www, dane przedstaw dla obydwu roczników.
   5. Wskaż ile placówek publicznych i niepublicznych (kolumna `Publiczność`) jest dla każdego województwa. Dane przedstaw dla każdego rocznika.
   6. Dla każdego województwa oblicz medianę oraz największą liczbę uczniów będących na nauczaniu domowym. wykorzystaj do tego zadania metodę `.agg()`. Dane przedstaw dla obydwu roczników.
   7. Sprawdź ile placówek nie posada adresu w swojej domenie tylko posiada pocztę w domenie ogólnej np. gmail, wp, itd. Dane wskaż dla obu roczników..
