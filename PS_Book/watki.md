# Wątki

## Wprowadzenie do programowania współbieżnego

Wielowątkowość pozwala obsługiwać kilka zadań współbieżnie w ramach jednego procesu. Jest przydatna w aplikacjach sieciowych, które podczas obsługi jednego połączenia mogą oczekiwać na dane, a w tym czasie obsługiwać inne połączenia.

**Współbieżność** oznacza, że wykonanie kilku zadań postępuje w tym samym okresie. **Równoległość** oznacza rzeczywiste wykonywanie zadań w tej samej chwili, na przykład na różnych rdzeniach procesora. Współbieżność nie gwarantuje równoległości ani skrócenia czasu działania programu.

Przykłady w tym rozdziale są przeznaczone dla **Pythona 3.10**. W standardowej implementacji CPython mechanizm **GIL** ogranicza równoległe wykonywanie kodu Pythona przez wątki. Wątki sprawdzają się przede wszystkim w zadaniach wymagających oczekiwania na operacje wejścia/wyjścia (I/O), takich jak komunikacja sieciowa. Obliczenia w czystym Pythonie, na przykład wyszukiwanie liczb pierwszych, zwykle nie przyspieszają po zwiększeniu liczby wątków. Narzut ich obsługi może nawet wydłużyć czas wykonania. Niektóre biblioteki wykonujące obliczenia poza kodem Pythona zwalniają GIL; ich zachowanie może być inne.

## Podstawy

* **Wątek** — jednostka wykonania w ramach procesu. Wątki współdzielą przestrzeń pamięci procesu, co ułatwia wymianę danych, ale wymaga koordynowania dostępu do wspólnych zasobów.
* **Proces** — uruchomiony program z własną przestrzenią pamięci wirtualnej. Procesy zapewniają większą izolację; komunikacja między nimi wymaga odpowiednich mechanizmów, takich jak kolejki lub pamięć współdzielona. Zwykle ich tworzenie wymaga więcej zasobów niż tworzenie wątków.

## Cykl życia wątku

Uproszczony opis cyklu życia wątku obejmuje:

1. **Utworzenie obiektu wątku** — wskazanie zadania, które ma zostać wykonane.
2. **Uruchomienie** — wywołanie metody `start()`.
3. **Wykonywanie zadania** — realizację kodu funkcji docelowej.
4. **Oczekiwanie** — czasowe wstrzymanie, na przykład podczas I/O lub oczekiwania na blokadę. Wątek może wielokrotnie przechodzić między wykonywaniem kodu a oczekiwaniem.
5. **Zakończenie** — po zakończeniu funkcji docelowej albo wskutek nieobsłużonego wyjątku.

Zakończenie pracy wątku nie oznacza usunięcia wszystkich obiektów, z których korzystał. Obiekty współdzielone mogą być nadal używane przez pozostałe wątki. Zasoby, takie jak otwarte pliki, należy zwalniać w sposób kontrolowany, na przykład przy użyciu `with`.

## Tworzenie wątku

```python
import threading
import time


def print_numbers(count, delay=1):
    for i in range(count):
        time.sleep(delay)  # Symulacja oczekiwania, np. na dane z sieci.
        print(f"Thread: {threading.current_thread().name}, Number: {i}")


my_thread = threading.Thread(
    target=print_numbers,
    args=(5,),
    kwargs={"delay": 1},
    name="NumberWorker",
)
my_thread.start()

for i in range(5):
    time.sleep(1)
    print(f"Main Thread, Number: {i}")

# Dalszy kod wykona się po zakończeniu pracy dodatkowego wątku.
my_thread.join()
print("Oba zadania zostały zakończone.")
```

Funkcja `print_numbers` wyświetla nazwę wątku i kolejne liczby, rozdzielając wypisania przerwą. `time.sleep()` służy tutaj do symulacji oczekiwania. Kolejność komunikatów z obu wątków nie jest gwarantowana.

Do konstruktora `threading.Thread` przekazujemy obiekt funkcji: `target=print_numbers`. Zapis `target=print_numbers()` wywołałby funkcję od razu w wątku tworzącym obiekt i przekazał jej wynik zamiast funkcji.

