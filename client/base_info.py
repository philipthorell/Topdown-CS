import pygame as pg


class BaseInfo:
    WIDTH, HEIGHT = 1200, 800
    screen_center = pg.Vector2(WIDTH // 2, HEIGHT // 2)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Client")
    clock = pg.time.Clock()
    FPS = 60

    quit = False

    delta_time: float = 0

    show_fps = True

    def draw_fps(self):
        fps = int(self.clock.get_fps())
        fps_font = pg.font.SysFont("Consolas", 12)
        fps_text = fps_font.render(f"FPS: {fps}", False, (0, 255, 0))
        black_rect = pg.Surface((50, 10))
        black_rect.blit(fps_text, (0, 0))
        self.screen.blit(black_rect, (0, 0))
