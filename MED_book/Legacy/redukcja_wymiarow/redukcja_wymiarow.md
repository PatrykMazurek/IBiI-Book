# Redukcja wymiarów

Redukcja wymiarowości polega na przeskalowaniu dużej liczby atrybutów lub kolumn (cech) do mniejszej liczby atrybutów. Głównym celem tej techniki jest uzyskanie optymalnej liczby cech dla takich zadań, jak klasyfikacja, regresja czy inne metody uczenia maszynowego, w tym uczenia nienadzorowanego. W przypadku Cyberbezpieczeństwa redukcja wymiaó może pomóc przy pokazaniu normalnego ruchu od prawdziwych ataków.

#### Problem klątwy wymiarowości

W uczeniu maszynowym często spotykamy się z problemem zwanym klątwą wymiarowości, który odnosi się do bardzo dużej liczby cech w danych. Im większa liczba cech, tym większa ilość danych jest wymagana, co prowadzi do powstawania bardziej skomplikowanych modeli. Takie modele mogą być podatne na przetrenowanie, co obniża ich efektywność.

#### Jak redukcja wymiarowości rozwiązuje problem?

Redukcja wymiarowości pomaga rozwiązać problem klątwy wymiarowości poprzez przekształcanie danych w sposób liniowy lub nieliniowy.

- Przekształcenia liniowe:
  - Analiza głównych składowych (PCA);
  - Liniowa analiza dyskryminacyjna;
  - Analiza czynnikowa;

- Przekształcenia nieliniowe:
  - t-SNE (t-Distributed Stochastic Neighbor Embedding);
  - Mapy własne Hessego;
  - Osadzanie widmowe;
  - zometryczne mapowanie cech;

#### Zalety redukcji wymiarowości

- filtruje nadmiarowe i mniej istotne cechy, poprawiając jakość danych;
- obniża złożoność modelu, dzięki czemu łatwiej jest pracować z mniejszą liczbą wymiarów;
- zmniejsza zużycie pamięci i koszty obliczeniowe podczas budowy modelu;
- umożliwia wizualizację wielowymiarowych danych, co wspomaga ich interpretację.


## Analiza głównych składowych (PCA)

W dziedzinie uczenia maszynowego uznaje się, że duża ilość danych sprzyja budowie modeli predykcyjnych o wysokiej jakości. Jednak rozbudowane zestawy danych wiążą się także z problemem dużej liczby wymiarów, znanym jako klątwa wymiarowości. Duża liczba atrybutów zwiększa złożoność modeli predykcyjnych, co może prowadzić do przetrenowania i trudności w interpretacji wyników.

**Pułapka PCA** PCA maksymalizuje wariancję. W ruchu sieciowym największą wariancję mają normalne, głośne procesy (np. backupy, ruch HTTP). Cichy atak APT albo powolna eksfiltracja po DNS ma minimalną wariancję – ślepe PCA potrafi uznać go za szum i wyciąć w ostatniej składowej.

#### Czym jest PCA

Analiza głównych składowych (ang. Principal Component Analysis, PCA) to jedna z najczęściej stosowanych technik redukcji wymiarowości. Jej celem jest przekształcenie pierwotnego zestawu danych o dużej liczbie wymiarów w zbiór o mniejszej liczbie wymiarów, bez istotnej utraty informacji. PCA pomaga wykrywać wzorce i korelacje w danych, eliminując nadmiarowość wynikającą z silnie skorelowanych atrybutów.

#### Jak działą PCA

Główne zadania PCA to:

* Wykrywanie związków i korelacji pomiędzy atrybutami – PCA identyfikuje silnie skorelowane atrybuty, które mogą wprowadzać nadmiarowość. Nadmiarowe cechy są usuwane lub zastępowane nowymi zmiennymi reprezentującymi ich wspólne informacje.
* Redukcja liczby wymiarów – Przy dużej liczbie atrybutów, np. 200 kolumn w zestawie danych, analiza i modelowanie stają się trudne. PCA redukuje tę liczbę do mniejszej, np. 10 lub 20 zmiennych, zachowując kluczowe informacje.

#### Przykładowy kod

