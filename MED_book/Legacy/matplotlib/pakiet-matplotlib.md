Najpopularniejszym pakietem, który może przedstawić dane na wykresach, jest niewątpliwie pakiet `matplotlib`. Pakiet ściśle jest powiązany z pakietem `numpy` – obiekty macierzowe czy wektory można w łatwy sposób stosować jako argumenty funkcji rysujących. Do rysowania wykresów będziemy wykorzystywać moduł `pyplot` z pakietu `matplotlib`.

Wymagane jest zaimportowanie potrzebnych bibliotek:

```python
from google.colab import drive

drive.mount('/content/drive')
!ln -s /content/gdrive/My\ Drive/ ./mydrive
```

```python
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
```

## Rysowanie podstawowych obiektów

Funkcja `matplotlib.pyplot.plot` pozwala na prezentowanie zmian w czasie, rysowanie obiektów czy przebiegu funkcji. Wierzchołki krzywej, którą chcemy narysować, możemy przekazać jako wektory o tych samych długościach, z których pierwszy dotyczy osi x (oś odciętych), a drugi osi y (oś rzędnych).

Dla przykładu narysowany zostanie wykres funkcji kwadratowej $f(x) = x^2$ dla $x\in[-6, 6]$.

```python
X = np.r_[-6:6:5]
Y = X**2
plt.plot(X,Y)
plt.show()
```

Zwiększenie dokładności wykresu (rozdzielczości) polega na zwiększeniu liczby wyświetlanych punktów.

```python
X = np.r_[-6:6:60j]
Y = X**2
plt.plot(X,Y)
plt.show()
```

W przypadku, kiedy wykres ma przedstawiać obserwacje – niepołączone ze sobą punkty – można zastosować funkcję `scatter()`.

```python
iris = sns.load_dataset("iris")
plt.scatter(iris.sepal_length, iris.sepal_width)
plt.show()
```

Otrzymany wykres nazywany jest wykresem rozproszonym — reprezentuje on graficznie odpowiadające sobie pary obserwacji z dwóch danych równolicznych wektorów x i y, tj. (xi, yi) dla kolejnych i. Ten typ wykresu bardzo często jest stosowany w statystyce, ponieważ w prosty i przejrzysty sposób pozwala zobrazować rodzaj zależności między badanymi zmiennymi.

Pakiet Pandas również pozwala na generowanie wykresów rozproszonych. Służy do tego wywołanie metody `plot()` na obiekcie `DataFrame` z argumentem `kind` ustawionym na `scatter`.

```python
iris.plot(x = "sepal_length", y = "sepal_width", kind="scatter")
plt.show()
```

Wykres typu rozproszonego (`plt.scatter`) pozwala na zdefiniowanie koloru odgórnie dla całego wykresu lub dla każdej z próbek osobno. Poniższy przykład przedstawia definiowanie koloru dla każdej próbki.

```python
rng = np.random.default_rng(0)
x = rng.normal(size=100)
y = rng.normal(size=100)
colors = rng.random(100)
sizes = 1000 * rng.random(100)
plt.scatter(x, y, c=colors, s=sizes, alpha=0.3)
plt.colorbar(); # Wyświetla skalę kolorów
```

Innym przykładem, w którym możemy zastosować wykres rozproszony, jest zbiór `Iris` z pakietu `Scikit-learn`, gdzie każda próbka reprezentuje jedną z trzech odmian irysa.

```python
from sklearn.datasets import load_iris
iris = load_iris()
features = iris.data.T
plt.scatter(features[0], features[1], alpha=0.4, s=100*features[3], c=iris.target, cmap='viridis')
plt.xlabel("Długość działki kielicha (cm)")
plt.ylabel("Szerokość działki kielicha (cm)");
```

### Wielokąty

W sytuacji, kiedy mamy do czynienia z wielokątem, który chcemy wypełnić, można zastosować funkcję `fill()`, która odpowiada za wypełnienie.

Argument `fill` kontroluje, czy wnętrze utworzonego wielokąta ma być wypełnione jednolitą barwą, a `hatch` - określonym deseniem.

