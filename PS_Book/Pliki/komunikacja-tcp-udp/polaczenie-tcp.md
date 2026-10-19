# Połączenie TCP

Aplikacje wykorzystujące protokół TCP (Transmission Control Protocol) zapewniają stabilną i niezawodną komunikację między klientem a serwerem. Wynika to z faktu, że dostarczenie każdego przesłanego pakietu musi zostać potwierdzone przez stronę odbierającą.

Podstawą działania zarówno aplikacji serwerowej, jak i klienckiej, jest gniazdo sieciowe (obiekt `socket`), które pozwala zdefiniować sposób komunikacji między aplikacjami.

Poniżej przedstawiono przykładowe implementacje aplikacji serwerowej oraz klienckiej.

#### **Serwer (`tcp_server_example.py`)**

```python
import socket

def start_tcp_server():
    # 1. Tworzymy gniazdo: AF_INET (IPv4), SOCK_STREAM (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # 2. Przypisujemy adres IP i port do gniazda
        server_socket.bind(('localhost', 12345))
        
        # 3. Nasłuchujemy nadchodzących połączeń (1 to rozmiar kolejki nieobsłużonych połączeń)
        server_socket.listen(1)
        print("Serwer TCP nasłuchuje na porcie 12345...")
        
        # 4. Akceptujemy połączenie - program zatrzyma się tutaj, czekając na klienta
        conn, addr = server_socket.accept()
        with conn:
            print(f"Połączono z klientem: {addr}")
            
            # 5. Odbieramy dane (maksymalnie 1024 bajty)
            data = conn.recv(1024)
            print(f"Otrzymano od klienta: {data.decode('utf-8')}")
            
            # 6. Odpowiadamy klientowi
            conn.sendall(b"Wiadomosc odebrana! Pozdro z serwera TCP.")

if __name__ == "__main__":
    start_tcp_server()
```

Głównym zadaniem aplikacji po stronie serwera jest nasłuchiwanie na nadchodzące połączenia oraz wymiana danych z klientami zgodnie z ustaloną specyfikacją. 

Pierwszym krokiem jest utworzenie obiektu `socket`. Kolejnym – zdefiniowanie, na jakim adresie (hoście) i porcie aplikacja ma oczekiwać na dane. Służy do tego metoda `bind()`. 
Aby gniazdo przeszło w tryb nasłuchiwania, wywołuje się metodę `listen()`. Informuje ona system operacyjny, że gniazdo jest gotowe do obsługi ruchu i pozwala ustalić wielkość kolejki dla oczekujących połączeń. 

Kluczowym momentem jest wywołanie metody `accept()`, która odpowiada za akceptację przychodzącego połączenia. Zwraca ona nowy obiekt gniazda dedykowany do komunikacji z podłączonym klientem oraz jego adres. 

Do odebrania informacji od klienta wykorzystuje się metodę `recv()`, ustalając rozmiar bufora przeznaczonego na przychodzące dane. Wysłanie odpowiedzi do klienta realizowane jest za pomocą metody `send()` lub `sendall()`. 

Podczas komunikacji musi być z góry ustalone, która aplikacja jako pierwsza wysyła dane, a która na nie oczekuje. Powyższy przykład wykorzystuje menedżer kontekstu (blok `with`), który automatycznie zarządza połączeniem i gwarantuje jego poprawne zamknięcie po wyjściu z bloku.

Domyślnie metoda `accept()` w znaczący sposób blokuje działanie aplikacji, czekając w nieskończoność na klienta. Aby temu zapobiec, można ustawić maksymalny czas oczekiwania na połączenie za pomocą metody `settimeout()`. Po jego upływie zostanie zgłoszony wyjątek, który należy obsłużyć.

```python
server_socket.settimeout(2.0)
try:
    conn, addr = server_socket.accept()
    # Obsługa połączenia...
except socket.timeout:
    pass # Minęły dwie sekundy, brak połączenia – można sprawdzić pętlę od nowa
except OSError:
    pass # Inny błąd gniazda
```

#### **Klient (`tcp_client_example.py`)**

Poniżej znajduje się przykład implementacji po stronie klienta:

```python
import socket

def start_tcp_client():
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

Celem aplikacji klienckiej jest nawiązanie połączenia z serwerem i wymiana informacji. Rozpoczynamy od utworzenia obiektu typu `socket`, podając parametry zgodne z konfiguracją serwera. 

Następnie wskazywany jest host i port docelowy w wywołaniu metody `connect()`. Po nawiązaniu połączenia można rozpocząć komunikację stosując odpowiednie metody:
* `recv()` – do pobrania danych z serwera (z określonym buforem).
* `send()` lub `sendall()` – do przesłania danych w kierunku serwera. 

Kolejność wywoływania metod zależy od tego, co jako pierwsze wykonywane jest po stronie serwera. Tutaj również wykorzystano blok `with`, który zarządza połączeniem – po zakończeniu pracy nie jest wymagane ręczne wywołanie metody `close()`, ponieważ system zamknie gniazdo automatycznie.

Zaprezentowany wyżej przykład ilustruje jedynie jednokrotną komunikację z serwerem. W rzeczywistych aplikacjach zazwyczaj stosuje się odpowiednie pętle i instrukcje warunkowe, aby podtrzymać wymianę danych.

#### Zadania

1. Rozbuduj podane przykłady tak, aby umożliwić przesyłanie wielu wiadomości (komunikację ciągłą) między serwerem a klientem.
2. Zmodyfikuj aplikację serwerową z zadania 1, tak aby mogła obsługiwać wielu klientów jednocześnie. Wykorzystaj wielowątkowość i stwórz rozwiązanie, w którym każde nowe połączenie jest obsługiwane przez osobny wątek.
3. Stwórz mechanizm do zarządzania połączeniami w aplikacji z zadania 2. Mechanizm powinien pozwalać na sprawdzenie liczby aktualnie podłączonych użytkowników oraz wyświetlanie podstawowych informacji o każdym połączeniu (tj. nazwa hosta/adres IP, data i czas nawiązania połączenia).

#### Literatura

{% embed url="https://realpython.com/python-sockets/" %}