```python
# PCA wymaga wcześniejszej standaryzacji danych!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Redukcja do 10 głównych składowych
pca = PCA(n_components=10, random_state=42)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

start = time.time()
rf_pca = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_pca.fit(X_train_pca, y_train)
train_time_pca = time.time() - start

y_pred_pca = rf_pca.predict(X_test_pca)
f1_pca = f1_score(y_test, y_pred_pca)
prec_pca = precision_score(y_test, y_pred_pca)
rec_pca = recall_score(y_test, y_pred_pca)

results.append({
    "Podejście": "PCA (10 składowych)",
    "Liczba cech": 10,
    "Czas treningu [s]": round(train_time_pca, 3),
    "F1-score": round(f1_pca, 4),
    "Precision": round(prec_pca, 4),
    "Recall": round(rec_pca, 4),
    "Interpretowalność": "Niska (Black Box)"
})

print("[PCA - 10 składowych]")
print(f"Czas treningu:       {train_time_pca:.3f} s")
print(f"F1-score:            {f1_pca:.4f} (Precision: {prec_pca:.4f}, Recall: {rec_pca:.4f})")
print(f"Zachowana wariancja: {pca.explained_variance_ratio_.sum():.1%}\n")

# Symulacja alertu w konsoli SOC dla pierwszego wykrytego ataku
attack_idx = np.where(y_pred_pca == 1)[0][0]
pca_alert = pd.Series(X_test_pca[attack_idx], index=[f'PC{i}' for i in range(1, 11)])
print("--- ALERT W KONSOLI SOC (DANE WEJŚCIOWE PO PCA) ---")
print(pca_alert.round(2).to_string())
```

## Analiza skupień

*Analiza skupień* polega na grupowaniu podobnych do siebie elementów. Przykładami zastosowań analizy skupień są:
- grupowanie podobnych produktów,
- grupowanie podobnych artykułów lub dokumentów,
- grupowanie podobnych klientów w zadaniach segmentacji rynku.

Głównym celem analizy skupień jest:

1. Minimalizacja odległości wewnątrz skupień – dystansu pomiędzy punktami danych w ramach tej samej grupy.
2. Maksymalizacja odległości pomiędzy skupieniami – dystansu między różnymi grupami danych.

Kluczowe pojęcia:
- *Odległość wewnątrz skupienia*: oznacza dystans pomiędzy punktami w obrębie danej grupy danych.
- *Odległość między skupieniami*: określa dystans pomiędzy różnymi grupami danych.

Warto zauważyć, że punkty danych są *nieoznakowane*, co sprawia, że analiza skupień jest zadaniem uczenia nienadzorowanego.

Istnieje wiele metod analizy skupień, z których każda grupuje dane w inny sposób. Dobór odpowiedniej metody zależy od charakteru danych i celu analizy.

#### Przykłądowy kod

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(24)
group1 = np.random.normal(loc=[2, 7], scale=0.5, size=(50, 2))
group2 = np.random.normal(loc=[5, 6], scale=0.5, size=(50, 2))
group3 = np.random.normal(loc=[4, 9], scale=0.5, size=(50, 2))

# Rysowanie punktów w różnych grupach
plt.figure(figsize=(10, 7))
plt.scatter(group1[:, 0], group1[:, 1], label='Grupa 1', alpha=0.7)
plt.scatter(group2[:, 0], group2[:, 1], label='Grupa 2', alpha=0.7)
plt.scatter(group3[:, 0], group3[:, 1], label='Grupa 3', alpha=0.7)

