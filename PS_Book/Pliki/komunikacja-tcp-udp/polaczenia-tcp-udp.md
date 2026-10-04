# Połączenia TCP/UDP

Do wykonania połączenia między serwerem a klientem wymagane jest stworzenie gniazda (socket) po obydwu stronach. Stworzenie gniazd pozwala na to aby jedna ze stron nasłuchiwała na połączenie a druga wykonywała połączenia z wybranym hostem. Możemy wyróżnić dwa rodzaje połączeń:

1. TCP (Transmission Control Protocol) - połączenie stabilne, w którym serwer musi zaakceptować przychodzące połączenie. Każdy wysłany pakiet przez serwer musi zostać potwierdzony przez klienta.
2. UDP (User Datagram Protocol) - połączenie mniej stabilne, narażone na utratę pakietów wysyłanych do klienta. Wysyłane pakiety przez serwer nie wymagają potwierdzenia po stronie klienta, co powoduje że można uzyskać większą prędkość przesyłania pakietów przy większym ryzyku utraty pakietów.

#### Tworzenie gniazda

Do stworzenia gniazd w języku Pythonie wykorzystujemy wbudowaną bibliotekę `socket`. Konstruktor `Socket()`, przy podaniu odpowiednich parametrów decyduje o rodzaju połączenia. Oto następujące parametry:

```python
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0)
```

* **family** (rodzaj adresacji) - określamy rodzaj adresowania po którym będziemy się komunikować w warstwie sieciowej.&#x20;
  * **socket.AF\_INET** (domyślny) - wykorzystanie adresacji IPv4 do wykonywania komunikacji.
  * socket.AF\_INET6 - wykorzystanie adresacji IPv6 do wykonywania komunikacji.
  * **socket.UNIX** - wykorzystywany do komunikacji między procesami (IPC) w systemie, ale tylko w obrębie tego samego komputera. Przeznaczone dla systemów typu Unix/Linux/macOS. Zamiast adresu IP wykorzystuje ścieżkę do pliku.
  * **socket.AF\_BLUETOOTH** - wykorzystywane do komunikacji przy użyciu bluetooth.
* **tyoe** (typ połączenia) - określenie rodzaju komunikacji i protokołu w warstwie sieciowej
  * **socket.SOCK\_STREAM** - tworzenie gniazda do komunikacji w której dostarczenie i kolejność pakietów jest zapewniona. Wykorzystywane z protokołem TCP.
  * **socket.SOCK\_DGRAM** - tworzenie gniazda datagramowe. Pakiety mogą nie dotzreć lub w innej kolejności. Wykorzystywane z protokołem UDP.
  * **socket.SOCK\_RAW** - tworzy "surowe" gniazdo, które pozwala ominąć warstwę transportową systemu operacyjnego i tworzyć własne nagłówki pakietów sieciowych.
* **proto** (protokuł) - za pomocą tego parametru można określi konkretny typ protokołu użytego w gnieździe. Domyślnie wartość "0" co pozwala systemowi automatycznie dobrać odpowiedni protokół w zależności od rodziny i typu.

W konstruktorze możemy podać 3 parametry ale w większości zadań wykorzystamy tylko dwa parametry.&#x20;
