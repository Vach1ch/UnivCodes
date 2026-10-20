# tcp_client.py

import socket
import time
import pandas as pd
import matplotlib.pyplot as plt

HOST = "127.0.0.1"
PORT = 5000

sizes_mb = [1, 5, 10, 20, 50]

results = []

for size_mb in sizes_mb:

    data = b'A' * (size_mb * 1024 * 1024)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORT))

    start = time.perf_counter()

    sock.sendall(data)

    sock.shutdown(socket.SHUT_WR)

    end = time.perf_counter()

    sock.close()

    elapsed = end - start

    throughput_bps = len(data) * 8 / elapsed
    throughput_mbps = throughput_bps / 1_000_000

    results.append([
        size_mb,
        elapsed,
        throughput_mbps
    ])

df = pd.DataFrame(
    results,
    columns=[
        "Объем (МБ)",
        "Время (с)",
        "Пропускная способность (Мбит/с)"
    ]
)

print(df)

plt.plot(
    df["Объем (МБ)"],
    df["Пропускная способность (Мбит/с)"],
    marker="o"
)

plt.title("Пропускная способность TCP")
plt.xlabel("Объем данных (МБ)")
plt.ylabel("Мбит/с")
plt.grid(True)
plt.show()