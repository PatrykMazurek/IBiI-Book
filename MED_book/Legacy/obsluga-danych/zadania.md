# Zadania

### Lab 2

Korzystając z pliku:

{% file src="../.gitbook/assets/HPC_2k.log_structured.csv" %}

Rozwiąż następujące zadania:

1. Konwersja czasu - kolumna `Time` zawiera czas w formacie UNIX Timestamp (liczba sekund od 1 stycznia 1970 r.). Stwórz nową kolumnę `Datetime`, konwertując wartości z kolumny `Time` na obiekt daty i czasu. Wyodrębnij godzinę z nowej kolumny do zmiennej `Hour`. Oblicz liczbę logów wygenerowanych w poszczególnych godzinach i zidentyfikuj okno czasowe z największą aktywnością systemu.
2. Identyfikacja najbardziej awaryjnego węzła - Klaster obliczeniowy składa się z wielu maszyn (węzłów). Należy ustalić, które z nich wymagają największej uwagi administratorów. Zgrupuj dane według kolumny `Node`. Policz całkowitą liczbę wystąpień dla każdego węzła. Posortuj wyniki malejąco i wyodrębnij 5 maszyn, które wygenerowały najwięcej zdarzeń w badanym okresie.
3. Identyfikacja stanów systemu - Kolumna `State` przechowuje informacje o statusie danego zdarzenia w klastrze. Zidentyfikuj wszystkie unikalne wartości występujące w kolumnie `State`. Oblicz procentowy udział każdego ze stanów w stosunku do wszystkich 2000 logów. Przedstaw wyniki z dokładnością do dwóch miejsc po przecinku (np. 45.50%), aby sprawdzić, czy dominują rutynowe komunikaty, czy zmiany stanu na niedostępny.

Korzystając z pliku:

{% file src="../.gitbook/assets/OpenSSH_2k.log" %}

Rozwiąż zadania:

1. Korzystając z biblioteki `pygrok`, `parse`, `re` lub innej dowolnej, przenieś plik z logami do obiektu `DataFrame`, a treść logu zapisz do kolumny `msg`.
2. Bazując na ramce danych z zadania 1, sprawdź, w ilu rekordach występują wartości puste (`None`).
3. Przygotuj zestawienie liczby logów wygenerowanych przez poszczególne procesy (np. `sshd`, `ftpd`, `su`).
4. Na bazie przygotowanego wcześniej `DataFrame`, przekonwertuj kolumnę z datą i czasem ze zwykłego tekstu na typ `datetime` (w pliku nie podano roku, wstaw rok 2025).
5. Wykorzystując dowolną bibliotekę (`pygrok`, `parse`, `re`), wyciągnij z kolumny `msg` informacje o adresie IP i nazwie użytkownika dla komunikatów, które zawierają "Failed password" oraz "Invalid user".
6. Korzystając z metod filtracji i grupowania, zastosuj je do zidentyfikowania i wyświetlenia zestawienia top 5 adresów IP generujących najwięcej błędów uwierzytelniania oraz top 5 najczęściej atakowanych nazw użytkowników (np. `root`, `admin`). Wyniki wyeksportuj do pliku `JSON`.

### Lab 3

{% file src="../.gitbook/assets/ssl.csv" %}

Rozwiąż następujące zadania:

1. Narysuj koło o środku w punkcie (0,0) i promieniu 2. Powinno być ono wypełnione półprzezroczystą barwą zieloną, mieć wyraźnie zaznaczony brzeg i nie wyglądać jak elipsa.
2. Korzystając z pakietu `seaborn` i danych `tips`, narysuj wykresy:
   1. Dwa wykresy (kołowy i słupkowy), które będą podsumowywać zmienną `smoker`.
   2. Utwórz wykres skrzynkowy dla procentowego udziału napiwku w całkowitej wartości rachunku w rozbiciu na podgrupy generowane przez kombinacje `sex` i `day`.
   3. Utwórz wykres skrzynkowy dla procentowego udziału napiwku w całkowitej wartości rachunku na podstawie ramki danych `tips`.
