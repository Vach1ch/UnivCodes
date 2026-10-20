# tcp_server.py

import socket

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("TCP-сервер запущен...")

while True:
    conn, addr = server.accept()

    total = 0

    while True:
        data = conn.recv(4096)

        if not data:
            break

        total += len(data)

    print(f"Получено {total} байт")

    conn.close()