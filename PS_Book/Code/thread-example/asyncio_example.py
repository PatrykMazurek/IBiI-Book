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