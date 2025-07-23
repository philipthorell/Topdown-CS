from dotenv import load_dotenv

import socket
import pickle
import os


load_dotenv()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_IP = os.getenv("local_server_ip_address")
        self.PORT = 5555
        self.ADDRESS = (self.SERVER_IP, self.PORT)
        self.HEADER = 64  # bytes
        self.FORMAT = "utf-8"

        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.ADDRESS)

            recv_length = self.client.recv(self.HEADER)
            recv_length = int(recv_length)

            player_data = self.client.recv(recv_length)
            return pickle.loads(player_data)

        except Exception as e:
            print(f"[ERROR] Connection error: {e}")

    def send(self, data):
        """

        :param data: Player object
        :return: list of player objects
        """
        try:
            msg = pickle.dumps(data)
            msg_length = len(msg)
            print("msg_length:", msg_length)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))  # padding msg_length

            self.client.send(send_length)
            self.client.send(msg)

            recv_length = self.client.recv(self.HEADER)
            recv_length = int(recv_length)
            print("recv_length:", recv_length)

            recv_data = self.client.recv(recv_length)
            return pickle.loads(recv_data)

        except (pickle.UnpicklingError, EOFError) as e:
            print(f"[ERROR] Pickle error: {e}")
        except socket.error as e:
            print(f"[ERROR] Socket error: {e}")
