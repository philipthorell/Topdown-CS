import pygame as pg
import pytmx

from client_info import ClientInfo
from network import Network
from shared.player import Player


class GameMatch(ClientInfo):
    player: Player
    connected = True

    WORLD_END = (2944, 2944)

    def __init__(self, network: Network):
        self.network = network
        self.player = self.network.receive()

        self.inputs = {"dir": (0, 0), "sprint": False, "disconnect": False}

        self.walls = []
        self.world_sprites = []

        self.show_debug = False

        self.load_map()

    def event_loop(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.inputs["disconnect"] = True
                self.quit = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.show_fps = not self.show_fps

                elif event.key == pg.K_F2:
                    self.show_debug = not self.show_debug

                elif event.key == pg.K_ESCAPE:
                    self.player.DISCONNECT = True
                    self.connected = False

    def load_map(self):
        tmx_data = pytmx.load_pygame("../shared/maps/dust2.tmx")

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in ["walls", "boxes"]:
                for x, y, gid in layer:
                    tile_image = tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        px = x * tmx_data.tilewidth
                        py = y * tmx_data.tileheight
                        wall_rect = pg.Rect(px, py, tmx_data.tilewidth, tmx_data.tileheight)
                        self.walls.append(wall_rect)

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in ["ground", "walls", "boxes"]:
                for x, y, gid in layer:
                    tile_image = tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        self.world_sprites.append(
                            (tile_image,
                             (x * tmx_data.tilewidth, y * tmx_data.tileheight))
                        )

    def draw_world(self):
        for sprite, pos in self.world_sprites:
            x = pos[0] + self.screen_center.x - self.player.pos.x - self.player.width // 2
            y = pos[1] + self.screen_center.y - self.player.pos.y - self.player.height // 2
            self.screen.blit(sprite, (x, y))

    def draw_wall_rects(self):
        for wall in self.walls:
            x = wall[0] + self.screen_center.x - self.player.pos.x - self.player.width // 2
            y = wall[1] + self.screen_center.y - self.player.pos.y - self.player.height // 2
            rect = (x, y, wall[2], wall[3])
            pg.draw.rect(self.screen, (255, 0, 0), rect, 1)

    def draw_world_border(self):
        # draw left line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y2 = self.WORLD_END[1] + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw top line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = self.WORLD_END[0] + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw right line
        x = self.WORLD_END[0] + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y = 0 + self.screen_center.y - self.player.pos.y - self.player.height // 2
        x2 = self.WORLD_END[0] + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = self.WORLD_END[1] + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)
        # draw bottom line
        x = 0 + self.screen_center.x - self.player.pos.x - self.player.width // 2
        y = self.WORLD_END[1] + self.screen_center.y - self.player.pos.y + self.player.height // 2
        x2 = self.WORLD_END[0] + self.screen_center.x - self.player.pos.x + self.player.width // 2
        y2 = self.WORLD_END[1] + self.screen_center.y - self.player.pos.y + self.player.height // 2
        pg.draw.line(self.screen, "black", (x, y), (x2, y2), 1)

    def draw_other_player(self, other_player):
        color = (0, 0, 255) if other_player.blue_team else (255, 0, 0)
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

        self.draw_world()

        for player in player_list:
            self.draw_other_player(player)
        self.player.draw(self.screen)

        if self.show_debug:
            self.draw_wall_rects()

        self.draw_world_border()

        if self.show_fps:
            self.draw_fps()

    def movement(self):
        keys = pg.key.get_pressed()
        dx = dy = 0

        if keys[pg.K_w]:
            dy -= 1
        if keys[pg.K_s]:
            dy += 1
        if keys[pg.K_a]:
            dx -= 1
        if keys[pg.K_d]:
            dx += 1

        sprint = keys[pg.K_LSHIFT]

        self.inputs["dir"] = (dx, dy)
        self.inputs["sprint"] = sprint

    def update(self):
        self.event_loop()

        self.movement()

        self.network.send(self.inputs)

        # {player_id: player_pos, ...}
        player_list: dict = self.network.receive()

        if not player_list:
            self.connected = False
            return

        self.player.pos = player_list.pop(self.player.id)

        print(self.player.pos)

        other_players = player_list.values()

        self.draw(other_players)