# Ustawienia wykresu
plt.title('Różne Grupy Punktów')
plt.xlabel('Cecha 1')
plt.ylabel('Cecha 2')
plt.legend()
plt.grid()
plt.show()
```

W jaki sposób można określić podobieństwo pomiędzy dwoma punktami danych, aby można było je przypisać do tego samego skupienia. Aby wyznaczyć podobieństwo lub jego brak, wykorzystujemy *miary odległości*, takie jak:

- Odległość euklidesowa:
  $$
  d_{euclidean} = \sqrt{\sum_{i=1}^k (x_i - y_i)^2}
  $$
- Odległość miejska (Manhattan):
  $$
  d_{manhattan} = \sum_{i=1}^k |x_i - y_i|
  $$
- Odległość Minkowskiego:
  $$
  d_{minkowski} = \left( \sum_{i=1}^k (|x_i - y_i|)^q \right)^{\frac{1}{q}}
  $$
W powyższych wzorach:
- $x_i$ i $y_i$ to współrzędne punktów w $k$-wymiarowej przestrzeni,
- $q$ to parametr odległości Minkowskiego, który definiuje jej charakter (np. dla $q=2$ staje się odległością euklidesową, a dla $q=1$ odległością miejską).

Miary te obliczają dystans pomiędzy dwoma punktami w przestrzeni wielowymiarowej, co pozwala określić ich podobieństwo.

#### Wyznaczenie liczby skupień

Jednym z najważniejszych problemów analizy skupień jest określenie liczby skupień w zestawie danych. Nie istnieje uniwersalny sposób na znalezienie odpowiedniej liczby grup, a różne algorytmy wymagają różnych podejść:
- W *hierarchicznej analizie skupień* i *algorytmie DBSCAN* liczby skupień nie trzeba definiować z góry.
- W algorytmach takich jak *centroidy*, *k-medioidy* oraz *widmowa analiza skupień* liczba skupień musi być zdefiniowana.

Wyznaczanie optymalnej liczby skupień nie jest proste. W tym celu można zastosować następujące techniki:
- *metoda łokcia*,
- *metoda profilu*.

##### **Metoda łokcia**

*Metoda łokcia* (ang. *elbow method*) jest jedną z najpopularniejszych technik określania liczby skupień. Polega na analizie odsetka wariancji wyjaśnionej przez poszczególne liczby skupień. Celem jest znalezienie takiej liczby grup, przy której dodanie kolejnego skupienia nie powoduje już znaczącej redukcji wariancji.

Miara używana w tej metodzie to *wewnątrzgrupowa suma kwadratów* (ang. *Within-Cluster Sum of Squares*, WCSS), znana również jako *bezwładność*. Jej wzór wygląda następująco:
$$
WCSS = \sum_{j=1}^k \sum_{i=1}^n \text{odległość}^2(x_i, C_j)
$$
gdzie:
- $C_j$ to centroid skupienia $j$,
- $x_i$ to punkty danych w danym skupieniu.

##### Przykładowy kod

```python
#ignorujemy ostrzeżenia
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# tworzymy ramkę danych
data = pd.DataFrame({"X": [12, 15, 18, 10, 8, 9, 12, 20],
                     "Y": [6, 16, 17, 8, 7, 6, 9, 18]})

# lista przechowująca wartości WCSS
wcss_list = []

# realizujemy pętlę dla różnych liczb skupień
for i in range(1, 6):
    # tworzy i dopasowuje model KMeans
    kmeans_model = KMeans(n_clusters=i, random_state=44)
    kmeans_model.fit(data)
    # dodaje wskaźnik WCSS (bezwładność) skupień do listy
    wcss_list.append(kmeans_model.inertia_)

# tworzymy wykres metody łokcia
plt.plot(range(1, 6), wcss_list, marker='*')
plt.title('Wybór optymalnej liczby skupień za pomocą metody łokcia')
plt.xlabel('Liczba skupień (k)')
plt.ylabel('Wewnątrzgrupowa suma kwadratów (bezwładność)')
plt.show()
```

##### **Metoda Profilu**

*Metoda profilu* (ang. *silhouette method*) służy do oceny i weryfikacji jakości skupień. Pozwala określić, jak dobrze każdy punkt danych został sklasyfikowany.

Wykres wskaźnika profilu pokazuje:
- Jak ściśle punkty danych są pogrupowane wewnątrz skupienia.
- Jak dokładnie poszczególne skupienia są rozdzielone.

Możemy w ten sposób określić optymalną liczbę skupień.

**Wskaźnik profilu**

Wartość wskaźnika profilu mieści się w przedziale od $-1$ do $1$:
- Dodatnia wartość oznacza dobrze oddzielone skupienia.
- Ujemna wartość wskazuje niewłaściwie przypisane punkty danych.
- Wartość $0$ sugeruje, że punkty znajdują się na granicy dwóch skupień.
Równanie wskaźnika profilu przedstawia się następująco:
$$
S(i) = \frac{b_i - a_i}{\max(b_i, a_i)}
$$
gdzie:
- $a_i$ – średnia odległość $i$-tego punktu danych od pozostałych punktów w swoim skupieniu.
- $b_i$ – średnia odległość $i$-tego punktu danych od punktów w pozostałych skupieniach.

**Wnioski**:
* Wartość $S(i)$ mieści się w przedziale $[-1, 1]$.
* Aby $S(i)$ było bliskie $1$, zmienna $a_i$ musi być bardzo mała w stosunku do $b_i$ ($a_i << b_i$).

##### Przykładowy kod

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# tworzymy ramkę danych
data = pd.DataFrame({"X": [12, 15, 18, 10, 8, 9, 12, 20],
                     "Y": [6, 16, 17, 8, 7, 6, 9, 18]})

# lista przechowująca wskaźniki profilu
score_list = []

# obliczamy wskaźnik profilu dla różnych liczby skupień
for i in range(2, 6):
    # tworzy i dopasowuje model KMeans
    kmeans_model = KMeans(n_clusters=i, random_state=123)
    kmeans_model.fit(data)

    # uzyskuje przewidywania
    pred = kmeans_model.predict(data)

    # oblicza wskaźnik profilu
    score = silhouette_score(data, pred, metric='euclidean')

    # dodaje wskaźnik profilu do listy
    score_list.append(score)

# tworzymy wykres współczynnika profilu
plt.bar(range(2, 6), score_list)
plt.title('Wykres profilu')
plt.xlabel('Liczba skupień (k)')
plt.ylabel('Współczynniki profilu')
plt.show()
```

