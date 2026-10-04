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