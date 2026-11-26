# uczenie nienadzorowane

## Przykładowe algorytmy

Algorytmy, które należą do uczenia nienadzorowanego:

* k-średnich (k-means)
* DBSCAN

### K-średnich (k-means)

K-średnich to algorytm należący do grupy algorytmów uczenia nienadzorowanego (ang. _Unsupervised Learning_). K-means nie jest algorytmem klasyfikacji, lecz klasteryzacji. Oznacza to, że algorytm ten w ogóle nie wie, czym jest „Zagrożenie”, a czym „Ruch normalny”.

#### Trenowanie modelu

W odróżnieniu od klasycznych klasyfikatorów do algorytmu k-means dostarczamy wyłącznie dane bez etykiet informujących, czy dany rekord jest poprawny, czy nie. Najpierw określamy, na jakich cechach (kolumnach) chcemy klasteryzować dane, a następnie normalizujemy je lub skalujemy tak, aby można było je w łatwy sposób porównywać. W kolejnym kroku określamy liczbę klastrów, do których zostaną przypisane dane.

Dla każdego klastra wyznaczany jest środek (centroid) – jest to średnia pozycja (środek ciężkości) wszystkich punktów należących do danego klastra. Najczęściej stosowane metody wyznaczania początkowych centroidów to:

* **Metoda losowa** – wybieramy losowo `K` punktów ze zbioru.
* **Metoda k-means++** – pierwszy punkt wybierany jest losowo, a kolejne z prawdopodobieństwem proporcjonalnym do kwadratu odległości od istniejących centroidów (preferowane są więc punkty bardziej oddalone).

Po tym etapie możemy dostarczyć nową próbkę i sprawdzić, do którego klastra zostanie przypisana.

Parametr `K` możemy dobrać na podstawie trzech metod:

**Metoda łokcia (Elbow Method)**

Metoda analizuje zależność pomiędzy liczbą klastrów a sumą kwadratów odległości punktów od centroidów, określaną jako WCSS (_Within-Cluster Sum of Squares_).

Wzór:

$$
WCSS = \sum_{j=1}^{K}\sum_{x_i \in C_j}\|x_i - \mu_j\|^2
$$

gdzie:

* `K` – liczba klastrów,
* C<sub>j</sub> – zbiór punktów należących do klastra `j`,
* x<sub>i</sub> – wektor cech analizowanego punktu,
* u<sub>j</sub> – centroid klastra `j`.

**Metoda sylwetki (Silhouette Score)**

Metoda ocenia, jak dobrze poszczególne punkty pasują do własnych klastrów w porównaniu z sąsiednimi klastrami. W przeciwieństwie do metody łokcia uwzględnia zarówno zwartość klastrów, jak i ich rozdzielenie.

Wzór:

$$
s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

gdzie:

* `a(i)` – średnia odległość punktu `i` od pozostałych punktów w jego klastrze,
* `b(i)` – najmniejsza średnia odległość punktu `i` od punktów innego klastra.

**Indeks Daviesa-Bouldina (Davies-Bouldin Index)**

Metoda bada, czy klastry są jednocześnie:

* zwarte, czyli punkty znajdują się blisko własnych centroidów,
* dobrze rozdzielone, czyli odległości między klastrami są odpowiednio duże.

Metoda jest szczególnie przydatna jako dodatkowe kryterium, ponieważ ocenia zarówno rozproszenie punktów, jak i separację klastrów.

Wzór:

$$
DB = \frac{1}{K}\sum_{i=1}^{K}\max_{j \ne i}
\left(\frac{S_i + S_j}{M_{ij}}\right)
$$

gdzie:

* S<sub>i</sub>, S<sub>j</sub> – miary rozproszenia punktów w klastrach `i` oraz `j`,
* M\_{ij} – odległość między centroidami klastrów `i` oraz `j`,
* `K` – liczba klastrów.

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

### Algorytm DBSCAN

*Techniki gęstościowe analizy skupień*, takie jak DBSCAN, przypominają intuicyjny sposób grupowania elementów przez człowieka. Algorytm ten wyróżnia się tym, że pozwala na identyfikację skupień o dowolnych kształtach i automatycznie rozpoznaje liczbę skupień w danych.

W prawdziwym Threat Huntingu **nie mamy kolumny `Label`** – nie wiemy z góry, które zdarzenia to ataki. Tu wchodzi uczenie nienadzorowane i algorytm **DBSCAN** (*Density-Based Spatial Clustering of Applications with Noise*).

#### Jak działa DBSCAN? (Wyjaśnienie krok po kroku)

W przeciwieństwie do K-Means, DBSCAN **nie każe nam zgadywać liczby klastrów**. Zamiast tego szuka gęstych skupisk punktów w przestrzeni, opierając się na zaledwie **dwóch parametrach**:
1. **`eps` ($\varepsilon$)** – promień sąsiedztwa wokół każdego punktu (jak daleko „sięga wzrok” algorytmu).
2. **`min_samples`** – minimalna liczba punktów, które muszą się znaleźć w promieniu `eps`, aby uznać dany obszar za gęsty klaster.

