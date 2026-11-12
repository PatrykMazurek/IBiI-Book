# Zabezpieczenie TLS/SSL

W przypadkach, kiedy wymagane jest bezpieczeństwo w komunikacji między aplikacjami, stosuje się warstwę szyfrującą TLS/SSL. W języku Python dostępna jest biblioteka `ssl`, która pomaga przy wykonywaniu połączeń szyfrowanych.

Do utworzenia połączenia szyfrowanego niezbędny jest publiczny certyfikat i klucz prywatny. W środowisku testowym można wygenerować certyfikat samopodpisany (self-signed) stosując poniższą komendę w terminalu:

```bash
mkdir certs
openssl req -x509 -newkey rsa:2048 -nodes \
-keyout certs/server.key -out certs/server.crt -days 365 \
-subj "/CN=localhost"
```

Powyższe polecenie wygeneruje dwa pliki: publiczny certyfikat (`server.crt`) oraz klucz prywatny (`server.key`) i do wygenerowania wykorzysta algorytm RSA z kluczem o długości 2048 bitów.

W środowisku testowym musimy przekazać klientowi wygenerowany certyfikat, tak aby aplikacja mogła swobodnie działać. W realnych przypadkach korzystać będziemy z certyfikatów i kluczy wygenerowanych przez certyfikowane organizacje zewnętrzne. Korzystanie z zewnętrznych organizacji pozwala na ułatwienie komunikacji, a systemy operacyjne posiadają wbudowaną bazę zaufanych certyfikatów.

### Szyfrowanie TCP

#### Dołożenie warstwy szyfrującej

Podstawowym rozwiązaniem na szyfrowane połączenie jest zastosowanie biblioteki `ssl`, za pomocą której możemy do połączenia TCP dołożyć warstwę szyfrującą.

Poniższe przykłady przedstawiają zestawione połączenia klient-serwer z wykorzystaniem szyfrowania.

**Serwer TCP/TLS**

```python
import ssl, socket

HOST = "localhost"
PORT = 8443

CERT_FILE = "certs/server.crt"
KEY_FILE = "certs/server.key"

def create_tls_context():
    # konfigurowanie połączenia szyfrowanego
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

Powyższy przykład przedstawia aplikację serwera, która tworzy połączenie nasłuchujące na przychodzące połączenia. W powyższym przykładzie ważnym aspektem jest tworzenie połączenia szyfrowanego. Funkcja `create_tls_context()` odpowiada za stworzenie wymaganej konfiguracji. Metoda `ssl.SSLContext()` tworzy konfigurację TLS dla serwera, parametr `PROTOCOL_TLS_SERVER` pozwala środowisku Python/OpenSSL negocjować odpowiednią wersję TLS. Metoda `context.load_cert_chain(CERT_FILE, KEY_FILE)` wczytuje klucz i certyfikat serwera. Ważnym elementem jest metoda `tls_context.wrap_socket()`, która dodaje do połączenia warstwę szyfrującą, przyjmując jako parametry surowe połączenie z klientem (`raw_socket`) oraz flagę `server_side=True`, która jednoznacznie wskazuje, że gniazdo ma pełnić rolę serwera w komunikacji TLS.

**Klient TCP/TLS**

```python
import ssl, socket

HOST = "localhost" # Adres spójny z ustawieniami serwera
SERVER_NAME = "localhost"
PORT =  8443
CA_CERT = "certs/server.crt"

# Tworzenie kontekstu i wskazanie pliku certyfikatu dla serwera self-signed
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
# Pobranie wersji szyfrowania
context.minimum_version = ssl.TLSVersion.TLSv1_2

