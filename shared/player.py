import pygame as pg


class Player:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    width, height = 50, 50

    velocity = 180

    DISCONNECT = False

    def __init__(self, player_id, x, y, blue_team):
        self.id = player_id

        self.pos = pg.Vector2(x, y)

        self.blue_team = blue_team

        self.color = (0, 0, 255) if blue_team else (255, 0, 0)

        draw_x = self.SCREEN_WIDTH//2 - self.width//2
        draw_y = self.SCREEN_HEIGHT//2 - self.height//2

        self.rect = pg.Rect(draw_x, draw_y, self.width, self.height)

    def draw(self, screen, offset: pg.Vector2 = None):
        if offset:
            if offset.x > self.pos.x and offset.y > self.pos.y:
                delta_pos = offset - self.pos
            else:
                delta_pos = self.pos - offset
            pg.draw.rect(screen, self.color, (delta_pos.x, delta_pos.y, self.width, self.height))
        else:
            pg.draw.rect(screen, self.color, self.rect)

    def handle_input(self, delta_time):
        keys = pg.key.get_pressed()

        speed = self.velocity * 3 if keys[pg.K_LSHIFT] else self.velocity

        if keys[pg.K_a]:
            self.pos.x -= speed * delta_time
        if keys[pg.K_d]:
            self.pos.x += speed * delta_time
        if keys[pg.K_w]:
            self.pos.y -= speed * delta_time
        if keys[pg.K_s]:
            self.pos.y += speed * delta_time
