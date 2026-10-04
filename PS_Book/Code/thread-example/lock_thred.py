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