# Wątki

#### Wprowadzenie do programowania współbieżnego&#x20;

Wielowątkowość jest odpowiedzią na wyzwania związane z efektywną obsługą wielu żądań jednocześnie. Wątki jako model współbieżności, pozwalają programiście projektować programy, które mogą wykonywać kilka operacji jednocześnie, zwiększając ogólną wydajność aplikacji.

#### Podstawy

Zrozumienie zasad działania wątków i procesów jest kluczowe w programowaniu większych aplikacji.

* &#x20;**Wątek** - najmniejsza jednostka wykonawcza w ramach procesu. Wątki dzielą wspólną przestrzeń  pamięci co zwiększa efektywność komunikacji między nimi.&#x20;
* **Procesy** -  Każdy z procesów posiada swoją przestrzeń pamięci, co powoduje większe zużycie zasobów i trudniejsze wykonywanie komunikacji między nimi. Wykorzystanie w zadaniach wymagających większego stopnia izolacji.

#### Cykl życia Wątku

Typowy cykl życia wątku obejmuje następujące etapy:

* **Stworzenie wątku** - deklaracja co wątek ma wykonywać&#x20;
* **Uruchomienie** - wywołanie odpowiednich metod pozwalających na start zadeklowanych zadań
* **Praca wątku** - wątek wykonuje zaplaowane metody, funkcje
* **Blokowani** - wątek może być czasowo wstrzymany w oczekiwaniu na I/O lub synchronizację&#x20;
* **Zakończenie** - wątek po wykonaniu odpowiednich zadań jest niszczony i czyszczona jest pamięć, którą wykorzystywał.

#### Tworzenie wątku

Tworzenie wątku będzie przedstawione dla język Python:

```py
import threading, time

# Funkcja, która będzi wykonywana w wątku
def print_numbers():
    for i in range(5):
        time.sleep(1)  # Symulacja dłuższej pracy
        print(f"Thread: {threading.current_thread().name}, Number: {i}")
# Tworzenie wątku
my_thread = threading.Thread(target=print_numbers)
# uruchomienie wątku
my_thread.start()
# Wątek główny 
for i in range(5):
    time.sleep(1)
    print(f"Main Thread, Number: {i}")
```

W powyższym przykładzie przygotowano funkcję, której zadaniem jest wyświetlanie nazwy wątku co jedną sekundę. Kolejnym krokiem jest tworzenie wątku przez wywołanie konstruktora z klasy  `Threading.Thread()`. Jako parametr została przekazana nazwa funkcji, która ma być wykonana w wątku. Następnie wykonywana jest metodę `start()`, która uruchamiany jest wątek, kolejnym krokiem jest wyświetlanie informacji o wątku głównym. W powyższym przykładnie może zaistnieć sytuacji gdzie wątek główny zakończy pracę a wątek dodatkowy nadal będzie pracował.

Konstruktor z klasy `threading` przyjmuje może przyjąć następujące argumenty:

* **target** - nazwa funkcji, która ma być uruchomiona przez wątek
* **args** - parametry, które mają być przekazane do watka&#x20;
* **name** - nazwa watka, wartość domyślna `None` wtedy wątek otrzymuje nazwę Thread-N gdzie n jest liczbą

#### Synchronizacja wątków

Środowisko, w którym wykorzystuje się wielowątkowość może być narażone na konflikt w postaci dostępu do tych samych zasobów przez więcej niż jeden wątek. Taka sytuacja może prowadzić do niepoprawnego działania programu lub uszkodzenie danych. Aby zapobiec takim sytuacją stosuje się mechanizmy synchronizacji lub specjalnie do tego przygotowane kolekcje, co pozwala na zachowanie bezpiecznego dostępu do danych.

Poniższy przykład wykorzystuje mechanizm `Lock` do zabezpieczenia wątka przy zapisie  do wspólnej zmiennej.

```python
import threading

# wspólna zmienna
shared_resource = 0
# tworzenie mechanizmu blokady
lock = threading.Lock()
# funkcja zwiększaąca wartość wspólnej zmiennej
def increment_shared_resource():
    global shared_resource
    for _ in range(100000):
        with lock:
            shared_resource += 1
# tworzenie wątków
thread1 = threading.Thread(target=increment_shared_resource)
thread2 = threading.Thread(target=increment_shared_resource)
# uruchomienie wątków
thread1.start()
thread2.start()
# oczekiwanie aż wątki zakończą prace
thread1.join()
thread2.join()
print(f"Final value of shared resource: {shared_resource}")
```

