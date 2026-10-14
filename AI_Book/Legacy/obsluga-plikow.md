# Obsługa plików

W analizie danych podstawowym miejscem gdzie można przechowywać dane są pliki, w zależności od zastosowań możemy wykorzystać kilka rozwiązań do odczytywania i zapisywana danych. Wyróżnić możemy:

* Wbudowane mechanizmy w środowisko Python (`open()`)
* Bibliotekę Numpy
* Bibliotekę Pandas

### Środowisko Python-a

Wbudowana w środowisko metoda `open()` pozwala na odczyt i zapis danych z pliku i do pliku. Zazwyczaj wykorzystywane jest z menadżerem kontekstu (`with`), który pomaga przy zarządzaniu zamykaniem pliku. Definiowanie odczytu lub zapisu odbywa się przez ustawienie odpowiedniego parametru w metodzie, który nazywany jest typem dostępu (type mode).&#x20;

* "w" - tryb zapisu, pozwala na zapis do pliku, tworzy nowy plik lub nadpisuje istniejący
* "r" - tryb odczytu (wartość domyślna), pozwala na odczyt z pliku.
* "a" - tryb dopisywania (append), pozwala na dopisanie danych na końcu pliku w istniejącym pliku.
* "x" - tryb tworzenia, tworzy plik tylko wtedy gdy plik nie istnieje.
* "b" - tryb binarny, stosowany przy pracy z plikami binarnymi.
* "t" - tryb tekstowy, zapisuje do pliku tekstowego, domyślny
* "+" - jednoczesny zapis i odczyt z pliku.

