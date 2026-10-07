# Filtracja i agregacja danych

W poprzedniej sekcji poznaliśmy jak można stworzyć ramkę danych (DataFrame). w tej sekcji poznamy sposoby na filtracje i agregacje danych oraz jak można zweryfikować czy dane nie zawierają pustych wartości.

Załóżmy że będziemy mieć następującą ramke danych

```python
import pandas as pd
import numpy as np

data = {
    'Imie': ['Anna', 'Jan', 'Piotr', 'Kasia', 'Marek', 'Ewa', 'Kamil'],
    'Dzial': ['IT', 'HR', 'IT', 'Sprzedaz', 'HR', 'IT', np.nan],
    'Wiek': [28, 34, 29, 42, 25, 31, np.nan],
    'Pensja': [8000, 6000, 8500, 9000, 5500, 9200, np.nan],
    'Lata_Pracy': [3, 7, 4, 12, 1, 5, np.nan]
}

df = pd.DataFrame(data)
```

### Filtrowanie Danych (Wybieranie wierszy)

Filtrowanie pozwala na wyciągnięcie z ramki tylko tych wierszy, które spełniają określone warunki (np. tylko osoby z działu IT).

#### Podstawowe warunki logiczne

Aby przefiltrować dane, podajemy w nawiasach kwadratowych warunek logiczny. Poniższy kod zwróci tylko tych pracowników, którzy zarabiają więcej niż 7000:

```python
dobrze_zarabiajacy = df[df['Pensja'] > 7000]
```

#### Wiele warunków jednocześnie (`&` i `|`)

Jeśli chcemy połączyć kilka warunków, używamy operatorów bitowych: **`&`** (AND - i) oraz **`|`** (OR - lub).

> **Uwaga:** Każdy z warunków składowych **musi** być otoczony nawiasami okrągłymi!

```python
mlodzi_z_it = df[(df['Dzial'] == 'IT') & (df['Wiek'] < 30)]

hr_lub_sprzedaz = df[(df['Dzial'] == 'HR') | (df['Dzial'] == 'Sprzedaz')]
```

#### Metoda `.query()`

Gdy warunków jest bardzo dużo, standardowa składnia staje się nieczytelna (tzw. "piekło nawiasów"). Metoda `.query()` pozwala zapisać logikę w postaci jednego tekstu:

```python
wynik = df.query('Pensja > 7000 and Dzial == "IT"')
```

#### Metoda `.isin()`

Gdy chcemy sprawdzić, czy wartość w kolumnie znajduje się na stworzonej przez nas liście, użycie wielu operatorów `|` bywa uciążliwe. Z pomocą przychodzi `.isin()`:

```python
wybrane_dzialy = df[df['Dzial'].isin(['HR', 'Sprzedaz'])]
```

#### Specjalistyczne metody selekcji

funkcja `filter()` - zwraca podzbiór wierszy lub kolumn dopasowanych na podstawie nazwy a nie wartości. Shemat wyglądan następująco

```
df.filter(items=None, like=None, regex=None, axis=1)
```

Jeżeli chemy zwrócić z N największych lub najmniejszych elmentów z danje kolumny, możemy zastosować funkcje `nlargest(n, columns)` i `nsmallest(n, columns)` funkcje dziłają lepiej niż funkcja sortująca wartośc `sort_values()`&#x20;

```python
print(df.nlargest(2, "Wiek"))
print(df.nsmallest(2, "Pensja"))
```

Wynik

```
    Imie     Dzial  Wiek  Pensja  Lata_Pracy
3  Kasia  Sprzedaz  42.0  9000.0        12.0
1    Jan        HR  34.0  6000.0         7.0
---------------
    Imie Dzial  Wiek  Pensja  Lata_Pracy
4  Marek    HR  25.0  5500.0         1.0
1    Jan    HR  34.0  6000.0         7.0
```



### Agregacja danych (Podsumowania i statystyki)

Agregacja to proces łączenia wielu pojedynczych wartości w jedną, syntetyczną metrykę (np. wyliczanie średniej dla całej firmy).

#### Całościowe statystyki

Jeśli chcesz wyciągnąć szybką informację dla jednej, konkretnej kolumny:

```python
srednia_pensja = df['Pensja'].mean()
suma_pensji = df['Pensja'].sum()
ilu_pracownikow = df['Imie'].count()
```

#### Grupowanie (`groupby()` )

Największa siła analityczna leży w grupowaniu, które działa identycznie jak tabele przestawne  Grupujemy wiersze po wspólnej cesze, a następnie wyliczamy statystyki dla _każdej z tych grup z osobna_.

```python
srednia_wg_dzialu = df.groupby('Dzial')['Pensja'].mean()
```

#### Złożona agregacja (`agg())`

W sytuacji, kiedy mamy za zadanie wywliczyć kilka różnych statystyk lub zbadać różne kolumny możemy zastosować metodę .agg(). W metodzie tej zamieszczamy dla jakiej kolumny i co chemy wykonać

```python
# Liczymy kilka wskaźników przy jednym przebiegu
statystyki = df.groupby('Dzial').agg({
    'Pensja': ['mean', 'sum'],
    'Wiek': 'max'
})
```

### Brakujące wartości (NaN)

Gdy wczytujesz dane do Pandas, puste komórki są domyślnie zamieniane na specjalną wartość **`NaN`** (Not a Number) lub **`<NA>`**.

#### Jak znaleźć brakujące dane?

W celu określenia czy w danych występują braki i jakiej skali są możemy wykożystać połączenie dwuch funkcji `isna()` oraz `sum()`. funkja isna() sprawdza czy występuje pusta wartość w kolumnie a funkcja `sum()` podaje sumę pustych rekordów.

```python
raport_brakow = df.isna().sum()
print(raport_brakow)
```

#### Usuwanie braków (`dropna()` )

W sytuwacji, kiedy w dużym zbiorze danych występują braki i jest możliwość usunięcia ich najlepiej zastosować metodę dropna(), która usunie wiersze w których występują braki.

```python
df_czyste = df.dropna()

df_wymagana_pensja = df.dropna(subset=['Pensja'])
```

#### Wypełnianie braków (`fillna()` )

Usuwanie danych to często strata cennych informacji. Bardziej zaawansowaną (i częstszą) metodą jest tzw. **imputacja**, czyli wypełnienie luk.

**Wypełnianie stałą wartością:**

```python
df_wypelnione_tekstem = df['Dzial'].fillna('Nieznany')
df_wypelnione_zerem = df['Pensja'].fillna(0)
```

**Wypełnianie średnią lub medianą:** Gdy brakuje danych liczbowych, często wstawiamy w ich miejsce średnią wartość, aby nie zaburzać ogólnych rozkładów statystycznych.

```python
srednia_pensja = df['Pensja'].mean()

df['Pensja'] = df['Pensja'].fillna(srednia_pensja)
```

**Metody propagacji: "forward fill" i "backward fill" (przydatne przy szeregach czasowych):**

```python
df_ffill = df.fillna(method='ffill') 
```
