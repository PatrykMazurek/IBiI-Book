import socket, struct, os, json
import threading

WORK = True

def start_file_server(host='0.0.0.0', port=5056):
    global WORK
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.settimeout(10)
        sock.listen(1)
        print(f"nasłuchiwanie na {host}:{port}")
        while WORK:
            try:
                conn, addr = sock.accept()
                print(f"[TCP] Klient {addr} podłączony.")
                th = threading.Thread(target=tcp_file_receiver, args=(conn,))
                th.start()
            except socket.timeout:
                print("przekroczono oczekiwanie")

    print("Zakończenie pracy serwera")



def recv_exactly(sock, n):
    """Funkcja pomocnicza czytająca z gniazda dokładnie N bajtów."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None # Połączenie zerwane przed pobraniem całości
        data.extend(packet)
    return bytes(data)

def tcp_file_receiver(conn):
    try:
        raw_json_len = recv_exactly(conn, 4)
        if not raw_json_len:
            print("[!] Klient zamknął gniazdo przed wysłaniem nagłówka.")
        else:
            json_length = struct.unpack('>I', raw_json_len)[0]
            json_bytes = recv_exactly(conn, json_length)
            metadane = json.loads(json_bytes.decode('utf-8'))

            file_name = metadane.get('file_name', 'nieznany_plik')
            recive_size = metadane.get('size', 0)
            author = metadane.get('author', 'Anonim')
            file_data = bytearray()
            print(f"[*] Plik: {file_name} | Autor: {author} | Rozmiar: {recive_size} B")
            # pobieranie właściwego pliku
            save_size = 0
            with open(f"{author}_{file_name}", "wb") as f:
                while save_size < recive_size:
                    to_save = min(4096, recive_size - save_size)
                    chunk = conn.recv(to_save)
                    if not chunk:
                        break
                    f.write(chunk)
                    save_size += len(chunk)
            if save_size == recive_size:
                print(f"[+] Plik {file_name} zapisany pomyślnie!")
                conn.sendall(b"OK - PLIK ZAPISANY")
            else:
                print("[!] Błąd transferu - zerwano polaczenie.")
                conn.sendall(b"ERROR - ZERWANY TRANSFER")
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__=="__main__":
    th_start = threading.Thread(target=start_file_server)
    th_start.start()
    while WORK:
        print("podaj 'q' aby zakończyć prace")
        text = input()
        if text =="q":
            WORK = False
            break
    th_start.join()
    print("zakończenie programu")

