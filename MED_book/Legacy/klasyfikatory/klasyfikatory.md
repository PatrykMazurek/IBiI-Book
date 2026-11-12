# Klasyfikatory 

Klasyfikatory odgrywają dużą rolę w analizie danych i w cyberbezpieczeństwie. Ich zastosowanie pozwala na dopasowanie wybranych produktów czy usług oraz może zapobiegać próbom oszustwa.

Głównym zadaniem klasyfikatorów jest dopasowywanie nowych danych na podstawie już istniejących reguł i kategorii.

Wyzwaniem w klasyfikacji są dane, które powinny zawierać odpowiednią ilość próbek dopasowanych do właściwych klas. Uwzględniając aspekty cyberbezpieczeństwa: jeżeli zbiór będzie zawierał 99% próbek z normalnym ruchem sieciowym i tylko 1% próbek z atakami, to klasyfikator nie będzie działał poprawnie bez odpowiedniego przygotowania.

### Zastosowanie

Standardowym zastosowaniem klasyfikatorów może być klasyfikacja obrazów, rekomendowanie filmów na platformach streamingowych, czy badanie zachowań i upodobań klientów w sektorze e-commerce. Poza typowymi zastosowaniami w analizie danych, klasyfikatory można również wykorzystać przy analizie wiadomości e-mail, filtrując, czy dana wiadomość jest spamem, czy próbą phishingu. Analizując logi sieciowe, możemy zidentyfikować, czy dany adres IP jest zaufany i możemy go przepuścić, lub czy dane zachowanie nie sugeruje ataku.

### Podział zbiorów

Niezależnie od rodzaju klasyfikatora, zbiory powinno się dzielić na dwie lub trzy kategorie:
* dwie kategorie - podział na zbiory treningowe i testowe w proporcjach 70/30 lub 80/20 
* trzy kategorie - podział na zbiory treningowe, walidacyjne i testowe w proporcjach 70/15/15 lub 80/10/10

Kluczowe dla poprawnego działania klasyfikatorów jest odpowiednie przygotowanie danych: 

* **Stratyfikacja (Zachowanie proporcji)** - zbiory często nie są zbalansowane. Zakładając, że podstawowy zbiór zawiera 99% poprawnego ruchu sieciowego i tylko 1% ataków, to przy zwykłym losowaniu może się okazać, że w zbiorze treningowym są wszystkie ataki, a w zbiorze testowym żadnego. Model może wtedy błędnie wskazywać 99% skuteczności.
* **Ścisła izolacja (Data Leakage)** - rekordy ze zbiorów treningowych i testowych nie mogą się ze sobą mieszać.
* **Przygotowanie cech (Skalowanie i transformacja)** - w zbiorach należy odpowiednio dostosować skalę w zależności od zastosowanych algorytmów. Algorytmy takie jak drzewa decyzyjne i lasy losowe działają dobrze na danych surowych, a algorytmy KNN czy SVM opierają się na obliczeniu odległości między pomiarami i często wymagają odpowiedniego skalowania.  

## Rodzaje klasyfikatorów

### Drzewa decyzyjne

Zasadę działania można porównać do gry "20 pytań". Na każdym etapie zadajemy pytanie w stylu "Tak/Nie" i na tej podstawie dopasowujemy dane do odpowiednich kategorii. 

Struktura algorytmu:
* **Pytanie główne – korzeń (Root)** - np. czy adres IP pochodzi z Europy? W ten sposób odpowiednio dzielimy dane wejściowe.
* **Kolejne pytania – węzły (Node)** - np. czy liczba nieudanych logowań > 3?
* **Ostatnie pytania – liście (Leaves)** - pozwalają określić, do jakiej klasy przypisać dany rekord, np. "zagrożenie (1)" lub "ruch normalny (0)".

Zaletą algorytmu jest fakt, że możemy przeanalizować poszczególne kroki podejmowania decyzji (model typu white-box). 

#### Uczenie algorytmu

Algorytm przegląda wszystkie dostępne cechy (np. porty, liczba pakietów, lokalizacja) i szuka takiego podziału, który da najczystsze grupy. "Czystość" (Purity) mierzy się za pomocą matematycznych kryteriów, takich jak Entropia lub Indeks Gini. Model zatrzymuje się, gdy dotrze do liści zawierających zdarzenia tylko jednej klasy lub osiągnie z góry narzuconą maksymalną głębokość (żeby uniknąć zapamiętania danych na pamięć, czyli przeuczenia).

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

## Ocena skuteczności modelu klasyfikacji

Ważnym etapem w pracy z danymi jest sprawdzenie, jak klasyfikatory radzą sobie z przygotowanymi danymi przed wdrożeniem do realnych systemów. 

Biblioteka `scikit-learn` oferuje różne metryki do oceny skuteczności modeli, takie jak:
- *macierz pomyłek (confusion matrix)*;
- *dokładność (accuracy)*;
- *precyzja (precision)*;
- *czułość (recall)*;
- *wskaźnik F1 (F1-score)*.

