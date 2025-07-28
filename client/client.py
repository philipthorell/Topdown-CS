import pygame as pg

from network import Network
from shared.player import Player


class Game:
    WIDTH, HEIGHT = 1200, 800
    screen_center = pg.Vector2(WIDTH//2, HEIGHT//2)
    pg.font.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Client")
    clock = pg.time.Clock()
    FPS = 60

    running = True

    delta_time: float = 0

    show_fps = True

    def __init__(self):
        self.network = Network()
        self.player: Player = self.network.get_player()

        if self.player is None:
            self.running = False

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.player.DISCONNECT = True
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_F1:
                    self.show_fps = not self.show_fps

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

    def draw_fps(self):
        fps = int(self.clock.get_fps())
        fps_font = pg.font.SysFont("Consolas", 12)
        fps_text = fps_font.render(f"FPS: {fps}", False, (0, 255, 0))
        black_rect = pg.Surface((50, 10))
        black_rect.blit(fps_text, (0, 0))
        self.screen.blit(black_rect, (0, 0))

    def draw(self, player_list):
        self.screen.fill((128, 128, 128))
        for player in player_list:
            self.draw_other_player(player)
        self.player.draw(self.screen)

        self.draw_world_border()

        if self.show_fps:
            self.draw_fps()

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(self.FPS) / 1000

            # Handle events
            self.event_loop()

            self.player.handle_input(self.delta_time)

            player_list: dict = self.network.send(self.player)
            if not player_list:
                break

            self.player = player_list[self.player.id]

            other_players = [player for player_id, player in player_list.items() if player_id != self.player.id]

            #print(self.player.pos)

            self.draw(other_players)

            pg.display.flip()

        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
