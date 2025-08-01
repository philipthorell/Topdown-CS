import socket
from threading import Thread, active_count
import pickle
import time

from game_data import GameData


class NetworkServer:
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    PORT = 5555
    SERVER_ADDRESS = (SERVER_IP, PORT)

    MAX_PLAYERS = 2
    HEADER = 64  # bytes
    FORMAT = "utf-8"

    TICK_RATE = 64

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.SERVER_ADDRESS)

        print(f"[SERVER] Server is bound to ip: {self.SERVER_IP} on port: {self.PORT}")
        self.server.listen(self.MAX_PLAYERS)
        print("[SERVER] Waiting for a connection, Server started!")
        print("-" * 50)

        self.game_data = GameData()

        self.connections = {}
        self.player_inputs = {}

        Thread(target=self.server_loop, daemon=True).start()

    def send_with_header(self, obj):
        msg = pickle.dumps(obj)
        msg_length = str(len(msg)).encode(self.FORMAT)
        msg_length += b" " * (self.HEADER - len(msg_length))  # padding msg_length

        return msg_length, msg

    def send_all(self, sockets):
        """Broadcast the full game state to all connected clients"""
        state = {player_id: player.pos for player_id, player in self.game_data.players.items()}
        msg = pickle.dumps(state)
        msg_len = str(len(msg)).encode(self.FORMAT)
        msg_len += b" " * (self.HEADER - len(msg_len))

        for s in sockets:
            try:
                s.sendall(msg_len)
                s.sendall(msg)
            except:
                continue

    def handle_client(self, connection: socket.socket, player_id: int):
        player_obj = self.game_data.get_player(player_id)

        send_length, msg = self.send_with_header(player_obj)
        connection.send(send_length)
        connection.send(msg)

        try:
            while True:
                msg_length = connection.recv(self.HEADER)
                if not msg_length:
                    print("EMPTY RECEIVE FROM PLAYER ID:", player_id)
                    continue
                msg_length = int(msg_length.decode(self.FORMAT).strip())

                msg = connection.recv(msg_length)
                received_data = pickle.loads(msg)

                # {"dir": (x, y), "sprint": bool, "disconnect": bool}
                player_input = received_data

                if player_input.get("disconnect"):
                    print("PLAYER CHOSE TO DISCONNECT, ID:", player_id)
                    break

                self.player_inputs[player_id] = {
                    "dir": player_input.get("dir"),
                    "sprint": player_input.get("sprint")
                }

                """
                old_player = self.game_data.get_player(player_id)

                self.game_data.player_collide_with_objects(player_obj, old_player.pos)

                self.game_data.update_player(player_id, player_obj)

                reply = self.game_data.players

                data_length, data = self.send_with_header(reply)
                connection.sendall(data_length)
                connection.sendall(data)"""

        except EOFError as e:
            print(f"[ERROR] (player ID: {player_id}) EOFError: {e}")

        except ConnectionResetError as e:
            print(f"[ERROR] (player ID: {player_id}) ConnectionResetError: {e}")

        # except Exception as e:
        #    print("[SERVER] Error:", e)

        finally:
            print("-" * 50)
            connection.close()
            self.game_data.remove_player_by_id(player_id)

    def server_loop(self):
        last_time = time.time()
        while True:
            now = time.time()
            dt = now - last_time
            if dt < 1 / self.TICK_RATE:
                time.sleep((1 / self.TICK_RATE) - dt)
                continue
            last_time = now

            # Apply inputs to players
            for player_id in self.game_data.players.keys():
                move_input = self.player_inputs.get(player_id, {"dir": (0, 0), "sprint": False})
                self.game_data.check_player_collision(player_id, move_input["dir"], move_input["sprint"], dt)
                #player.move(move_input["dir"], move_input["sprint"], dt)

            # Send state to all clients
            self.send_all(list(self.connections.values()))

    def await_new_clients(self):
        while True:
            connection, address = self.server.accept()

            print(f"[NEW CONNECTION] {address} connected.")
            print(f"[ACTIVE CONNECTIONS] {active_count() - 1}")
            print("-" * 50)

            player_id = self.game_data.add_player()

            self.connections[player_id] = connection

            Thread(target=self.handle_client, args=(connection, player_id), daemon=True).start()


if __name__ == "__main__":
    network_server = NetworkServer()
    network_server.await_new_clients()