3. Korzystając z pliku `ssl.csv`, wykonaj następujące zadania:
   1. Odczytaj dane z kolumny `cipher` i zidentyfikuj najczęściej używane algorytmy szyfrujące. Dane przedstaw na wykresie i odpowiedz, czy najpopularniejszy algorytm jest bezpiecznym rozwiązaniem.
   2. Bazując na danych z pliku i kolumnie `source_ip`, wyszukaj stacje robocze lub serwery generujące największy ruch SSL. Przedstaw na wykresie 6 najaktywniejszych urządzeń.
   3. Kolumna `certificate_validation_status` zawiera dane o certyfikatach. Przedstaw na wykresie kołowym informacje zawarte w tej kolumnie. Sprawdź, jaki rodzaj certyfikatu występuje najczęściej. W kolumnie może wystąpić znak "`-`", co oznacza brak danych o certyfikacie; takie informacje również zamieść na wykresie.
   4. Kolumna `timestamp_unix` zawiera znacznik czasowy. Przekonwertuj ją na czas i policz, ile połączeń występuje w każdej godzinie. Wyniki przedstaw na wykresie liniowym.

Dla każdego wykresu opisz osie, nadaj tytuł wykresu oraz legendę.

### Lab 4

1. Wczytaj dane z pliku `ds_salaries.csv`, a następnie oblicz średnią arytmetyczną i medianę dla kolumny `salary_in_usd`. Zidentyfikuj wartości odstające na podstawie odchylenia standardowego i odfiltruj rekordy, których wartość przekracza 3-krotność odchylenia standardowego od średniej. Na wykresie pudełkowym narysuj rozkład dla kolumny `salary_in_usd` przed i po filtracji.
2. Wczytaj dane z pliku `googleplaystore.csv`, który zawiera informacje o aplikacjach w sklepie Google Play. Na początku sprawdź, czy w kolumnie `Rating` występują puste rekordy (braki danych) – jeżeli tak, to je usuń. Następnie na podstawie kolumny `Rating` oblicz dominantę i narysuj histogram ocen. 
3. Wczytaj dane z pliku `KAG_energydata_complete.csv`. Sprawdź, czy nie występują braki danych w kolumnach od `T1` do `T9` – jeżeli wystąpią, usuń wybrakowane rekordy. Następnie przeanalizuj temperatury i oblicz wariancję oraz odchylenie standardowe dla każdego pomieszczenia, wskazując, które z nich charakteryzuje się najbardziej stabilną temperaturą. Korzystając z histogramów, przedstaw rozkład temperatur na wykresie.
4. Korzystając ze zbioru NYC Taxis (`taxis`) wbudowanego w bibliotekę `seaborn`, załaduj dane do ramki danych. Sprawdź, czy w kolumnie `distance` występują braki danych oraz wartości nietypowe (kursy o ujemnej lub zerowej długości). Jeśli takie występują, usuń te rekordy. Oblicz wartości kurtozy i skośności dla kolumny `distance`. Następnie dodaj nową kolumnę o nazwie `distance_log`, którą uzupełnisz zlogarytmowaną wartością dystansu w tym celu zastosuj funkcję `np.log1p(df["distance"])`. Przygotuj wykresy gęstości dla kolumn `distance` oraz `distance_log`. Aby to zrobić, zapoznaj się z wykresem KDE (Kernel Density Estimation) dostępnym w bibliotece `seaborn`.

Pliki do zadań 1-3 można pobrać za pomocą następujących skryptów:

**Zadania 1**

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "ds_salaries.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "ruchi798/data-science-job-salaries",
  file_path,
)
```

**Zadanie 2**

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "googleplaystore.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "lava18/google-play-store-apps",
  file_path,
)
```
**Zadanie 3**
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "KAG_energydata_complete.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "loveall/appliances-energy-prediction",
  file_path,)
```