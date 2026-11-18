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

Wyróżniamy kilka sposobów uczenia maszynowego:
* **uczenie nadzorowane** - do nauki dostarczamy zbiory z etykietami i system zna rozwiązania i wie czy wykonał zadanie właściwie czy nie.
* **Uczenie nienadzorowane** - do nauki dostarczamy surowy zbiór danych bez etykiet i system musi sam znaleść regóły czy zależności. 
* **Uczenie ze wzmocnieniem** - do algorytmu uczenia dostarczamy zbiory, na których algorytm się uczy i przy każdym przejściu dostaje kary za źle wykonany akcję i nagrody za dobrze wykonaną akcję.
