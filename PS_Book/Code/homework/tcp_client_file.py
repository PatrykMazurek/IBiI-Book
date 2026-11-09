import socket, os, struct, json, sys

def send_file():
    ADDR = "pmazurek.ddns.net"
    PORT = 5056
    FILE_NAME = "Nowy_statut.pdf"
    FILE_PATH = "C:\\Studia\\"+FILE_NAME
    file_size = os.path.getsize(FILE_PATH)
    metadate = {
        "file_name":FILE_NAME,
        "size":file_size,
        "author": 123556
    }

    json_string = json.dumps(metadate)
    json_byte = json_string.encode("UTF-8")
    json_length = len(json_byte)
    print(f"rozmiar pliku do przesłania:{json_length}")
    header = struct.pack(">I", json_length)
    print(f"Binarne bajty nagłówka {header}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ADDR, PORT))
            sock.sendall(header)
            sock.sendall(json_byte)

            send = 0
            with open(FILE_PATH, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    send += len(chunk)

                    procent = (send / file_size) * 100 if file_size > 0 else 100
                    sys.stdout.write(f"\r[>] Wysłano: {procent:.1f}% ({send}/{file_size} B)")
                    sys.stdout.flush()
            print("\n[*] Oczekiwanie na potwierdzenie od serwera...")
            response = sock.recv(1024).decode('utf-8')
            print(f"[+] Serwer zwrócił: {response}")
    except ConnectionRefusedError:
        print(f"\n[!] Błąd połączenia: Serwer {ADDR}:{PORT} odrzuca połączenie.")
        print("    Upewnij się, że serwer na Raspberry Pi jest uruchomiony i IP jest poprawne.")
    except Exception as e:
        print(f"\n[!] Wystąpił nieoczekiwany błąd komunikacji: {e}")

if __name__=="__main__":
    send_file()