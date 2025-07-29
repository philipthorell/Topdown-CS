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
        del self.players[player_id]

    def add_player(self):
        player_id = self.generate_id()

        # If there are less or equal blues, then join blue. If there are fewer reds, then join red.
        blue_team = len(self.blues) <= len(self.reds)

        x = 1750 if blue_team else 800
        y = 550 if blue_team else 800

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
            if hasattr(layer, 'data') and layer.properties.get("collidable", False):
                for x, y, gid in layer:
                    if gid != 0:  # If there's a tile at this position
                        px = x * tmx_data.tilewidth
                        py = y * tmx_data.tileheight
                        print(f"Wall tile at ({px}, {py}) is collidable")
                        wall_rect = pg.Rect(px, py, tmx_data.tilewidth, tmx_data.tileheight)
                        self.walls.append(wall_rect)

    def player_collide_with_objects(self, the_player: Player, old_player_pos: pg.Vector2):
        # if player is at the LEFT border
        if the_player.pos.x < self.WORLD_SIZE[0][0]:
            the_player.pos.x = self.WORLD_SIZE[0][0]
        # if player is at the RIGHT border
        if the_player.pos.x > self.WORLD_SIZE[1][0]:
            the_player.pos.x = self.WORLD_SIZE[1][0]
        # if player is at the TOP border
        if the_player.pos.y < self.WORLD_SIZE[0][1]:
            the_player.pos.y = self.WORLD_SIZE[0][1]
        # if player is at the BOTTOM border
        if the_player.pos.y > self.WORLD_SIZE[1][1]:
            the_player.pos.y = self.WORLD_SIZE[1][1]

        for wall in self.walls:
            rect = pg.Rect(the_player.pos.x, the_player.pos.y, the_player.rect.width, the_player.rect.height)
            if rect.colliderect(wall):
                print(the_player.pos, "PLAYER_POS")
                print(wall)
                print(f"[{wall[0]}, {wall[1]}], [{wall[2]}, {wall[3]}] WALL_POS")
                the_player.pos = old_player_pos
