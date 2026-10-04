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
