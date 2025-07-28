from random import randint
from itertools import count

from shared.player import Player


class GameData:
    WORLD_SIZE = (0, 0), (2500, 2500)

    def __init__(self):
        self.id_list = count(10000)  # starts from 10000 and goes on infinite
        self.player_ids = set()
        self.blues = {}
        self.reds = {}
        self.players = {}

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
        x = randint(self.WORLD_SIZE[0][0], self.WORLD_SIZE[1][0])
        y = randint(self.WORLD_SIZE[0][1], self.WORLD_SIZE[1][1])

        # If there are less or equal blues, then join blue. If there are fewer reds, then join red.
        blue_team = len(self.blues) <= len(self.reds)

        self.player_ids.add(player_id)

        player = Player(player_id, x, y, blue_team)
        self.players[player_id] = player

        if blue_team:
            self.blues[player_id] = player
        else:
            self.reds[player_id] = player

        return player_id

    def player_out_of_bounds(self, the_player: Player):
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
