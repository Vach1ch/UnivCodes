# tcp_block_test.py

import socket
import time
import numpy as np
import pandas as pd

HOST = "127.0.0.1"
PORT = 5000

TOTAL_SIZE = 20 * 1024 * 1024

block_sizes = [
    512,
    1024,
    4096,
    8192,
    16384,
    65536
]

results = []

for block_size in block_sizes:

    speeds = []

    for _ in range(10):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.connect((HOST, PORT))

        block = b'A' * block_size

        remaining = TOTAL_SIZE

        start = time.perf_counter()

        while remaining > 0:

            current = min(
                block_size,
                remaining
            )

            sock.sendall(block[:current])

            remaining -= current

        sock.shutdown(socket.SHUT_WR)

        finish = time.perf_counter()

        sock.close()

        speed = (
            TOTAL_SIZE * 8 /
            (finish - start)
        ) / 1_000_000

        speeds.append(speed)

    results.append([
        block_size,
        np.mean(speeds),
        np.std(speeds)
    ])

df = pd.DataFrame(
    results,
    columns=[
        "Размер блока",
        "Средняя скорость",
        "СКО"
    ]
)

print(df)