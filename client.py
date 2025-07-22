import pygame as pg

from network import Network


WIDTH, HEIGHT = 500, 500
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client")
clock = pg.time.Clock()
FPS = 60


class Game:
    running = True

    def __init__(self):
        self.network = Network()
        self.player = self.network.get_player()

        if self.player is None:
            self.running = False

    def draw(self, player2):
        screen.fill("white")
        player2.draw(screen)
        self.player.draw(screen)

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            player2 = self.network.send(self.player)

            self.player.handle_input()

            self.draw(player2)

            pg.display.flip()

            clock.tick(FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