Na tej podstawie DBSCAN dzieli wszystkie zdarzenia (logi) na **3 kategorie**:
* **Punkt rdzeniowy (*Core Point*):** ma co najmniej `min_samples` sąsiadów w promieniu `eps` – to środek gęstego skupiska (np. typowy, codzienny ruch biurowy albo powtarzalny beaconing botnetu).
* **Punkt brzegowy (*Border Point*):** sam ma mniej niż `min_samples` sąsiadów, ale leży w zasięgu punktu rdzeniowego – należy do obrzeży klastra.
* **Szum / Anomalia (*Noise*, etykieta `-1`):** nie jest ani punktem rdzeniowym, ani brzegowym – to samotny punkt na uboczu. **W SOC etykieta `-1` to gotowy kandydat na alert (anomalię)!**

#### Dlaczego redukcja wymiarowości jest kluczowa przed DBSCAN?

DBSCAN liczy odległości między punktami. W przestrzeni 50 wymiarów (klątwa wymiarowości) wszystkie punkty stają się od siebie podobnie oddalone – algorytm „ślepnie” i oznacza niemal cały ruch jako szum `-1`. Dopiero po redukcji (np. Selekcja cech + t-SNE / UMAP) DBSCAN potrafi czysto rozdzielić:
* gęste klastry normalnego ruchu,
* osobne, ciasne klastry powtarzalnych ataków (np. skanowanie / C2),
* pojedyncze anomalie (`-1`).

Sprawdźmy to na żywo w poniższej komórce!

##### Przykładowa implementacja

```python
# EKSPERYMENT A: DBSCAN na surowych 50 wymiarach (klątwa wymiarowości w akcji!)
db_raw_50d = DBSCAN(eps=3.0, min_samples=15).fit(X_vis_50d)
unique_50d, counts_50d = np.unique(db_raw_50d.labels_, return_counts=True)
print("=== DBSCAN na surowych 50 cechach ===")
print("Wykryte klastry (etykieta: liczba zdarzeń):", dict(zip(unique_50d, counts_50d)))
print("-> Wniosek: w 50 wymiarach odległości się rozmywają, algorytm oznacza wszystko jako szum (-1)!\n")

# EKSPERYMENT B: DBSCAN na zredukowanych danych 2D po t-SNE (bez użycia etykiet y_vis!)
tsne_scaled = StandardScaler().fit_transform(tsne_2d)
db_2d = DBSCAN(eps=0.18, min_samples=15).fit(tsne_scaled)
db_labels = db_2d.labels_

# Analiza wykrytych klastrów (dopiero teraz podglądamy prawdziwe etykiety y_vis, żeby ocenić wynik)
print("=== DBSCAN na danych zredukowanych (Top 10 -> t-SNE 2D) ===")
cluster_summary = []
for cl in sorted(set(db_labels)):
    mask = (db_labels == cl)
    n_pts = mask.sum()
    n_att = y_vis[mask].sum()
    pct_att = (n_att / n_pts) * 100
    name = "Szum / Anomalie (-1)" if cl == -1 else f"Klaster {cl}"
    cluster_summary.append({
        "Grupa DBSCAN": name,
        "Liczba zdarzeń": n_pts,
        "Prawdziwe ataki": n_att,
        "Udział ataków [%]": round(pct_att, 1)
    })

summary_db_df = pd.DataFrame(cluster_summary)
print(summary_db_df.to_string(index=False))

# Wizualizacja: Co widzi analityk z DBSCAN (bez etykiet) vs Prawda (Ground Truth)
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Lewy wykres: Wynik DBSCAN (uczenie nienadzorowane)
palette_db = {cl: ('#000000' if cl == -1 else sns.color_palette("tab10")[cl % 10]) for cl in sorted(set(db_labels))}
sns.scatterplot(
    x=tsne_scaled[:, 0], y=tsne_scaled[:, 1], hue=db_labels,
    palette=palette_db, alpha=0.8, s=30, ax=axes[0]
)
axes[0].set_title("Wynik DBSCAN (czarne kropki = szum / anomalie -1)", fontsize=12)
axes[0].set_xlabel("t-SNE Wymiar 1 (skalowany)")
axes[0].set_ylabel("t-SNE Wymiar 2 (skalowany)")
axes[0].legend(title="Klaster DBSCAN", loc="best")

# Prawy wykres: Prawdziwe etykiety (Ground Truth)
sns.scatterplot(
    x=tsne_scaled[:, 0], y=tsne_scaled[:, 1], hue=y_vis,
    palette={0: '#a6bddb', 1: '#e31a1c'}, alpha=0.8, s=30, ax=axes[1]
)
axes[1].set_title("Prawdziwe etykiety (Ground Truth – do weryfikacji)", fontsize=12)
axes[1].set_xlabel("t-SNE Wymiar 1 (skalowany)")
axes[1].set_ylabel("t-SNE Wymiar 2 (skalowany)")
handles, _ = axes[1].get_legend_handles_labels()
axes[1].legend(handles, ['Benign (0)', 'Attack (1)'], title="Prawdziwy ruch")

plt.tight_layout()
plt.show()
```

DBSCAN to skuteczna metoda wykrywania skupień o dowolnych kształtach, szczególnie w obecności szumu. Nie wymaga definiowania liczby skupień, co odróżnia go od metod takich jak KMeans Algorytm działa dobrze na danych rzeczywistych, gdzie kształty skupień mogą być nieregularne.ień.