Wybrane argumenty konstruktora:

| Argument | Znaczenie |
| --- | --- |
| `target` | Funkcja lub inny obiekt wywoływalny, który ma wykonać wątek. |
| `args` | Krotka argumentów pozycyjnych funkcji. Dla jednego argumentu: `(5,)`. |
| `kwargs` | Słownik argumentów nazwanych funkcji, np. `{"delay": 1}`. |
| `name` | Nazwa wątku. Bez jawnej nazwy Python 3.10 tworzy nazwę automatycznie, np. `Thread-1 (print_numbers)`. |
| `daemon` | Określa, czy wątek jest demoniczny. Domyślnie dziedziczy tę właściwość po wątku, który go tworzy. |

Metoda `start()` uruchamia zadanie w osobnym wątku; jeden obiekt `Thread` można uruchomić tylko raz. Bezpośrednie wywołanie `run()` nie tworzy osobnego wątku.

Metoda `join()` wstrzymuje wątek wywołujący do zakończenia wskazanego wątku. Nie uruchamia go ani nie przerywa jego działania. Po `join(timeout=...)` należy sprawdzić `is_alive()`, aby ustalić, czy wątek nadal pracuje.

W przykładzie dodatkowy wątek jest niedemoniczny. Nawet bez `join()` interpreter czekałby na jego zakończenie przed wyjściem z programu. Jawne `join()` określa jednak, w którym miejscu program ma zaczekać. Wątki demoniczne mogą zostać przerwane podczas kończenia programu, dlatego nie należy polegać na nich przy zapisie ważnych danych.

## Synchronizacja wątków

Gdy kilka wątków korzysta ze wspólnych danych, wynik może zależeć od kolejności ich operacji. Taki problem nazywamy **wyścigiem danych**. **Sekcja krytyczna** to fragment kodu, którego wykonanie wymaga kontrolowanego dostępu do współdzielonego zasobu.

Poniższy przykład wykorzystuje `Lock` do ochrony aktualizacji wspólnego licznika:

```python
import threading


shared_resource = 0
lock = threading.Lock()


def increment_shared_resource():
    global shared_resource
    for _ in range(100_000):
        with lock:
            shared_resource += 1


thread1 = threading.Thread(target=increment_shared_resource)
thread2 = threading.Thread(target=increment_shared_resource)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print(f"Final value of shared resource: {shared_resource}")
```

Po prawidłowym zakończeniu obu wątków licznik wynosi `200000`. `with lock:` pobiera blokadę przed wejściem do sekcji krytycznej i zwalnia ją przy wyjściu, również w przypadku wyjątku. Wszystkie wątki wykonujące konfliktujące operacje na chronionych danych muszą korzystać z tej samej blokady.

Aktualizacja `shared_resource += 1` obejmuje odczyt, obliczenie i zapis. Nie należy traktować jej jako gwarantowanej operacji atomowej ani polegać na GIL jako zamienniku synchronizacji. Usunięcie blokady nie musi ujawnić problemu w każdym uruchomieniu — poprawny wynik pojedynczej próby nie dowodzi poprawności programu.

Blokada powinna obejmować całą operację potrzebną do zachowania spójności danych. Sekcję krytyczną warto utrzymywać możliwie krótką, ale nie wolno skracać jej kosztem poprawności. Ochrona całej metody może być uzasadniona, jeśli wszystkie jej operacje tworzą jedną sekcję krytyczną.

### Zakleszczenia

**Zakleszczenie (deadlock)** może wystąpić, gdy wątek A posiada blokadę pierwszą i czeka na drugą, a wątek B posiada drugą i czeka na pierwszą. Żaden z nich nie może kontynuować pracy.

Aby ograniczyć ryzyko zakleszczeń:

* pobieraj wiele blokad zawsze w tej samej, ustalonej kolejności;
* używaj `with`, aby blokada została zwolniona po opuszczeniu sekcji krytycznej;
* unikaj oczekiwania na zakończenie innego wątku, gdy trzymasz blokadę potrzebną temu wątkowi;
* w uzasadnionych przypadkach stosuj limity czasu i obsługuj sytuację, w której nie udało się uzyskać zasobu.

