import pygame

pygame.init()


class TaskHandler:
    def __init__(self):
        self.task_surface = pygame.Surface((960, 720))
        self.task_surface.set_colorkey((18, 52, 86))

        # Clean Window Resources
        self.clean_window_background = pygame.image.load('images/tasks/window_background.png')

        self.window_mark1 = pygame.image.load('images/tasks/window_mark1.png')
        self.window_mark1.set_colorkey((255, 255, 255))

        self.window_mark2 = pygame.image.load('images/tasks/window_mark2.png')
        self.window_mark2.set_colorkey((255, 255, 255))

        self.window_mark3 = pygame.image.load('images/tasks/window_mark3.png')
        self.window_mark3.set_colorkey((255, 255, 255))

        self.squeegee = pygame.image.load('images/tasks/squeegee.png')
        self.squeegee.set_colorkey((255, 255, 255))

    def renew_task_surface(self):
        self.task_surface.fill((18, 52, 86))

    def task_clean_windows(self, x: int, y: int, surface: pygame.Surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        surface.blit(self.clean_window_background, (x - 480, y - 360))
        surface.blit(self.window_mark1, (x - 50, y - 50))
        surface.blit(self.window_mark2, (x - 150, y + 100))
        surface.blit(self.window_mark3, (x + 150, y - 150))

        clean_rect = pygame.Rect(mouse_x - 99, mouse_y - 98, 197, 10)

        surface.blit(self.squeegee, (mouse_x - 100, mouse_y - 100))
