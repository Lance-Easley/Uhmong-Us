from entities.tasks.BaseTask import *
import pygame


class CheckTemperature(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.scanner = pygame.image.load('images/tasks/check-temperature/scanner.png').convert()
        self.scanner_rect = pygame.Rect(810, 420, 300, 300)

        self.progress = 0

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.progress = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.scanner, (480, 180))

        # Visuals
        if pygame.mouse.get_pressed(3)[0] and self.scanner_rect.collidepoint(mouse_x, mouse_y) and self.progress < 150:
            self.progress += 40 * dt
            pygame.draw.rect(self.display, (255, 255, 255), (785, 420 + (self.progress * 2), 350, 10))
        elif self.progress >= 150:
            return self.success(dt)
        else:
            self.progress = 0
