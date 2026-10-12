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