## Selekcja cech (Feature Selection)

Selekcja cech (Feature Selection) polega na wybraniu podzbioru oryginalnych kolumn z danych i odrzuceniu reszty (szumu oraz duplikatów). W przeciwieństwie do ekstrakcji cech (jak PCA), nic tu nie przekształcamy ani nie mieszamy

W uczeniu maszynowym selekcję cech dzieli się na trzy główne rodziny metod:

#### Metody filtrujące (Filter Methods)

Oceniana jest cecha czy kolumna na podstawie tylko statysytk:
* Próg wariancji (Variance Threshold): usuwane są kolumny, które prawie zawsze mają tę samą wartość (np. `Protocol_Version` = IPv4 w 99,9% logów nic nie wnosi).
* Macierz korelacji: jeśli dwie kolumny są ze sobą skorelowane w 98% (np. `Bytes_Sent` i `Packets_Sent`), jedną z nich jest usuwana, bo niesie tę samą informację.
* Testy statystyczne (Chi-Square, ANOVA, Mutual Information): sprawdzają, jak silny związek ma dana kolumna z etykietą ataku.

#### Metody opakowujące (Wrapper Methods)

Model jest wyznacznikiem najlepszej liczby kolumn. Model testuje różne kombinacje i sprawdzany jest wybnik F1-score

* RFE (Recursive Feature Elimination): trenuje model na wszystkich cechach, usuwając najsłabszą, trenuje ponownie i powtarza proces, aż zostanie np. Top 10 kolumn.
* Forward / Backward Selection: stopniowe dokładanie (lub odejmowanie) pojedynczych cech i mierzenie, czy jakość detekcji rośnie.

#### Metody wbudowane (Embedded Methods)

Selekcja dzieje się automatycznie w trakcie treningu samego modelu – algorytm sam uczy się, które kolumny są przydatne, a które ignorować:
* Drzewa decyzyjne i lasy losowe: podczas dzielenia danych model oblicza ważność każdej cechy (feature_importances_).
* Regularyzacja L1 (Lasso): w modelach liniowych nakłada „karę” na wagi cech, Kolumny, które uzna za szum nakłada wagę zero.

##### Przykładowy kod

