import pygame as pg

from client_info import ClientInfo
from network import Network
from menu import Menu
from game_match import GameMatch


class Client(ClientInfo):
    running = True

    def __init__(self):
        self.network = Network()
        self.connected = False
        self.menu = Menu()
        self.game = None

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(self.FPS) / 1000  # convert from ms to seconds

            if self.menu:
                self.menu.update()

                if self.menu.quit:
                    self.running = False

                if self.menu.connect_to_server:
                    self.connected = self.network.connect(self.menu.text_input)
                    if self.connected:
                        print("CONNECTED TO SERVER")
                        self.game = GameMatch(self.network)
                        self.game.load_in_player()
                        self.menu = None
                    else:
                        print("FAILED TO CONNECT")
                        self.menu.connect_to_server = False
                        self.menu.show_connection_error = True

            elif self.game:
                self.game.update(self.delta_time)

                if self.game.quit:
                    self.running = False

                if not self.game.connected:
                    self.network.disconnect()
                    self.menu = Menu()
                    self.game = None

            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    client = Client()
    client.run()
