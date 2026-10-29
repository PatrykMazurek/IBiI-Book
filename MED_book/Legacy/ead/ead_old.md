# Eksploracyna analiza danych

### miary tendencji centralnej 

Tendencja centralna określa trend, w którym wartości są zgrupowane wokół średnich, takich jak średnia arytmetyczna, dominanta czy mediana. Głównym celem tendencji centralnej jest wyznaczenie wartości mieszczącej się w centrum obserwacji.

### Średnia arytmetyczna

Wartość średnia jest wskaźnikiem arytmetycznym, obliczanym poprzez podzielenie sumy obserwacji przez liczbę obserwacji. Jest ona wrażliwa na obecność elementów odstających i szumu, dlatego za każdym razem gdy do grupy zostaną dodane jakieś nietypowe wartości, średnia tej grupy będzie odbiegać od typowej wartości środkowej.

### Mediana

Mediana wyznacza punkt środkowy (wartość środkową) w grupie uporządkowanych obserwacji. Jeśli liczba obserwacji ( N ) jest nieparzysta, mediana to wartość znajdująca się dokładnie w środku posortowanego ciągu. Jeśli liczba obserwacji jest parzysta, mediana jest średnią arytmetyczną dwóch środkowych wartości.

```python
salaries = pd.Series([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 150])

print("--- Zarobki w zespole IT (w tys. PLN) ---")
print(f"Średnia: {salaries.mean():.2f}k")
print(f"Mediana: {salaries.median():.2f}k")
```
### Dominanta (moda)

Dominanta określa najczęściej występujący element w grupie obserwacji. Dominanta pojawia się często w analizie danych i jest zwykłe stosowana w przypadku wartości kategorialnych. Jeżeli wszystkie wartości w grupie są niepowtarzalne, to dla takiej grupy nie da się wyznaczyć dominanty. Możliwe jest także, że w danej grupie większa liczba wartości ma taką samą częstość występowania. W takich przypadkach może występować wiele dominant.

```python
bugs_per_commit = pd.Series([0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 3, 0, 0])

print("\n--- Błędy w commitach ---")
print(f"Dominanta (najczęstsza wartość): {bugs_per_commit.mode()[0]}")
```

### Wariancja

Wariancja mierzy odchylenie od średniej. Stanowi ona wartość przeciętną kwadratu różnicy pomiędzy obserwowanymi wartościami a średnią. Głównym problemem w przypadku wariancji jest jednostka, ponieważ podnosimy do kwadratu różnicę między obserwacjami a średnią. Załóżmy, że  $x_1,x_2,\dots, x_N$  stanowią  N  obserwacji. Wzór na wariancję tych wartości wygląda następująco:
$$
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\overline{x})^2
$$

### Odchylenie standardowe

*Odchylenie standardowe* - jest to pierwiastek kwadratowy z wariancji. Jego jednostka jest taka sama jak pierwotnych obserwacji. Dzięki temu analitykowi łatwiej jest ocenić dokładne odchylenie od średniej. Mniejsza wartość odchylenia standardowego reprezentuje bliższą odległość obserwacji od średniej; oznacza to, że obserwacje są rozproszone w mniejszym zakresie. Większa wartość odchylenia standardowego oznacza dużą odległość obserwacji od średniej, czyli że są one bardziej rozproszone. Przyjmijmy, że $x_1,x_2,\dots, x_N$ stanowią $N$ obserwacji. Wzór na odchylenie standardowe tych wartości jest zaprezentowany poniżej:
$$
\sigma=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i-\overline{x})^2}
$$

```python
server_1 = pd.Series(np.random.normal(200, 5, 1000))   # stabilny (odchylenie ~5ms)
server_2 = pd.Series(np.random.normal(200, 50, 1000))  # niestabilny (odchylenie ~50ms)

print("\n--- Odchylenie standardowe (Ping w ms) ---")
print(f"Serwer 1 (stabilny) - Odchylenie: {server_1.std():.2f} ms")
print(f"Serwer 2 (niestabilny) - Odchylenie: {server_2.std():.2f} ms")
```

### Skośność i kurtoza

Skośność mierzy symetrię rozkładu. Określa ona stopień odchylenia od rozkładu normalnego. Przyjmuje wartości dodatnie, ujemne lub zero.

* Wartość  0  oznacza idealnie normalny kształt rozkładu.
* Skośność dodatnia jest widoczna na wykresie jako ogon wydłużony w prawo; oznacza to, że elementy odstające znajdują się po prawej stronie, a zwykłe dane mieszczą się po lewej stronie. Skośność dodatnia występuje wtedy, gdy średnia jest większa od mediany i dominanty.
* Skośność ujenna jest widoczna na wykresie jako ogon wydłużony w lewo; oznacza to, że elementy odstające znajdują się po lewej stronie, a zwykłe dane mieszczą się po prawej stronie. Skośność ujemna występuje wtedy, gdy średnia jest mniejsza od mediany i dominanty.

