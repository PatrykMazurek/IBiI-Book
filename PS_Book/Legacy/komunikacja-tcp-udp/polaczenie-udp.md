# Połączenie UDP

Aplikacje oparte na komunikacji UDP (*User Datagram Protocol*) nie gwarantują niezawodnego dostarczenia pakietów między serwerem a klientem. Oznacza to, że pakiety mogą zostać utracone, zduplikowane lub dotrzeć w niewłaściwej kolejności. Brak mechanizmów potwierdzania doręczenia (*acknowledgements*) oraz kontroli przepływu sprawia jednak, że komunikacja jest szybsza i charakteryzuje się mniejszym narzutem sieciowym.

#### **Serwer (**`udp_serwer_example.py`**)**

```python
import socket

def start_udp_server():
    # 1. Tworzymy gniazdo: AF_INET (IPv4), SOCK_DGRAM (UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # 2. Przypisujemy adres i port, na którym serwer będzie nasłuchiwał
        server_socket.bind(('localhost', 54321))
        print("Serwer UDP nasłuchuje na porcie 54321...")
        
        # 3. Odbieramy dane bezpośrednio (brak metod listen() oraz accept())
        data, addr = server_socket.recvfrom(1024)
        print(f"Otrzymano wiadomość: '{data.decode('utf-8')}' od {addr}")
        
        # 4. Odsyłamy odpowiedź do nadawcy
        server_socket.sendto(b"Wiadomosc UDP dotarla elegancko!", addr)

if __name__ == "__main__":
    start_udp_server()
```

Powyższy przykład przedstawia prostą aplikację serwerową korzystającą z protokołu UDP. W pierwszym kroku tworzymy gniazdo sieciowe za pomocą klasy `socket`, wybierając rodzinę adresów `AF_INET` (IPv4) oraz protokół `SOCK_DGRAM` (datagramowy, czyli UDP). Następnie za pomocą metody `bind()` wiążemy gniazdo z konkretnym adresem IP oraz portem.

W przeciwieństwie do protokołu TCP, w UDP nie nawiązujemy połączenia przed transmisją. Aplikacja nie wywołuje metod `listen()` ani `accept()`. Odbiór danych realizowany jest za pomocą metody `recvfrom(1024)`, która blokuje wykonanie programu do momentu odebrania pakietu. Metoda ta zwraca zarówno treść wiadomości, jak i krotkę `(adres_ip, port)` zawierającą adres nadawcy. Odpowiedź do klienta wysyłamy za pomocą metody `sendto()`, przekazując bajty oraz adres docelowy.

#### **Klient (**`udp_client_example.py`**)**

```python
import socket

def start_udp_client():
    # 1. Tworzymy gniazdo UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        server_address = ('localhost', 54321)
        
        # 2. Wysyłamy dane bezpośrednio pod adres serwera (bez connect())
        client_socket.sendto(b"Siema serwer, lecimy na UDP!", server_address)
        
        # 3. Czekamy na ewentualną odpowiedź od serwera
        data, addr = client_socket.recvfrom(1024)
        print(f"Odpowiedź z serwera: {data.decode('utf-8')}")

if __name__ == "__main__":
    start_udp_client()
```

Powyższy kod przedstawia aplikację kliencką. Podobnie jak w przypadku serwera, na początku tworzymy gniazdo `socket` z trybem UDP. Klient nie musi wywoływać metody `bind()`, ponieważ system operacyjny automatycznie przypisze mu wolny port lokalny podczas wysyłania pierwszego pakietu.

Wywołanie metody `sendto()` pozwala na natychmiastowe przesłanie danych do serwera bez uprzedniego uzgadniania połączenia (brak metody `connect()`). Odbiór odpowiedzi od serwera realizujemy analogicznie za pomocą metody `recvfrom()`.

W obu przykładach nie występują żadne pakiety kontrolne ani procesy handshake (znane z TCP). Protokół UDP umożliwia wysłanie wiadomości niezależnie od tego, czy druga strona jest w danym momencie uruchomiona i gotowa do odbioru.

---

#### Zadania do wykonania

