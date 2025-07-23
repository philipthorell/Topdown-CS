import socket
from threading import Thread, active_count
import pickle

from shared.player import Player


SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5555
SERVER_ADDRESS = (SERVER_IP, PORT)

MAX_PLAYERS = 2
HEADER = 64  # bytes
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)

print(f"[SERVER] Server is bound to ip: {SERVER_IP} on port: {PORT}")
print("[SERVER] Server is starting...")
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
    #print(f"[SERVER] Sending player {player} object: {players[player].__dict__}")
    connection.send(pickle.dumps(players[player]))

    connected = True
    while connected:
        try:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if not msg_length:
                continue
            msg_length = int(msg_length)

            msg = connection.recv(msg_length)
            received_data: Player = pickle.loads(msg)

            if not received_data:
                print(f"[SERVER] Player {player} lost connection!")
                connected = False
            else:
                player_out_of_bounds(received_data)

                players[player] = received_data

                reply = players

                connection.sendall(pickle.dumps(reply))

        except EOFError:
            connected = False

        except Exception as e:
            print("[SERVER] Error:", e)
            connected = False

    print(f"[SERVER] Player {player} disconnected!")
    connection.close()
    global current_player
    current_player -= 1


current_player = 0
while True:
    connection, address = server.accept()
    print(f"[NEW CONNECTION] {address} connected.")

    thread = Thread(target=threaded_client, args=(connection, current_player))
    thread.start()

    print(f"[ACTIVE CONNECTIONS] {active_count() - 1}")

    current_player += 1
