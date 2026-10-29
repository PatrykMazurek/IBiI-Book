# Eksploracyjna Analiza Danych

### Miary tendencji centralnej

Miary tendencji centralnej pozwalają określić środek ciężkości rozkładu danych. Ich głównym celem jest wskazanie typowej wartości, wokół której skupiają się zebrane obserwacje (np. za pomocą średniej arytmetycznej, mediany czy dominanty).

```python
# Importy wymagane do poniższych przykładów
import pandas as pd
import numpy as np
```

### Średnia arytmetyczna

Średnia arytmetyczna to suma wszystkich obserwacji podzielona przez ich liczbę. Jest to miara bardzo wrażliwa na obecność elementów odstających (tzw. outlierów) oraz szumu. Oznacza to, że dodanie do zbioru nawet pojedynczych, skrajnie nietypowych wartości sprawi, że średnia znacząco odchyli się od faktycznego "środka" danych.

### Mediana

Mediana wyznacza punkt środkowy w grupie uporządkowanych (posortowanych) obserwacji. Jeśli liczba obserwacji (_N_) jest nieparzysta, mediana to wartość znajdująca się dokładnie w środku ciągu. Jeśli liczba obserwacji jest parzysta, mediana jest średnią arytmetyczną dwóch środkowych wartości. W przeciwieństwie do średniej arytmetycznej, mediana jest odporna na wartości odstające.

```python
salaries = pd.Series([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 150])

print("--- Zarobki w zespole IT (w tys. PLN) ---")
print(f"Średnia: {salaries.mean():.2f}k")
print(f"Mediana: {salaries.median():.2f}k")
```

### Dominanta (moda)

Dominanta określa najczęściej występujący element w zbiorze danych. Pojawia się często w analizie danych i jest zwykle stosowana w przypadku zmiennych kategorialnych. Jeżeli wszystkie wartości w grupie są unikalne, to dla takiego zbioru nie da się wyznaczyć dominanty. Możliwe jest także, że w danej grupie więcej niż jedna wartość ma taką samą, najwyższą częstość występowania. W takich przypadkach mówimy o rozkładzie wielomodalnym (występuje wiele dominant).

```python
bugs_per_commit = pd.Series([0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 3, 0, 0])

print("\n--- Błędy w commitach ---")
print(f"Dominanta (najczęstsza wartość): {bugs_per_commit.mode()[0]}")
```

### Wariancja

Wariancja mierzy rozproszenie (odchylenie) danych wokół średniej. Stanowi ona wartość przeciętną kwadratów różnic pomiędzy obserwowanymi wartościami a średnią. Głównym problemem w interpretacji wariancji jest jej jednostka – ze względu na podnoszenie różnic do kwadratu, jednostka wariancji to kwadrat jednostki oryginalnych danych (np. metry kwadratowe zamiast metrów).

Załóżmy, że x<sup>1</sup> x<sup>2</sup>, ..., x<sup>n</sup> stanowią _N_ obserwacji, a  to ich średnia. Wzór na wariancję (populacyjną) wygląda następująco:

$$
\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \overline{x})^2
$$

### Odchylenie standardowe

Odchylenie standardowe to po prostu pierwiastek kwadratowy z wariancji. Dzięki tej operacji jednostka odchylenia standardowego jest taka sama jak jednostka pierwotnych obserwacji. Ułatwia to analitykowi ocenę, jak bardzo dane różnią się od wartości średniej.

* Mniejsza wartość odchylenia standardowego oznacza, że obserwacje są skupione blisko średniej (rozproszone w mniejszym zakresie).
* Większa wartość odchylenia standardowego wskazuje na to, że dane są silnie rozproszone.

Wzór na odchylenie standardowe prezentuje się następująco:

$$
\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \overline{x})^2}
$$

```python
server_1 = pd.Series(np.random.normal(200, 5, 1000))   # stabilny (odchylenie ~5ms)
server_2 = pd.Series(np.random.normal(200, 50, 1000))  # niestabilny (odchylenie ~50ms)

print("\n--- Odchylenie standardowe (Ping w ms) ---")
print(f"Serwer 1 (stabilny) - Odchylenie: {server_1.std():.2f} ms")
print(f"Serwer 2 (niestabilny) - Odchylenie: {server_2.std():.2f} ms")
```

### Skośność i kurtoza

