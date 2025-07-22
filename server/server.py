from dotenv import load_dotenv

import socket
from _thread import start_new_thread
import sys
import os


load_dotenv()

server = os.getenv("local_server_ip_address")
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(3)
print("Waiting for a connection, Server started!")


def threaded_client(connection: socket.socket):
    connection.send(str.encode("Connected"))

    while True:
        try:
            data = connection.recv(2048)

            if not data:
                print("Disconnected")
                break
            else:
                reply = data.decode("utf-8")
                print("Received:", reply)
                print("Sending:", reply)

            connection.sendall(str.encode(reply))

        except Exception:
            break

    print("Lost connection!")
    connection.close()


while True:
    connection, address = s.accept()
    print("Connected to:", address)

    start_new_thread(threaded_client, (connection, ))
