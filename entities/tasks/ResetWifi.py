from entities.tasks.BaseTask import *
from random import randint
import pygame


class ResetWifi(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.progress_modifier = 1
        self.desktop_background = pygame.image.load('images/tasks/reset_wifi/desktop.png').convert()
        self.reset_symbol = pygame.image.load('images/tasks/reset_wifi/reset_symbol.png').convert()
        self.loading_bar = pygame.image.load('images/tasks/reset_wifi/loading_bar.png').convert()

        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.loading_text = self.font.render("Resetting...", True, (0, 0, 0))
        self.loading_text_rect = self.loading_text.get_rect()
        self.loading_text_rect.center = (SCREEN_HALF_X, SCREEN_HALF_Y)

        self.wifi_text = self.font.render("Reset Wifi", True, (0, 0, 0))
        self.wifi_text_rect = self.wifi_text.get_rect()
        self.wifi_text_rect.center = (SCREEN_HALF_X, SCREEN_HALF_Y)

        self.reset_button_rect = pygame.Rect(933, 508, 54, 64)

        self.loading_progress = 0
        self.has_clicked_reset = False

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.loading_progress = 0
        self.has_clicked_reset = False

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.desktop_background, (480, 180))

        # Visuals
        if self.has_clicked_reset:
            self.display.blit(self.loading_bar, (763, 568))
            pygame.draw.rect(self.display, "#00FF00", pygame.Rect(766, 571, (3.88 * self.loading_progress), 38))
            if not self.show_success:
                self.loading_progress += 30 * self.progress_modifier * dt

                if round(self.loading_progress % 20) == 0:
                    self.progress_modifier = randint(1, 10) / 10

                self.display.blit(self.loading_text, (763, 542))
        else:
            self.display.blit(self.reset_symbol, (933, 508))
            self.display.blit(self.wifi_text, (901, 464))

        if self.loading_progress > 100:
            self.loading_progress = 100
            self.show_success = True

        # Mouse Interactions
        if not self.show_success:
            if pygame.mouse.get_pressed(3)[0]:
                if not self.has_clicked_reset and self.reset_button_rect.collidepoint(mouse_x, mouse_y):
                    self.has_clicked_reset = True
        else:
            return self.success(dt)
