from dotenv import load_dotenv

import socket
import os


load_dotenv()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv("local_server_ip_address")
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception:
            pass

    def send(self, data: str):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


n = Network()
print(n.send("hello"))
print(n.send("working"))
