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