import pygame as pg

from network import Network


class Game:
    WIDTH, HEIGHT = 1200, 800
    screen_center = pg.Vector2(WIDTH//2, HEIGHT//2)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Client")
    clock = pg.time.Clock()
    FPS = 60

    running = True

    def __init__(self):
        self.network = Network()
        self.player = self.network.get_player()

        if self.player is None:
            self.running = False

    def draw_players(self, other_player):
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
            if player.id != self.player.id:
                self.draw_players(player)
        self.player.draw(self.screen)

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

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            self.player.handle_input()

            player_list = self.network.send(self.player)
            for player in player_list:
                if player.id == self.player.id:
                    self.player = player

            print(self.player.pos)

            self.draw(player_list)

            pg.display.flip()

            self.clock.tick(self.FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