```python
t = np.linspace(0, np.pi, 2000, endpoint=False)
X = np.cos(3*t) * np.cos(t)
Y = np.cos(3*t) * np.sin(t)
plt.fill(X, Y, fill=False, hatch=".")
plt.title("wykrees wielokąta", loc="right")
plt.xlabel("wartośc osi x")
plt.ylabel("watrości osi y")
plt.show()
```

## Adnotacje tekstowe

Funkcja `title()` dodaje tytuł do wykresu. Przy użyciu argumentu `loc` możemy określić położenie tekstu (`center`, `left`, `right`). Natomiast podpisywanie osi x i osi y można wykonać, wywołując funkcje `xlabel()` i `ylabel()`.

Dodanie tekstu w dowolnym miejscu wykresu, aby opisać obiekty, można wykonać, wywołując metodę `text()`. Jako parametry przekazujemy współrzędne i tekst, który ma być widoczny na wykresie.

## Parametry graficzne

### Sposoby określania punktów i odcinków

Większość funkcji rysujących wykresy z pakietu `matplotlib.pyplot` ma wspólny zestaw argumentów (o takich samych lub równoważnych nazwach), które odpowiadają za sposób rysowania poszczególnych elementów rysunku.

### Odcinki

W przypadku funkcji rysujących odcinki (np. `plot()` i `fill()`) do wyboru mamy cztery podstawowe typy linii: ciągła (domyślna), przerywana, "kreska-kropka" oraz kropkowana (zob. tabela poniżej). Odpowiednią wartość należy nadać argumentowi `linestyle` (lub `ls`), aby uzyskać żądany styl.


|typ linii                       |oznaczenie          |alias   |
|--------------------------------|--------------------|--------|
|linia ciągła                    |"solid"           |"-"   |
|linia przerywana                |"dashed"          |"--"  |
|linia typu "kreska-kropka"      |"dashdot"         |"-."  |
|linia kropkowana                |"dotted"          |":"   |

Grubość linii możemy zmienić za pośrednictwem argumentu `linewidth` (lub `lw`). Wyrażamy ją przy użyciu liczby zmiennopozycyjnej.

### Punkty

Wybór dostępnych symboli oznaczających punkty jest znacznie szerszy. W przypadku większości funkcji punkty są nanoszone na wykres w postaci wypełnionych jednolitą barwą kropek. Aby dostosować ich kształt do naszych potrzeb, należy posłużyć się parametrem `marker`. Dostępne symbole, które wprowadzamy w postaci napisów, to: `"."`, `","`, `"o"`, `"v"`, `"^"`, `"<"`, `">"`, `"1"`, `"2"`, `"3"`, `"4"`, `"s"`, `"p"`, `"h"`, `"H"`, `"*"`, `"x"`, `"d"`, `"D"`.

## Określanie kolorów

Kolorystyka wykresów jest ważnym elementem prezentacji wyników, można to określić w wybrany sposób:

### Pełna nazwa lub literowy identyfikator koloru

Ustawiając wartość atrybutu `color` używając pełnej nazwy koloru lub jednoliterowego identyfikatora, możemy zmienić np. kolor wypełnienia wnętrza figury:

```python
t = np.linspace(0, np.pi, 2000, endpoint=False)
X = np.cos(3*t) * np.cos(t)
Y = np.cos(3*t) * np.sin(t)
plt.fill(X, Y, fill=True, color="tan")
plt.show()
```

Najważniejsze kolory i odpowiadające im identyfikatory prezentuje tabela:

|barwa                           |pełna nazwa          |identyfikator  |
|--------------------------------|-------------------- |---------------|
|czerwona                        |"red"              |"r"          |
|zielona                         |"green"            |"g"          |
|niebieska                       |"blue"             |"b"          |
|cyjan                           |"cyan"             |"c"          |
|magenta                         |"magenta"          |"m"          |
|żółta                           |"yellow"           |"y"          |
|czarna                          |"black"            |"k"          |
|biała                           |"white"            |"w"          |

Pełne nazwy kolorów, które możemy wykorzystać, możemy odczytać ze słownika:

```python
colors = matplotlib.colors.cnames
len(colors)
colors
```

