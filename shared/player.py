import pygame as pg


class Player:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    width, height = 50, 50

    def __init__(self, player_id, x, y, color):
        self.id = player_id

        self.pos = pg.Vector2(x, y)
        self.color = color

        draw_x = self.SCREEN_WIDTH//2 - self.width//2
        draw_y = self.SCREEN_HEIGHT//2 - self.height//2

        self.rect = pg.Rect(draw_x, draw_y, self.width, self.height)
        self.vel = 3

    def draw(self, screen, offset: pg.Vector2 = None):
        if offset:
            if offset.x > self.pos.x and offset.y > self.pos.y:
                delta_pos = offset - self.pos
            else:
                delta_pos = self.pos - offset
            pg.draw.rect(screen, self.color, (delta_pos.x, delta_pos.y, self.width, self.height))
        else:
            pg.draw.rect(screen, self.color, self.rect)

    def handle_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.pos.x -= self.vel
        if keys[pg.K_d]:
            self.pos.x += self.vel
        if keys[pg.K_w]:
            self.pos.y -= self.vel
        if keys[pg.K_s]:
            self.pos.y += self.vel

        self.update()

    def update(self):
        #self.rect = (self.pos.x, self.pos.y, self.width, self.height)
        pass
