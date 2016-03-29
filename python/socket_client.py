# -*- coding: utf-8 -*-

import socket as socketlib

HOST = "127.0.0.1"
PORT = 50029
BUFFER_SIZE = 64 * 1024 * 1024


if __name__ == "__main__":
    socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
    socket.create_connection((HOST, PORT), timeout=20)
    print("Connected to %s:%d" % (HOST, PORT))

    data = b"0123456789" * 2048
    print("Sending data, len = ", len(data))
    socket.send(data)

    print("Waiting for data")
    data = socket.recv(BUFFER_SIZE)
    while data:
        print("Received len=", len(data))
        data = socket.recv(BUFFER_SIZE)

    socket.close()
    print("Socket closed")
