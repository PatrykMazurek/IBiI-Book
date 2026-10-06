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

Aby rozpocząć pracę z pakietem `Numpy`, należy dodać go do środowiska pracy i wykonać import pakietu przez&#x20;

```python
import numpy as np
```

#### Tworzenie tablic (`ndarray`)

Najprostszy sposób na tworzenie tablic obiektu `ndarray` (ang. _N-dimensional array_) jest wywołanie funkcji `array()`. Zwracany jest obiekt reprezentującą n-wymiarową tablicę. &#x20;

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

#### Typy przechowywanych elementów

Tablice w pakiecie Numpy są dość wrażliwe na przechowywanie elementów, głownie przechowywują jeden typ na cały obiekt ndarray. Abys sprawdzić jakiego typu obiekty są przechowywane w tablicy możemy odwołać się do atrybutu `dtype` lub `dtype.name`.&#x20;

```python
print(f"dtype = {np.array([3,6,3,50]).dtype}")
print(f"dtype.name = {np.array([3.0, 0.6, 0.6, 5.1, 8.4]).dtype.name}")
print(f"dtype = {np.array(["Warszawa", "Kraków", "Katowice"]).dtype}")
print(f"dtype.name = {np.array(["Warszawa", "Kraków", "Katowice", "Radom"]).dtype.name}")
```

Wynik

```
dtype = int64
dtype.name = float64
dtype = str256
dtype.name = str256
```

Przykładowo, typy `int64` oraz `float64` **nie są klasami języka Python**, tzn. nie są równoważne typom wbudowanym `int` i `float`. Są to **typy wykorzystywane wewnętrznie przez pakiet `numpy`** do reprezentowania danych liczbowych - odwzorowywane bezpośrednio na typy języka C.

Interfejs pomiędzy tymi konkretnymi reprezentacjami typu `dtype` a językiem Python zapewniają odpowiednie klasy NumPy, np. `np.int64` oraz `np.float64`.

Przykładowa typy danych w pakiecie Numpy

| `int8`, `uint8`   | `'i1'`, `'u1'`   | $$8$$ bitowa liczba całkowita ($$1$$ bajt) ze znakiem lub bez                                                                                                                                                                                  |
| ----------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `int16`, `uint16` | `'i2'`, `'u2'`   | $$16$$-bitowa liczba całkowita ze znakiem lub bez                                                                                                                                                                                              |
| `int32`, `uint32` | `'i4'`, `'u4'`   | $$32$$-bitowa liczba całkowita ze znakiem lub bez                                                                                                                                                                                              |
| `int64`, `uint64` | `'i8'`, `'u8'`   | $$64$$-bitowa liczba całkowita ze znakiem lub bez                                                                                                                                                                                              |
| `float16`         | `'f2'`           | liczba zmiennoprzecinkowa o połowicznej precyzji                                                                                                                                                                                               |
| `float32`         | `'f4'` lub `'f'` | <p>standardowa liczba zmiennoprzecinkowa o pojedynczej precyzji,<br>kompatybilna ze zmienną typu <code>float</code> języka C</p>                                                                                                               |
| `float128`        | `f16` lub `g`    | liczba zmiennoprzecinkowa o rozszerzonej precyzji                                                                                                                                                                                              |
| `bool_`           | `'?'`            | wartości logiczne `True` lub `False`                                                                                                                                                                                                           |
| `object_`         | `'O'`            | typ obiektu języka Python, wartość może być dowolnym obiektem języka Python                                                                                                                                                                    |
| `string_`         | `'S'`            | <p>łańcuch znaków ASCII o określonej długości (każdy znak zajmuje <span class="math">1</span> bajt pamięci);<br>w celu utworzenia łańcucha o długości równej <span class="math">10</span> należy skorzystać z typu danych <code>s10</code></p> |
| `unicode_`        | `'U'`            | <p>łańcuch znaków Unicode o określonej długości (liczba bajtów zależy od platformy);<br>semantyka specyfikacji jest identyczna jak w przypadku typu <code>string_</code> (np. <code>u10</code>)</p>                                            |

