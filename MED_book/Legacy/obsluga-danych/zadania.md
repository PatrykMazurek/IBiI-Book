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

### Lab 5

{% file src="../.gitbook/assets/HR.csv" %}

1. Kupiłeś szpulę filamentu o średnicy **1.75 mm** do swojej drukarki 3D. Chcesz zmierzyć, jak bliska jest rzeczywista średnica filamentu deklarowanej wartości. Za pomocą suwmiarki wykonujesz pięć pomiarów w różnych punktach na szpuli:\
   `1.78, 1.75, 1.72, 1.74, 1.77`. Oblicz średnią oraz odchylenie standardowe dla tego zbioru wartości.
2. Masz wątpliwości, czy filament do drukarki 3D rzeczywiście ma deklarowane $1.75 mm$ średnicy. Za pomocą suwmiarki wykonałeś $34$ pomiary. Średnia próby wynosi $1.715588$, a standardowe odchylenie próby $0.029252$.\
   Jaki jest $99$-procentowy przedział ufności dla średniej średnicy filamentu na całej szpuli?
3. Odczytaj plik _HR.csv_ i rozwiąż zadania z nim związane. Poszczególne kolumny oznaczają:

* `satisfaction_level` - poziom satysfakcji pracownika w skali od $0$ do $1$;
* `last_evaluation` - ocena pracownika w skali od $0$ do $1$;
* `number_project` - liczba projektów, w które zaangażowany był dany pracownik;
* `average_montly_hours` - średnia liczba godzin w miesiącu spędzona w biurze;
* `time_spend_company` - liczba lat spędzonych w firmie;
* `work_accident` - informacja, czy pracownik miał wypadek przy pracy (`1` - tak, `0` - nie);
* `left` - informacja, czy pracownik się zwolnił (`1` - tak, `0` - nie);
* `promotion_last_5years` - informacja, czy pracownik otrzymał awans w ciągu ostatnich pięciu lat (`1` - tak, `0` - nie);
* `sales` - dział zatrudnienia;
*   `salary` - wysokość zarobków (grupy).

    Zadania do wykonania

    1. Jaka jest minimalna i maksymalna ocena poziomu satysfakcji pracownika?
    2. Jaka jest średnia ocena pracownika, a jaka mediana?
    3. Ile jest/było pracowników w poszczególnych działach? Sporządź odpowiedni wykres słupkowy.
    4. Podaj liczbę pracowników, Którzy zwolnili się i jaki to jest procent danego działu?
    5. Podaj liczbę pracowników, kórzy otrzymali awans i jaki jest to procent danego działu?
    6. Wyznacz macierz korelacji dla kolumn ramki `hr` z uwzględnieniem zarobków (w tym celu dokonaj odpowiedniej konwersji danych kategorycznych na dane numeryczne). Utwórz odpowiednią mapę ciepła. Zrób to samo, ale osobno dla pracowników, którzy się zwolnili, oraz tych, którzy zostali.
    7. Zbadaj, czy istnieje związek między poziomem satysfakcji a tym, czy pracownik opuścił firmę. Wykonaj to na trzy sposoby:

    * zbadaj korelację między poziomem satysfakcji a decyzją o odejściu;
    * za pomocą testu t-Studenta oceń, czy istnieją statystycznie istotne różnice w poziomie satysfakcji między pracownikami, którzy się zwolnili, a tymi, którzy zostali.

    8. Czy wynagrodzenie wpływa na rotację pracowników? Sprawdź to na trzy sposoby:

    * za pomocą wizualizacji rozkładu wynagrodzenia w zależności od rotacji (wykres słupkowy);
    * za pomocą obliczania procentu pracowników, którzy odeszli, w różnych grupach płacowych;
    * za pomocą testu chi-kwadrat.

    9. Zbadaj, za pomocą testu t-Studenta - porównanie poziomu satysfakcji między pracownikami, którzy otrzymali awans, a tymi, którzy nie otrzymali.
    10. Dokonaj kategoryzacji oceny poziomu satysfakcji na 6 przedziałów: $\[0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0]$ nazwanych odpowiednio: `Lowest`, `Low`, `Average`, `Good`, `High`, `Highest`. Przedstaw na wykresie słupkowym liczbę pracowników, którzy się zwolnili i którzy się nie zwolnili, w zależności od skategoryzowanej oceny poziomu satysfakcji.

4. Korzystając ze zbioru `UNSW-NB15`, przeanalizuj i odpowiedz czy jest różnica między zwykłym ruchem sieciowym a atakami. Wczytaj dane i sprawdź czy występują puste dane (NaN), jeżeli tak to usuń rekordy.
   1. Oblicz liczebność ruchu prawidłowego (`label=0`) oraz ruchu związanego z atakami (`label=1`)
   2. Dla kolumny `sbytes` oblicz: średnią, medianę, odchylenie standardowe oraz zidentyfikuj wartości ekstremalne (minima i maksymalne)
   3. Przedstaw na histogramie wartości dla kolumny `sbytes` dla ruchu normalnego i ataków.
   4. Dodaj nową kolumnę `log_sbytes`, którą uzupełnisz w następujący sposób: `log_sbytes = np.log1p(sbytes)`. Przedstaw nową kolumnę na wykresie dla obydwu badanych grup.
   5. Wylosuj po 2000 rekordów z każdej z grup i przeprowadź dwustronny test t-studenta dla prób niezależnych dla zmiennej `lon_sbytes`. Sprawdź hipotezę czy czy sam wolumen przesłanych danych od źródła do celu jest wiarygodną metryką do budowy reguł detekcyjnych.

