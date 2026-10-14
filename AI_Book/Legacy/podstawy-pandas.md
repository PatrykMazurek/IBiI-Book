# Podstawy Pandas

#### Rozpoczęcie pracy z palietem Pandas

Pakiet pandas nie jest domyślnie zaimplementowane w środwisko Pytno, należ go zaistalować&#x20;

```bash
pip install pandas
```

Po instalacji pakitu pandas możemy z niego skorzystać przez zaimportowanie biblioteki do plików w języku Python

```python
import pandas as pd
```



w sytuacji kiedy studenci nie pracowali z Pandas&#x20;

podstawy, tworzenie ramek danych,&#x20;

Bibliotek Pandas opiera się na dwóch podstawowych strukturach:

* **Series** - jednowymiarowa tablica z indeksami pozwalająca na przechowanie obiektów dowolnego typu np. liczby całkowite, zmiennoprzecinkowe, ciągi znakowe czy obiekty.
* **DataFrame** - dwuwymiarowa struktura przechowywująca dane różnego typu, uporządkowana w kolumny i wiersz.

#### Series

Tworzenie obiektów Series możemy wykonać na kilka różach sposobów, najpopularniejszym jest utworzenie listy z obiektami i przekazanie jej do konstruktora obiektu Series (przykład poniżej)

```python
data = pd.Series( 
    [10, 20, 30],
)
print(data)
```

W wyniku otrzymamy następujące informacje w pierwszej komunie indeksy, w drugiej wartości a na samym końcu&#x20;

```
0    10
1    20
2    30
dtype: int64
```

Można zdefiniować włąsne indeksy&#x20;

```python
data = pd.Series(
    [10, 20, 30],
    index=["a", "b", "c"]
)
print(data)
```

W wyniku działani skryptu zamiast numeracni otrzymamy "a", "b", "c" jako etykiety elementów.

```
a    10
b    20
c    30
dtype: int64
```

Kolejnym sposobem na tworzenie obietów Series jest zastosowanie słowników&#x20;

```python
dane = {
    "Polska": 38,
    "Niemcy": 84,
    "Francja": 68
}
populacja = pd.Series(dane)
print(populacja)
```

W wyniku działania skryptu otrzymamy nowy obiekt Series, w którym eytkietom jest klucz ze słownika a wartością jest wartość ze słownika.

```
Polska     38
Niemcy     84
Francja    68
dtype: int64
```

**Pobieranie elementu**&#x20;

Dysponując pewnym obiektem:

```python
s = pd.Series(
    [100, 200, 300],
    index=["a", "b", "c"]
)
```

Najpopularniejsze metody do pobierania elementów z obiektu Series są:&#x20;

* `.loc` - **na podstawie etykiety ideksu**

```python
print(s.loc["b"])
```

Wynik

```
200
```

* `.iloc` **- na podstawie pozycji**

```python
print(s.iloc[0])
```

Wynik:

```
100
```

**Dodanie nowego elementu**

Dodanie nowego elementu możemy wykonać przez dopisanie wartości do nieistniejącego indeksu&#x20;

```python
s.loc["d"] = 40
print(s)
```

Wynik otrzymamy obiekt Series z nowym indeksem "d" o wartości 40

```
a    10
b    20
c    30
d    40
dtype: int64
```

**Aktualizacja pojedynczego elementu**

Załóżmy że będziemy edytować element "c" z wartość 30 na 300 jest na kilka sposobów:

* Na podstawie etykiety indeksu (`.loc`)

```python
s.loc["c"] = 300
print(s)
```

Wynik:

```
a     10
b     20
c     300
d     40
dtype: int64
```

* Na podstawie pozycji elementu (`.iloc`)

```python
s.iloc[1] = 200
print(s)
```

Wynik

```
a     10
b     200
c     300
d     40
dtype: int64
```



**Aktualizacja kilku elementów**&#x20;

**Aktualizacja na podstawie warunków**

**Usuwanie elementu `.drop()`**



aktualizować, dodawać, usuwać wartości z Series&#x20;

#### DataFrame

jak tworzyć obiekty Series

Jak można je wyświelić

aktualizować, dodawać, usuwać wartości z DataFrame

#### Zadania

#### Literatura dodatkowa

{% embed url="https://www.geeksforgeeks.org/pandas/introduction-to-pandas-in-python/" %}

{% embed url="https://www.programiz.com/python-programming/pandas/introduction" %}

{% embed url="https://www.w3schools.com/python/pandas/default.asp" %}

{% embed url="https://pandas.pydata.org/docs/user_guide/10min.html" %}
