import pygame as pg

from client_info import ClientInfo
from network import Network
from shared.player import Player


class GameMatch(ClientInfo):
    player: Player
    connected = True

    def __init__(self, network: Network):
        self.network = network
        self.player = self.network.receive()

    def event_loop(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.player.DISCONNECT = True
                self.quit = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.show_fps = not self.show_fps

                elif event.key == pg.K_ESCAPE:
                    self.player.DISCONNECT = True
                    self.connected = False

    def draw_world_border(self):
        # draw left line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y2 = 2500 + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw top line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = 2500 + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw right line
        x = 2500 + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = 2500 + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = 2500 + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw bottom line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = 2500 + self.screen_center.y - self.player.pos.y + self.player.height // 2
        x2 = 2500 + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = 2500 + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)

    def draw_other_player(self, other_player):
        color = other_player.color
        dx = other_player.pos.x - self.player.pos.x
        dy = other_player.pos.y - self.player.pos.y
        x = self.screen_center.x + dx
        y = self.screen_center.y + dy
        rect = (
            x - other_player.width//2,
            y - other_player.height//2,
            other_player.width,
            other_player.height
        )
        pg.draw.rect(self.screen, color, rect)

    def draw(self, player_list):
        self.screen.fill((128, 128, 128))
        for player in player_list:
            self.draw_other_player(player)
        self.player.draw(self.screen)

        self.draw_world_border()

        if self.show_fps:
            self.draw_fps()

    def update(self, delta_time):
        self.event_loop()

        self.player.handle_input(delta_time)

        self.network.send(self.player)

        player_list: dict = self.network.receive()

        if not player_list:
            self.connected = False
            return

        self.player = player_list.pop(self.player.id)

        other_players = player_list.values()

        self.draw(other_players)
