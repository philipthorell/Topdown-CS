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
print("[SERVER] Waiting for a connection, Server started!")


WORLD_SIZE = (0, 0), (2500, 2500)

players = [
    Player(1, 0, 0, 50, 50, (255, 0, 0)),  # Player 1
    Player(2, 100, 100, 50, 50, (0, 0, 255))   # Player 2
]


def player_out_of_bounds(the_player: Player):
    if the_player.pos.x < WORLD_SIZE[0][0]:
        the_player.pos.x = WORLD_SIZE[0][0]
    if the_player.pos.x > WORLD_SIZE[1][0]:
        the_player.pos.x = WORLD_SIZE[1][0]
    if the_player.pos.y < WORLD_SIZE[0][1]:
        the_player.pos.y = WORLD_SIZE[0][1]
    if the_player.pos.y > WORLD_SIZE[1][1]:
        the_player.pos.y = WORLD_SIZE[1][1]


def threaded_client(connection: socket.socket, player: int):
    print(f"[SERVER] Sending player {player} object: {players[player].__dict__}")
    connection.send(pickle.dumps(players[player]))

    while True:
        try:
            received_data: Player = pickle.loads(connection.recv(2048))

            if not received_data:
                print(f"[SERVER] Player {player} Disconnected")
                break
            else:
                player_out_of_bounds(received_data)

                players[player] = received_data

                reply = players
                #print("Received:", received_data)
                #print("Sending:", reply)

            connection.sendall(pickle.dumps(reply))

        except Exception as e:
            print("[SERVER] Error:", e)
            break

    print(f"[SERVER] Player {player} lost connection!")
    connection.close()
    global current_player
    current_player -= 1


current_player = 0
while True:
    connection, address = server.accept()
    print("[SERVER] Connected to:", address)

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
