# Biblioteka Numpy

Pakiet **NumPy** (_Numerical Python)_ - dostarcza podstawowych narzędzi do obliczeń numerycznych dla programistów języka Python. Większość pakietów naukowych i obliczeniowych korzysta z obiektów tablicowych NumPy jako uniwersalnego formatu wymiany danych.

Pakiet `numpy` zawiera m.in.:

* **`ndarray`** – wydajną implementację tablic wielowymiarowych, umożliwiającą szybkie wykonywanie operacji arytmetycznych i elastyczne _broadcasting_ (rozgłaszanie);
* **funkcje matematyczne** przeznaczone do wykonywania szybkich operacji na całych tablicach danych bez potrzeby używania pętli;
* **narzędzia do zapisu i odczytu danych tablicowych** z plików znajdujących się na dysku lub w mapowanym obszarze pamięci;
* **obsługę algebry liniowej, generowania liczb losowych i transformacji Fouriera**;
* **interfejs programistyczny C (API)** umożliwiający łączenie pakietu `numpy` z bibliotekami napisanymi w językach C, C++ lub Fortran.

Większość aplikacji związanych z analizą danych skupia się głównie na następujących możliwościach pakietu `numpy`:

* **szybkie operacje** wykonywane na wektoryzowanych tablicach, przydatne podczas obróbki i czyszczenia danych, a także m.in. podczas tworzenia podzbiorów, filtrowania i przekształcania danych;
* **standardowe algorytmy tablicowe**, takie jak sortowanie, wyszukiwanie elementów unikalnych oraz tworzenie zestawień;
* **wydajne generowanie parametrów statystycznych**, a także agregacja i podsumowywanie danych;
* **wyrównywanie danych i relacyjne operacje**, umożliwiające łączenie heterogenicznych zbiorów danych;
* **tworzenie logicznych operacji warunkowych** bezpośrednio na tablicach, bez potrzeby używania zagnieżdżonych instrukcji `if-elif-else`;
* **grupowe operacje na danych** – agregacja, transformacja i stosowanie funkcji.

Biblioteka `numpy` jest bardzo ważną biblioteką do obliczeń numerycznych w Pythonie między innymi dlatego, że została zaprojektowana z myślą o **wydajnym wykonywaniu obliczeń na dużych tablicach danych**. Wynika to m.in. z faktu, że:

* Wewnętrznie pakiet `numpy` przechowuje dane w **stykających się ze sobą blokach pamięci**, niezależnie od innych wbudowanych obiektów Pythona.
* Algorytmy pakietu `numpy`, napisane w języku C, mogą wykonywać operacje na tym obszarze pamięci bez sprawdzania typów i bez dodatkowego narzutu.
* Tablice `numpy` zajmują ponadto znacznie mniej pamięci niż wbudowane sekwencje Pythona.
* Operacje pakietu `numpy` mogą **przetwarzać całe tablice danych w sposób wektorowy**, bez potrzeby tworzenia w Pythonie pętli `for`, które są niewydajne w przypadku dużych zbiorów danych.

Funkcje `numpy` działają szybciej niż ich odpowiedniki napisane w czystym Pythonie, ponieważ są **zaimplementowane w języku C** i nie wprowadzają dodatkowego obciążenia typowego dla interpretowanego kodu

### Wprowadzenie i tworzenie tablic&#x20;

Aby rozpocząć pracę z pakiemtem `Numpy`, należy dodać go do środowiska pracy i wykonać import pakietu przez&#x20;

```python
import numpy as np
```

#### Tworzenie tablic (`ndarray`)

Najprostrzy sposób na tworzenie tablic obiektu ndarray (ang. _N-dimensional array_) jest wywołanie funkcji array(). Zwracany jest obiekt reprezentującą n-wymiarową tablicę. &#x20;

* wektor (dla n = 1)
* macierz (dla n > 1)

Jako argument do funkcji przekazujemy listę lub krotkę

```python
import numpy as np
v = np.array([-5, 6, 7, 8, 2, 1])
m = np.array([(2, 4, 6, 8),
            (12, 14, 16, 18),
            (22, 24, 26, 28)])
```

Innym sposobem na tworzenie obiektów klasy `ndarray` jest zastosowanie funkcji `arange()`&#x20;

```python
n = np.arange(0,40, 5)
```

Atrybuty określające pomocne przy określaniu wymiarów i kształtów tablic.

* `ndim` - zwraca wymiary macierzy
* `shape` - zwraca kształtu macierzy
* `size` - zwraca liczę elementów w macierzy

funkcja `len()` zwraca liczbę elementów z pierwszego wymiaru obiektu `ndarray`

```python
print("size\t shape\t len()")
print(f"{m.size}\t {m.shape}\t {len(m)}")
print("-"*25)
print(f"{v.size}\t {v.shape}\t {len(v)}")
```

Wynik

```
size	 shape	 len()
12		 (3, 4)	 3
-------------------------
6      (6,)    6
```



### Indeksowanie i wycinanie (scaling)



### Matematyka i wektoryzacja



### Zmiana kształtu i rozmiaru



### Zadania



### Literatura