Samo użycie `with` nie zapobiega zakleszczeniom wynikającym z niewłaściwej kolejności pobierania blokad.

## Komunikacja między wątkami

Wątki mogą wymieniać dane przez współdzielone obiekty, kolejki i mechanizmy sygnalizacji. Samo przekazanie obiektu do kilku wątków nie zapewnia bezpiecznego dostępu do jego danych.

### Kolejka `queue.Queue`

`queue.Queue` zapewnia synchronizację operacji dodawania i pobierania elementów. Poniższy przykład przedstawia jednego producenta i jednego konsumenta:

```python
import queue
import threading
import time


message_queue = queue.Queue()
STOP = object()  # Osobny znacznik, który nie koliduje z treścią wiadomości.


def produce_messages():
    try:
        for i in range(5):
            time.sleep(1)
            message_queue.put(f"Message {i}")
    finally:
        message_queue.put(STOP)


def consume_messages():
    while True:
        message = message_queue.get()
        if message is STOP:
            break
        print(f"Consumed: {message}")


producer_thread = threading.Thread(target=produce_messages)
consumer_thread = threading.Thread(target=consume_messages)

producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()
```

Producent umieszcza pięć wiadomości w kolejce, a następnie znacznik końca. Konsument oczekuje w `get()` na kolejne elementy i kończy pracę po pobraniu znacznika. Blok `finally` zapewnia wysłanie znacznika także wtedy, gdy producent zakończy pracę wskutek wyjątku. W tym przykładzie jeden znacznik wystarcza dla jednego konsumenta; przy wielu konsumentach trzeba zaplanować zakończenie pracy każdego z nich.

Kolejka chroni swoje operacje, ale nie zapewnia automatycznej ochrony późniejszych modyfikacji obiektu pobranego z kolejki, jeśli nadal współdzielą go inne wątki.

W przykładzie użyto `Thread.join()`, czyli oczekiwania na zakończenie wątku. Osobnym mechanizmem jest `Queue.join()`, które czeka na potwierdzenie przetworzenia wszystkich dodanych elementów. Przy jego użyciu po każdym `get()` należy wywołać `task_done()` po zakończeniu obsługi elementu, również znacznika końca. W powyższym przykładzie nie używamy `Queue.join()`, więc takie potwierdzenia nie są potrzebne.

### Zdarzenie `threading.Event`

`Event` jest współdzieloną flagą służącą do sygnalizacji. Może na przykład informować, że dane są gotowe albo że wątek powinien zakończyć pracę.

```python
import threading
import time


event = threading.Event()


def wait_for_event():
    print("Waiting for the event...")
    event.wait()
    print("Event has been set!")


def set_event():
    time.sleep(2)
    print("Setting the event...")
    event.set()


thread1 = threading.Thread(target=wait_for_event)
thread2 = threading.Thread(target=set_event)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
```

Początkowo flaga jest wyzerowana. `set()` ustawia ją i pozwala oczekującym wątkom kontynuować pracę. Jeśli flaga była już ustawiona, `wait()` wraca od razu. Wywołanie `clear()` ponownie zeruje flagę; samo `wait()` jej nie zeruje.

Bez ustawienia flagi `wait()` bez limitu czasu może czekać bez końca. Wariant `event.wait(timeout=5)` zwraca `False`, gdy czas upłynie bez ustawienia flagi, a `True`, gdy oczekiwanie zakończy się jej ustawieniem. Program powinien odpowiednio obsłużyć oba wyniki.

Do kontrolowanego zatrzymywania okresowej pracy można użyć osobnego zdarzenia `stop_event`. Pętla `while not stop_event.wait(3):` wykonuje kolejne iteracje po trzysekundowym oczekiwaniu i kończy się po ustawieniu flagi. Pierwsza iteracja nastąpi po oczekiwaniu; jeśli potrzebny jest natychmiastowy skan, wykonaj go przed pętlą. Wątek sterujący wywołuje `stop_event.set()`, a następnie `join()`. Sygnał nie przerywa automatycznie operacji I/O już wykonywanej przez wątek.