**Skośność** mierzy asymetrię rozkładu. Określa stopień, w jakim rozkład odchyla się od idealnie symetrycznego rozkładu normalnego. Skośność może przyjmować wartości dodatnie, ujemne lub równe zero:

* Wartość równa 0 oznacza idealnie symetryczny kształt rozkładu (często typowy dla rozkładu normalnego).
* **Skośność dodatnia** (prawostronna) jest widoczna na wykresie jako ogon wydłużony w prawo. Oznacza to, że wartości odstające znajdują się po prawej stronie, a większość typowych danych skupia się po lewej. Występuje najczęściej, gdy średnia jest większa od mediany i dominanty.
* **Skośność ujemna** (lewostronna) charakteryzuje się ogonem wydłużonym w lewo. Elementy odstające znajdują się po lewej stronie, a większość danych koncentruje się z prawej strony. Występuje, gdy średnia jest mniejsza od mediany i dominanty.

**Kurtoza** mierzy tzw. "ogonowość" (grubość ogonów) rozkładu w stosunku do rozkładu normalnego. Mówi o tym, jak często w danych występują wartości skrajne (odstające). Istnieją trzy rodzaje kurtozy:

* **Rozkład mezokurtyczny:** rozkład normalny o kurtozie równej zero (w standardowym ujęciu nadmiarowym).
* **Rozkład platykurtyczny:** ma ujemną wartość kurtozy nadmiarowej. Jest "cienkoogonowy" i bardziej spłaszczony w porównaniu do rozkładu normalnego (mniej wartości skrajnych).
* **Rozkład leptokurtyczny:** cechuje się dodatnią kurtozą nadmiarową. Jest "gruboogonowy" i bardziej spiczasty, co oznacza większe prawdopodobieństwo wystąpienia wartości skrajnych (elementów odstających).

```python
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

Zrozumienie relacji występujących między zmiennymi jest kluczowe w analizie danych – np. specjalista HR może chcieć zbadać związek pomiędzy oceną wydajności pracownika a jego poziomem satysfakcji z pracy. Do określania relacji pomiędzy dwiema zmiennymi służą wskaźniki kowariancji i korelacji.

### Kowariancja

Kowariancja mierzy kierunek związku pomiędzy parą zmiennych. Ukazuje, w jakim stopniu i kierunku zmiana jednej zmiennej wpływa na zmianę drugiej. Jej wartość mieści się w nieograniczonym zakresie od $-\infty$ do $+\infty$. Głównym problemem w pracy z kowariancją jest fakt, że uzyskane wyniki są trudne w interpretacji co do siły związku, ponieważ miara ta nie jest znormalizowana i zależy od jednostek badanych cech.

### Współczynnik korelacji Pearsona

Korelacja dostarcza nam więcej informacji o sile relacji pomiędzy zmiennymi. Współczynnik korelacji liniowej Pearsona to znormalizowana wersja kowariancji. Jego wartość zawsze mieści się w przedziale \[-1, 1].

* **Wartość ujemna** reprezentuje korelację odwrotną – wzrost wartości jednej zmiennej wiąże się ze spadkiem wartości drugiej zmiennej.
* **Wartość dodatnia** reprezentuje korelację wprost proporcjonalną – wzrost wartości jednej zmiennej wiąże się ze wzrostem wartości drugiej.
* **Wartość 0** wskazuje na brak korelacji liniowej między zmiennymi (choć mogą być ze sobą powiązane w sposób nieliniowy).

### Współczynnik korelacji rang Spearmana

Współczynnik korelacji rang Spearmana to nieparametryczny odpowiednik współczynnika Pearsona, który bada relację monotoniczną. Zamiast pracować na bezpośrednich wartościach liczbowych, ocenia siłę relacji dla ich rang (pozycji w posortowanym zbiorze). Najpierw rangujemy obserwacje obu zmiennych, a następnie obliczamy klasyczną korelację na tak przygotowanych rangach. Mechanizm ten można stosować zarówno do ciągłych, jak i dyskretnych zmiennych porządkowych.

Korzystamy z korelacji rang Spearmana (zamiast korelacji Pearsona) w przypadku skośnych rozkładów danych, zależności nieliniowych (ale monotonicznych) oraz przy występowaniu licznych elementów odstających, ponieważ miara ta jest na nie znacznie bardziej odporna.
