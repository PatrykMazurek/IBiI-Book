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

#### Biblioteka asyncio

Biblioteka, której zadaniem jest wykonywanie różnych zadań w sposób asynchroniczny bazując na jednym wątku. W porównaniu do biblioteki threading nie są tworzone wątki systemowe ale bazując na jednym wątku wykonanie kilku zadań "jednocześnie" odpowiednio rozkładając obciążenie na każde z zadań.&#x20;

Przykład:

```python
import asyncio, time, random

async def download_data(task_is, task_time):
    print(f"start zadania {task_is}")
    # symulacja operacji I/O
    result = random.randint(0,1000)
    await asyncio.sleep(task_time)
    return f"Zadanie {task_is}, wynik {result}"

async def main():
    start_time = time.time()

    task_1 = asyncio.create_task(download_data(1, 2))
    task_2 = asyncio.create_task(download_data(2, 3))
    task_3 = asyncio.create_task(download_data(3, 1))

    print("Wszystkie zadania zostały zlecone, program robi inne rzeczy...")

    re_1 = await task_1
    re_2 = await task_2
    re_3 = await task_3

    finish_time = time.time()
    print(f"\nWszystkie zadania ukończone w czasie: {finish_time - start_time:.2f} sekundy")
    print(f"Otrzymane wyniki: {re_1}, {re_2}, {re_3}")

if __name__=="__main__":
    asyncio.run(main())
```

Powyższy przykład przedstawia wykonywanie trzech zadań asynchronicznie i odbieranie wyników przez pętle główną. Na poczku jest definiowane zadanie, które wspiera asynchroniczne działanie (`async def`), funkcja ma symulować dłuższe zadanie. W funkcji zastosowano rozwiązanie `await asyncio.slle()` do chwilowego zatrzymania zadania a nie blokowania całego wątku. Wywołanie asynchronicznych zadań odbywa się przez wywołanie metody `asyncio.create_task()` Metoda jako parametr przyjmuje np. funkcje, która ma być wykonana asynchronicznie. Następnie program główny oczekuje na zakończenie zadania przez słowo kluczowe `await`. uruchomienie głównej cześći programu wykonywane jest za pomocą metody `asyncio.run()`.&#x20;



#### Zadania

1. Napisz program wielowątkowy, który korzystaj z `ThreadPoolExecutor` i stałej puli wątków o liczbie `n`. Wypełnij listę **łącznie 1000 elementów**. Spośród wylosowanych liczb dodawaj do wspólnej listy tylko te, które są podzielne przez `3`. Zakres losowanych liczb całkowitych przyjmij jako parametr programu i podaj go przy prezentacji wyniku; dopuszczaj powtórzenia. Synchronizuj zapis do wspólnej listy. Zakończ pracę wątków jeżeli liczba elementów w liście osiągnie 1000 elementów.
2. Zasymuluj system zamówień w restauracji. Stwórz wątek-Kucharz: dodaje gotowe potrawy do bezpiecznej wątkowo kolejki `queue.Queue` oraz stwórz pulę wątków w liczbie 2 wątki-Kelnerzy, których zadaniem jest  pobieranie z kolejki elementów (potraw) dodanych przez wątek-kucharz i symulowanie roznoszenia potraw. Zastosuj opóźnienie (`time.sleep`) z losową wartością oraz wyświetlaj komunikaty o dodaniu i pobraniu elementów z kolejki.
3. Napisz funkcję asynchroniczną `fetch_data(id, sleep_time)`, która zwraca komunikat `"Dane z ID: {id}"` po upływie `sleep_time` sekund. W funkcji `main()` utwórz dwa zadania za pomocą `asyncio.create_task`, w międzyczasie wyświetl napis `"Wykonuję inne operacje..."`, a na koniec poczekaj na wyniki zadań
4. Napisz prosty system producent-konsument z użyciem `asyncio.Queue`. Producent (`producer`) generuje 5 elementów (liczby od 1 do 5) w odstępie 0.5 sekundy i wrzuca je do kolejki. Konsument (`consumer`) pobiera elementy z kolejki i przetwarza je (np. wypisuje na ekran z opóźnieniem 1 sekundy).
   1. Zmodyfikuj zadanie tak aby można było podać liczbę elementów, które ma produkować producent (`producer`).
5. \* Stwórz aplikację bazującą na wielowątkowości, która ma za zadanie odczytywać strony internetowe i pobierać informacje w postaci adres URL, opis strony, język strony (lang). Aplikacja ma szukać linków dostępnych na stronie i odwiedzać unikalne linki, które jeszcze nie były odwiedzane. Zadanie ma działać przynajmniej 20 minut, wyniki zapis do pliku w trzech formatach: strony odwiedzone (adres URL, opis, język strony), linki do odwiedzenia, linki błędne.