### Definicja koloru przez paletę RGB

Innym sposobem określania koloru jest zastosowanie palety RGB, którą możemy definiować na dwa sposoby:


*   Zapis szesnastkowy "#rrggbb" (`#ffff00`) - każdy z elementów `rr` (czerwony), `gg` (zielony), `bb` (niebieski) określa intensywność dla każdego z kolorów, podawaną w przedziale od `00` do `ff`.
*   Zapis numeryczny, podanie krotki `(r,g,b)` - każdy z kolorów podawany jest z zakresu $[0,1]$, np. `color=(0.5,0.5,0.0)`.

### Przedziały szarości

Jeżeli w parametrze `color` umieścimy pojedynczą wartość numeryczną z przedziału $[0,1]$, otrzymamy odpowiedni poziom szarości. Wartość `1.0` określa kolor biały, a wartość `0.0` określa kolor czarny.

### Przezroczystość

Każdą z dostępnych barw możemy modyfikować, ustalając stopień jej przezroczystości. Argument `alpha` przyjmuje wartość z zakresu od 0 (przezroczysty) do 1 (całkowicie widoczny). Ponadto barwy półprzezroczyste możemy wprowadzać przy użyciu krotek typu `(r,g,b,a)`.

## Napisy formatujące

W funkcji `plot()` można w łatwiejszy sposób formatować kolor wykresu, styl linii czy punktory. Można to wykonać przy użyciu jednego napisu formatującego (ang. *format string*). Używa się tutaj oznaczeń przedstawionych w tabeli, np. zapis "`gp--`" oznacza, że stosujemy zielony kolor linii (`g`), punkty na wykresie będą pięciokątami (`p`), a linia będzie typu przerywanego (`--`).

```python
u = np.r_[-5:5:10j]
plt.plot(u, u**2, "gp--") # kolejno: x, y, format
plt.show()
```

### Wymiary osi

Wartości na osiach x (odciętych) i y (rzędnych) są automatycznie ustawiane na podstawie danych przekazanych do zaznaczenia na wykresie. Istnieje możliwość ręcznego ustawienia zakresu, podając odpowiednie argumenty: `xmin`, `xmax` dla osi x i `ymin`, `ymax` dla osi y.

Funkcja `axis()` pozwala zdefiniować wymiar przez podanie czteroelementowej listy `[xmin, xmax, ymin, ymax]`, lub można modyfikować wygląd wykresu na podstawie napisów, np.:
* `"off"` - wyłącza rysowanie osi układu współrzędnych oraz ich etykiet;
* `"equal"` - zachowuje proporcje między osiami (dzięki temu rysowany okrąg nie będzie przypominał elipsy);
* `"tight"` - dostosowuje zakres osi do danych, minimalizując marginesy.

```python
t = np.linspace(0, np.pi, 2000, endpoint=False)
X = np.cos(3*t) * np.cos(t)
Y = np.cos(3*t) * np.sin(t)
plt.axis("equal")
plt.xlim(xmin=-2, xmax=2)
plt.ylim(-2, 2)
plt.fill(X, Y, fill=True, facecolor="yellow", edgecolor='green', linewidth=2)
plt.show()
```

### Oznaczenie punktów na osiach

Jeżeli wykres wymaga nadania odpowiednich oznaczeń dla każdej z osi, można zastosować funkcje `xticks()` oraz `yticks()`. Jako argumenty przekazywane są listy o tej samej długości: pierwsza zawiera współrzędne punktów, a druga napisy.

```python
X = np.linspace(-2*np.pi, 2*np.pi, 200)
Y = np.cos(X)
plt.axis([-2.1 * np.pi, 2.1 * np.pi, -1.1, 1.1])
plt.xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
 ["-2\u03C0", "\u03C0", "0", r"$\pi$", r"$2\pi$"])
plt.yticks([-1, -0.5, 0, 0.5, 1])
plt.text(1,0.7, r"$f(x)=\cos(x)$", color="r")
plt.plot(X, Y, color="r")
plt.show()
```

### Legenda

