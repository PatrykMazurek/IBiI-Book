# Zabezpieczenie TSL\SSL

W przypadkach kiedy wymagane jest bezpieczeństwo w komunikacji między aplikacjami stosuje się warstwę szyfrującą TSL\SSL. W języku Python dostępna jest biblioteka `ssl`, która pomaga przy wykonywaniu połączeń  szyfrowanych.

Do utworzenia połączenia szyfrowanego niezbędny jest publiczny certyfikat i klucz prywatny. W środowisku testowym można wygenerować certyfikat samopodpisany (self-signed) stosując poniższ komendę w terminalu:

```
openssl req -x509 -newkey rsa:2048 -nodes \
-keyout key.pem -out cert.pem -days 365 \
-subj "/CN=localhost"
```

Powyższy polecenie wygeneruje dwa pliki: publiczny certyfikat (`cert.pem`) oraz klucz prywatny (`key.pem`) i do wygenerowania wykorzysta.

W środwisku testowym musimy przkazać klientowi wygenerowany ccertyfikat tak aby aplikacja mogła swobodnie działać. w Realnych przypadakch korzystać będziemy z certyfikatów i kluczy wygenerowanych przez certyfikowane organizacje zewnętrzne. Kożystanie z zewnętrnych organizacjii pozwala na ułatwienie ułatwienie komunikacji i systemy operacyjne posiadają bazę certyfiaktów.

#### Dołożenie wartswy szyfrującej

Podstawownym rozwiązaniem na szyfrowane połączenie jest zastosowanie biblioteki `ssl`, za pomocą której możemy do połączenia TCP dołożyć warstwe szyfrującą.&#x20;

Poniższe przykłady przedstawiają zestawione połączenia klient serwer z wykorzystaniem szyfrowania

**Serwer TCP/TLS**

```python
import ssl, socket

HOST = "localhost"
PORT = 8443

CERT_FILE = "certs/server.crt"
KEY_FILE = "certs/server.key"

def create_tls_context():
    # konfigurowanie połączenie szfroawnego
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    return context

tls_context = create_tls_context()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"TLS server działa na {HOST}:{PORT}")

    while True:
        raw_socket, address = server_socket.accept()
        print(f"TCP connection: {address}")
        # dołożenie warstwy szyfrującej do połączenia
        try:
            raw_socket.settimeout(10)
            with tls_context.wrap_socket(raw_socket, server_side=True) as tls_socket:
                # informacje o wersji i szyfrowaniu
                print("TLS:", tls_socket.version())
                print("Cipher:", tls_socket.cipher())
                # Odebranie danych od klienta
                data = tls_socket.recv(4096)
                print("Odebrano:", data)
                # Odpowiedz serwera 
                tls_socket.sendall(b"TLS server received: " + data)

        except ssl.SSLError as error:
            print("TLS error:", error)
        except TimeoutError:
            print("Connection timeout")
        finally:
            raw_socket.close()
```

Powyższy przykład przedstawia aplikacje serwera, która tworzy połączenie nasłuchujące na przychodzące połączenia. W powyższym przykładzie ważnym aspektem jest tworzenie połączenia szyfrowanego. Funkcje `create_tls_context()` odpowiada za stworzenie wymaganej konfiguracji. Metoda `ssl.SSLContext()` tworzy konfigurację TLS dla servera, parametr `PROTOCOL_TLS_SERVER` pozwala środowisku Python/OpenSSL negocjować  odpowiednią wersję TLS. Metoda `context.load_cert_chain(CERT_FILE, KEY_FILE)` wczytuje klucz i certyfikat serwera. Ważnym elementem jest metoda `tls_context.wrap_socket()`, która dodaje do połączenia warstwe szyfrującą przyjmując jako parametry surowe połączenie z klientem (`raw_socket`) oraz&#x20;

**Klient TCP/TLS**

```python
import ssl, socket

HOST = "pi-server.home"
SERVER_NAME = "pi-server"
PORT =  8443
CA_CERT = "cert/server.crt"
# 
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
# Pobranie wersji szyfrowania
context.minimum_version = ssl.TLSVersion.TLSv1_2

with socket.create_connection((HOST, PORT), timeout=10) as raw_socket:
    with context.wrap_socket(raw_socket, server_hostname=SERVER_NAME) as tls_socket:
        # pobranie inormacji o certyfikacie, kodowaniu, i wersji TLS
        print("TLS version:")
        print(tls_socket.version())
        print("Cipher:")
        print(tls_socket.cipher())
        print("Server certificate:")
        print(tls_socket.getpeercert())
        # Przesłąnie informacji do servera
        #logika servera
        tls_socket.sendall(
            b"Hello through TLS!"
        )
        
        response = tls_socket.recv(4096)
        # Odczytanie informacji od servera
        print("Response:")
        print(response.decode())
```

Powyższy przykład przedstawia szyfrowane połączenie, w wersji laboratoryjnej&#x20;

#### biblioteka asyncio

Nowszym rozwiązaniem jest zastosowanie biblioteki asyncio, która pozwala na asynchroniczne szyfrowane połączenie między urządzeniami.&#x20;

#### Zadania



#### Literatura

{% embed url="https://docs.python.org/3/library/ssl.html" %}