### Confusion matrix (Macierz pomyłek)

Jest to jedna z najpopularniejszych metod do weryfikacji wyników klasyfikacji. W wyniku otrzymujemy macierz 2 x 2, która zawiera:

* *Prawdziwie pozytywne (**TP**)*
    Przypadki, w których:
    - Model przewiduje wartość **Tak**,
    - Rzeczywista wartość również wynosi **Tak**.<br>

* *Prawdziwie negatywne (**TN**)*
    Przypadki, w których:
    - Model przewiduje wartość **Nie**,
    - Rzeczywista wartość również wynosi **Nie**.<br>

* *Fałszywie pozytywne (**FP**)*
    Przypadki, w których:
    - Model przewiduje wartość **Tak**,
    - Rzeczywista wartość wynosi **Nie**.<br>

* *Fałszywie negatywne (**FN**)*
    Przypadki, w których:
    - Model przewiduje wartość **Nie**,
    - Rzeczywista wartość wynosi **Tak**.<br>

Macierz potrafi pokazać, gdzie występuje problem w klasyfikacji.

Przykładowy kod, przedstawiający wyniki macierzy pomyłek:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sns.heatmap(confusion_matrix(target_test, predictions), annot = True, cmap='Blues', fmt='g')
plt.show()
```

#### Accuracy - dokładność klasyfikacji

Dokładność modelu (accuracy) można wyrazić za pomocą pojęć TN (True Negative), TP (True Positive), FN (False Negative) i FP (False Positive) za pomocą następującego wzoru:
$$
\mbox{accuracy} = \frac{TP+TN}{TP+TN+FP+FN}
$$

#### Precision - precyzja

Określa, jaka część wyników wskazanych przez klasyfikator jako pozytywne/negatywne jest faktycznie pozytywna/negatywna.

$$
\mbox{precision} = \frac{TP}{TP+FP}
$$

#### Recall - czułość

Określa, jaką część próbek pozytywnej/negatywnej klasy (ze wszystkich, które powinien był wykryć) wykrył klasyfikator.
$$
\mbox{Recall} = \frac{TP}{TP+FN}
$$

Do przeprowadzenia kompletnej oceny klasyfikatora w uczeniu maszynowym wykorzystuje się różne miary, które pomagają zrozumieć jego skuteczność. Narzędzie, które to automatyzuje w Pythonie, to funkcja `classification_report` z biblioteki `scikit-learn`.

```python
from sklearn.metrics import classification_report

c_report = classification_report(target_test, predictions, output_dict=True)
pd.DataFrame(c_report)
```

## Zadania

1. Odczytaj plik `login.csv` i podziel dane na dwa zbiory: uczący i testowy (80/20). Przy podziale nie zapomnij zastosować `stratify`. Wytrenuj klasyfikator drzew decyzyjnych i sprawdź jego działanie, obliczając wskaźniki: `Confusion matrix`, `Accuracy`, `Precision`, `Recall`. Możesz do tego zastosować funkcję `classification_report`. 
    Zapoznaj się z metodą `plot_tree` lub `export_text` z pakietu `sklearn.tree` i przedstaw reguły wyuczone przez klasyfikator. Przy generowaniu tekstu lub wykresu nie zapomnij zastosować parametru `feature_names` z listą kolumn. Zidentyfikuj najdłuższą ścieżkę do liścia z decyzją "zablokowany". Wytrenuj ponownie model, zmieniając parametr `max_depth` na 2 i sprawdź, jak wpłynie to na czułość (`recall`) klasyfikatora.
2. Odczytaj dane z pliku `transakcje.csv` i przygotuj dane do trenowania lasów losowych. Po wytrenowaniu modelu przeanalizuj macierz pomyłek. Wyciągnij z wytrenowanego modelu wektor `feature_importances_` i stwórz wykres słupkowy pokazujący 3 najważniejsze cechy, którymi kierują się lasy losowe przy wykrywaniu oszustw.
3. Odczytaj dane ze zbioru `SMS Spam Collection Dataset`, sprawdź, czy występują braki w kolumnach `class` lub `sms` (pozostałe kolumny pomiń). Podziel dane na dwa zbiory: uczący i testowy (80/20). Przy podziale nie zapomnij zastosować `stratify`. Wytrenuj naiwny klasyfikator Bayesa, a następnie sprawdź jego skuteczność, wyświetlając macierz pomyłek. Spróbuj stworzyć swoje własne wiadomości, aby przetestować działanie klasyfikatora na realnych danych.

Skrypt do pobrania plików do zadania 3:
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = "spam.csv"

# Load the latest version
df = kagglehub.load_dataset( KaggleDatasetAdapter.PANDAS, "uciml/sms-spam-collection-dataset", file_path,)

print("First 5 records:", df.head())
```