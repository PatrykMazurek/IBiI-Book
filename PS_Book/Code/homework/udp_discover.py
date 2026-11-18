import ipaddress
import socket, os


def discover_broadcast():
    network = ipaddress.IPv4Network("172.26.9.0/24", strict=False)
    print(f"Adres adres rozgłoszeniowy: {network.broadcast_address}")
    return network

def find_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        network = discover_broadcast()
        server_address = (str(network.broadcast_address), 5006)
        client_socket.sendto(b"DISCOVER_RPi", server_address)
        data, addr = client_socket.recvfrom(512)
        print(f"Odpowiedź z serwera: {data.decode('utf-8')}")

find_server()