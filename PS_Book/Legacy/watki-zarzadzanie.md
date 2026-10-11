# Wątki - zarządzanie

### Zarządzanie wątkami

W porzedniej lekcji poznane zostały sposoby na tworzenie wątków za pomocą biblioteki `threading`. w obecnym rozdziale zostanie przedstawione jak tworzyć pulę wątków i jednocześnie zarzącać nimi.&#x20;

#### Tworzenie puli wątków

Środowisko Python udostępnia udostępnia bibliotekę `concurrent.futures`, któraa pozwala w prosty sosób na zlecanie zadań asynchronicznie i zarzącać nimi.

Poniżej przedstawiony został przykład utworzenia puli wątków z daaniami&#x20;

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, random, threading

def do_something_long(id_task):
    print(f"Start zadania {id_task}")
    # tu zrób coś długiego
    result = random.randint(1, 6)
    time.sleep(result)
    print(f"Wątek: {threading.current_thread().name} zakończył prace" )
    return result

if __name__=="__main__":
    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="uken") as executors:
        tasks = [i for i in range(8)]
        fufute_results = {executors.submit(do_something_long, task): task for task in tasks}

        for future_result in as_completed(fufute_results):
            id_task = fufute_results[future_result]
            try:
                data = future_result.result()
                print(f"Otrzymano wyniki: {data} z zadania {id_task}")
            except Exception as e:
                print(f"Zadanie {id_task} zgłosiło wyjątek {e}")
```

Powyższy przykład przedstawia tworzenie puli 4 wątków (`ThreadPoolExecutor(max_workers=4)`), które mają wykonać 8 zadań. Każdy z wątków dostaje zadania (`do_something_long`) w którym symulowany jest dłuższe wykonanie zadania. Meoda executors.submit() przypisuje zadanie do wykonania i zwraca obiekt Future, który reprezentuje przyszły wynik. Zadania umiszczane są w kolejce i w zależności od tego czy, któryś wątek jest dostępny przydzielane są zadania. Pętla z metodą as\_complite() oczekuje na ukończenie zadań i pozwala przetworzyć ich rezultaty w momencie, gdy są gotowe. W powyższym przykładzie został użyt blok with, który pomaga przy zarządzaniu w tym przypadku wątkami i dba o to aby po zakończeniu wszystkich zadań pula wątków zostałą prawidłowo zamknięta.

#### Sprawdzanie pracy wątków

W sytuacjach kiedy wykonywane są dłuższe zadania jest możliwość sprawdzenia czy wątek a bardziej zadanie nadal pracuje. Można to zweryfikować na obiekcie `Future`, który zwracany jest przez  `ThreadPoolExecutor`. Dostępne ą dwa sposoby:

* `future.done()` Zwraca `True`, jeżeli zadanie zostanie zakończone (sukcesem, błęde lub anulowane), zwraca `False` jeżeli zadanie nadal działa w tle.
* `future.running()` - Zwraca `True`, jeżeli zadanie jest aktualnie wykonywane przez wątek.

Przykład

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

Środowisko Python pozwala na wcześniejsze zakończenie pracy zadań w wątku lub anulowanie zadań, które jeszcze nie rozpoczeły pracy a czekają na wykonanie. Dostępne jest kilka sposbów jak można to wykonać.

* Anulowanie zadania (`future.cancel()`) - metoda, która pozwala anulować zadanie, które zosały zlecona ale jeszcze nie są wykonywane. Zwraca True w sytuacji kiedy uda się anulowaćzadanie, zwraca False kiedy zadanie już trwa lub zostało zakończone

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

* Kontrolowanie zamykania (`shutdown`) - kiedy korzystane jest z bloku `with`, program autoamtycznie czeka aż wszystkie zadania zostaną zakończone.Można to kontrolować wywołując metodę `shotdown()` z odpowiednimi parametrami:
  * &#x20;`wait=False` powoduje że pula wątków kończy pracę natychmiast bez czekania aż zadani się zakończą.&#x20;
  * `cancel_futures=True` anutoomatycznie anuluje wszystkie zadania oczekujące na wykonanie w kolejce.

```python
executor = ThreadPoolExecutor(max_workers=2)
# ... zlecasz dużo zadań ...
executor.shutdown(wait=True, cancel_futures=True)
```