Ważnym elementem wykresu jest legenda, która może zawierać opis każdego elementu wykresu w przypadku, kiedy tych elementów jest więcej. Do jej rysowania służy funkcja `legend()`. Każdy element wykresu można oznaczyć za pomocą atrybutu `label`.

```python
angle = np.linspace(0, 2*np.pi, 60)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'k-', label="sin(x)")
plt.plot(angle, np.cos(angle), 'r-.', label="cos(x)")
plt.legend()
plt.show()
```

Położenie legendy na wykresie możemy zmienić przy użyciu argumentu `loc`. Domyślnie jest to prawy górny róg wykresu (`"upper right"`), można jednak podać także `"best"` lub inną lokalizację (zob. dokumentację).

## Rysowanie wielu wykresów

### Wiele obiektów na jednym wykresie

Funkcje rysujące możemy wywoływać kolejno, jedna po drugiej - wówczas do tego samego rysunku dodawane będą nowe obiekty. Warto zaznaczyć, że w takim wypadku skala wartości na osiach odciętych (x) i rzędnych (y) zostanie automatycznie uzgodniona dla wszystkich składowych wykresu.

```python
angle = np.linspace(0, 2*np.pi, 200)
X = 3+2*np.sin(angle)
Y = 3+2*np.cos(angle)
plt.axis("equal")
plt.plot(X, Y, 'k')

X1 = np.array([0,0,1,1])
Y1 = np.array([0,1,1,0])
plt.fill(X1, Y1, color="#77A112")

X2 = np.linspace(-2*np.pi, 0, 100)
Y2 = np.sin(X2) + 5
plt.plot(X2, Y2, color="#2142A8")

X3 = np.r_[-8:-2:10j]
Y3 = np.random.normal(2,1.5,10)
plt.scatter(X3, Y3, color="#611248")

plt.text(-2, 7,'przykładowy tekst')
plt.show()
```

Innym sposobem tworzenia legendy jest przekazanie do funkcji `legend()` wybranych krzywych wraz z etykietami, co spowoduje opisanie tych krzywych na wykresie.

```python
angle = np.linspace(0, 2*np.pi, 60)
plt.axis("equal")
w1 = plt.plot(angle, np.sin(angle), 'k-')
w2 = plt.plot(angle, np.cos(angle), 'r-.')
w3 = plt.plot(angle, np.cos(angle)-0.5, 'b--')
plt.legend([w1[0], w2[0]], ["sin(x)","cos(x)"])
plt.show()
```

Funkcje `plot()` i `fill()` pozwalają na podanie macierzy z większą liczbą kolumn, które będą odpowiadać za każdy element wykresu.

```python
np.random.seed(113)
X = np.arange(100)
Y1 = np.random.normal(0,1,100).cumsum()
Y2 = np.random.normal(0,1,100).cumsum()
plt.plot(X, np.c_[Y1, Y2])
plt.show()
```

Podany powyżej efekt można uzyskać na podstawie podania wielu par wektorów x, y oraz formatujących napisów.

```python
plt.plot(X, Y1, "b-", X, Y2, "k--")
plt.show()
```

### Wiele wykresów na jednej stronie

Innym podejściem jest zamieszczenie wielu wykresów na jednej "stronie" czy na jednym rysunku. Rysowanie takich wykresów pomaga przy porównywaniu jednej zmiennej, ale pod różnym kątem (z różnych punktów widzenia).

### Podział strony na regiony

Podział strony działa podobnie jak tabela: zawiera kolumny i wiersze, a w każdej komórce możemy zamieścić oddzielny wykres. W tym celu stosuje się funkcję `subplot()`, do której jako argumenty podajemy liczbę wierszy i kolumn oraz numer podwykresu, na którym chcemy rysować. Podwykresy numerowane są wierszami, od góry do dołu.

*   Dwa wykresy jeden pod drugim (w dwóch wierszach)

```python
angle = np.linspace(0, 2*np.pi, 20)
plt.subplot(2,1,1)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'k-', label="sin(x)")
plt.legend()
plt.subplot(2,1,2)
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'r-.', label="cos(x)")
plt.legend()
plt.show()
```

* Dwa wykresy obok siebie (w dwóch kolumnach)