W powyższym przykładzie tworzony jest obiekt Lock z biblioteki threading za pomocą, którego można blokować dostęp do wspólnego zasobu wykorzystywanego przez wątki. Mechanizm blokady najlepiej stosować na operacja atomowych czyli np. przypisywaniu nowej wartości. Blokad ni zaleca się stosować na całych metodach ponieważ zmniejsza wydajność.&#x20;

Blokowanie wątków niesie ze sobą pewne zagrożenie w postaci zablokowania wątku i problemów z jego odblokowaniem.&#x20;

Unikanie zablokowani wątków wymaga starannego programowania i&#x20;

#### Komunikacja między wątkami

W aplikacjach wielowątkowych wątki często muszą się ze sobą komunikować i wymieniać dane. Skuteczna komunikacja jest kluczowym aspektem do poprawnego działania nowoczesnych aplikacji.&#x20;

W języku Python jest kilka możliwości przekazania informacji między wątkami, takimi sposobami mogą być przekazane zmienne, obiekty między wątkami, odpowiednie kolekcje, lub zdarzenia, które mogą być wywołane przez wątki.

Kolejki (queue) stanowią wygodny sposób komunikacji między wątkami, Poniższy przykład przedstawia wykorzystanie kolejek w języku Python

```python
import threading, queue, time

# Tworzenie kolejki dla wątków
message_queue = queue.Queue()
# Funkcja produkująca wiadomości
def produce_messages():
    for i in range(5):
        time.sleep(1)
        message_queue.put(f"Message {i}")
# Funkcja pobierająca wiadomości
def consume_messages():
    while True:
        message = message_queue.get()
        if message == "STOP":
            break
        print(f"Consumed: {message}")
# tworzenie wątkuów
producer_thread = threading.Thread(target=produce_messages)
consumer_thread = threading.Thread(target=consume_messages)
# Uruchamienie wątku
producer_thread.start()
consumer_thread.start()
# oczekiwanie na zakończenie pracy wątka produkującego wiadomości
producer_thread.join()
# dodanie informacji do kolejki o zakończenie pracy wątku
message_queue.put("STOP")
# oczekiwanie na zakończenie pracy metody pobierającego wiadomości
consumer_thread.join()
```

Powyższy przykład przedstawia użycie kolejki do komunikacja między wątkami. Każdy z wątków dostaje konkretne zadanie, jeden produkuje wiadomości, a drugi pobiera wiadomości. Wątek produkujący wiadomości ma założoną liczbę kroków do wykonania a drugi wątek oczekuje na wiadomości i czeka na odpowiedni sygnał aby zakończyć pracę.&#x20;

Innym sposobem na zarządzanie wątkami jest stosowanie odpowiednich wyzwalaczy.

```python
import threading, time

# Tworzenie obiektu Event
event = threading.Event()
# Funkcja oczekująca na wydarzenie
def wait_for_event():
    print("Waiting for the event...")
    event.wait()  # oczekiwanie na zwolnienie wątka
    print("Event has been set!")
# Funkcja wysyłająca obiekt wydarzenia
def set_event():
    time.sleep(2)
    print("Event is set!")
    event.set()  # ustawienie wydarzenia, umożliwiając czekującemu wątkowi na kontynłacje działania
# Tworzenie wątków
thread1 = threading.Thread(target=wait_for_event)
thread2 = threading.Thread(target=set_event)
# Uruchamianie wątkuów
thread1.start()
thread2.start()
# Oczekiwanie na zakończenie pracy wątków
thread1.join()
thread2.join()
```

Powyższy przykład przedstawia mechanizm blokowania wątku lub inaczej usypiania wątku. Metoda `wait()` powoduje że wątek zostaje zablokowany i czeka do momentu kiedy inny wątek wywoła metodę `set()`. Probelmem tego rozwiązania jest fakt że w programie przynajmniej jeden wątek musi wywłać mteodę `set()` aby nie doszło do całkowitego zablokowania progamu.

#### Zadania



#### Literatura

{% embed url="https://medium.com/@me.mdhamim/a-comprehensive-guide-to-python-threading-advanced-concepts-and-best-practices-9f3aea6f0a63" %}

{% embed url="https://docs.python.org/3/library/threading.html" %}

{% embed url="https://brandonrohrer.com/threading.html" %}
