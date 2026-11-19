# Uczenie nadzorowane

## Przykładowe algorytmy

Algorytmy należące do uczenia nadzorowanego:

* Drzewa decyzyjne
* Lasy losowe
* Naiwny klasyfikator Bayesa
* K-NN
* Maszyna wektorów nośnych (SVM)

### Drzewa decyzyjne

Drzewa decyzyjne to algorytm należący do uczenia nadzorowanego. Zasadę jego działania można porównać do gry „20 pytań”. Na każdym etapie zadajemy pytanie w stylu „Tak/Nie” i na tej podstawie dopasowujemy dane do odpowiednich kategorii.

Struktura algorytmu:
* **Pytanie główne – korzeń (ang. *Root*)** – np. czy adres IP pochodzi z Europy? W ten sposób odpowiednio dzielimy dane wejściowe.
* **Kolejne pytania – węzły (ang. *Nodes*)** – np. czy liczba nieudanych logowań wynosi $> 3$?
* **Ostatnie pytania – liście (ang. *Leaves*)** – pozwalają określić, do jakiej klasy przypisać dany rekord, np. „zagrożenie (1)” lub „ruch normalny (0)”.

Zaletą algorytmu jest fakt, że możemy przeanalizować poszczególne kroki podejmowania decyzji (model typu *white-box*).

#### Uczenie algorytmu

Algorytm przegląda wszystkie dostępne cechy (np. porty, liczbę pakietów, lokalizację) i szuka takiego podziału, który da najczystsze grupy. „Czystość” (ang. *Purity*) mierzy się za pomocą matematycznych kryteriów, takich jak entropia lub indeks Giniego. Model zatrzymuje się, gdy dotrze do liści zawierających zdarzenia tylko jednej klasy lub osiągnie z góry narzuconą maksymalną głębokość (żeby uniknąć zapamiętania danych na pamięć, czyli przeuczenia — ang. *overfitting*).

#### Algorytmy drzew decyzyjnych

Do budowy drzew decyzyjnych można zastosować różne algorytmy, m.in.: CART, ID3, C4.5, C5.0. Najczęściej stosowane są CART i ID3.

##### CART (Classification and Regression Tree)

W tym algorytmie cecha (kolumna) do podziału jest wybierana na podstawie wskaźnika Giniego. Wartość wskaźnika Giniego obliczana jest jako różnica między $1$ a sumą kwadratów prawdopodobieństw każdej klasy:

$$
G = 1 - \sum_{i=1}^{C} p_i^2
$$

gdzie:
* $G$ – wskaźnik Giniego,
* $C$ – liczba klas w zbiorze danych,
* $p_i$ – prawdopodobieństwo przynależności do klasy $i$.

**Wartości wskaźnika Giniego:**
* $G = 0$: Wszystkie elementy należą do jednej klasy (idealna czystość).
* $G = 0.5$: Elementy są równomiernie podzielone między dwie klasy (maksymalne zróżnicowanie dla klasyfikacji binarnej).
* $G \to 1$: Elementy są równomiernie rozłożone pomiędzy bardzo dużą liczbę klas.

Do kolejnego podziału wybierana jest cecha o najmniejszym wskaźniku Giniego.

Algorytm tworzy drzewa binarne, czyli w każdym węźle możemy odpowiedzieć tylko „tak” lub „nie”.

##### ID3 (Iterative Dichotomiser 3)

Algorytm opiera się na entropii. W każdym węźle oblicza, która cecha najbardziej zmniejszy chaos w danych, i to według niej dokonuje podziału.

$$
\text{IG} = H(D) - \sum_{i=1}^{n} \frac{|D_i|}{|D|} H(D_i)
$$

gdzie:
* $\text{IG}$ – przyrost informacji (ang. *Information Gain*),
* $H(D)$ – entropia przed podziałem danych,
* $H(D_i)$ – entropia dla części zbioru $D_i$ po podziale,
* $\frac{|D_i|}{|D|}$ – stosunek liczby elementów w podzbiorze $D_i$ do całkowitej liczby elementów w zbiorze $D$.

Entropia jest definiowana jako:

$$
H(D) = - \sum_{i=1}^{C} p_i \log_2(p_i)
$$

