# Nauczanie nadzorowane

## Przykładowe algorytmy 
    
Algorytmy, które należą do nauczania nadzorowanego:

* Drzewa losowe
* Lasy losowe
* Naiwny klasyfikator Bayesa
* K-NN
* Maszyna wektorów nośnych (SVN)

### Drzewa decyzyjne

Algorytm należący do nauczania nadzorowanego. Zasadę działania można porównać do gry "20 pytań". Na każdym etapie zadajemy pytanie w stylu "Tak/Nie" i na tej podstawie dopasowujemy dane do odpowiednich kategorii. 

Struktura algorytmu:
* **Pytanie główne – korzeń (Root)** - np. czy adres IP pochodzi z Europy? W ten sposób odpowiednio dzielimy dane wejściowe.
* **Kolejne pytania – węzły (Node)** - np. czy liczba nieudanych logowań > 3?
* **Ostatnie pytania – liście (Leaves)** - pozwalają określić, do jakiej klasy przypisać dany rekord, np. "zagrożenie (1)" lub "ruch normalny (0)".

Zaletą algorytmu jest fakt, że możemy przeanalizować poszczególne kroki podejmowania decyzji (model typu white-box). 

#### Uczenie algorytmu

Algorytm przegląda wszystkie dostępne cechy (np. porty, liczba pakietów, lokalizacja) i szuka takiego podziału, który da najczystsze grupy. "Czystość" (Purity) mierzy się za pomocą matematycznych kryteriów, takich jak Entropia lub Indeks Gini. Model zatrzymuje się, gdy dotrze do liści zawierających zdarzenia tylko jednej klasy lub osiągnie z góry narzuconą maksymalną głębokość (żeby uniknąć zapamiętania danych na pamięć, czyli przeuczenia).

#### Algorytmy drzew decyzyjnych

Do budowy drzew decyzyjnych można zastosować przykładowe algorytmy: CART, ID3, C4.5, C 5.0. najczęściej stosowane są CART i ID3

##### CART (Classification and Regression Tree)

CART (Classification and Regression Tree) - w tym algorytmie cecha (kolumna) do podziału jest wybierana na podstawie wskaźnika Giniego. Wartość wskaźnika Giniego obliczana jest jako różnica między sumą kwadratów prawdopodobieństw każdej klasy a 1:

$$
G = 1 - \sum_{i=1}^{C} p_i^2
$$

Gdzie:
- $G$ – wskaźnik Giniego.
- $C$ – liczba klas w zbiorze danych.
- $p_i$ – prawdopodobieństwo przynależności do klasy $i$.

**Wartości wskaźnika Giniego:**
- $G = 0$: Wszystkie elementy należą do jednej klasy.
- $G = 1$: Elementy są równomiernie rozłożone pomiędzy klasy.
- $G = 0.5$: Elementy są równomiernie podzielone między dwie klasy.

Cecha o najmniejszym wskaźniku Giniego jest wybierana do kolejnego podziału.

Algorytm tworzy drzewa binarne, czyli w każdym węźle możemy odpowiedzieć tylko "tak" lub "nie".

##### ID3 (Iterative Dichotomiser 3)

ID3 (Iterative Dichotomiser 3) - algorytm opiera się na entropi, w każdym węźle liczy, która cecha najbardziej zmniejszy chaos w danych i to po niej dokonuje podziału.

$$
\text{IG} = H(D) - \sum_{i=1}^{n} \frac{|D_i|}{|D|} H(D_i)
$$

Gdzie:
- $\text{IG}$ – przyrost informacji (ang. *Information Gain*).
- $H(D)$ – entropia przed podziałem danych.
- $H(D_i)$ – entropia dla części zbioru $D_i$ po podziale.
- $\frac{|D_i|}{|D|}$ – stosunek liczby elementów w podzbiorze $D_i$ do całkowitej liczby elementów w zbiorze $D$.

Entropia jest definiowana jako:

$$
H(D) = - \sum_{i=1}^{C} p_i \log_2(p_i)
$$
gdzie:
- $H(D)$ – entropia.
- $C$ – liczba klas.
- $p_i$ – prawdopodobieństwo przynależności do klasy $i$.

**Wartości entropii:**
- $H(D) = 0$: Wszystkie elementy należą do jednej klasy.
- $H(D) = 1$: Elementy są równomiernie rozłożone między klasy.

Cecha o największym przyroście informacji jest wybierana do podziału danych.

Algorytm tworzy drzewo, w których węzły nie miszą mieć tylko dwóch roześć tylko w zależści od danych mogą mieć wiecej.

#### Przykład działania algorytmu

Załóżmy sytuację z banku: dział bezpieczeństwa chce przygotować system do weryfikacji, czy konto mogło zostać przejęte:

