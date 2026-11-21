# Zadania

1. Stwórz jednowymiarową tablicę zawierającą liczby całkowite od `1` do `20`. Następnie:
* Zmień jej kształt na macierz o wymiarach 4x5.
* Oblicz sumę wszystkich elementów, wartość maksymalną oraz średnią dla całej macierzy.
* Wyciągnij z niej tylko drugi wiersz oraz ostatnią kolumnę.
2. Masz tablicę z wartościami losowymi: 
```python
random_number = np.array([12.5, -3.0, 0.0, 21.4, -7.2, 15.0, 28.9, -0.5, 19.1, 31.2])
```

* Policz ile wartości jest poniżej `0`
* Stwórz nową tablicę, w której wszystkie wartości ujemne zostaną zamienione na 0.0, a wartości powyżej 25.0 zostaną obcięte do 25.0.
3. Dostałeś macierz z pomiarami z czujników, ale część danych przepadła i masz tam wartości `np.nan`:
```python
data = np.array([
    [10.0, 20.0, np.nan, 40.0],
    [5.0,  np.nan, 15.0, 25.0],
    [np.nan, 100.0, 200.0, 300.0]
])
```
* Napisz kod, który zastąpi każdą wartość NaN średnią arytmetyczną z jej własnego wiersza (oczywiście liczoną z pominięciem NaN).
4. Utwórz tablicę $5\times5$ wypełnioną wartościami z rozkładu normalnego i wykonaj na niej następujące operacje:
* oblicz sumę wartości dla każdego wiersza;
* oblicz sumę wartości dla każdej kolumny;
* znajdź indeksy wartości maksymalnej dla całej tablicy;
* zastosuj macierz logiczną, aby znaleźć wszystkie wartości większe niż `0.5`;
* zastąp wszystkie wartości mniejsze niż `-0.5` lub większe od `0.5` liczbą `0`.
5. Stwórz wektor z losowymi liczbami całkowitymi z zakresu od `1` do `100` (np. `50` elementów) i wykonaj na niej następujące operacje:
* oblicz średnią, medianę i odchylenie standardowe;
* znajdź minimalną i maksymalną wartość;
* posortuj tablicę rosnąco.
6. Utwórz jednowymiarową tablicę `x` o długości `20,` składającą się z liczb od `1` do `20`. Wykonaj następujące operacje:
* wyciągnij z tablicy `x` elementy z indeksów od `4` do `16`;
* zwróć wszystkie elementy większe niż `8`;
* zmień wszystkie elementy o wartościach podzielnych przez `3` na `100`.
7. Stwórz dwie tablice 2D o wymiarach $2\times 3$ i wykonaj następujące operacje:
* połącz obie tablice wzdłuż osi poziomej (oś `1`);
* połącz obie tablice wzdłuż osi pionowej (oś `0`);
* podziel wynikową tablicę z pkt 1 na dwie równe części wzdłuż osi poziomej (znajdź odpowiednią metodę).