```python
angle = np.linspace(0, 2*np.pi, 20)
plt.subplot(1,2,1)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'k-', label="sin(x)")
plt.legend()
plt.subplot(1,2,2)
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'r-.', label="cos(x)")
plt.legend()
plt.show()
```

*  Cztery wykresy

```python
angle = np.linspace(0, 2*np.pi, 20)
plt.subplot(2,2,1)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'k-', label="sin(x)")
plt.legend()
plt.subplot(2,2,2)
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'r-.', label="cos(x)")
plt.legend()
plt.subplot(2,2,3)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'y--', label="sin(x)")
plt.legend()
plt.subplot(2,2,4)
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'g-', label="cos(x)")
plt.legend()
plt.show()
```

### Nieregularny podział strony

Wykorzystując funkcję `subplot2grid()`, możemy uzyskać mniej regularne podziały. W tym przypadku również obszar rysunku zostaje pokryty siatką o danej liczbie wierszy i kolumn, ale dzięki argumentom `rowspan` i `colspan` — możemy tworzyć podrysunki zajmujące więcej niż jedno pole:

```python
angle = np.linspace(0, 2*np.pi, 20)
plt.subplot2grid((3,4), (0,0), colspan=4)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'k-', label="sin(x)")
plt.legend()
plt.subplot2grid((3,4), (1,0), colspan=2, rowspan=2)
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'r-.', label="cos(x)")
plt.legend()
plt.subplot2grid((3,4), (1,2), colspan=2)
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'y--', label="sin(x)")
plt.legend()
plt.subplot2grid((3,4), (2,2))
plt.axis("equal")
plt.plot(angle, np.cos(angle), 'g-', label="cos(x)")
plt.legend()
plt.subplot2grid((3,4), (2,3))
plt.axis("equal")
plt.plot(angle, np.sin(angle), 'm-', label="sin(x)")
plt.legend()
plt.show()
```

### Synchronizacja osi układu współrzędnych

Przy użyciu argumentów `sharex` i `sharey` funkcji `subplot()` oraz `subplot2grid()` możemy sprawić, że podwykresy będą miały zsynchronizowane zakresy na wybranych osiach.

```python
np.random.seed(101)
X1 = np.random.normal(0, 1, 25)
X2 = np.random.normal(0, 1, 100)

# rysunek 1
ax1 = plt.subplot(2,2,1)
plt.vlines(np.arange(len(X1)), 0, X1)
plt.axhline(0, ls="-", color="k", alpha=0.5)
plt.setp(ax1.get_yticklabels(), visible=False)
plt.xticks([])

# rysunek 2
ax2 = plt.subplot(2,2,2, sharey=ax1)
plt.vlines(np.arange(len(X2)), 0, X2)
plt.axhline(0, ls="-", color="k", alpha=0.5)
ax2.xaxis.set_ticks_position("top")

# rysunek 3
ax3 = plt.subplot(2,2,3, sharex=ax1)
plt.plot(X1.cumsum(), "k-")

# rysunek 4
ax4 = plt.subplot(2,2,4, sharex = ax2, sharey=ax3)
plt.plot(X2.cumsum(), "k-")
ax4.yaxis.set_ticks_position("right")

plt.show()
```

## Graficzne przedstawianie danych

### Podstawowe wykresy dla danych jakościowych

Rozważmy badanie opinii społecznej, w którym stu ankietowanych zapytano o ich preferencje dotyczące owoców, wyniki prezentowały się następująco:

|Modele AI         |Liczba respondentów  |Procent   |
|------------------|---------------------|----------|
|GPT (openAI)      |	                 35|       35%|
|Gemini (Google)   |                   30|       30%|
|Claude (Anthropic)|                   20|    	 20%|
|DeepSeek	         |                   15|    	 15%|
|Razem             |  	              100|    	100%|

```python
p = [0.35, 0.3, 0.2, 0.15]
an = ["GPT", "Gemini", "Claude", "DeepSeek"]
```

### Wykresy słupkowe i kołowe