Listę najważniejszych typów wewnętrznych `numpy` można poznać, analizując zawartość obiektu `np.sctypeDict`.&#x20;

Do zmiany typu już utworzonego obiektu możemy zastosować funkcję `astype()`, podając obiekt i typ na, który chcemy zmodyfikować obiekt.

```python
print(f"typ = {n.dtype} : {n}")
n = np.astype(n, np.float16)
print(f"typ = {n.dtype} : {n}")
```

Wynik

```
typ = int64 : [ 0  5 10 15 20 25 30 35]
typ = float16 : [ 0.  5. 10. 15. 20. 25. 30. 35.]
```

Pakiet Numpy jest restrykcyjny co do przechowywanych typów w tablicach. Jest możliwość aby w macierzy przechowywać różne typy danych i wymaga to konwersji do ogólnego typu jakim jest `object`, wykonać to można w następujący sposób.

```python
m1 = np.array([2,'kot', 5.6, True, [1,2]], dtype=np.object_)
```

Wynik

```
[2 'kot' 5.6 True list([1, 2])]
```

#### Tworzenie tablic specjalnych&#x20;

**Ciąg arytmetyczny o:**&#x20;

* **zadanych przyrostach -** Ciąg liczb zawartych w przedziale $$[a,b)$$ i różnicach równych $$k$$ utworzymy, wywołując `arange(a, b, k)` .
* **zadanej długości -** W celu utworzenia ciągu arytmetycznego złożonego z wartości z przedziału $$[a,b]$$ i długości $$d$$ możemy posłużyć się wywołaniem `linspace(a, b, d)`, np.:

**Macierze:**

* **jedn9ostkowa i inne diagonalne -** Macierz jednostkową, tzn. macierz o wartościach równych $$0$$ poza główną przekątną oraz $$1$$ na głównej przekątnej otrzymujemy przy użyciu `eye()`. Jeżeli chodzi o wartości na głównej przekątnej to bardziej ogólnie będzie działać funkcja `diag()`.

```python
np.eye(6)
np.eye(3, 3, dtype = np.bool_)
np.diag([11,12,13])
```

Wynik

```
[[1. 0. 0. 0. 0. 0.]
 [0. 1. 0. 0. 0. 0.]
 [0. 0. 1. 0. 0. 0.]
 [0. 0. 0. 1. 0. 0.]
 [0. 0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 0. 1.]]
---------------
[[ True False False]
 [False  True False]
 [False False  True]]
---------------
[[11  0  0]
 [ 0 12  0]
 [ 0  0 13]]
```

**Tablice**

* **wypełnione jednykami lub zerami -** Funkcja `zeros()` tworzy tablicę zer o podanym kształcie, a funkcja `ones()` tablice jedynek o zadanym kształcie.
* **niezainicjalizowane -** Funkcja `empty()` utworzy tablicę w której znajdują się przypadkowe dane - elementy nie są w cale inicjowane. Dzięki tej funkcji mamy najszybszy sposób tworzenia tablicy o zadanym kształcie.
* **wypełnione elemenetami pseudolosowymi** - Pakiet `numpy` pozwala na generowanie wartości pseudolosowych z szerokiej gamy rozkładów dostępnych w module random.&#x20;



### Indeksowanie i wycinanie (scaling)

W NumPy mamy cztery główne sposoby dobierania się do danych: klasyczny slicing (jak w listach), indeksowanie wielowymiarowe, indeksowanie logiczne (maski) oraz tzw. _fancy indexing_.

#### Podstawowe wycinanie

Działa to dokładnie tak samo jak w standardowych listach w Pythonie, ale z jedną gigantyczną przewagą: możemy to robić dla wielu wymiarów jednocześnie.

Ogłlny schemta dla tablicy 1D: **tablica\[start : stop : krok]**

```python
arr = np.arange(10) 

print(arr[2:6])
print(arr[:4])
print(arr[1:8:2])
print(arr[::-1])
```

wynik

```
[2 3 4 5]
---------------
[0 1 2 3]
---------------
[1 3 5 7]
---------------
[9 8 7 6 5 4 3 2 1 0]
```

