from entities.tasks.BaseTask import *
import pygame


class Lights(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.rack = pygame.image.load('images/sabotages/lights/rack.png').convert()
        self.button_on = pygame.image.load('images/sabotages/lights/button_on.png').convert()
        self.button_off = pygame.image.load('images/sabotages/lights/button_off.png').convert()

        self.button_rects = {
            1: pygame.rect.Rect(480, 380, 100, 100),
            2: pygame.rect.Rect(580, 380, 100, 100),
            3: pygame.rect.Rect(680, 380, 100, 100),
            4: pygame.rect.Rect(480, 480, 100, 100),
            5: pygame.rect.Rect(580, 480, 100, 100),
            6: pygame.rect.Rect(680, 480, 100, 100)
        }
        self.button_statuses = {
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False
        }

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.button_statuses = {
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False
        }

        self.task_surface.fill((18, 52, 86))

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed(3)[0]

        # Still needs testing and adjustments to look and function correctly
        self.display.blit(self.rack, (480, 180))

        # Visuals
        for key in range(1, 7):
            status = self.button_statuses[key]
            rect = self.button_rects[key]

            if mouse_pressed and rect.collidepoint(mouse_x, mouse_y):
                status = not status
            self.display.blit(self.button_on if status else self.button_off, rect)

        if all(self.button_statuses.values()):
            self.success(dt)
