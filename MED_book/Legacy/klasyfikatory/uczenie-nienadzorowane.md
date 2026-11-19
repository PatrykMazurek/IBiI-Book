# Uczenie nienadzorowane

## Przykładowe algorytmy

Algorytmy, które należą do uczenia nienadzorowanego:
* k-średnich (k-means)

### K-średnich (k-means)

K-średnich to algorytm należący do grupy algorytmów uczenia nienadzorowanego (ang. *Unsupervised Learning*). K-means nie jest algorytmem klasyfikacji, lecz klasteryzacji. Oznacza to, że algorytm ten w ogóle nie wie, czym jest „Zagrożenie”, a czym „Ruch normalny”.

#### Trenowanie modelu

W odróżnieniu od klasycznych klasyfikatorów do algorytmu k-means dostarczamy wyłącznie dane bez etykiet informujących, czy dany rekord jest poprawny, czy nie. Najpierw określamy, na jakich cechach (kolumnach) chcemy klasteryzować dane, a następnie normalizujemy je lub skalujemy tak, aby można było je w łatwy sposób porównywać. W kolejnym kroku określamy liczbę klastrów, do których zostaną przypisane dane. 

Dla każdego klastra wyznaczany jest środek (centroid) – jest to średnia pozycja (środek ciężkości) wszystkich punktów należących do danego klastra. Najczęściej stosowane metody wyznaczania początkowych centroidów to:
* **Metoda losowa** – wybieramy losowo $K$ punktów ze zbioru.
* **Metoda k-means++** – pierwszy punkt wybierany jest losowo, a kolejne z prawdopodobieństwem proporcjonalnym do kwadratu odległości od istniejących centroidów (preferowane są więc punkty bardziej oddalone).

Po tym etapie możemy dostarczyć nową próbkę i sprawdzić, do którego klastra zostanie przypisana.

Parametr $K$ możemy dobrać na podstawie trzech metod:

**Metoda łokcia (Elbow Method)**

Metoda analizuje zależność pomiędzy liczbą klastrów a sumą kwadratów odległości punktów od centroidów, określaną jako WCSS (*Within-Cluster Sum of Squares*).

Wzór:
$$
WCSS = \sum_{j=1}^{K}\sum_{x_i \in C_j}\|x_i - \mu_j\|^2
$$

gdzie:
- $K$ – liczba klastrów,
- $C_j$ – zbiór punktów należących do klastra $j$,
- $x_i$ – wektor cech analizowanego punktu,
- $\mu_j$ – centroid klastra $j$.

**Metoda sylwetki (Silhouette Score)**

Metoda ocenia, jak dobrze poszczególne punkty pasują do własnych klastrów w porównaniu z sąsiednimi klastrami. W przeciwieństwie do metody łokcia uwzględnia zarówno zwartość klastrów, jak i ich rozdzielenie.

Wzór:
$$
s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

gdzie:
- $a(i)$ – średnia odległość punktu $i$ od pozostałych punktów w jego klastrze,
- $b(i)$ – najmniejsza średnia odległość punktu $i$ od punktów innego klastra.

**Indeks Daviesa-Bouldina (Davies-Bouldin Index)**

Metoda bada, czy klastry są jednocześnie:
- zwarte, czyli punkty znajdują się blisko własnych centroidów,
- dobrze rozdzielone, czyli odległości między klastrami są odpowiednio duże.

Metoda jest szczególnie przydatna jako dodatkowe kryterium, ponieważ ocenia zarówno rozproszenie punktów, jak i separację klastrów.

Wzór:
$$
DB = \frac{1}{K}\sum_{i=1}^{K}\max_{j \ne i}
\left(\frac{S_i + S_j}{M_{ij}}\right)
$$

gdzie:
- $S_i, S_j$ – miary rozproszenia punktów w klastrach $i$ oraz $j$,
- $M_{ij}$ – odległość między centroidami klastrów $i$ oraz $j$,
- $K$ – liczba klastrów.

#### Przykładowa implementacja (Python)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. PRZYGOTOWANIE DANYCH (Ruch sieciowy)
# Zwróć uwagę: NIE MA KOLUMNY "Zagrożenie"! Algorytm działa w ciemno.
# Mamy tu 2 grupy normalnego ruchu i 2 drastyczne anomalie na końcu.
data = {
    'liczba_pakietow': [100, 105, 95, 110, 90, 500, 520, 480, 510, 490, 50000, 52000],
    'rozmiar_sesji_kb': [5, 6, 4, 5, 7,  80, 85, 75, 82, 78, 9000, 9500]
}
df = pd.DataFrame(data)
X = df[['liczba_pakietow', 'rozmiar_sesji_kb']]

# 2. SKALOWANIE CECH (Krytyczne dla odległości geometrycznej!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. TRENOWANIE K-MEANS
# Zakładamy biznesowo, że ruch dzieli się na 2 normalne profile (np. www i poczta)
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(X_scaled)  # Przekazujemy TYLKO X!

# Przypisujemy każdemu pakietowi numer klastra, do którego trafił
df['klaster'] = kmeans.labels_

# 4. DETEKCJA ANOMALII (Szukanie zagrożeń)
# Zagrożeniem (anomalią) są pakiety, które leżą skrajnie daleko od centrum swojego klastra.
# Wyliczamy odległość każdego punktu od przypisanego mu centroidu (środka ciężkości).
odleglosci = kmeans.transform(X_scaled)

# Odległość do najbliższego centroidu (dla każdego wiersza wybieramy mniejszą wartość)
df['odleglosc_od_centrum'] = np.min(odleglosci, axis=1)

# Ustalamy próg - jeśli pakiet leży bardzo daleko (np. odległość > 2.5), to podnosimy alarm
prog_anomalii = 2.5
df['alarm_zero_day'] = df['odleglosc_od_centrum'].apply(lambda x: "TAK 🔴" if x > prog_anomalii else "NIE 🟢")

print("=== WYNIKI KLASTERYZACJI I DETEKCJI ANOMALII ===")
print(df)
```