import pygame as pg
import pytmx

from random import randint
from itertools import count

from shared.player import Player


class GameData:
    WORLD_SIZE = (0, 0), (5888, 5888)

    def __init__(self):
        self.id_list = count(10000)  # starts from 10000 and goes on infinite
        self.player_ids = set()
        self.blues = {}
        self.reds = {}
        self.players = {}

        self.walls = []
        self.load_map()

    def get_player(self, player_id):
        return self.players[player_id]

    def update_player(self, player_id: int, player: Player):
        self.players[player_id] = player

    def generate_id(self):
        new_id = next(self.id_list)
        return new_id

    def remove_player_by_id(self, player_id):
        self.player_ids.remove(player_id)
        if self.players[player_id].blue_team:
            del self.blues[player_id]
        else:
            del self.reds[player_id]
        del self.players[player_id]

    def add_player(self):
        player_id = self.generate_id()

        # If there are less or equal blues, then join blue. If there are fewer reds, then join red.
        blue_team = len(self.blues) <= len(self.reds)

        x = 1750 if blue_team else 1200
        y = 550 if blue_team else 2650

        self.player_ids.add(player_id)

        player = Player(player_id, x, y, blue_team)
        self.players[player_id] = player

        if blue_team:
            self.blues[player_id] = player
        else:
            self.reds[player_id] = player

        return player_id

    def load_map(self):
        tmx_data = pytmx.TiledMap("../shared/maps/dust2.tmx")

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in ["walls", "boxes"]:
                for x, y, gid in layer:
                    tile_image = tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        px = x * tmx_data.tilewidth
                        py = y * tmx_data.tileheight
                        wall_rect = pg.Rect(px, py, tmx_data.tilewidth, tmx_data.tileheight)
                        self.walls.append(wall_rect)

    def check_player_collision(self,
                               player_id: int,
                               direction: tuple[float, float],
                               sprint: bool,
                               delta_time: float):

        player = self.players[player_id]

        speed = 180 * (3 if sprint else 1)
        dx, dy = direction

        dx *= speed * delta_time
        dy *= speed * delta_time

        for tile in self.walls:
            # Check for collision in x direction
            if tile.colliderect(player.pos.x + dx, player.pos.y, player.width, player.height):
                if dx < 0:
                    dx = tile.right - player.pos.x
                elif dx > 0:
                    dx = tile.left - (player.pos.x + player.width)

            # Check for collision in y direction
            if tile.colliderect(player.pos.x, player.pos.y + dy, player.width, player.height):
                if dy < 0:
                    dy = tile.bottom - player.pos.y
                elif dy > 0:
                    dy = tile.top - (player.pos.y + player.height)

        player.pos += pg.Vector2(dx, dy)

                    #new_rect = player_rect.move(dx, 0)
        #if not any(new_rect.colliderect(wall) for wall in self.walls):
        #    player_rect = new_rect

        # Then try moving on Y axis
        #new_rect = player_rect.move(0, dy)
        #if not any(new_rect.colliderect(wall) for wall in self.walls):
        #    player_rect = new_rect

        #new_pos = player_rect.topleft

        #player.pos = pg.Vector2(new_pos)
