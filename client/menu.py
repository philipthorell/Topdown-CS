import pygame as pg

from client_info import ClientInfo


class Menu(ClientInfo):
    server_connect_screen = False
    ip_insert_active = False
    connect_to_server = False
    show_connection_error = False
    text_input = ""

    def __init__(self):
        title_font = pg.font.SysFont("Consolas", 120)
        self.title_text = title_font.render("Topdown CS", 1, "lightblue")
        self.title_rect = self.title_text.get_rect(center=(self.screen_center.x, 170))

        self.online_btn = self.create_btn("Online")
        self.online_rect = self.online_btn.get_rect(center=(self.screen_center.x, 400))

        self.offline_btn = self.create_btn("Offline")
        self.offline_rect = self.offline_btn.get_rect(center=(self.screen_center.x, 550))

        self.server_input_box = pg.Rect(self.screen_center.x - 350, 300, 700, 70)
        self.connect_btn = pg.Surface((200, 60))
        self.connect_btn.fill("orange")
        self.connect_rect = self.connect_btn.get_rect(center=(700, 400))

        btn_font = pg.font.SysFont("Consolas", 40)
        btn_text = btn_font.render("Connect", 1, "lightblue")
        btn_rect = btn_text.get_rect(center=(self.connect_btn.get_width() // 2,
                                             self.connect_btn.get_height() // 2))

        self.connect_btn.blit(btn_text, btn_rect)

    def event_loop(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.quit = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.show_fps = not self.show_fps

                elif self.ip_insert_active:
                    if event.key == pg.K_RETURN:
                        self.connect_to_server = True

                    elif event.key == pg.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]

                    elif len(self.text_input) < 30:
                        self.text_input += event.unicode

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self.check_button_input(mouse_pos)

    def create_btn(self, text):
        box = pg.Surface((300, 90))
        box.fill("orange")

        btn_font = pg.font.SysFont("Consolas", 60)
        btn_text = btn_font.render(text, 1, "lightblue")
        btn_rect = btn_text.get_rect(center=(box.get_width()//2, box.get_height()//2))

        box.blit(btn_text, btn_rect)

        return box

    def draw_title(self):
        self.screen.blit(self.title_text, self.title_rect)

    def draw_buttons(self):
        self.screen.blit(self.online_btn, self.online_rect)
        self.screen.blit(self.offline_btn, self.offline_rect)

    def draw_server_connect(self):
        color = "lightblue" if self.ip_insert_active else "blue"
        pg.draw.rect(self.screen, color, self.server_input_box, 2)

        font = pg.font.SysFont("Consolas", 40)

        text_surface = font.render(self.text_input, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(self.server_input_box.x + 20,
                                                   self.server_input_box.y + (self.server_input_box.height//2) - (text_surface.get_height()//2)))

        self.screen.blit(text_surface, text_rect)

        self.screen.blit(self.connect_btn, self.connect_rect)

        if self.show_connection_error:
            error_font = pg.font.SysFont("Consolas", 40)

            error_surface = error_font.render("Couldn't connect to server.", True, (255, 0, 0))
            error_rect = error_surface.get_rect(center=(self.screen_center.x, 200))

            self.screen.blit(error_surface, error_rect)

    def draw(self):
        self.screen.fill((128, 128, 128))

        if self.server_connect_screen:
            self.draw_server_connect()
        else:
            self.draw_title()
            self.draw_buttons()

        if self.show_fps:
            self.draw_fps()

    def check_button_input(self, mouse_pos):
        if self.server_connect_screen:
            self.ip_insert_active = False
            if self.server_input_box.collidepoint(mouse_pos):
                self.ip_insert_active = True
            elif self.connect_rect.collidepoint(mouse_pos):
                self.connect_to_server = True

        else:
            if self.online_rect.collidepoint(mouse_pos):
                self.server_connect_screen = True
            elif self.offline_rect.collidepoint(mouse_pos):
                pass

    def update(self):
        self.event_loop()
        self.draw()
