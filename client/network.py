import socket
import pickle


class Network:
    client: socket.socket
    PORT = 5555
    HEADER = 64  # bytes
    FORMAT = "utf-8"

    def connect(self, server_ip: str):
        if not server_ip:
            return False

        address = (server_ip, self.PORT)

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(address)
            return True

        except socket.gaierror as e:
            print(f"[ERROR] (CONNECTION) socket.gaierror: {e}")
            print(f"IP address is not a valid IP address")
        except ConnectionRefusedError as e:
            print(f"[ERROR] (CONNECTION) ConnectionRefusedError: {e}")
        #except OSError as e:
        #    print(f"[ERROR] (CONNECTION) OSError: {e}")
        #    return False
        except TimeoutError as e:
            print(f"[ERROR] (CONNECTION) TimeoutError: {e}")
            return False

    def disconnect(self):
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()

    def receive(self):
        recv_length = self.client.recv(self.HEADER)

        if not recv_length:
            return
        recv_length = int(recv_length)

        data = self.client.recv(recv_length)
        player_list = pickle.loads(data)

        return player_list

    def send(self, data):
        try:
            msg = pickle.dumps(data)

            msg_length = len(msg)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))  # padding msg_length

            self.client.send(send_length)
            self.client.send(msg)

        except pickle.UnpicklingError as e:
            print(f"[ERROR] (SEND) Pickle error: {e}")
        except EOFError as e:
            print(f"[ERROR] (SEND) EOFError error: {e}")
        except socket.error as e:
            print(f"[ERROR] (SEND) Socket error: {e}")
