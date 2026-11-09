import socket, os

def get_local_info():
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    return hostname, local_ip

def udp_discovery_server(host='0.0.0.0', port=5006):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    hostname, address_ip = get_local_info()
    print(f"[UDP] Serwer Discovery nasłuchuje na {host}:{port}")

    try:
        while True:
            data, addr = sock.recvfrom(512)
            message = data.decode('utf-8').strip()

            if message == "DISCOVER_RPi":
                print(f"[Odkrycie] Zapytanie od {addr[0]}:{addr[1]}")

                # Zbieranie prostej metryki (np. Load Average na RPi)
                try:
                    load = os.getloadavg()
                    response = f"ACK_RPi|Load:{load[0]}|hostname:{hostname}|ip_address:{address_ip}"
                except AttributeError:
                    response = "ACK_RPi|Load:N/A"

                # Odesłanie odpowiedzi do klienta
                sock.sendto(response.encode('utf-8'), addr)
    except KeyboardInterrupt:
        print("\n[UDP] Zamykanie serwera.")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_discovery_server()