Zmienne takie jak wyżej najczęściej przedstawia się przy użyciu wykresu słupkowego (ang. bar plot), gdzie każdy słupek reprezentuje oddzielną kategorię, a jego wysokość lub długość odpowiada liczbie zaobserwowanych wartości danego rodzaju. Do sporządzenia takiego wykresu możemy użyć funkcji `bar()` z pakietu `matplotlib.pyplot`. Jako argumenty podajemy współrzędne lewych boków słupków, ich wysokości oraz szerokości.

Wykres kołowy (ang. pie chart) możemy narysować, wywołując funkcję `pie()`. W tym przypadku każda kategoria reprezentowana jest przez osobny wycinek koła o powierzchni proporcjonalnej do częstości występowania obserwacji.

```python
# wykres słupkowy
plt.subplot(1,2,1)
# współrzędne środków słupków
x = np.arange(len(p))
# szerokość słupka
s = 0.6
plt.bar(x-s/2, p, s, color =  ["0.25", "0.5", "0.7", "0.9"])
# wykres kołowy
plt.subplot(1,2,2)
plt.pie(p, labels=an, colors = ["0.25", "0.5", "0.7", "0.9"], shadow=True, startangle=65)
plt.axis("equal")
plt.title("preferencje modeli AI")
plt.show()
```

Dzięki metodzie `plot()` w klasie `pandas.Series` przy użyciu argumentu `kind` możemy również rysować wykres słupkowy i kołowy. Na przykład wartość "bar" i "barh" dadzą nam w wyniku wykres słupkowy, a "pie" - kołowy.

### Mapy ciepła

Mapy ciepła to graficzna reprezentacja danych macierzowych (dwuwymiarowych), w której poszczególne wartości przypisane są do odpowiednich kolorów. Zastosowanie map ciepła pozwala w łatwy sposób znaleźć minima i maksima w zbiorze danych, korelacje między danymi oraz zachodzące wzorce.

```python
flights = sns.load_dataset("flights")
flights_pivot = flights.pivot_table(index='month', columns='year', values='passengers', observed=False)
sns.heatmap(flights_pivot, annot=True, fmt=".0f", linewidths=0.5)
plt.show()
```

Bardzo często mapy ciepła stosuje się dla macierzy korelacji.

```python
iris = sns.load_dataset("iris")
cr_matrix = iris.corr(numeric_only=True)
sns.heatmap(cr_matrix, annot=True, cmap='YlGnBu')
plt.show()
```

## Wizualizacja niepewności

W przypadku każdych pomiarów o charakterze naukowym uwzględnienie ich niepewności jest prawie tak samo ważne, jeśli nie ważniejsze, jak dokładne podanie zmierzonej wartości.
Zakładając, że przeprowadzane jest badanie sprawdzające podatność użytkowników na phishing. Podstawowym wskaźnikiem jest odsetek osób, które kliknęły zawarty w wiadomości link, obliczony względem liczby użytkowników, którym wiadomość dostarczono. Porównanie tego wskaźnika między grupami, na przykład osobami po szkoleniu i bez szkolenia, pozwala ocenić różnice w reakcji na próbę phishingu. Wyniki można przedstawić na wykresie punktowym ze słupkami błędu oznaczającymi 95% przedziały ufności Wilsona, które pokazują niepewność oszacowania odsetka kliknięć.

### Słupki błędu

Jednym ze standardowych sposobów wizualizacji niepewności jest użycie tzw. słupków błędów. Najprostsze słupki błędów można utworzyć za pomocą pojedynczego wywołania funkcji:

```python
x = np.linspace(0, 10, 10)
dy = 0.8
y = np.sin(x) + dy * np.random.randn(10)
plt.errorbar(x, y, yerr=dy, fmt='.k');
```

Argument `fmt` zawiera kod formatu kontrolujący wygląd linii i punktów. Kod ten ma taką samą składnię jak kody stosowane w wywołaniach `plt.plot`. Oprócz podstawowych argumentów funkcja `errorbar` przyjmuje też wiele opcjonalnych parametrów, pozwalających precyzyjnie dostroić dane wyjściowe. Za ich pomocą można łatwo dostosować wygląd paska błędów.

```python
plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
ecolor='lightgray', elinewidth=3, capsize=0);
```