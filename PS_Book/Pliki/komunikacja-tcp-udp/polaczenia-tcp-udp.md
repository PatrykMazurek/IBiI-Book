# Połączenia TCP/UDP

Nawiązanie połączenia między serwerem a klientem wymaga utworzenia gniazda (ang. *socket*) po obu stronach. Utworzenie gniazd pozwala jednej ze stron nasłuchiwać nadchodzących połączeń, podczas gdy druga strona inicjuje połączenie z wybranym hostem. Możemy wyróżnić dwa główne protokoły komunikacyjne:

1. **TCP (Transmission Control Protocol)** – protokół połączeniowy i stabilny. W jego przypadku serwer musi zaakceptować przychodzące połączenie, a każdy wysłany pakiet wymaga potwierdzenia odbioru przez stronę przeciwną.
2. **UDP (User Datagram Protocol)** – protokół bezpołączeniowy, niegwarantujący dostarczenia danych. Pakiety wysyłane przez serwer nie wymagają potwierdzenia odbioru po stronie klienta. Pozwala to na uzyskanie większej prędkości przesyłu, jednak wiąże się z ryzykiem utraty pakietów lub zmiany ich kolejności.

#### Tworzenie gniazda

Do tworzenia gniazd sieciowych w języku Python wykorzystujemy wbudowaną bibliotekę `socket`. Wywołanie konstruktora `socket.socket()` wraz z odpowiednimi parametrami decyduje o rodzaju realizowanego połączenia. Poniżej przedstawiono jego główne argumenty:

```python
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0)
```

* **family** (rodzina adresów) – określa rodzaj adresacji, w oparciu o którą będziemy się komunikować w warstwie sieciowej.
  * **socket.AF_INET** (wartość domyślna) – wykorzystanie adresacji IPv4.
  * **socket.AF_INET6** – wykorzystanie adresacji IPv6.
  * **socket.AF_UNIX** (wcześniej `socket.UNIX`) – służy do komunikacji międzyprocesowej (IPC) w systemie, ale tylko w obrębie tego samego komputera. Przeznaczone dla systemów typu Unix/Linux/macOS. Zamiast adresu IP wykorzystuje ścieżkę do pliku.
  * **socket.AF_BLUETOOTH** – wykorzystywane do komunikacji przy użyciu Bluetooth.
* **type** (typ gniazda) – określa rodzaj komunikacji i protokołu w warstwie transportowej.
  * **socket.SOCK_STREAM** – tworzy gniazdo strumieniowe. Zapewnia niezawodną komunikację, w której zagwarantowane jest dostarczenie i prawidłowa kolejność pakietów. Wykorzystywane głównie z protokołem TCP.
  * **socket.SOCK_DGRAM** – tworzy gniazdo datagramowe. Pakiety mogą nie dotrzeć do celu lub pojawić się w innej kolejności. Wykorzystywane z protokołem UDP.
  * **socket.SOCK_RAW** – tworzy „surowe” gniazdo, które pozwala pominąć warstwę transportową systemu operacyjnego i konstruować własne nagłówki pakietów sieciowych.
* **proto** (protokół) – za pomocą tego parametru można określić konkretny typ protokołu użytego w gnieździe. Domyślnie przyjmuje wartość `0`, co pozwala systemowi automatycznie dobrać odpowiedni protokół w zależności od ustawionej rodziny i typu.

W konstruktorze możemy podać trzy parametry, jednak w większości typowych zadań wykorzystamy tylko dwa pierwsze (rodzinę i typ).