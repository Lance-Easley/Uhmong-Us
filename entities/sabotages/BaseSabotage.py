from constants import *
import pygame

pygame.init()
pygame.font.init()


def bold_text(x: int, y: int, surface: pygame.Surface, outline: int, message: str):
    font = pygame.font.Font("freesansbold.ttf", 32)
    message_text = font.render(message, True, (0, 0, 0))
    message_text_rect = message_text.get_rect()

    # Outlines
    message_text_rect.center = (x + outline, y + outline)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x + outline, y)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x + outline, y - outline)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x, y + outline)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x, y - outline)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x - outline, y + outline)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x - outline, y)
    surface.blit(message_text, message_text_rect)

    message_text_rect.center = (x - outline, y - outline)
    surface.blit(message_text, message_text_rect)

    message_text = font.render(message, True, (255, 255, 255))
    message_text_rect = message_text.get_rect()
    message_text_rect.center = (x, y)
    surface.blit(message_text, message_text_rect)


def render_newline_text(x: int, y: int, text: str, surface: pygame.Surface, separation: int, font: pygame.font.Font):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        surface.blit(font.render(line, True, (0, 0, 0)), (x, y + separation * index))


class BaseSabotage:
    def __init__(self, surface: pygame.Surface):
        self.display = surface

        self.sabotage_surface = pygame.Surface((960, 720))
        self.sabotage_surface.set_colorkey((18, 52, 86))

        self.show_success = False
        self.show_failure = False
        self.frame = 35

    def success(self, dt: float):
        if self.frame > 0:
            bold_text(SCREEN_HALF_X, SCREEN_HALF_Y, self.display, 2, "Sabotage Completed!")

            self.frame -= 40 * dt
        else:
            return True

    def fail(self, dt: float):
        if self.frame > 0:
            bold_text(SCREEN_HALF_X, SCREEN_HALF_Y, self.display, 2, "Sabotage Failed.")

            self.frame -= 40 * dt
        else:
            return True