## Zadania

Poniższe zadania wykonaj w Pythonie 3.10. W zadaniach 1–2 zapewnij kontrolowane zatrzymanie wątku, na przykład przez `threading.Event`, oraz oczekiwanie na jego zakończenie przez `join()`. Wątki robocze powinny mieć jasno określone zadania i sposób przekazywania wyników.

1. Stwórz wątek, który co trzy sekundy skanuje wybrany folder i informuje o zmianach względem poprzedniego skanu. Uwzględnij dodanie, usunięcie i modyfikację pliku, określaną na podstawie czasu modyfikacji lub rozmiaru. Pierwszy skan ustala stan początkowy. Skanuj tylko wskazany folder, bez podfolderów. Obsłuż sytuację, w której plik zniknie podczas skanowania.

2. Stwórz wątek, który w konfigurowalnym odstępie czasu skanuje wskazany folder i przenosi znalezione pliki do podfolderów według rozszerzeń: `txt`, `doc`, `csv`, `pdf` do `dokumenty`; `png`, `jpg`, `bmp` do `image`; pozostałe, w tym pliki bez rozszerzenia, do `różne`. Utwórz brakujące foldery docelowe, ignoruj wielkość liter rozszerzeń i nie skanuj podfolderów. Nie nadpisuj istniejących plików — w razie konfliktu dodaj do nazwy kolejny numer. Na potrzeby ćwiczenia używaj plików, których zapis został już zakończony. Obsłuż błędy dostępu i zniknięcie pliku przed przeniesieniem.

3. Wyszukaj wszystkie liczby pierwsze w przedziale od `2` do `1_000_000` włącznie, wykorzystując cztery wątki robocze. Podziel przedział na rozłączne części, zbierz wyniki i sprawdź ich zgodność z wersją sekwencyjną. Zwróć uwagę na wpływ GIL na czas wykonania obliczeń w CPythonie 3.10.

4. Napisz program wielowątkowy wykonujący **łącznie 1000 losowań**, a nie 1000 losowań na każdy wątek. Spośród wylosowanych liczb dodawaj do wspólnej listy tylko te, które są podzielne przez `3`. Zakres losowanych liczb całkowitych przyjmij jako parametr programu i podaj go przy prezentacji wyniku; dopuszczaj powtórzenia. Rozdziel wszystkie 1000 losowań między wątki, również gdy liczba losowań nie dzieli się przez liczbę wątków. Synchronizuj zapis do wspólnej listy. Liczba elementów listy wynikowej zależy od wyników losowania i nie musi wynosić 1000.

5. Porównaj czasy wykonania zadań 3 i 4 dla `1`, `4` i `6` wątków roboczych oraz wersji sekwencyjnej. Zachowaj ten sam algorytm, zakres danych i łączną liczbę operacji. W zadaniu 4 zachowaj też ten sam zakres losowania. Mierz czas za pomocą `time.perf_counter()`, uwzględniając uruchomienie wątków i oczekiwanie na ich zakończenie; nie uwzględniaj wypisywania wyników. Każdy wariant uruchom co najmniej pięć razy i porównaj mediany. Podaj wersję interpretera i liczbę rdzeni procesora. Wyjaśnij wyniki, uwzględniając GIL, synchronizację i narzut tworzenia wątków. Przy zaledwie 1000 losowaniach narzut oraz wahania pomiaru mogą dominować; brak przyspieszenia jest poprawnym wynikiem eksperymentu.

## Literatura

Dokumentacja dla wersji Pythona używanej na kursie:

{% embed url="https://docs.python.org/3.10/library/threading.html" %}

{% embed url="https://docs.python.org/3.10/library/queue.html" %}

Materiały uzupełniające; przykłady należy odnosić do środowiska kursowego:

{% embed url="https://medium.com/@me.mdhamim/a-comprehensive-guide-to-python-threading-advanced-concepts-and-best-practices-9f3aea6f0a63" %}

{% embed url="https://brandonrohrer.com/threading.html" %}
