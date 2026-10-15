# Zadania

### Lab 2

Korzystająć z pliku:

{% file src="../.gitbook/assets/HPC_2k.log_structured.csv" %}

Rozwiąż następujące zadania

1. Konwersja czasu - kolumna `Time` zawiera czas w formacie UNIX Timestamp (liczba sekund od 1 stycznia 1970 r.). Stwórz nową kolumnę `Datetime`, konwertując wartości z kolumny `Time` na obiekt daty i czasu. Wyodrębnij godzinę z nowej kolumny do zmiennej `Hour`. Oblicz liczbę logów wygenerowanych w poszczególnych godzinach i zidentyfikuj okno czasowe z największą aktywnością systemu.
2. Identyfikacja najbardziej awaryjnego węzła - Klaster obliczeniowy składa się z wielu maszyn (węzłów). Należy ustalić, które z nich wymagają największej uwagi administratorów. Zgrupuj dane według kolumny `Node`. Policz całkowitą liczbę wystąpień dla każdego węzła. Posortuj wyniki malejąco i wyodrębnij 5 maszyn, które wygenerowały najwięcej zdarzeń w badanym okresie.
3. Identyfikacja stanów systemu - Kolumna `State` przechowuje informacje o statusie danego zdarzenia w klastrze. Zidentyfikuj wszystkie unikalne wartości występujące w kolumnie `State`. Oblicz procentow udział każdego ze stanów w stosunku do wszystkich 2000 logów. Przedstaw wyniki z dokładnością do dwóch miejsc po przecinku (np. 45.50%), aby sprawdzić, czy dominują rutynowe komunikaty, czy zmiany stanu na niedostępny.

Korzystając z pliku

{% file src="../.gitbook/assets/OpenSSH_2k.log" %}

Rozwiąrz zadania:

1. Korzystając z biblioteki `pygrok`, `parse`, `re` lub innej dowolnej przenieś plik z logami do obiektu `DataFrame` treść logu zapisz do kolumny `msg`
2. Bazujać na ramce danych z zadania 1 sprawdz w ilu rekordach występują wartości puste (`None`).
3. Przygotuj zestawienie liczby logów wygenerowanych przez poszczególne procesy (np. `sshd`, `ftpd`, `su`).
4. Na bazie przygotowanego wcześniej `DataFrame`, przekonwertuj kolumnę z datą i czasem ze zwykłego tekstu na typ `datetime` (w pliku nie podano roku wstaw rok 2025).
5. Wykorzystując dowolną bibliotekę (pygrok, parse, re) wyciągnij z kolumny `msg` informacje o adresie ip i nazwie użytkownika dla komunikatów, które zawierają "Failed password" oraz "Invalid user".
6. Korzystając z metod filtracji i grupowania, zastosuj je do zidentyfikowania i wyświetlenia zestawienia top 5 adresów IP generujących najwięcej błędów uwierzytelniania oraz top 5 najczęściej atakowanych nazw użytkowników (np. `root`, `admin`). Wyniki wyeksportuj do pliku `JSON`.&#x20;

