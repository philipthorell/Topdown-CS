import socket
from threading import Thread, active_count
import pickle

from game import Game


SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5555
SERVER_ADDRESS = (SERVER_IP, PORT)

MAX_PLAYERS = 2
HEADER = 64  # bytes
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)

print(f"[SERVER] Server is bound to ip: {SERVER_IP} on port: {PORT}")
print("[SERVER] Server is starting...")
server.listen(MAX_PLAYERS)
print("[SERVER] Waiting for a connection, Server started!")
print("-" * 50)


game = Game()


def send_with_header(obj):
    msg = pickle.dumps(obj)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))  # padding msg_length

    return send_length, msg


def threaded_client(connection: socket.socket, player_id: int):
    player_obj = game.get_player(player_id)

    send_length, msg = send_with_header(player_obj)
    connection.send(send_length)
    connection.send(msg)

    connected = True
    while connected:
        try:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if not msg_length:
                print("EMPTY RECEIVE")
                continue
            msg_length = int(msg_length)

            msg = connection.recv(msg_length)
            received_data = pickle.loads(msg)  # Player Object

            if not received_data:
                print(f"[SERVER] Player {player_id} lost connection!")
                connected = False
            else:
                player_obj = received_data

                if player_obj.DISCONNECT:
                    print("PLAYER CHOSE TO DISCONNECT, ID:", player_id)
                    connected = False
                    continue

                game.player_out_of_bounds(player_obj)

                game.update_player(player_id, player_obj)

                reply = game.players

                data_length, data = send_with_header(reply)
                connection.sendall(data_length)
                connection.sendall(data)

        except EOFError:
            print(f"[SERVER] Player {player_id} disconnected! [EOFError]")
            connected = False

        except Exception as e:
            print("[SERVER] Error:", e)
            connected = False

    print("-" * 50)
    connection.close()
    game.remove_player_by_id(player_id)


while True:
    connection, address = server.accept()
    print(f"[NEW CONNECTION] {address} connected.")
    print(f"[ACTIVE CONNECTIONS] {active_count()}")
    print("-" * 50)

    player_id = game.add_player()

    thread = Thread(target=threaded_client, args=(connection, player_id))
    thread.start()
