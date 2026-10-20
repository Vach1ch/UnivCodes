# udp_client.py

import socket
import time

HOST = "127.0.0.1"
PORT = 6000

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

packet = b'A' * 4096

packets = 5000

start = time.perf_counter()

for _ in range(packets):
    sock.sendto(packet, (HOST, PORT))

finish = time.perf_counter()

sock.sendto(
    b"END",
    (HOST, PORT)
)

total_bytes = len(packet) * packets

throughput = (
    total_bytes * 8 /
    (finish - start)
) / 1_000_000

print(
    f"UDP скорость: "
    f"{throughput:.2f} Мбит/с"
)