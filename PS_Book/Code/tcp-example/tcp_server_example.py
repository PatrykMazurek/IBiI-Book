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