Pobranie materiałów do zajęć

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "UNSW_NB15_training-set.csv"

df = kagglehub.load_dataset(  KaggleDatasetAdapter.PANDAS,  "mrwellsdavid/unsw-nb15",  file_path,)

print("First 5 records:", df.head())
```

### Lab 6

{% file src="../.gitbook/assets/transakcje.csv" %}

{% file src="../.gitbook/assets/login.csv" %}

1. Odczytaj plik `login.csv` i podziel dane na dwa zbiory: uczący i testowy (80/20). Przy podziale nie zapomnij zastosować `stratify`. Wytrenuj klasyfikator drzew decyzyjnych i sprawdź jego działanie, obliczając wskaźniki: `Confusion matrix`, `Accuracy`, `Precision`, `Recall`. Możesz do tego zastosować funkcję `classification_report`. Zapoznaj się z metodą `plot_tree` lub `export_text` z pakietu `sklearn.tree` i przedstaw reguły wyuczone przez klasyfikator. Przy generowaniu tekstu lub wykresu nie zapomnij zastosować parametru `feature_names` z listą kolumn. Zidentyfikuj najdłuższą ścieżkę do liścia z decyzją "zablokowany". Wytrenuj ponownie model, zmieniając parametr `max_depth` na 2 i sprawdź, jak wpłynie to na czułość (`recall`) klasyfikatora.
2. Odczytaj dane z pliku `transakcje.csv` i przygotuj dane do trenowania lasów losowych. Po wytrenowaniu modelu przeanalizuj macierz pomyłek. Wyciągnij z wytrenowanego modelu wektor `feature_importances_` i stwórz wykres słupkowy pokazujący 3 najważniejsze cechy, którymi kierują się lasy losowe przy wykrywaniu oszustw.
3. Odczytaj dane ze zbioru `SMS Spam Collection Dataset`, sprawdź, czy występują braki w kolumnach `class` lub `sms` (pozostałe kolumny pomiń). Podziel dane na dwa zbiory: uczący i testowy (80/20). Przy podziale nie zapomnij zastosować `stratify`. Wytrenuj naiwny klasyfikator Bayesa, a następnie sprawdź jego skuteczność, wyświetlając macierz pomyłek. Spróbuj stworzyć swoje własne wiadomości, aby przetestować działanie klasyfikatora na realnych danych.

Skrypt do pobrania plików do zadania 3:

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = "spam.csv"

# Load the latest version
df = kagglehub.load_dataset( KaggleDatasetAdapter.PANDAS, "uciml/sms-spam-collection-dataset", file_path,)

print("First 5 records:", df.head())
```

### Lab 7 



1. Korzystając ze zbioru danych `UNSW-NB15_1.csv`, przygotuj dane do trenowania modelu `k-means`. W tym celu podziel zbiór na dwie części: treningową i testową. Ze zbioru treningowego wyfiltruj wyłącznie normalny ruch (`Label = 0`), a następnie usuń kolumny `Label`, `attack_cat` oraz pozostałe kolumny kategoryczne. Przeprowadź standaryzację cech (`StandardScaler`), dopasowując skaler na zbiorze treningowym.

    Wyznacz optymalną liczbę klastrów za pomocą metody łokcia (Elbow Method – wykres inercji) i zaprezentuj wyniki na wykresie. Następnie wytrenuj model `k-means` dla wybranej liczby klastrów. Po wytrenowaniu modelu wyznacz próg alarmowy jako 95. procent odległości punktów ze zbioru treningowego od ich najbliższych centroidów.
2. 
    Przygotuj zbiór testowy w analogiczny sposób (usuń kolumny kategoryczne, odetnij `Label` i `attack_cat` na czas predykcji oraz zastosuj wcześniej dopasowany `StandardScaler`). Przeprowadź predykcję na zbiorze testowym i oceń wyniki, porównując je z rzeczywistymi etykietami. Przedstaw macierz pomyłek i metryki Precision, Recall, F1-score. 

2. Wczytaj dane treningowe i testowe z pliku xyz.zip, zawierającego informacje o incydentach IDS. Porównaj działanie klasyfikatorów k-NN, Random Forest oraz Naive Bayes. Zestaw ze sobą czas uczenia, czas predykcji oraz metryki klasyfikacji: Accuracy, F1-score i Recall. Na podstawie uzyskanych wyników oraz czasu działania wskaż najlepszy algorytm. Przedstaw na wykresach macierz pomyłek dla każdego modelu oraz porównanie czasów uczenia i predykcji. 

#### Skrypt do zadania 1
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "UNSW-NB15_1.csv"
file_path_head = "NUSW-NB15_features.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS, "harshwardhanbhangale/unsw-complete-dataset", file_path,)

print("First 5 records:", df.head())

df_head = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS, "harshwardhanbhangale/unsw-complete-dataset",
    file_path_head,
   pandas_kwargs={"encoding": "cp1252"})

df.columns = df_head['Name'].tolist()
```