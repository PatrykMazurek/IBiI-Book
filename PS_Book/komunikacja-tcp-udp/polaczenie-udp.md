# Połączenie UDP

Aplikacje oparte o komunikację UDP (User Datagram Protocol) nie gwarantują dostarczenia pakietów między serwerem a klientem, co może powodować utratę niektórych pakietów lub dostarczenie ich w niewłaściwej kolejności. Brak potwierdzenia po stronie klienta powoduje że komunikacje jest szybsza.

#### **Serwer (**`udp_serwer_example.py`**)**

```python
import socket

def start_udp_server():
    # 1. Tworzymy gniazdo: AF_INET (IPv4), SOCK_DGRAM (UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # 2. Przypisujemy adres i port
        server_socket.bind(('localhost', 54321))
        print("Serwer UDP nasłuchuje na porcie 54321...")
        
        # 3. Od razu odbieramy dane (nie ma listen() ani accept())
        data, addr = server_socket.recvfrom(1024)
        print(f"Otrzymano wiadomość: '{data.decode('utf-8')}' od {addr}")
        
        # 4. Odsyłamy odpowiedź do nadawcy
        server_socket.sendto(b"Wiadomosc UDP dotarla elegancko!", addr)

if __name__ == "__main__":
    start_udp_server()
```

Powyższy przykład przedstawia aplikacje po stronie serwera stosującą komunikację UDP. Zadaniem aplikacji jest nasłuchiwanie na klientów i odsyłanie odpowiednich pakietów do klienta. Proces można przedstawić w kilku krokach:



1. tworzenie obiektu typu Socket do wysyłania odpowiednich pakietów
2. Przypisanie odpowiednich adresu i portu (`bind`)
3. Odbieranie informacji od klienta, który chce otrzymywać pakiety wysyłane przez serwer (`recvfrom`).
4. Wysyłanie odpowiedzi do klienta (`sendto`)

#### **Klient (**`udp_client_example.py`**)**

```python
import socket

def start_udp_client():
    # 1. Tworzymy gniazdo UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        server_address = ('localhost', 54321)
        
        # 2. Wysyłamy dane prosto pod adres serwera (bez connect())
        client_socket.sendto(b"Siema serwer, lecimy na UDP!", server_address)
        
        # 3. Czekamy na ewentualną odpowiedź
        data, addr = client_socket.recvfrom(1024)
        print(f"Odpowiedź z serwera: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_udp_client()
```

Powyższy kod przedstawia tworzenie aplikacji klienckiej do odbierania wiadomości i można ją przedstawić w kilku krokach.

1. Otwarcie gniazda i ustawienie odpowiedniego trybu pracy&#x20;
2. Ustawienie odpowiedniego adresu i portu do komunikacji.
3. Wysłanie wiadomości do serwera aby serwer wiedziała że istniejemy.
4. Odbieranie informacji przesłanych przez serwer.

#### Zadania

1. Napisz prosty serwer UDP, który odsyła odebraną wiadomość w odwrotnej kolejności.
2. Rozbuduj klienta UDP tak, aby wysyłał wiadomości w pętli (np. co sekundę).
3. Sprawdź, co się stanie, gdy:
   * serwer nie działa,
   * klient poda błędny port,
   * wysłane dane będą większe niż rozmiar bufora.
4. Skorzystaj z obiektów JSON i przygotuj aplikację serwerową tak aby rozsyłała informacje w postaci JSON-a, a klient odpowiednio je odbierała i wyświetlał na ekran.
5. Stwórz aplikację, którą będzie działać na zasadzie "broadcast-u" i rozsyłać wiadomości do wszystkich, któryż w danym momencie nasłuchują. Stwórz rozwiązanie, które pozwoli identyfikować użytkowników i wywołać do wszystkich z pominięciem nadawcy. &#x20;

#### Literatura
