# Połączenie TCP

Aplikacje działające na podstawie połączeń typu TCP (Transmission Control Protocol) zapewniają stabilną komunikacje między klientem a serwerem. Zapewnione jest to przez to że każdy przesłany pakiet przez serwer musi być potwierdzony przez klienta.

#### **Serwer  (**`tcp_server_example.py`**)**

```python
import socket

def start_tcp_server():
    # 1. Tworzymy gniazdo: AF_INET (IPv4), SOCK_STREAM (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # 2. Przypisujemy adres IP i port do gniazda
        server_socket.bind(('localhost', 12345))
        
        # 3. Nasłuchujemy nadchodzących połączeń (1 to rozmiar kolejki)
        server_socket.listen(1)
        print("Serwer TCP nasłuchuje na porcie 12345...")
        
        # 4. Akceptujemy połączenie - program zatrzyma się tutaj, czekając na klienta
        conn, addr = server_socket.accept()
        with conn:
            print(f"Połączono z klientem: {addr}")
            
            # 5. Odbieramy dane (max 1024 bajty)
            data = conn.recv(1024)
            print(f"Otrzymano od klienta: {data.decode('utf-8')}")
            
            # 6. Odpowiadamy klientowi
            conn.sendall(b"Wiadomosc odebrana! Pozdro z serwera TCP.")

if __name__ == "__main__":
    start_tcp_server()
```

Zadaniem aplikacji po stronie serwera jest nasłuchiwanie na przychodzące połączenie oraz wykonywanie założonej komunikacji. cały proces aplikacji mozna przedstawić w kilku krokach:

1. Tworzenie obiektu socket (`Socket`), któy  będzie nasłuchiwał na przychodzące połączenia
2. Przypisanie adresu i portu do obiektu socket (`bind`)
3. Nasłuchiwanie na przychodzące połączenia (`listen`), możliwość stworzenia kolejki oczekujących połączeń.
4. Akceptacja połączenia (`accept`) oraz pobranie informacji o połączeniu
5. Odbieranie danych przychodzących od klienta (`recv`), należy ustawić wielkość bufora.
6. Wysłanie odpowiedzi do klienta (`sendall`)

Krok 5 i 6 powtarzamy do momentu kiedy działa połączenie z klientem&#x20;

#### **Klient** (`tcp_client_example.py`)

Poniżej przedstawiam przykład aplikacji po stronie klienta&#x20;

```python
import socket

def tcp_client_example.py():
    # 1. Tworzymy gniazdo (takie samo jak w serwerze)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # 2. Nawiązujemy połączenie z serwerem
        client_socket.connect(('localhost', 12345))

        # 3. Wysyłamy wiadomość
        client_socket.sendall(b"Siema serwer, tu klient TCP!")

        # 4. Czekamy na odpowiedź
        data = client_socket.recv(1024)
        print(f"Odpowiedź z serwera: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_tcp_client()
```

Aplikacja klienta ma za zadanie nawiązać połączenie z wybranym serwerem i wykonywać założoną komunikacje. Powyższy przykład aplikacji po stronie klienta można przedstawić w kilku krokoach:

1. w pierwszyk kroku tworzone i otwierane jest gniazdo do wykonania połączenia, w konstruktorze podawane są odpoweidnie parametry.
2. następnie wykonywana jest metoda connect, w której jako parametr podawane są dane do połączenia tj. ardes i port.
3. w zależności od założeń komunikacji wykonywanej między urządzeniami, możemy wysłać dane lub czekać na dane od serwera. W powyższym przypadku najpierw wysyłamy dane do serwera.
4. Ostatnim krokiem jest odebranie danych od serwera i wyświetlenie ich na ekranie.

Powyższy przykład wykonyje jednokrotną komunikację z serwerem, aby powyższy przykład działał lepiej można przedstawić w pętli.

#### Zadania

1. Rozbuduj podane przykłady o możliwość przesyłania większej liczby wiadomości między serwerem a klientem.
2. Rozbuduj aplikacje po stronie z zadania 1 o możliwość obsługi większej liczby klientów. W zadaniu wykorzystaj wątki i stwórz rozwiązanie, w którym każde połączenie będzie obsługiwane w osobnym wątku.&#x20;
3. Do zadania 2 zaproponuj rozwiązanie za pomocą, którego będzie możliwość monitorowania ile połączeń jest aktywnych.
4. Stwórz mechanizm do zarządzania połączeniami z zadania 3, w taki sposób aby można było sprawdzić ile jest połączonych użytkowników oraz wyświetlić informacje o połączeniu tj. nazwa hosta, adres IP, data połączenia.&#x20;

#### Literatura&#x20;

{% embed url="https://realpython.com/python-sockets/" %}
