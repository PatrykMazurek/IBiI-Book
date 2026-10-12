import asyncio, time

# 1 blokada kodu wolniejsze zadania
def long_task(task_id):
    print(f"Rozpoczęcie blokującego zapytania od klienta {task_id}")
    time.sleep(3)
    print(f"Zakończono zapytanie dla klienta {task_id}")
    return f"Dane klienta {task_id}"

async def main():
    start = time.time()

    task_1 = asyncio.to_thread(long_task, 1)
    task_2 = asyncio.to_thread(long_task, 2)

    re = await asyncio.gather(task_1, task_2)

    finish = time.time()

    print(f"wyniki: {re}")
    print(f"Czas wykonania: {finish - start:.2f} sekundy")



if __name__=="__main__":
    asyncio.run(main())