gdzie:
* $H(D)$ – entropia,
* $C$ – liczba klas,
* $p_i$ – prawdopodobieństwo przynależności do klasy $i$.

**Wartości entropii (dla klasyfikacji binarnej):**
* $H(D) = 0$: Wszystkie elementy należą do jednej klasy.
* $H(D) = 1$: Elementy są równomiernie rozłożone między dwie klasy.

Do podziału danych wybierana jest cecha o największym przyroście informacji.

Algorytm tworzy drzewo, w którym węzły nie muszą mieć tylko dwóch rozgałęzień, lecz w zależności od danych mogą mieć ich więcej.

#### Przykład działania algorytmu

Załóżmy sytuację z banku: dział bezpieczeństwa chce przygotować system do weryfikacji, czy konto mogło zostać przejęte:

1. Czy kraj logowania jest zgodny z profilem klienta?
   * **Tak:** Czy urządzenie jest zaufane?
     * **Tak:** przyznaj dostęp.
     * **Nie:** wyślij kod weryfikacyjny.
   * **Nie:** Czy w ostatniej minucie było $> 5$ błędnych prób logowania?
     * **Tak:** alarm — próba przejęcia konta.

#### Przykładowy kod

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import classification_report, confusion_matrix

# 1. PRZYGOTOWANIE DANYCH (Zabawkowy zbiór logowań)
# Cechy: [Liczba błędnych haseł, Czy kraj obcy (1=Tak), Godzina logowania (0-24)]
# Cel (Target): 1 = Atak (Zagrożenie), 0 = Normalny ruch
data = {
    'bledne_hasla': [0, 1, 0, 7, 5, 0, 1, 8, 0, 6],
    'obcy_kraj':    [0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
    'godzina':      [12, 14, 9, 3,  2, 18, 11, 4, 15, 2],
    'zagrozenie':   [0,  0,  0, 1,  1, 0,  0,  1, 0,  1]
}
df = pd.DataFrame(data)

X = df[['bledne_hasla', 'obcy_kraj', 'godzina']]
y = df['zagrozenie']

# 2. PODZIAŁ NA ZBIORY (Z zachowaniem proporcji klas - stratify!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. TRENING MODELU
# Ustawiamy max_depth=3, aby drzewo było proste i uniknęło przeuczenia (overfittingu)
clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# 4. OCENA WYNIKÓW
y_pred = clf.predict(X_test)
print("=== RAPORT KLASYFIKACJI ===")
print(classification_report(y_test, y_pred))

# 5. WIZUALIZACJA REGUŁ (Co wymyśliło drzewo?)
print("\n=== STRUKTURA WYUCZONEGO DRZEWA ===")
reguly = export_text(clf, feature_names=list(X.columns))
print(reguly)
```

### Lasy losowe

Lasy losowe (ang. *Random Forest*) to algorytm uczenia nadzorowanego, który wykorzystuje wiele drzew decyzyjnych (ang. *Decision Tree*) do podejmowania decyzji. Zamiast polegać na jednym drzewie decyzyjnym, budowany jest cały las drzew, a następnie łączone są ich przewidywania.

#### Uczenie algorytmu

Załóżmy, że mamy zbiór składający się z $10\,000$ wierszy logów. Do poszczególnych drzew nie jest przekazywany cały zbiór, lecz losowane są rekordy ze zwracaniem (z możliwością powtórzeń). Powoduje to, że niektóre rekordy nie trafią do danego drzewa. Następnie każde drzewo wykonuje trening nie na wszystkich dostępnych cechach, lecz na ich losowym podzbiorze (zazwyczaj jest to pierwiastek kwadratowy z liczby wszystkich cech). Cały proces trenowania przebiega tak samo jak dla zwykłych drzew decyzyjnych. Właściwe działanie i testowanie polega na przepuszczeniu danych przez wszystkie wytrenowane drzewa. Na końcu każde drzewo zwraca wynik, a ostateczna decyzja podejmowana jest na podstawie większości głosów.

#### Przykład działania

Załóżmy, że musimy podjąć decyzję kredytową, bazując na wytrenowanym lesie losowym, który składa się ze 100 drzew. Do algorytmu przekazujemy informacje o kredytobiorcy i możemy otrzymać następujący wynik:

1. Czy kredytobiorca może spłacić kredyt?
   * **Tak:** 79 głosów
   * **Nie:** 21 głosów

**Wynik:** decyzja kredytowa pozytywna.

#### Przykładowy kod

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. PRZYGOTOWANIE DANYCH (Symulacja logów z firewalla)
# Cechy: [Liczba pakietów, Rozmiar payloadu (bajty), Port docelowy]
# Target: 1 = Atak (Zagrożenie), 0 = Normalny ruch
data = {
    'liczba_pakietow': [10, 15, 12, 5000, 8, 11, 4500, 9, 14, 5200],
    'rozmiar_payloadu':[500, 600, 550, 1200, 480, 520, 1150, 490, 610, 1300],
    'port_docelowy':   [80, 443, 80, 22, 443, 80, 22, 443, 80, 22],
    'zagrozenie':      [0, 0, 0, 1, 0, 0, 1, 0, 0, 1] # Zaledwie 3 ataki na 10 zdarzeń
}
df = pd.DataFrame(data)

X = df[['liczba_pakietow', 'rozmiar_payloadu', 'port_docelowy']]
y = df['zagrozenie']

# 2. PODZIAŁ DANYCH
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. TRENING MODELU - LAS LOSOWY
# n_estimators=100 -> Tworzymy "komitet" 100 drzew decyzyjnych
# class_weight='balanced' -> BARDZO WAŻNE W SECURITY! Algorytm sam nakłada 
# wyższe kary za przeoczenie rzadkiej klasy (ataku).
rf_clf = RandomForestClassifier(
    n_estimators=100, 
    max_depth=5, 
    class_weight='balanced', 
    random_state=42
)
rf_clf.fit(X_train, y_train)

# 4. OCENA WYNIKÓW
y_pred = rf_clf.predict(X_test)
print("=== RAPORT KLASYFIKACJI (LAS LOSOWY) ===")
print(classification_report(y_test, y_pred))

# 5. CO JEST NAJWAŻNIEJSZE DLA MODELU? (Feature Importance)
print("\n=== WAŻNOŚĆ CECH W WYKRYWANIU ZAGROŻEŃ ===")
importances = rf_clf.feature_importances_
for name, importance in zip(X.columns, importances):
    print(f"{name}: {importance:.2%}")
```

### Naiwny klasyfikator Bayesa

Naiwny klasyfikator Bayesa to algorytm uczenia nadzorowanego, który stosuje twierdzenie Bayesa do wyliczenia prawdopodobieństwa przynależności obserwacji do określonej klasy.

Algorytm opiera się na twierdzeniu Bayesa, które w kontekście cyberbezpieczeństwa zadaje jedno konkretne pytanie: *Jakie jest prawdopodobieństwo, że ta wiadomość to phishing, pod warunkiem że widzę w niej słowa „pilne”, „hasło” i „zablokowane”?*

Algorytm przyjmuje skrajnie optymistyczne (a w rzeczywistości często błędne) założenie, że wszystkie cechy są od siebie całkowicie niezależne. Naiwny klasyfikator Bayesa zakłada, że wystąpienie w mailu słowa „zresetuj” nie ma absolutnie żadnego związku z wystąpieniem słowa „hasło”. Liczy prawdopodobieństwo dla każdego słowa z osobna, a na koniec po prostu je przez siebie mnoży.

#### Warianty algorytmu

Występują różne warianty tego klasyfikatora — ich wybór zależy od rodzaju danych, którymi dysponujemy:

* **Gaussian Naive Bayes (gaussowski)** – algorytm oblicza średnią oraz odchylenie standardowe dla każdej cechy w ramach danej klasy i na tej podstawie szacuje prawdopodobieństwo. Stosowany przy danych liczbowych (ciągłych), gdy cechy przyjmują wartości z rozkładu zbliżonego do normalnego (np. wzrost, waga, wiek, temperatura, pomiary z czujników).
* **Multinomial Naive Bayes (wielomianowy)** – algorytm najlepiej pracuje na danych dyskretnych i tekście (zliczanie elementów). Najczęściej stosuje się go w przetwarzaniu języka naturalnego (NLP) do analizy tekstu (np. zliczanie, ile razy dane słowo wystąpiło w dokumencie przy użyciu metod *Bag of Words* lub *TF-IDF*).
* **Bernoulli Naive Bayes (Bernoulliego)** – algorytm pracuje na danych binarnych. Sprawdza się, gdy cechy przyjmują tylko dwie wartości: tak/nie, prawda/fałsz lub 0/1 (np. czy dane słowo w ogóle występuje w e-mailu — bez względu na to, ile razy — albo czy klient posiada dany produkt).
* **Categorical Naive Bayes (kategoryczny)** – algorytm pracuje na danych kategorycznych (nominalnych). Stosowany jest dla cech, które dzielą obiekty na skończoną liczbę kategorii bez porządku liczbowego (np. kolor: czerwony, zielony, niebieski; dzień tygodnia; płeć; miasto).

#### Uczenie klasyfikatora

Algorytm nie trenuje się w klasyczny sposób, tworząc odpowiednie reguły czy wagi. W tym przypadku tworzony jest globalny słownik na podstawie danych historycznych. Dla zbioru treningowego wyliczane są częstości występowania danych słów, np. słowo „kliknij” występuje w $65\%$ wiadomości phishingowych i tylko w $5\%$ normalnych wiadomości. Stosowane jest też wygładzanie (np. Laplace'a) dla słów, które wcześniej nie wystąpiły. Model wykorzystuje wyuczone prawdopodobieństwa do obliczenia wyniku dla każdej klasy i wybiera tę o najwyższej wartości.

#### Przykładowy kod

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. PRZYGOTOWANIE DANYCH (Zabawkowy zbiór wiadomości SMS/Email)
# Target: 1 = Phishing (Zagrożenie), 0 = Normalna wiadomość (Ham)
data = {
    'tresc': [
        "Pilne! Zablokowano twoje konto w banku. Kliknij link aby odblokowac.",
        "Czesc, o ktorej dzisiaj idziemy na to spotkanie?",
        "Wygrałeś nowego iPhone! Odbierz nagrode pod tym adresem natychmiast.",
        "W załączeniu przesyłam raport finansowy za ubiegły miesiąc.",
        "Zresetuj swoje haslo do systemu klikajac w ponizszy odnosnik.",
        "Kupisz po drodze chleb i mleko?",
        "Twoja paczka zostala wstrzymana z powodu niedoplaty 2 PLN. Zaplac teraz.",
        "Dzięki za wczorajszą pomoc przy projekcie!"
    ],
    'phishing': [1, 0, 1, 0, 1, 0, 1, 0]
}
df = pd.DataFrame(data)

# 2. TRANSFORMACJA TEKSTU NA LICZBY (Worek Słów)
vectorizer = CountVectorizer()
# fit_transform uczy się słownika z naszych wiadomości i zamienia je na macierz liczb
X_wektory = vectorizer.fit_transform(df['tresc']) 
y = df['phishing']

# 3. PODZIAŁ DANYCH
X_train, X_test, y_train, y_test = train_test_split(
    X_wektory, y, test_size=0.25, random_state=42, stratify=y
)

# 4. TRENOWANIE MODELU - NAIWNY BAYES
# MultinomialNB domyślnie ma włączone wygładzanie Laplace'a (parametr alpha=1.0)
nb_clf = MultinomialNB(alpha=1.0)
nb_clf.fit(X_train, y_train)

# 5. OCENA WYNIKÓW
y_pred = nb_clf.predict(X_test)
print("=== RAPORT KLASYFIKACJI (NAIWNY BAYES) ===")
print(classification_report(y_test, y_pred))

# 6. TEST NA ŻYWO (Zobaczymy co model powie na nową wiadomość)
nowy_sms = ["Hej, zablokowano mi dostep, wyslij mi nowe haslo natychmiast!"]
# WAŻNE: Na nowych danych robimy TYLKO .transform(), a nie .fit_transform()!
nowy_sms_wektor = vectorizer.transform(nowy_sms)
werdykt = nb_clf.predict(nowy_sms_wektor)

print("\n=== TEST NA ŻYWO ===")
print(f"Wiadomość: '{nowy_sms[0]}'")
print(f"Werdykt modelu: {'PHISHING 🔴' if werdykt[0] == 1 else 'CZYSTE 🟢'}")
```

### K-NN

Algorytm $k$ najbliższych sąsiadów (ang. *k-Nearest Neighbors*, KNN) to klasyfikator z rodziny uczenia nadzorowanego, reprezentujący tzw. uczenie leniwe (ang. *lazy learning*). Algorytm jest prosty i intuicyjny do zaimplementowania. Często stosowany jest w systemach rekomendacyjnych, w których można polecać użytkownikowi np. filmy czy produkty do zakupu. W cyberbezpieczeństwie można go zastosować do analizy plików, które mogą zawierać złośliwe oprogramowanie. Innym przykładem jest analiza zachowania użytkowników (UEBA – *User and Entity Behavior Analytics*), czyli weryfikacja zachowań użytkowników na podstawie dotychczasowych doświadczeń i pomiarów.

#### Uczenie klasyfikatora

Klasyfikator podczas uczenia nie buduje żadnego modelu matematycznego, nie wylicza wag ani reguł — po prostu zapamiętuje dostarczone dane, dlatego nazywany jest algorytmem uczenia leniwego. Powoduje to, że jest pamięciożerny, ponieważ wszystkie dane przechowuje w pamięci.

Klasyfikacja polega na dostarczeniu nowej próbki i obliczeniu odpowiednich odległości od danych treningowych. Najczęstsze miary stosowane w algorytmie K-NN:

* **Euklidesowa:** $\sqrt{\sum_{i=1}^n (x_i - y_i)^2}$
* **Manhattan:** $\sum_{i=1}^n |x_i - y_i|$
* **Kosinusowa:** $1 - \frac{x \cdot y}{\|x\| \|y\|}$

Algorytm wymaga określenia liczby najbliższych sąsiadów, na podstawie których będzie klasyfikował nowy pomiar. Zalecane jest stosowanie nieparzystej liczby sąsiadów, np. $3, 5, 7, \dots, n$ (aby uniknąć remisów w głosowaniu).

Decyzja podejmowana jest na podstawie klasy reprezentowanej przez największą liczbę spośród $k$ najbliższych sąsiadów.

#### Przykładowy kod

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. PRZYGOTOWANIE DANYCH (Symulacja sesji sieciowych)
# Cechy: Czas trwania sesji (sekundy), Przesłane bajty, Liczba pakietów
# Target: 1 = Atak DDoS, 0 = Normalny ruch
data = {
    'czas_sesji': [12.5, 10.2, 0.5, 0.2, 15.0, 0.4, 22.1, 0.1, 14.5, 0.3],
    'przeslane_bajty': [4500, 3200, 85000, 92000, 5100, 88000, 6200, 95000, 4800, 90000],
    'liczba_pakietow': [30, 25, 1500, 1600, 40, 1550, 45, 1700, 35, 1650],
    'zagrozenie': [0, 0, 1, 1, 0, 1, 0, 1, 0, 1]
}
df = pd.DataFrame(data)

X = df[['czas_sesji', 'przeslane_bajty', 'liczba_pakietow']]
y = df['zagrozenie']

# 2. PODZIAŁ DANYCH
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. SKALOWANIE CECH (Krytyczny krok dla K-NN!)
# Sprowadzamy wszystkie cechy do tej samej skali (średnia 0, odchylenie standardowe 1)
scaler = StandardScaler()

# Uczymy skaler tylko na danych treningowych i od razu transformujemy
X_train_scaled = scaler.fit_transform(X_train)

# Dane testowe TYLKO transformujemy (nie uczymy na nich skalera - to byłby wyciek danych!)
X_test_scaled = scaler.transform(X_test)

# 4. INICJALIZACJA I "TRENING" MODELU K-NN
# Ustawiamy k=3 (nieparzysta liczba najbliższych sąsiadów)
knn_clf = KNeighborsClassifier(n_neighbors=3, metric='euclidean')

# Tu algorytm nie uczy się matematyki, tylko ładuje przeskalowane dane do pamięci
knn_clf.fit(X_train_scaled, y_train)

# 5. EWALUACJA
y_pred = knn_clf.predict(X_test_scaled)
print("=== MACIERZ POMYŁEK (K-NN) ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== RAPORT KLASYFIKACJI ===")
print(classification_report(y_test, y_pred))

# 6. TEST NA NOWYM PAKIECIE
nowy_pakiet = pd.DataFrame({'czas_sesji': [0.15], 'przeslane_bajty': [91000], 'liczba_pakietow': [1580]})

# Pamiętajmy: Nowe dane muszą przejść przez ten sam skaler!
nowy_pakiet_scaled = scaler.transform(nowy_pakiet)
decyzja = knn_clf.predict(nowy_pakiet_scaled)

print(f"\nWerdykt dla nowego pakietu: {'ATAK DDOS 🔴' if decyzja[0] == 1 else 'RUCH NORMALNY 🟢'}")
```

### Maszyna wektorów nośnych (SVM)

Maszyna wektorów nośnych (ang. *Support Vector Machine*, SVM) to algorytm uczenia maszynowego, którego głównym zadaniem jest znajdowanie granicy oddzielającej od siebie różne klasy danych.

Jest to algorytm uczenia nadzorowanego, czyli bazuje na danych historycznych, które są opisane (etykietowane). Zadaniem SVM jest wyznaczenie granicy decyzyjnej — w zależności od zastosowania może to być np. klasyfikacja ruchu sieciowego.

Algorytm opiera się na kilku ważnych pojęciach:

* **Hiperpłaszczyzna** – granica decyzyjna rozdzielająca dane na klasy. Jej wymiar zależy od liczby cech w zbiorze danych.
* **Wektory nośne** – punkty danych najbliższe hiperpłaszczyźnie, które definiują jej orientację i maksymalizują margines.
* **Margines** – największa odległość pomiędzy punktami danych dwóch klas a hiperpłaszczyzną. Szerszy margines oznacza bardziej stabilny model.

#### Typy jąder (ang. *Kernel*)

Wybór odpowiedniego jądra jest kluczowy dla skuteczności algorytmu i zależy od natury danych oraz rodzaju zadania.

**Typy:**
1. **Jądro liniowe (Linear)**
   * **Opis:** Stosowane, gdy dane są liniowo separowalne.
   * **Zalety:** Szybkie obliczeniowo i proste w interpretacji.
   * **Przykład zastosowania:** Analiza tekstu, klasyfikacja obrazów w niskowymiarowych przestrzeniach.
2. **Jądro RBF (gaussowskie, ang. *Gaussian*)**
   * **Opis:** Umożliwia modelowanie złożonych, nieliniowych zależności.
   * **Zalety:** Wszechstronne i skuteczne w większości nieliniowych problemów.
   * **Przykład zastosowania:** Rozpoznawanie obrazów, analiza bioinformatyczna.
3. **Jądro wielomianowe (Polynomial)**
   * **Opis:** Stosowane, gdy zależności między cechami mają charakter wielomianowy.
   * **Zalety:** Pozwala na modelowanie bardziej złożonych, nieliniowych zależności.
4. **Jądro sigmoidalne (Sigmoid)**
   * **Opis:** Często używane w zadaniach inspirowanych sieciami neuronowymi.
   * **Zalety:** Przydatne w zadaniach klasyfikacyjnych o bardziej specyficznych zależnościach.

Wybór jądra to kluczowy etap budowy modelu SVM. Eksperymenty z różnymi typami jąder i dostrajanie ich parametrów pozwalają na osiągnięcie najlepszego dopasowania do danych oraz maksymalizację skuteczności algorytmu.

#### Przykładowy kod

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

# 1. PRZYGOTOWANIE DANYCH (Profilowanie ruchu sieciowego)
data = {
    'req_per_min': [15, 20, 18, 500, 480, 22, 12, 510, 19, 530],
    'avg_size_kb': [5.2, 4.8, 5.0, 1.2, 1.5, 6.1, 4.5, 1.1, 5.5, 1.0],
    'zagrozenie':  [0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
}
df = pd.DataFrame(data)

X = df[['req_per_min', 'avg_size_kb']]
y = df['zagrozenie']

# 2. PODZIAŁ DANYCH
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. SKALOWANIE CECH
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. TRENOWANIE MODELU SVM
svm_clf = SVC(C=1.0, kernel='rbf', random_state=42)
svm_clf.fit(X_train_scaled, y_train)

# 5. EWALUACJA (Tekstowa)
y_pred = svm_clf.predict(X_test_scaled)
print("=== RAPORT KLASYFIKACJI (SVM) ===")
print(classification_report(y_test, y_pred))
print(f"Liczba wektorów nośnych: {sum(svm_clf.n_support_)}")
```