Kurtoza mierzy ogonowość (grubość ogona) w stosunku do rozkładu normalnego. Duża wartość kurtozy oznacza gruboogonowość, czyli obecność większej liczby elementów odstających w obserwacjach, natomiast kurtoza o małej wartości mówi nam o cienkoogonowości, czyli mniejszej liczbie elementów odstających wśród obserwacji. Istnieją trzy rodzaje kształtów kurtozy: rozklady mezokurtyczny, platykurtyczny i leptokurtyczny. Wyjaśnijmy znaczenie tych terminów:

* rozkład normalny o zerowej kurtozie jest zwany rozkładem mezokurtycznym;
* rozkład platykurtyczny ma ujemną wartość kurtozy i jest cienkoogonowy w porównaniu do rozkładu normalnego;
* kurtoza w rozkładzie leptokurtycznym przekracza wartość trzy, on sam zaś cechuje się gruboogonowością w porównaniu do rozkładu normalnego.


```python
import scipy.state as state
app_time = np.random.exponential(scale=2, size=1000) 

# Rozkład normalny / symetryczny (np. szum czujników IoT)
sensor_noise = np.random.normal(loc=0, scale=1, size=1000)

app_series = pd.Series(app_time)
sensor_series = pd.Series(sensor_noise)

print("--- Skośność (Skewness) ---")
print(f"Czas w aplikacji (skośność dodatnia): {app_series.skew():.2f}")
print(f"Szum sensora (symetryczny): {sensor_series.skew():.2f}")

print("\n--- Kurtoza (Kurtosis) ---")
# Wysoka kurtoza oznacza "grubsze ogony" i wyższe prawdopodobieństwo skrajnych wartości
print(f"Czas w aplikacji (kurtoza): {app_series.kurtosis():.2f}")
print(f"Szum sensora (kurtoza): {sensor_series.kurtosis():.2f}")
```
### Współczynnik kowariancji i korelacji

Pomiar relacji pomiędzy zmiennymi przydaje się do zrozumienia dynamiki występującej między zmiennymi; np. kierownik działu kadr musi znać stopień relacji pomiędzy oceną wydajności pracownika a oceną satysfakcji. Do określania relacji pomiędzy zmiennymi służą wskaźniki kowariancji i korelacji.

**Kowariancja**

Kowariancja mierzy związek pomiędzy parą zmiennych. Ukazuje ona stopień zmian w zmiennych, tj. w jakim stopniu zmiana jednej zmiennej wpływa na drugą zmienną. Jej wartość mieści się w zakresie od  −∞  do  +∞ . Problem z kowariancją polega na tym, że uzyskiwane za jej pomocą wyniki nie są miarodajne, gdyż nie są znormalizowane.

### Współczynnik korelacji Pearsona

Korelacja wyjaśnia rodzaj relacji pomiędzy zmiennymi. Dostarcza ona więcej informacji od kowariancji i stanowi jej znormalizowaną wersję. Zakres korelacji mieści się w przedziale od  [−1,1] .

* Wartość ujemna reprezentuje zmniejszenie wartości jednej zmiennej w wyniku zwiększenia wartości innej zmiennej.
* Wartość dodatnia reprezentuje zwiększenie wartość jednej w wyniku zwiększenia wartości innej zmiennej i odwrotnie.
* Wartość  0  wskazuje na brak korelacji między zmiennymi lub oznacza, że zmienne są wzajemnie niezależne.

### Współczynnik korelacji rang Spearmana

Współczynnik korelacji rang Spermana jest korelacją Pearsona dla rang obserwacji. Jest to nieparametryczny wskaźnik korelacji rang. Ocenia siłę relacji dwóch zrangowanych zmiennych. Zrangowane zmienne są posortowanymi liczbami porządkowymi. Najpierw rangujemy obserwacje, a następnie obliczamy korelację rang. Mechanizm ten można stosować zarówno do dyskretnych, jak i ciągłych zmiennych porządkowych.

Korzystamy z korelacji rang Spearmana zamiast korelacji Pearsona w przypadku skośnego rozkładu danych lub występowania licznych elementów odstających, ponieważ nie ma on żadnych założeń dotyczących rozkładu danych.

## Zadania

1. Odczytaj dane z pliku `ds_salaries.csv`, a następnie oblicz średnią arytmetyczną i medianę dla kolumny `salary_in_usd`. Zidentyfikuj wartości odstające na podstawie obliczenia odchylenia standardowego i odfiltruj rekordy przekraczające 3 krotność odchylania standardowego. Na wykresie pudełkowym narysuj wartości dla kolumny `salary_in_usd` przed i po filtracji.
2. Odczytaj dane z pliku `googleplaystore.csv`, który zawiera dane o plik aplikacjach w sklepie Google App. Na początku sprawdź, czy w kolumnie `Rating` występują puste rekordy, jeżeli tak to usuń je. Następnie na podstawie kolumny `Rating` oblicz dominantę i narysuj histogram ocen. 
3. Odczytaj dane z pliku `KAG_energydata_complete.csv`, sprawdz czy nie występują braki w kolumnach `T1`, ..., `T9`, jeżeli będą występować braki usuń rekordy. Następnie przeanalizuj temperatury i oblicz wariancje i odchylanie standardowe dla każdego pomieszczenia wskazując, które pomieszczenie charakteryzuje się bardziej stabilną temperaturą. Korzystając z histogramu przedstaw temperatury na wykresie.   