1. **Echo z odwracaniem wyrazów:**  
   Napisz dwie aplikacje (klient i serwer UDP), które umożliwią przesyłanie wiadomości tekstowych. Aplikacja serwera powinna nasłuchiwać na porcie `5000` i odsyłać do klienta każdą otrzymaną wiadomość, zamieniając kolejność wyrazów na przeciwną, o ile wiadomość zawiera więcej niż jeden wyraz. Serwer powinien wyświetlać w konsoli adres IP oraz port nadawcy. Aplikacja kliencka powinna umożliwić użytkownikowi wprowadzanie tekstu z klawiatury – po wpisaniu słowa `"exit"` program kończy pracę. W kliencie należy na bieżąco wyświetlać komunikaty powrotne z serwera.

2. **Kalkulator sieciowy JSON:**  
   Zaimplementuj prosty kalkulator działający w architekturze klient-serwer oparty na UDP. Klient przesyła do serwera obiekt w formacie `JSON` zawierający dwa argumenty liczbowe oraz nazwę operacji matematycznej. Serwer wykonuje obliczenia i odsyła wynik również w formacie `JSON`. Komunikacja powinna odbywać się na porcie `5001`. Obsługiwane operacje to: dodawanie, odejmowanie, mnożenie oraz dzielenie. Serwer powinien poprawnie obsługiwać błędne dane wejściowe oraz próbę dzielenia przez zero.

3. **Przesyłanie dużego pliku:**  
   Stwórz aplikację serwerową, której zadaniem jest przesłanie do klienta zawartości dużego pliku tekstowego. Ponieważ pakiety UDP mają ograniczenia rozmiaru (oraz ryzyko zgubienia), serwer powinien podzielić plik na mniejsze fragmenty (np. paczki po 1024 bajty) i przesyłać je sekwencyjnie. Klient odbiera poszczególne fragmenty i zapisuje je finalnie do nowego pliku tekstowego. Na zakończenie napisz skrypt sprawdzający (np. poprzez porównanie sum kontrolnych MD5 lub bezpośrednie otwarcie), czy dane są kompletne i identyczne z oryginałem.

4. **Czat grupowy:**  
   Napisz prosty czat grupowy oparty na protokole UDP. Użytkownicy powinni mieć możliwość dołączenia do serwera, podania swojego pseudonimu oraz wymieniania wiadomości z pozostałymi uczestnikami. Serwer pełni funkcję centralnego pośrednika: odbiera pakiety od jednego klienta i przekazuje je do wszystkich pozostałych zarejestrowanych uczestników. Przygotuj następujące komendy sterujące protokołem komunikacyjnym:
   * `REGISTER <nick>` – dodaje klienta do aktywnej listy użytkowników,
   * `UNREGISTER` – usuwa klienta z listy,
   * `LIST` – zwraca użytkownikowi listę aktualnie podłączonych osób,
   * `SEND <nick> <wiadomosc>` – wysyła prywatną wiadomość do wskazanego użytkownika,
   * `BROADCAST <wiadomosc>` – rozsyła wiadomość publiczną do wszystkich klientów.

5. **Mechanizm utrzymania połączenia (Heartbeat / Keep-Alive):**  
   Rozbuduj aplikację serwerową z zadania 4 tak, aby okresowo (np. co 120 sekund) weryfikowała, czy klienci nadal istnieją i nasłuchują. Do tego celu zastosuj mechanizm `PING` – `PONG`. Serwer wysyła pakiet `PING` do klienta i czeka 5 sekund na odpowiedź. Procedurę można powtórzyć maksymalnie 3 razy – w przypadku braku odpowiedzi klient jest automatycznie usuwany z listy aktywnych uczestników. Klient po odebraniu komunikatu `PING` natychmiast odsyła pakiet `PONG`. *Wskazówka:* Ponieważ aplikacje testujesz lokalnie na `localhost`, pamiętaj o dodaniu unikalnego identyfikatora klienta, aby poprawnie przetestować działanie mechanizmu dla wielu instancji uruchomionych na tej samej maszynie.

---

#### Literatura
* Doozer, J. *High-Performance Networking with Python sockets.*
* Kurose, J. F., Ross, K. W. *Computer Networking: A Top-Down Approach.*