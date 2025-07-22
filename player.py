import pygame as pg


class Player:
    def __init__(self, x, y, width, height, color):
        self.pos = pg.Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

    def handle_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.pos.x -= self.vel
        if keys[pg.K_RIGHT]:
            self.pos.x += self.vel
        if keys[pg.K_UP]:
            self.pos.y -= self.vel
        if keys[pg.K_DOWN]:
            self.pos.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.pos.x, self.pos.y, self.width, self.height)