1. Czy kraj logowania jest zgodny z profilem klienta?
  * Tak: Czy urządzenie jest zaufane?
    * Tak: daj dostęp 
    * Nie: wyślij kod weryfikacyjny
  * Nie: Czy w ostatniej minucie było >5 błędnych prób logowania?
    * Tak: alarm, próba przejęcia konta

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

Lasy losowe (Random Forest) to algorytm uczenia nadzorowanego, który wykorzystuje wiele drzew decyzyjnych (Decision Tree) do podejmowania decyzji. Zamiast polegać na jednym drzewie decyzyjnym, budowany jest cały las drzew, a następnie łączone są ich przewidywania.

#### Uczenie algorytmu 

Zakładając, że mamy zbiór składający się z 10 000 wierszy logów: do poszczególnych drzew nie jest przekazywany cały zbiór, lecz losowane są rekordy z możliwością powtórzeń. Powoduje to, że niektóre rekordy nie trafią do danego drzewa. Następnie każde drzewo wykonuje trening nie na wszystkich dostępnych cechach, tylko na losowych (zazwyczaj jest to pierwiastek kwadratowy z liczby wszystkich cech). Cały proces trenowania przebiega tak samo jak dla zwykłych drzew decyzyjnych. Właściwe działanie i testowanie polega na przepuszczeniu danych przez wszystkie wytrenowane drzewa. Na końcu każde drzewo zwraca wynik, a ostateczna decyzja podejmowana jest na podstawie większości głosów.

#### Przykład działania

Załóżmy, że musimy podjąć decyzję kredytową, bazując na wytrenowanym lesie losowym, który składa się ze 100 drzew. Do algorytmu przekazujemy informacje o kredytobiorcy i możemy otrzymać następujący wynik:
1. Czy kredytobiorca może spłacić kredyt?
  * Tak: 79 głosów
  * Nie: 21 głosów

Wynik: Decyzja kredytowa pozytywna

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
Algorytm opiera się na twierdzeniu Bayesa, które w kontekście cyberbezpieczeństwa zadaje jedno, konkretne pytanie: Jakie jest prawdopodobieństwo, że ta wiadomość to phishing, pod warunkiem, że widzę w niej słowa "pilne", "hasło" i "zablokowane"?

Algorytm przyjmuje skrajnie optymistyczne (a w rzeczywistości często błędne) założenie, że wszystkie cechy są od siebie całkowicie niezależne. Naiwny Bayes zakłada, że wystąpienie w mailu słowa "zresetuj" nie ma absolutnie żadnego związku z wystąpieniem słowa "hasło". Bayes liczy prawdopodobieństwo dla każdego słowa z osobna, a na koniec po prostu je przez siebie mnoży.

#### warianty algorytmu

Występują różne warianty tego klasyfikatora w zależności od danych, które możemy zastosować.
* **Gaussian Naive Bayes (Gaussowski)** - Algorytm oblicza średnią oraz odchylenie standardowe dla każdej cechy w ramach danej klasy i na tej podstawie szacuje prawdopodobieństwo. Stosowany przy danych liczbowych (ciągłych). Używany, gdy cechy przyjmują wartości ciągłe z rozkładu zbliżonego do normalnego (np. wzrost, waga, wiek, temperatura, pomiary z czujników). 
* **Multinomial Naive Bayes (Wielomianowy)** - Algorytm najlepiej pracuje na danych dyskretnych i tekście (zliczanie elementów). • Najczęściej stosuje się go w przetwarzaniu języka naturalnego (NLP) do analizy tekstu (np. zliczanie, ile razy dane słowo wystąpiło w dokumencie przy użyciu metod Bag of Words lub TF-IDF).
* **Bernoulli Naive Bayes (Bernoulliego)** - Algorytm pracuje na danych binarnych. • Sprawdza się, gdy cechy przyjmują tylko dwie wartości: tak/nie, prawda/fałsz lub 0/1 (np. czy dane słowo w ogóle występuje w e-mailu – bez względu na to, ile razy, albo czy klient posiada dany produkt).
* **Categorical Naive Bayes (Kategoryczny)** - Algorytm pracuje na danych kategorycznych (nominalnych). Stosowany dla cech, które dzielą obiekty na skończoną liczbę kategorii bez porządku liczbowego (np. kolor: czerwony, zielony, niebieski; dzień tygodnia; płeć; miasto).

#### Uczenie klasyfikatora 

Algorytm nie trenuje się w klasyczny sposób, tworząc odpowiednie reguły czy wagi. W przypadku tego algorytmu tworzony jest globalny słownik semantyczny z danych historycznych. Dla każdego zbioru (treningowego/testowego) wyliczane są częstotliwości występowania danych słów, np. słowo "kliknij" występuje w 65% wiadomości phishingowych i tylko w 5% normalnych wiadomości. Stosowane jest też wygładzenie dla słów, które jeszcze nie występowały. Model wykorzystuje wyuczone prawdopodobieństwo do obliczenia wyniku dla każdej klasy i wybiera tę o najwyższym wyniku. 

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

