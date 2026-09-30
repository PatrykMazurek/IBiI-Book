# Biblioteka Pandas

Biblioteka Pandas to podstawa analizy danych w języku Python. Biblioteka, które pozwala na łatwe wczytanie danych, czyszczenie i raportowanie.&#x20;

Najważniejszą strukturą w Pandas jest Data Frame (ramka danych). Jest to dwu-wymiarowa tablica, która ma etykiety osi (indeksy wierszy oraz nazwy kolumn). Zaletami ramki danych jest elestyczność co do typów danych, które są przechowywane w strukturze. Każda kolumna może przechowywać inny typ np. tekst, liczby zmiennoprzecinkowe czy datę.&#x20;

Na początek należy importować biblioteki:

```python
import numpy as np
import pandas as pd
```

#### Tworzenie Ramek Danych

Aby rozpocząć pracę z przetwarzaniem danych w Pandas należy utworzyć obietk klasy `Pandas.Core.DataFrame`, w tym celu należy wywłoać konstruktor `DataFrame()`. Konstruktor można wywołać bez argumentów lub jeżeli ramka danych ma zostać wypełniona danymi to parametr data moąn przekazać słowni, listę list, tablice dwuwymiarową NumPy, obkeity klasy Series lub inne ramki danych.

**Tworzenie ramek ze słowników**

Przekazująć do konstruktora klasy DataFrame słownik, możemy stworzyć ramke danych, w któej nazwy kolumn będą odpowiadać kluczom ze słownika.

```python
data = {
    'Uzytkownik': ['Anna', 'Bartek', 'Celina'],
    'Wiek': [28, 34, 22],
    'Wydano_PLN': [120.50, 450.00, 89.90]
}

df = pd.DataFrame(data)
print(df[df['Wydano_PLN'] > 100])
```

Wynik



**Tworzenie ramek z list**

Kiedy przekazujemy do konstruktora listę lub tablice dwuwymiarową wtedy nazwy kolumn są generowane automatycznie, jest możliwość nadania nazw kolumn stosując parametr columns, w którym podajemy nazwy kolumn.

```python
matrix = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

# Przekazujemy macierz i definiujemy nazwy kolumn oraz indeksy
df_matrix = pd.DataFrame(
    data=matrix,
    columns=['Kolumna_A', 'Kolumna_B', 'Kolumna_C']
)

print(df_matrix)
```

Wynik

```
```

**Tworzenie ramek z innych źróde**

Kolejnym sposobom stworzenia ramki danych jest załadaowanie danuch z źródeł zewnętrznych, Takim przykładem jset Pakiet Seaborn, który zawiera zbiory danych przydatne do samodzielego cwiczenia analizy danych, tworzenia wykresów, mapciepła, itp. Aby załadować dane możemy skorzystać z funkcji `load_dataset()`.  Przykład zastosowania:

```python
import seaborn as sns
flights = sns.load_dataset('flights')
tips = sns.load_dataset('tips')
iris = sns.load_dataset('iris')
```

Link do pakietu seaborn i dostępnych zborów danych zamieszczony jest literaturze

**Tworzenie ramek danych z plików**

Częstym przypadkiem jest ładowanie danych zapisanych w pliku. Pakiet Pandas zawiera kilka funkcji ułatwiających wczytanie danych z różnych formatów. Przykłąd wycztania danych:

```python
csv_df = pd.read_csv("data.csv")
json_df = pd.read_json("data.json")
xml_df =  pd.read_xml("data.xml")
```

Podstawowym argumentem w funkcji pd.read\_xxx() jest podanie ścieżki do pliku. Dodatkowe opcjonalne parametry zależne są od formatu pliku, który jest wczytywany.&#x20;

Dodatkowo pakiet Pandas pozwala na pobieranie danych ze stron internetowych (ang. _web scraping_) i konwertowania danych tabelarycznych do formatu ramek danych. Pakiet Pandas zawiera funkcje pozwalające na importowanie i eksportowanie danych z/do SQL.

#### Odczytywanie informacji o ramkach danych

Niezależnie od tego w jaki sposób została stworzony obiekt typu DataFrame, jest kilka metod, które pozwalają na pozyskani informacji na temat struktury oraz danych zapisanych w ramce danych.

**Rozmiar ramki danych**

Podstawowym sposobem na sprawdzenie wymiarów ramki danych jest atrybut `shape`, który zwraca liczbę wierszy i kolumn. Atrybut `size` zwróci liczbę elementów w race danych, a zastosowanie funkcji `len()` zwróci liczbę wierszy w ramce danych.

```python
flights.shape, flights.size, len(flights)
```

**Informacje o danych w kolumnach**

Obiekty DataFrame mogą przechowywać różnego typu dane w kolumnach, atrybut `dtypes` zwraca informacje o typach przechowywanych w kolumnach.

```python
flights.dtypes
```

wynik

```
year             int64
month         category
passengers       int64
dtype: object
```

W celu uzyskania nieco dokładniejszych informacji o obiekcie, typie zminnych (kolumn), liczbie elementów i zajmowanej przestrzeni w pamici&#x20;

```
flights.info()
```

wynik

```
<class 'pandas.DataFrame'>
RangeIndex: 144 entries, 0 to 143
Data columns (total 3 columns):
 #   Column      Non-Null Count  Dtype   
---  ------      --------------  -----   
 0   year        144 non-null    int64   
 1   month       144 non-null    category
 2   passengers  144 non-null    int64   
dtypes: category(1), int64(2)
memory usage: 2.9 KB
```

**Wyświetlanie zawartości ramek danych**

Podstawowa pętla for po ramce danych iteruje ni po każdym wierszu ale kolumnach wyświetlając nazwy kolumn&#x20;

```python
for f in flight:
    print(f)
```



### Literatura

{% embed url="https://pandas.pydata.org/" %}

{% embed url="https://seaborn.pydata.org/" %}
