import socket

def client_connection():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("localhost", 5500))
        # odebranie wiadomości od serwera
        while True:
            data = client_socket.recv(1024)
            print(data.decode("utf-8"))
            data_to_send: str = input()
            client_socket.sendall(bytes(str(data_to_send).encode(encoding="utf-8")))
            if data_to_send == "q":
                data = client_socket.recv(1024)
                print(data.decode("utf-8"))
                print("zakończenie komunikacji z serwerem")
                break
            data = client_socket.recv(1024)
            print(f"wizdomość z serwera: \n{data.decode("utf-8")}" )

if __name__ == "__main__":
    client_connection()
