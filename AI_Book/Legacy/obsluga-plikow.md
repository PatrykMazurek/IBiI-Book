# Obsługa plików

W analizie danych podstawowym miejscem, gdzie można przechowywać dane, są pliki. W zależności od zastosowań możemy wykorzystać kilka rozwiązań do odczytywania i zapisywania danych. Wyróżnić możemy:

* Wbudowane mechanizmy w środowisko Python (`open()`)
* Bibliotekę Pandas

### Środowisko Pythona

Wbudowana w środowisko funkcja `open()` pozwala na odczyt danych z pliku i zapis do niego. Zazwyczaj wykorzystywana jest z menedżerem kontekstu (`with`), który pomaga przy zarządzaniu zamykaniem pliku. Definiowanie odczytu lub zapisu odbywa się przez ustawienie odpowiedniego parametru w metodzie, który nazywany jest trybem dostępu (ang. *mode*). 

* "w" - tryb zapisu, pozwala na zapis do pliku, tworzy nowy plik lub nadpisuje istniejący.
* "r" - tryb odczytu (wartość domyślna), pozwala na odczyt z pliku.
* "a" - tryb dopisywania (append), pozwala na dopisanie danych na końcu istniejącego pliku.
* "x" - tryb tworzenia, tworzy plik tylko wtedy, gdy on nie istnieje.
* "b" - tryb binarny, stosowany przy pracy z plikami binarnymi.
* "t" - tryb tekstowy, zapisuje do pliku tekstowego, domyślny.
* "+" - jednoczesny zapis i odczyt z pliku.

