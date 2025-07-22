import pygame as pg

from player import Player


WIDTH, HEIGHT = 500, 500
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client")
clock = pg.time.Clock()
FPS = 60

client_number = 0


class Game:
    running = True

    def __init__(self):
        self.player = Player(50, 50, 100, 100, (0, 255, 0))

    def draw(self):
        screen.fill("white")
        self.player.draw(screen)

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.player.handle_input()

            self.draw()

            pg.display.flip()

            clock.tick(FPS)

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
