# Wprowadzenie do Pandas: Filtrowanie, Agregacja i Czyszczenie Danych

Aby rozpocząć pracę, musimy zaimportować bibliotekę `pandas` i stworzyć naszą bazową **ramkę danych** (DataFrame). Wyobraź sobie DataFrame jak arkusz kalkulacyjny w Excelu, w którym kolumny to zmienne, a wiersze to obserwacje (np. pracownicy).

```python
import pandas as pd
import numpy as np

# Przykładowy zbiór danych pracowników (zawiera również braki danych - NaN)
data = {
    'Imie': ['Anna', 'Jan', 'Piotr', 'Kasia', 'Marek', 'Ewa', 'Kamil'],
    'Dzial': ['IT', 'HR', 'IT', 'Sprzedaz', 'HR', 'IT', np.nan],
    'Wiek': [28, 34, 29, 42, 25, 31, np.nan],
    'Pensja': [8000, 6000, 8500, 9000, 5500, 9200, np.nan],
    'Lata_Pracy': [3, 7, 4, 12, 1, 5, np.nan]
}

df = pd.DataFrame(data)
```

---

## 1. Filtrowanie Danych (Wybieranie wierszy)

Filtrowanie pozwala na wyciągnięcie z ramki tylko tych wierszy, które spełniają określone warunki (np. tylko osoby z działu IT).

### Podstawowe warunki logiczne
Aby przefiltrować dane, podajemy w nawiasach kwadratowych warunek logiczny. Poniższy kod zwróci tylko tych pracowników, którzy zarabiają więcej niż 7000:

```python
dobrze_zarabiajacy = df[df['Pensja'] > 7000]
```

### Wiele warunków jednocześnie (`&` i `|`)
Jeśli chcemy połączyć kilka warunków, używamy operatorów bitowych: **`&`** (AND - i) oraz **`|`** (OR - lub). 
> **Uwaga:** Każdy z warunków składowych **musi** być otoczony nawiasami okrągłymi!

```python
# Pracownicy z IT, którzy mają mniej niż 30 lat
mlodzi_z_it = df[(df['Dzial'] == 'IT') & (df['Wiek'] < 30)]

# Pracownicy z HR lub z działu Sprzedaży
hr_lub_sprzedaz = df[(df['Dzial'] == 'HR') | (df['Dzial'] == 'Sprzedaz')]
```

### Metoda `.isin()`
Gdy chcemy sprawdzić, czy wartość w kolumnie znajduje się na stworzonej przez nas liście, użycie wielu operatorów `|` bywa uciążliwe. Z pomocą przychodzi `.isin()`:

```python
# Znacznie krótszy zapis niż używanie operatora OR
wybrane_dzialy = df[df['Dzial'].isin(['HR', 'Sprzedaz'])]
```

### Metoda `.query()` - faworyt jeśli chodzi o czytelność
Gdy warunków jest bardzo dużo, standardowa składnia staje się nieczytelna (tzw. "piekło nawiasów"). Metoda `.query()` pozwala zapisać logikę w postaci jednego tekstu:

```python
# Wykonuje to samo, co pierwszy przykład, ale czyta się to jak zwykły język angielski
wynik = df.query('Pensja > 7000 and Dzial == "IT"')
```

---

## 2. Agregacja Danych (Podsumowania i statystyki)

Agregacja to proces łączenia wielu pojedynczych wartości w jedną, syntetyczną metrykę (np. wyliczanie średniej dla całej firmy).

### Całościowe statystyki
Jeśli chcesz wyciągnąć szybką informację dla jednej, konkretnej kolumny:

```python
srednia_pensja = df['Pensja'].mean()
suma_pensji = df['Pensja'].sum()
ilu_pracownikow = df['Imie'].count()
```

### Grupowanie: `.groupby()`
Największa siła analityczna leży w grupowaniu, które działa identycznie jak tabele przestawne (Pivot Tables) w Excelu. Grupujemy wiersze po wspólnej cesze, a następnie wyliczamy statystyki dla *każdej z tych grup z osobna*.

```python
# Średnia pensja wyliczona osobno dla każdego działu
srednia_wg_dzialu = df.groupby('Dzial')['Pensja'].mean()
```
*Jak czytać ten kod? "Weź DataFrame (`df`), pogrupuj go po unikalnych wartościach w kolumnie Dział (`.groupby('Dzial')`), z wygenerowanych grup wyciągnij tylko kolumnę Pensja (`['Pensja']`) i policz dla niej średnią (`.mean()`)."*

### Złożona agregacja: `.agg()`
Często analityk chce wyliczyć kilka różnych statystyk naraz lub zbadać różne rzeczy dla różnych kolumn. Służy do tego elastyczna metoda `.agg()`.

```python
# Liczymy kilka wskaźników przy jednym przebiegu
statystyki = df.groupby('Dzial').agg({
    'Pensja': ['mean', 'sum'],
    'Wiek': 'max'
})
```

---

## 3. Brakujące wartości (NaN): Diagnoza i Czyszczenie

Gdy wczytujesz dane do Pandas, puste komórki są domyślnie zamieniane na specjalną wartość **`NaN`** (Not a Number) lub **`<NA>`**.

### Diagnoza: Jak znaleźć brakujące dane?
Zanim zaczniesz sprzątać, musisz wiedzieć, gdzie leży problem i jaka jest jego skala. Łącząc `.isna()` z funkcją sumującą `.sum()`, otrzymamy precyzyjny raport o brakach w kolumnach:

```python
# Zwraca liczbę brakujących wartości dla każdej kolumny
raport_brakow = df.isna().sum()
print(raport_brakow)
```

### Usuwanie braków: `.dropna()`
Gdy masz ogromny zbiór danych, a braki stanowią zaledwie ułamek procenta, najprostszym wyjściem jest usunięcie wybrakowanych wierszy.

```python
# Jeśli wiersz ma chociaż jedno puste pole (NaN) - wylatuje z tabeli
df_czyste = df.dropna()

# Usuwa wiersz tylko wtedy, gdy brakuje wartości w kolumnie 'Pensja'
df_wymagana_pensja = df.dropna(subset=['Pensja'])
```

### Wypełnianie braków: `.fillna()`
Usuwanie danych to często strata cennych informacji. Bardziej zaawansowaną (i częstszą) metodą jest tzw. **imputacja**, czyli wypełnienie luk.

**Wypełnianie stałą wartością:**
```python
df_wypelnione_tekstem = df['Dzial'].fillna('Nieznany')
df_wypelnione_zerem = df['Pensja'].fillna(0)
```

**Wypełnianie średnią lub medianą:**
Gdy brakuje danych liczbowych, często wstawiamy w ich miejsce średnią wartość, aby nie zaburzać ogólnych rozkładów statystycznych.

```python
# Obliczamy średnią
srednia_pensja = df['Pensja'].mean()

# Wypełniamy braki w kolumnie 'Pensja' obliczoną średnią
df['Pensja'] = df['Pensja'].fillna(srednia_pensja)
```

**Metody propagacji: "forward fill" i "backward fill" (przydatne przy szeregach czasowych):**
```python
# bierze ostatnią znaną wartość z góry i "ciągnie" ją w dół
df_ffill = df.fillna(method='ffill') 
```