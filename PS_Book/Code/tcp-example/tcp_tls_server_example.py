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