with socket.create_connection((HOST, PORT), timeout=10) as raw_socket:
    with context.wrap_socket(raw_socket, server_hostname=SERVER_NAME) as tls_socket:
        # pobranie informacji o certyfikacie, kodowaniu i wersji TLS
        print("TLS version:")
        print(tls_socket.version())
        print("Cipher:")
        print(tls_socket.cipher())
        print("Server certificate:")
        print(tls_socket.getpeercert())
        
        # Przesłanie informacji do serwera
        tls_socket.sendall(
            b"Hello through TLS!"
        )
        
        response = tls_socket.recv(4096)
        # Odczytanie informacji od serwera
        print("Response:")
        print(response.decode())
```

Powyższy przykład przedstawia szyfrowane połączenie w wersji laboratoryjnej, gdzie jawnie wskazujemy plik z certyfikatem urzędu CA, aby klient mógł pomyślnie zweryfikować tożsamość serwera posługującego się certyfikatem samopodpisanym.

#### Problemy z certyfikatami self-signed i przekazywanie certyfikatu

Gdy korzystamy z własnego certyfikatu, serwer automatycznie wysyła go do klienta przy próbie połączenia, ale klient domyślnie je odrzuca, ponieważ nie ufa wystawcy. Mamy dwa sposoby na rozwiązanie tego problemu:

**1. Przekazanie pliku (Podejście zalecane)**
Z serwera należy skopiować sam publiczny certyfikat (plik `.crt` lub `.pem`) i umieścić go na maszynie klienta kanałem pobocznym (np. przez bezpieczne połączenie SSH). Następnie klient wskazuje ten plik w kodzie: `context = ssl.create_default_context(cafile="sciezka/do/server.crt")`. Zwróć uwagę, że plik klucza prywatnego (`.key`) musi zawsze pozostać chroniony i nie może opuścić serwera!

**2. Wyłączenie weryfikacji (Tylko do testów developerskich)**
Jeśli zależy nam tylko na sprawdzeniu komunikacji sieciowej i nie przejmujemy się bezpieczeństwem, możemy kazać klientowi zignorować ostrzeżenia. Należy wtedy skonfigurować kontekst w następujący sposób:
```python
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```
Pamiętaj, że w środowisku produkcyjnym takie ustawienie jest niedopuszczalne, gdyż naraża aplikację na ataki Man-in-the-Middle.

#### Korzystanie z systemowej bazy certyfikatów

W środowisku produkcyjnym rzadko przekazujemy certyfikat plikiem bezpośrednio do klienta. Zamiast tego aplikacje klienckie polegają na systemowej bazie zaufanych certyfikatów (Trust Store), czyli np. publicznych certyfikatach głównych dostarczanych przez system operacyjny.

Aby zobaczyć to w działaniu, nie musimy odwoływać się do specyficznych dla danego systemu operacyjnego magazynów. Możemy użyć uniwersalnej metody `get_ca_certs()`. Wystarczy utworzyć domyślny kontekst SSL – Python automatycznie zlokalizuje i załaduje certyfikaty zaufane przez dany system (np. z katalogu `/etc/ssl/certs` na systemach Linux lub z systemowego magazynu Windows/macOS).

```python
import ssl
import pprint

# Utworzenie domyślnego kontekstu (automatycznie ładuje systemowe certyfikaty CA)
context = ssl.create_default_context()

# Pobranie listy załadowanych certyfikatów (w czytelnej formie słownika)
ca_certs = context.get_ca_certs(binary_form=False)

print(f"Z systemu załadowano {len(ca_certs)} certyfikatów zaufanych CA.\n")

# Wyświetlenie informacji o pierwszym certyfikacie z brzegu
if ca_certs:
    print("Przykładowy certyfikat (Wystawca / Podmiot):")
    # Zwrócony certyfikat zawiera m.in. klucz 'subject' (kogo dotyczy) i 'issuer' (kto wydał)
    pprint.pprint(ca_certs[0]['subject'])
```

### Szyfrowanie UDP 

#### Szyfrowanie UDP/DTLS

Dodanie warstwy szyfrującej dla protokołu UDP 

#### Zadania

#### Literatura

{% embed url="https://docs.python.org/3/library/ssl.html" %}