```python
# Wyciągamy Top 10 najważniejszych cech z modelu bazowego
importances = pd.Series(rf_base.feature_importances_, index=X_train.columns)
top_10_features = importances.nlargest(10).index.tolist()

# Wizualizacja Top 10 cech
plt.figure(figsize=(9, 4.5))
importances.nlargest(10).sort_values().plot(kind='barh', color='#2b5c8f')
plt.title("Top 10 cech wykrywających atak (Feature Selection)")
plt.xlabel("Ważność cechy (Gini importance)")
plt.tight_layout()
plt.show()

# Trening na zredukowanym zbiorze (10 cech)
start = time.time()
rf_sel = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_sel.fit(X_train[top_10_features], y_train)
train_time_sel = time.time() - start

y_pred_sel = rf_sel.predict(X_test[top_10_features])
f1_sel = f1_score(y_test, y_pred_sel)
prec_sel = precision_score(y_test, y_pred_sel)
rec_sel = recall_score(y_test, y_pred_sel)

results.append({
    "Podejście": "Feature Selection (Top 10)",
    "Liczba cech": 10,
    "Czas treningu [s]": round(train_time_sel, 3),
    "F1-score": round(f1_sel, 4),
    "Precision": round(prec_sel, 4),
    "Recall": round(rec_sel, 4),
    "Interpretowalność": "Bardzo wysoka"
})

print("[FEATURE SELECTION - 10 cech]")
print(f"Czas treningu:  {train_time_sel:.3f} s (przyspieszenie: {train_time_base / train_time_sel:.2f}x)")
print(f"F1-score:       {f1_sel:.4f} (Precision: {prec_sel:.4f}, Recall: {rec_sel:.4f})")
```

## Ocena jakości analizy skupień

Ocena jakości analizy skupień jest kluczowym etapem weryfikacji skuteczności algorytmu grupowania. Mimo że ocena technik uczenia nienadzorowanego jest trudnym zadaniem, dostępne są różne metody, które można podzielić na dwie główne kategorie:
* Wewnętrzna ocena jakości,
* Zewnętrzna ocena jakości.

### Wewnętrzna ocena jakości

##### Indeks Daviesa-Bouldina

*Indeks Daviesa-Bouldina* (DBI) mierzy stosunek odległości wewnątrzgrupowej do odległości międzygrupowej. Mniejsza wartość DBI oznacza lepsze wyniki.
$$
DBI = \frac{1}{n} \sum_{i=1}^{n} \max_{i \neq j} \left( \frac{\sigma_i + \sigma_j}{d(c_i, c_j)} \right)
$$
gdzie:
- $n$ – liczba skupień,
- $c_i$ – centroid skupienia $i$,
- $\sigma_i$ – średnia odległość punktów od centroidu $c_i$ (odległość wewnątrzgrupowa),
- $d(c_i, c_j)$ – odległość między centroidami $c_i$ i $c_j$ (odległość międzygrupowa).

##### Współczynnik profilu

Współczynnik profilu mierzy podobieństwo punktów w skupieniu do pozostałych punktów w tym samym skupieniu oraz do punktów w sąsiadujących skupieniach. Wyższa wartość oznacza lepsze wyniki.

$$
S(i) = \frac{b_i - a_i}{\max(a_i, b_i)}
$$

Gdzie:
- $a_i$ – średnia odległość punktu $i$ do innych punktów w jego skupieniu,
- $b_i$ – średnia odległość punktu $i$ do punktów w najbliższym sąsiadującym skupieniu.

### Zewnętrzna ocena jakości

##### Współczynnik Randa

Mierzy podobieństwo skupień do klasyfikacji wzorcowej na podstawie odsetka właściwych decyzji.
$$
RI = \frac{PP + PN}{PP + PN + FP + FN}
$$
gdzie:
- $PP$ – liczba prawdziwie pozytywnych,
- $PN$ – liczba prawdziwie negatywnych,
- $FP$ – liczba fałszywie pozytywnych,
- $FN$ – liczba fałszywie negatywnych.


##### Indeks Jaccarda

Mierzy podobieństwo między dwoma zbiorami danych.
$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$
Wartości przyjmowane przez współczynnik Jaccarda zawierają się w podzbiorze zbioru liczb rzeczywistych $[0,1]$. Jeśli współczynnik Jaccarda przyjmuje wartości bliskie zeru, zbiory są od siebie różne, natomiast gdy jest bliski $1$, zbiory są do siebie podobne.

##### Wskaźnik F1

Średnia harmoniczna precyzji i czułości.
$$
F_{\beta} = \frac{(1 + \beta^2) \cdot \text{precyzja} \cdot \text{czułość}}{\beta^2 \cdot \text{precyzja} + \text{czułość}}
$$
Gdzie $\beta$ kontroluje względne znaczenie precyzji i czułości.

##### Wskaźnik Fowlkesa-Mallowsa

Średnia geometryczna precyzji i czułości:
$$
FM = \sqrt{\text{precyzja} \cdot \text{czułość}}
$$