więcej sposobów na dostęp do pliku można przeczytać [tutaj](https://www.datacamp.com/tutorial/python-write-to-file?utm_cid=23340058065\&utm_aid=192632748929\&utm_campaign=230119_1-ps-dscia~dsa-tofu~python_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na\&utm_loc=9252650-\&utm_mtd=-c\&utm_kw=\&utm_source=google\&utm_medium=paid_search\&utm_content=ps-dscia~emea-en~dsa~tofu~tutorial~python\&gad_source=1\&gad_campaignid=23340058065\&gbraid=0AAAAADQ9WsGukgp9itcNQxq0kVyl6L3EA\&gclid=CjwKCAjwvsvTBhBaEiwAmf-3nr4koQibK8brbxR3mu1ATaeKAzQPk3c6BXAYJpdxc2FS3FtJVAzyCRoClaIQAvD_BwE)

**Stosowanie instrukcji** `with`

Standardową operację na pliku można wykonać w następujący sposób&#x20;

```python
plik = open("dane.txt", "r") 
# operacje na pliku 
plik.close()
```

Powyższy przykład przedstawia sposób utworzenia dostępu do pliku, wykonania pewnych operacji na nim i zamknięcie pliku. W powyższym przypadku należy pamiętać o zamknięciu pliku po zakończonej pracy na nim.&#x20;

W Pythonie stosowanie istrukcji `with` jest dużo wygodniejszym rozwiązaniem, ponieważ po wyjściu z bloku `with` zamknięcie jset automatycznie wykonywane.

```
with open("dane.txt", "r") as plik: 
    # operacje na pliku
```

**Kodowanie znaków**

W przypadku pracy z danymi takimi jak tekst ważnym elementem jest kodowanie znaków. Metoda `open()` poza ścieżką do pliku, trybem dostępu ma też możliwość ustawienia kodowania znaków, odpowiada za to parametr `encoding`.&#x20;

```python
with open("dane.txt", "w", encoding="utf-8") as plik: 
    plik.write("Zażółć gęślą jaźń")
```

Za pomocą zastosowania parametru `encoding` możemy zapisać specyficzne znaki dla danego języka.

**Odczytywanie plik tekstowego** (`.txt`, `.log`)

Odczytywanie danych z plików możemy wykobać na różne sposoby w zależność od wymogów. Środowisko Python zawiera kilka metod, które pomagają przy wykonaiu tych operacji.

* odczyt całego pliku

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    zawartosc = file.read()
```

* odczyt linii po linii

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    for linia in file:
        print(linia.strip())
```

* odczyt wszystkich linii pliku do listy

```python
with open("dane.txt", "r", encoding="utf-8") as file:
    linie = file.readlines()    
```

**Odczyt pliku tabelarycznego** (`.csv`)

Środowisko Pythn-a posiada wbudowaną bibliotekę `csv`, która pozwala na łatwy i szybki odczyt danych z pliku csv.

* Odczyt pliku jako listy wartości

```python
import csv

with open("dane.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    naglowek = next(reader)  # Pobranie pierwszego wiersza (nagłówka)
    for row in reader:
        print(row)
```

* Odczyt pliku jako słownik (klucz - wartość)

```python
import csv

with open("dane.csv", "r", encoding="utf-8") as file:
    dict_reader = csv.DictReader(file)
    for row in dict_reader:
        print(f"Imię: {row['imie']}, Wiek: {row['wiek']}")
```

**Zapis do pliku tekstowego**

W zależności od tego co chcemy zapisać lub dopisać do pliku, operacje tą możemy wykonać ustawiając opdpowiedni parametr w metodzie open(). Środowiesko Python przygotował kilka sposobów na zapisywanie danych w zależności od tego jakiego rodzau mamy dane.

* zapisywanie tekstu do pliku

```python
tekst = "dowolny tekst, który ma być zapisany do pliku"

with open("plik.txt", "w", encoding="utf-8") as fw:
    fw.write(tekst)
```

*   Zapisywanie wieli liń do pliku

    W sytuacji kiedy mamy tekst np. w liście i chcemy go zapisać za jednym razem bez stosowania pętli.

```python
tab = ["dowolny tekst\n", "zapisany\n", "w wielu liniach\n"]

with open("plik.txt", "w", encoding="utf-8") as fw:
    fw.writelines(tab)
```

Powyższe przykłady były zapisywane przy użyciu bloku `with`, któy zarządza dostępem do pliku i automaycznie po wyjściu z bloku zapisuje dane i zamyka dostęp.

**Zapis do pliku tabelarycznego `scv`**

W przypadkach kiedy dane mamy ustrukturyzowane zapisane np. do tabel czy słowników możemy skorzystać z wbudowanej w środowisko biblioteki `csv`.  Przygoytwane metody pozwalaja na zapis danych:

* dane zapisane z tabel (lista list)

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

* &#x20;dane zapisane z słowników

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

W każdym z podanych przykładów można ustawić odpowiedni znak odzielający poszczególne dane.&#x20;

### Biblioteka Pandas

W sytuacjach kiedy chcemy odczytać lub zapisać dane do formatów typu: `json`, `xml`, `excel sql` możemy wykorzystwać specjalnie do tego przygotowane biblioteki ale te same mozliwości udostępnia biblioteka `pandas`.

**Odczytywanie danych z pliku.**

Metody do odczytu danych z pliku są definiowane w następujący sposób:

Schemat:

```r
read_xxx(scieżka_do_pliku)
```

Przykłady

| Metoda                        | Opis               |
| ----------------------------- | ------------------ |
| `pd.read_csv("plik.csv")`     | odczyt pliku csv   |
| `pd.read_excel("plik.xsls").` | odczyt pliku excel |
| `pd.read_xml("plik.xml")`     | odczyt pliku xml   |
| `pd.read_hdf("plik.h5")`      | odczyt pliku hdf5  |
| `pd.read_orc("plik.orc")`     | odczyt pliku orc   |

Odczytywane dane z plików automatycznie są zapisywane do obiektów DataFrame co pozwala na łatwiejsze manipulowanie nimi.&#x20;

```python
df = pd.read_csv("dane.csv")
```

Powyższy fragment odczytuje wszystkie dane z pliku `dane.csv`, jeżeli w pliku zdefiniowane będą nazwy kolumn to automatycznie zostaną uzupełnione w obiekcie DataFreme.&#x20;

Zapisując do DataFrem można odczytać na różne sposoby:

* **Wybrane kolumny**

```python
df = pd.read_csv(
    "dane.csv",
    usecols=["imie", "punkty"]
)
```

* **Określenie odczytu liczby lini**

```python
df = pd.read_csv(
    "dane.csv", 
    nrows=100
)
```

* **Wskazanie typu danych**

```python
df = pd.read_csv(
    "dane.csv",
    dtype={
        "imie": "string",
        "punkty": "int64"
    }
)
```

Powyższe przykłady są tylko częścią możliwości odczytywania danych w `Pandas`. W zależności od typu pliku można ustawić odpowiednie parametry specyficzne dla każdego z formatów.

**Zapis danych do pliku**

Podobnie jak przy odczycie plików, w bibliotece `Pandas` zdefiniowano kilka metod pozwalających na zapis danych umieszczonych w DataFrame do pliku. Metody do odczytu danych z pliku są definiowane w następujący sposób:

Schemat:

```python
df.to_xxx(sciezka_do_pliku)
```

Przykłady:

| Metoda                     | Opis                 |
| -------------------------- | -------------------- |
| `df.to_csv("plik.csv")/`   | zapis do pliku csv   |
| `df.to_excel("plik.xsls")` | zapis do pliku excel |
| `df.to_html("plik.xml")`   | zapis do pliku html  |
| `df.to_hdf("plik.h5")`     | zapis do pliku hdf5  |
| `df.to_json("plik.orc")`   | zapis do pliku json  |

Podobnie jak w przypadku metod do odczytu plików można zdefiniować odpowiednie parametry dla odpowiedniego formatu, po więcej szczegołów należy zapozać się z dokumentacją.

### Literatura

[datacamp.com - How to Read a File Line by Line in Python](https://www.datacamp.com/tutorial/python-read-file-line-by-line)

[datacamp.com - Python Write to File: How to Work With Text, CSV, and JSON Files Safely](https://www.datacamp.com/tutorial/python-write-to-file?utm_cid=23340058065\&utm_aid=192632748929\&utm_campaign=230119_1-ps-dscia~dsa-tofu~python_2-b2c_3-emea_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na\&utm_loc=9252650-\&utm_mtd=-c\&utm_kw=\&utm_source=google\&utm_medium=paid_search\&utm_content=ps-dscia~emea-en~dsa~tofu~tutorial~python\&gad_source=1\&gad_campaignid=23340058065\&gbraid=0AAAAADQ9WsGukgp9itcNQxq0kVyl6L3EA\&gclid=CjwKCAjwvsvTBhBaEiwAmf-3nr4koQibK8brbxR3mu1ATaeKAzQPk3c6BXAYJpdxc2FS3FtJVAzyCRoClaIQAvD_BwE)

[w3schools.com - Python file open](https://www.w3schools.com/python/python_file_handling.asp)

[Coddykit - zapisywanie DataFrame do pliku](https://www.coddykit.com/pl/courses/learn_pandas/writing-dataframes-to-files-10405746)

[Pandas - dokumentacja](https://pandas.pydata.org/docs/reference/io.html)
