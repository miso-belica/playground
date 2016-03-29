# -*- coding: utf-8 -*-

import socket as socketlib
from time import sleep

HOST = ""  # symbolic name meaning all available interfaces
PORT = 50029  # arbitrary non-privileged port
BUFFER_SIZE = 64 * 1024 * 1024


if __name__ == "__main__":
    s = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
    s.bind((HOST, PORT))

    s.listen(1)
    conn, addr = s.accept()
    print("Connected by", addr)

    print("Waiting for data")
    data = conn.recv(BUFFER_SIZE)
    if data:
        print("Received data and sending them back, len =", 1000)
        conn.sendall(data[:1000])
        sleep(5)
        print("Sending them back - 2nd part, len =", len(data[1000:]))
        conn.sendall(data[1000:])
    else:
        print("No data received")

    sleep(10)
    conn.close()
    s.close()