Więcej o sposobach dostępu do pliku można przeczytać [tutaj](https://www.datacamp.com/tutorial/python-write-to-file).

**Stosowanie instrukcji `with`**

Standardową operację na pliku można wykonać w następujący sposób:

```python
plik = open("dane.txt", "r") 
# operacje na pliku 
plik.close()
```

Powyższy przykład przedstawia sposób utworzenia dostępu do pliku, wykonania pewnych operacji na nim i zamknięcia go. W tym przypadku należy pamiętać o ręcznym zamknięciu pliku po zakończonej pracy. 

W Pythonie stosowanie instrukcji `with` jest dużo wygodniejszym rozwiązaniem, ponieważ po wyjściu z bloku `with` zamknięcie pliku jest wykonywane automatycznie.

```python
with open("dane.txt", "r") as plik: 
    # operacje na pliku
```

**Kodowanie znaków**

W przypadku pracy z danymi takimi jak tekst, ważnym elementem jest kodowanie znaków. Funkcja `open()`, poza ścieżką do pliku i trybem dostępu, ma też możliwość ustawienia kodowania znaków – odpowiada za to parametr `encoding`. 

```python
with open("dane.txt", "w", encoding="utf-8") as plik: 
    plik.write("Zażółć gęślą jaźń")
```

Dzięki zastosowaniu parametru `encoding` możemy poprawnie zapisać znaki specyficzne dla danego języka (np. polskie znaki diakrytyczne).

**Odczytywanie pliku tekstowego (`.txt`, `.log`)**

Odczytywanie danych z plików możemy wykonać na różne sposoby w zależności od wymogów. Środowisko Python zawiera kilka metod, które pomagają przy wykonaniu tych operacji.

* Odczyt całego pliku:

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    zawartosc = file.read()
```

* Odczyt linia po linii:

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    for linia in file:
        print(linia.strip())
```

* Odczyt wszystkich linii pliku do listy:

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    linie = file.readlines()    
```

**Odczyt pliku tabelarycznego (`.csv`)**

Środowisko Pythona posiada wbudowaną bibliotekę `csv`, która pozwala na łatwy i szybki odczyt danych z pliku CSV.

* Odczyt pliku jako lista wartości:

```python
import csv

with open("dane.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    naglowek = next(reader)  # Pobranie pierwszego wiersza (nagłówka)
    for row in reader:
        print(row)
```

* Odczyt pliku jako słownik (klucz-wartość):

```python
import csv

with open("dane.csv", "r", encoding="utf-8") as file:
    dict_reader = csv.DictReader(file)
    for row in dict_reader:
        print(f"Imię: {row['Imię']}, Wiek: {row['Wiek']}")
```

**Zapis do pliku tekstowego**

W zależności od tego, co chcemy zapisać lub dopisać do pliku, operację tę możemy wykonać ustawiając odpowiedni parametr w funkcji `open()`. Środowisko Python oferuje kilka sposobów na zapisywanie danych w zależności od ich rodzaju.

* Zapisywanie tekstu do pliku:

```python
tekst = "dowolny tekst, który ma być zapisany do pliku"

with open("plik.txt", "w", encoding="utf-8") as fw:
    fw.write(tekst)
```

* Zapisywanie wielu linii do pliku:

W sytuacji, kiedy mamy tekst np. w liście i chcemy go zapisać za jednym razem bez stosowania pętli:

```python
tab = ["dowolny tekst\n", "zapisany\n", "w wielu liniach\n"]

with open("plik.txt", "w", encoding="utf-8") as fw:
    fw.writelines(tab)
```

Powyższe przykłady korzystają z bloku `with`, który zarządza dostępem do pliku i automatycznie po wyjściu z bloku zapisuje dane oraz zamyka dostęp.

**Zapis do pliku tabelarycznego `.csv`**

W przypadkach, kiedy mamy ustrukturyzowane dane zapisane np. w tabelach czy słownikach, możemy skorzystać z wbudowanej biblioteki `csv`. Przygotowane metody pozwalają na zapis danych:

* Dane zapisane w formie tabeli (lista list):

```python
import csv

dane = [
    ["Imię", "Nazwisko", "Wiek"],
    ["Jan", "Kowalski", "30"],
    ["Anna", "Nowak", "25"]
]

with open("dane.csv", mode="w", newline="", encoding="utf-8") as plik:
    writer = csv.writer(plik, delimiter=";")
    writer.writerows(dane)
```

* Dane zdefiniowane jako lista słowników:

```python
import csv

dane = [
    {"Imię": "Jan", "Nazwisko": "Kowalski", "Wiek": 30},
    {"Imię": "Anna", "Nazwisko": "Nowak", "Wiek": 25}
]

pola = ["Imię", "Nazwisko", "Wiek"]
with open("dane_slownik.csv", mode="w", newline="", encoding="utf-8") as plik:
    writer = csv.DictWriter(plik, fieldnames=pola)
    writer.writeheader()
    writer.writerows(dane)
```

W każdym z podanych przykładów można ustawić odpowiedni znak oddzielający poszczególne dane (parametr `delimiter`). 

### Biblioteka Pandas

W sytuacjach, kiedy chcemy odczytać lub zapisać dane do formatów takich jak: `json`, `xml`, `excel`, czy bazy `sql`, możemy wykorzystywać specjalnie do tego przygotowane biblioteki, ale te same możliwości udostępnia potężna biblioteka `pandas`.

**Odczytywanie danych z pliku**

Metody do odczytu danych z pliku są definiowane w następujący sposób:

Schemat:

```python
read_xxx(ścieżka_do_pliku)
```

Przykłady:

| Metoda                        | Opis               |
| ----------------------------- | ------------------ |
| `pd.read_csv("plik.csv")`     | odczyt pliku csv   |
| `pd.read_excel("plik.xlsx")`  | odczyt pliku excel |
| `pd.read_xml("plik.xml")`     | odczyt pliku xml   |
| `pd.read_hdf("plik.h5")`      | odczyt pliku hdf5  |
| `pd.read_orc("plik.orc")`     | odczyt pliku orc   |

Odczytywane dane z plików automatycznie są ładowane do obiektów typu `DataFrame`, co pozwala na bardzo łatwe manipulowanie nimi. 

```python
import pandas as pd

df = pd.read_csv("dane.csv")
```

Powyższy fragment odczytuje wszystkie dane z pliku `dane.csv`. Jeżeli w pliku zdefiniowane będą nazwy kolumn, to automatycznie zostaną one uzupełnione w obiekcie `DataFrame`. 

Ładując dane do `DataFrame`, można odczytywać je na różne sposoby, konfigurując odpowiednie parametry:

* **Wybrane kolumny:**

```python
df = pd.read_csv(
    "dane.csv",
    usecols=["imie", "punkty"]
)
```

* **Określenie odczytu liczby linii:**

```python
df = pd.read_csv(
    "dane.csv", 
    nrows=100
)
```

* **Wskazanie typu danych:**

```python
df = pd.read_csv(
    "dane.csv",
    dtype={
        "imie": "string",
        "punkty": "int64"
    }
)
```

Powyższe przykłady są tylko ułamkiem możliwości odczytywania danych w `pandas`. W zależności od typu pliku można ustawić odpowiednie parametry specyficzne dla każdego z formatów.

**Zapis danych do pliku**

Podobnie jak przy odczycie plików, w bibliotece `pandas` zdefiniowano szereg metod pozwalających na zapis danych umieszczonych w `DataFrame` do pliku. 

Schemat:

```python
df.to_xxx(ścieżka_do_pliku)
```

Przykłady:

| Metoda                     | Opis                 |
| -------------------------- | -------------------- |
| `df.to_csv("plik.csv")`    | zapis do pliku csv   |
| `df.to_excel("plik.xlsx")` | zapis do pliku excel |
| `df.to_html("plik.html")`  | zapis do pliku html  |
| `df.to_hdf("plik.h5")`     | zapis do pliku hdf5  |
| `df.to_json("plik.json")`  | zapis do pliku json  |

Podobnie jak w przypadku metod do odczytu plików, można zdefiniować parametry specyficzne dla danego formatu. Po więcej szczegółów warto zajrzeć do oficjalnej dokumentacji.

### Literatura

* [DataCamp - How to Read a File Line by Line in Python](https://www.datacamp.com/tutorial/python-read-file-line-by-line)
* [DataCamp - Python Write to File: How to Work With Text, CSV, and JSON Files Safely](https://www.datacamp.com/tutorial/python-write-to-file)
* [W3Schools - Python file open](https://www.w3schools.com/python/python_file_handling.asp)
* [Coddykit - Zapisywanie DataFrame do pliku](https://www.coddykit.com/pl/courses/learn_pandas/writing-dataframes-to-files-10405746)
* [Pandas - Dokumentacja IO](https://pandas.pydata.org/docs/reference/io.html)