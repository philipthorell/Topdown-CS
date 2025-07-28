import pygame as pg

from client_info import ClientInfo
from network import Network
from menu import Menu
from game_match import GameMatch


class Client(ClientInfo):
    running = True
    state = "Menu"

    def __init__(self):
        self.network = Network()
        self.menu = Menu()
        self.game = None

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(self.FPS) / 1000  # convert from ms to seconds

            if self.state == "Menu":
                self.menu.update()

                if self.menu.quit:
                    self.running = False

                if self.menu.connect_to_server:
                    connected = self.network.connect(self.menu.text_input)
                    if connected:
                        self.game = GameMatch(self.network)
                        self.menu = None
                        self.state = "Playing"
                    else:
                        self.menu.connect_to_server = False
                        self.menu.show_connection_error = True

            elif self.state == "Playing":
                self.game.update(self.delta_time)

                if self.game.quit:
                    self.running = False

                if not self.game.connected:
                    self.network.disconnect()
                    self.menu = Menu()
                    self.game = None
                    self.state = "Menu"

            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    pg.font.init()

    client = Client()
    client.run()