Ogłlny schemta dla tablicy 2D: **tablica\[wiesz, kolumna]**

```python
arr2d = np.array([
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12]
])

print(arr2d[0:2, 1:]) 
print(arr2d[:, 2])
```

wynik

```
[[2 3 4]
 [6 7 8]]
---------------
[ 3  7 11]
```

#### Indeksowanie logiczne

To jedna z najczęściej wykorzystwanych technik w analizie danych (np. w bibliotece Pandas). Pozwala na filtrowanie tablicy na podstawie warunku. Nie korzystamy zindeksów, ale tworzymy "maskę" z wartości `True` i `False`.

```python
arr = np.array([10, 15, 20, 25, 30])

print(arr[arr > 15])
```

Wynik

```
[20 25 30]
```

Jest też możłiwość łączenia warunków używając operatorów & (AND) oraz | (or), każdy warunek powinien znaleść się w nawiasach.

```python
print(arr[(arr > 15) & (arr < 30)])
```

wynik

```
[20 25]
```

#### Fancy Indexing (Indeksowanie tablicami)

Czasami wymagane jest wyciągnięcie konkretnych wierszy lub elementów w określonej kolejności, które nie układają się w równy schemat (jak w slicingu). Możemy podać listę pożądanych indeksów.

```python
arr_names = np.array(['Kasia', 'Tomek', 'Ania', 'Piotr', 'Zosia'])

indeksy = [0, 3, 4]
print(arr_names[indeksy]) 
```

wynik

```
['Kasia' 'Piotr' 'Zosia']
```

### Matematyka i wektoryzacja

**Podstawowa arytmetyka**&#x20;

Pakiet Numpy pozwala na łatwe stosowanie znaków matematycznych między tablicami.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)
print(a * b)
print(a ** 2)
```

wynik

```
[11 22 33]
[10 40 90]
[1 4 9]
```

Dodatkowo pakiet Numpy posada wbudowaną całą bibliotekę zaawansowaną gotową do pracy na wektorach.

```python
x = np.array([0, np.pi/2, np.pi])

print(np.sin(x))
print(np.exp(x))
print(np.sqrt(a))
```

wynik

```
[0.0000000e+00 1.0000000e+00 1.2246468e-16]
[ 1.          4.81047738 23.14069263]
[1.         1.41421356 1.73205081]
```

Kiedy mamy macierz, nie zawsze wymagane jest sumowanie wszystkich elmentów, tylko wystarczy że wyciągnięte zostaną wnioski dla poszczególnych kolumn lub wierszy. Do tego służy parametr `axis` (oś).

* Brak `axis`: sumuje wszystko do jednej liczby.
* `axis=0`: "Zwiń" osie pionowe (wiersze). Sumujesz w dół kolumn. Zwraca wynik dla każdej kolumny.
* `axis=1`: "Zwiń" osie poziome (kolumny). Sumujesz w poprzek wierszy. Zwraca wynik dla każdego wiersza.

```python
oceny = np.array([
    [4, 5, 3, 5],  # Uczeń 0
    [2, 3, 4, 3],  # Uczeń 1
    [5, 5, 5, 4]   # Uczeń 2
])

# 1. Jaka jest średnia z CAŁEJ klasy ze wszystkich przedmiotów?
srednia_ogolna = np.mean(oceny) 

# 2. Jakie są średnie z poszczególnych PRZEDMIOTÓW?

srednia_przedmioty = np.mean(oceny, axis=0)

# 3. Jakie są średnie na koniec roku poszczególnych UCZNIÓW?
srednia_uczniowie = np.mean(oceny, axis=1)
```

wynik

```
4.0
[3.66666667 4.33333333 4.         4.        ]
[4.25 3.   4.75]
```

Poza podstawowymi operacjami typu `+`, `-`, `*`, `/` czy ufuncs (jak `np.sin()`), NumPy oferuje dedykowane narzędzia do algebry liniowej, statystyki i zaawansowanego sterowania przepływem danych za pomocą logiki.



