from random import randint

from shared.player import Player


class Game:
    WORLD_SIZE = (0, 0), (2500, 2500)

    def __init__(self):
        self.id_range = (1, 10000)
        self.player_ids = set()
        self.players = [
            # Player(1, 0, 0, 50, 50, (255, 0, 0)),  # Player 1
            # Player(2, 100, 100, 50, 50, (0, 0, 255))   # Player 2
        ]

    def set_player(self, player_id: int, player: Player):
        self.players[player_id] = player

    def generate_id(self):
        while True:
            new_id = randint(*self.id_range)
            if new_id not in self.player_ids:
                return new_id

    def add_player(self):
        player_id = self.generate_id()
        x = randint(self.WORLD_SIZE[0][0], self.WORLD_SIZE[1][0])
        y = randint(self.WORLD_SIZE[0][1], self.WORLD_SIZE[1][1])
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.player_ids.add(player_id)
        self.players.append(Player(player_id, x, y, color))
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