Algorytm K najbliższych sąsiadów (k-nearest neighbors, KNN) to klasyfikator z serin uczenia nadzorowanego oraz uczenia leniwego. Algorytm jest prosty i itnuicyjny do zalimplementowania. często stoswany jest w systemach gdzie mozna użytkownikowi rekomendować np. filmy, produkty do zakupu. W cyberbezpieczeństwie mozna go zastsować do analizy plików, które mogą zawierć złośliwe oprogramowanie. Innym przykładem może być analiza zachowania użytkowników (UEBA - User and Entity Behavior Analytics) weryfikacja zachowań urzytkowników na podstawie dotychcasowych doświadczeń i pomiarów.

#### Uczenie klasyfikatora

Klasyfikator podczas uczenie nie buduje żadnego modelu matematycznego, nie wylicza wag ani regół tylko zapamiętuje dostarczone dane dlatego nayzany jest leniwym uczeniem. Powoduje to że algorytm jest pamięcio żerny, ponieważ wszystkie dane trzyma w pamięci. 

Weryfikacja działa polega na dostarczeniu nowej prubki i obliczeniu odpowiednich odległości od danych treningowych. Najczęstrze miary stosowane w algorytmie K-NN:

* **Euklidesowa:** $ \sqrt{\sum_{i=1}^n (x_i - y_i)^2} $
* **Manhattan:** $ \sum_{i=1}^n |x_i - y_i| $
* **Cosinusowa:** $ 1 - \frac{x \cdot y}{\|x\| \|y\|} $

Algorytm potrzebuje określić liczbę najbliższych sąsiadów na podstwie, któych będzie klasyfikował nowy pomiar. Zalecane jest stoswoanie nieparzystej liczbie sąsiadów. np. 3,5,7,...,n.

Decyzja jest podejmowana na podstawie największej liczby sąsadów z zadeklarowanej liczby k sąsiadów.

#### Przykładowy algorytm

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

#### Maszyna Wektorów Nośnych (SVM)

Support Vector Machine (SVM) to algorytm uczenia maszynowego, którego głównym zadaniem jest znajdowanie granicy oddzielającej od siebie różne klasy danych.

Jest to algorytm uczenia nadzorowaneo czyli bazuje na danych historycznych, któe są opisane (etykietowane). SVM ma za zadanie wyszukać granice decyzyjności w zależności od zastosowania może to być określenie ruchu sieciowego.

Algorytm posiada kilka ważnych pijęć:

* **Hiperpłaszczyzna** - Granica decyzyjna rozdzielająca dane na klasy. Jej wymiar zależy od liczby cech w zbiorze danych.
* **Wektory nośne** - Punkty danych najbliższe hiperpłaszczyźnie, które definiują jej orientację i maksymalizują margines.
* **Margines** -  Największa odległość pomiędzy punktami danych dwóch klas a hiperpłaszczyzną. Szerszy margines oznacza bardziej stabilny model.

#### Typy jąder (Kernel)

Wybór odpowiedniego jądra jest kluczowy dla skuteczności algorytmu i zależy od natury danych oraz zadania.

**Typy:**
1. Liniowe jądro
  * Opis: Stosowane, gdy dane są liniowo separowalne.
  * Zalety: Szybkie obliczeniowo i proste w interpretacji.
  * Przykład zastosowania: Analiza tekstu, klasyfikacja obrazów w niskowymiarowych przestrzeniach.

2. RBF (Gaussian) jądro
- Opis: Umożliwia modelowanie złożonych, nieliniowych zależności.
- Zalety: Wszechstronne i skuteczne dla większości nieliniowych problemów.
- Przykład zastosowania:** Rozpoznawanie obrazów, analiza bioinformatyczna.

3. Jądro wielomianowe (Polynomial)
- Opis: Stosowane, gdy zależności między cechami mają charakter wielomianowy.
- Zalety: Pozwala na modelowanie bardziej złożonych nieliniowych zależności.

4. Jądro sigmoidalne (Sigmoid)
- Opis: Często używane w zadaniach inspirowanych sieciami neuronowymi.
- Zalety: Przydatne w zadaniach klasyfikacyjnych z bardziej specyficznymi zależnościami.

Wybór jądra to kluczowy etap budowy modelu SVM. Eksperymenty z różnymi typami jąder i dostrajanie ich parametrów pozwalają na osiągnięcie najlepszego dopasowania do danych i maksymalizacji skuteczności algorytmu.

#### Przykładowy algorytm

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