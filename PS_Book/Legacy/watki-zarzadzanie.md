# Wątki - zarządzanie

### Zarządzanie wątkami

W poprzedniej lekcji poznane zostały sposoby na tworzenie wątków za pomocą biblioteki `threading`. W obecnym rozdziale zostanie przedstawione, jak tworzyć pulę wątków i jednocześnie zarządzać nimi.

#### Tworzenie puli wątków

Środowisko Python udostępnia bibliotekę `concurrent.futures`, która pozwala w prosty sposób na asynchroniczne zlecanie zadań i zarządzanie nimi.

Poniżej przedstawiony został przykład utworzenia puli wątków z zadaniami:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random, threading

def do_something_long(id_task):
    print(f"Start zadania {id_task}")
    # tu zrób coś długiego
    result = random.randint(1, 6)
    time.sleep(result)
    print(f"Wątek: {threading.current_thread().name} zakończył pracę")
    return result

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="uken") as executors:
        tasks = [i for i in range(8)]
        future_results = {executors.submit(do_something_long, task): task for task in tasks}

        for future_result in as_completed(future_results):
            id_task = future_results[future_result]
            try:
                data = future_result.result()
                print(f"Otrzymano wyniki: {data} z zadania {id_task}")
            except Exception as e:
                print(f"Zadanie {id_task} zgłosiło wyjątek {e}")
```

Powyższy przykład przedstawia tworzenie puli 4 wątków (`ThreadPoolExecutor(max_workers=4)`), które mają wykonać 8 zadań. Każdy z wątków dostaje zadanie (`do_something_long`), w którym symulowane jest dłuższe wykonanie. Metoda `executors.submit()` przypisuje zadanie do wykonania i zwraca obiekt `Future`, który reprezentuje przyszły wynik. Zadania umieszczane są w kolejce i w zależności od tego, czy któryś wątek jest dostępny, przydzielane są do wykonania. Pętla z metodą `as_completed()` oczekuje na ukończenie zadań i pozwala przetworzyć ich rezultaty w momencie, gdy są gotowe. W powyższym przykładzie został użyty blok `with`, który pomaga przy zarządzaniu wątkami i dba o to, aby po zakończeniu wszystkich zadań pula wątków została prawidłowo zamknięta.

#### Sprawdzanie pracy wątków

W sytuacjach, kiedy wykonywane są dłuższe zadania, istnieje możliwość sprawdzenia, czy wątek (a dokładniej zadanie) nadal pracuje. Można to zweryfikować na obiekcie `Future`, który zwracany jest przez `ThreadPoolExecutor`. Dostępne są dwa sposoby:

* `future.done()` – zwraca `True`, jeżeli zadanie zostanie zakończone (sukcesem, błędem lub po anulowaniu), oraz `False`, jeżeli zadanie nadal działa w tle.
* `future.running()` – zwraca `True`, jeżeli zadanie jest aktualnie wykonywane przez wątek.

Przykład:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def long_task():
    time.sleep(2)
    return "Gotowe"

with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(long_task)
    
    print(f"Czy zadanie się rozpoczęło/trwa? {future.running()}") # True
    print(f"Czy zadanie zostało ukończone? {future.done()}")       # False
    time.sleep(2.5)
    print(f"Czy zadanie zostało ukończone teraz? {future.done()}") # True
```

#### Zamykanie wątków

Środowisko Python pozwala na wcześniejsze zakończenie pracy zadań w wątku lub anulowanie zadań, które jeszcze nie rozpoczęły pracy i czekają w kolejce na wykonanie. Dostępnych jest kilka sposobów, jak można to wykonać:

* Anulowanie zadania (`future.cancel()`) – metoda, która pozwala anulować zadanie zlecone, ale jeszcze niewykonywane. Zwraca `True` w sytuacji, gdy uda się je anulować, oraz `False`, kiedy zadanie już trwa lub zostało zakończone.

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task():
    time.sleep(2)

with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(task)
    
    is_cancel = future.cancel()
    print(f"Czy anulowano zadanie? {is_cancel}")
```

* Kontrolowanie zamykania (`shutdown`) – kiedy korzystasz z bloku `with`, program automatycznie czeka, aż wszystkie zadania zostaną zakończone. Można to kontrolować, wywołując metodę `shutdown()` z odpowiednimi parametrami:
  * `wait=False` – powoduje, że pula wątków kończy pracę natychmiast bez czekania, aż zadania się zakończą.
  * `cancel_futures=True` – automatycznie anuluje wszystkie zadania oczekujące na wykonanie w kolejce.

```python
executor = ThreadPoolExecutor(max_workers=2)
# ... zlecasz dużo zadań ...
executor.shutdown(wait=False, cancel_futures=True)
```

#### Zadania

1. Napisz program wielowątkowy, który korzystaj z `ThreadPoolExecutor` i stałej puli wątków o liczbie `n`. Wypełnij listę **łącznie 1000 elementów**. Spośród wylosowanych liczb dodawaj do wspólnej listy tylko te, które są podzielne przez `3`. Zakres losowanych liczb całkowitych przyjmij jako parametr programu i podaj go przy prezentacji wyniku; dopuszczaj powtórzenia. Synchronizuj zapis do wspólnej listy. Zakończ pracę wątków jeżeli liczba elementów w liście osiągnie 1000 elementów.
2. \* Stwórz aplikację bazującą na wielowątkowości, która ma za zadanie odczytywać strony internetowe i pobierać informacje w postaci adres URL, opis strony, język strony (lang). Aplikacja ma szukać linków dostępnych na stronie i odwiedzać unikalne linki, które jeszcze nie były odwiedzane. Zadanie ma działać przynajmniej 20 minut, wyniki zapis do pliku w trzech formatach: strony odwiedzone (adres URL, opis, język strony), linki do odwiedzenia, linki błędne.
