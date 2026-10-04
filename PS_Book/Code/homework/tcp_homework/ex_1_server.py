import socket

def start_tcp_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 5500))
        server_socket.listen(1)
        print("server TCP nasłuchuje na porcie 5500...")
        conn, addr = server_socket.accept()
        print(f"połązcenie z klientem {addr}")
        while conn:
            conn.send(bytes(str("podaj dowolny tekst, albo 'q' aby zakonczyc komunikacje").encode("utf-8")))
            # server oczekuje na wiadomość
            data = conn.recv(1024)
            if data.decode("utf-8") == "q":
                conn.sendall(b"bye!")
                print("zakończenie komunikacji mięzy klientem a serwerem")
                break
            conn.sendall(b"dzienki za tekst")


if __name__ == "__main__":
    print("rozpoczęcie pracy serwera")
    start_tcp_server()

