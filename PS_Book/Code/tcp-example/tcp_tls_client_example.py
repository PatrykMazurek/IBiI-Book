import ssl, socket

HOST = "pi-server.home"
SERVER_NAME = "pi-server"
PORT =  8443

CA_CERT = "cert/server.crt"

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)

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
