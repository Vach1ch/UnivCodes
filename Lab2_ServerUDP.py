# udp_server.py

import socket

HOST = "127.0.0.1"
PORT = 6000

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind((HOST, PORT))

received = 0

print("UDP-сервер запущен")

while True:

    data, addr = sock.recvfrom(65535)

    received += len(data)

    if data == b"END":
        break

print(
    f"Получено {received} байт"
)