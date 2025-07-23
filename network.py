from dotenv import load_dotenv

import socket
import pickle
import os


load_dotenv()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.getenv("local_server_ip_address")
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            player_data = self.client.recv(2048)
            return pickle.loads(player_data)
        except Exception as e:
            print(f"[Connection Error] {e}")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            recv_data = self.client.recv(2048)
            return pickle.loads(recv_data)
        except (pickle.UnpicklingError, EOFError) as e:
            print(f"Pickle error: {e}")
        except socket.error as e:
            print(f"Socket error: {e}")
