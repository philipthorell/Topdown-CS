from dotenv import load_dotenv

import socket
from _thread import start_new_thread
import pickle
import os

from player import Player


load_dotenv()

server_ip = os.getenv("local_server_ip_address")
port = 5555
MAX_PLAYERS = 2


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((server_ip, port))
except socket.error as e:
    print(e)

server.listen(MAX_PLAYERS)
print("Waiting for a connection, Server started!")


players = [
    Player(0, 0, 50, 50, (255, 0, 0)),  # Player 1
    Player(100, 100, 50, 50, (0, 0, 255))   # Player 2
]


def threaded_client(connection: socket.socket, player: int):
    print(f"[SERVER] Sending player {player} object: {players[player].__dict__}")
    connection.send(pickle.dumps(players[player]))

    while True:
        try:
            received_data = pickle.loads(connection.recv(2048 * 2))

            if not received_data:
                print("Disconnected")
                break
            else:
                players[player] = received_data

                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received:", received_data)
                print("Sending:", reply)

            connection.sendall(pickle.dumps(reply))

        except Exception:
            break

    print("Lost connection!")
    connection.close()
    global current_player
    current_player -= 1


current_player = 0
while True:
    connection, address = server.accept()
    print("Connected to:", address)

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
