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
