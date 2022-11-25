from entities.tasks.BaseTask import *
import pygame


class NominateForAwards(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.desk = pygame.image.load('images/tasks/nominate_for_awards/desk.png').convert()
        self.cover = pygame.image.load('images/tasks/nominate_for_awards/cover.png').convert()
        self.card = pygame.image.load('images/tasks/nominate_for_awards/card.png').convert()
        self.pen = pygame.image.load('images/tasks/nominate_for_awards/pen.png').convert()

        self.pen.set_colorkey((255, 255, 255))

        self.card_surface = pygame.Surface((220, 120))
        self.card_rect = pygame.Rect(850, 480, 220, 120)
        self.card_pile_rect = pygame.Rect(1100, 246, 220, 120)

        self.drawn_amount = 0
        self.last_pencil_point = None

        self.mouse_was_down = False

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.card_surface.blit(self.card, (0, 0))
        self.card_rect = pygame.Rect(850, 480, 220, 120)

        self.last_pencil_point = None
        self.drawn_amount = 0

        self.mouse_was_down = False

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pencil_pos = (mouse_x - self.card_rect.x, mouse_y - self.card_rect.y)

        self.display.blit(self.desk, (480, 180))

        if pygame.mouse.get_pressed(3)[0]:
            if self.card_rect.collidepoint(mouse_x, mouse_y):
                if self.drawn_amount < 100:
                    if self.last_pencil_point is None:
                        pygame.draw.circle(self.card_surface, (0, 0, 255), pencil_pos, 2)
                    else:
                        pygame.draw.line(self.card_surface, (0, 0, 255), self.last_pencil_point, pencil_pos, 3)
                    if self.last_pencil_point != pencil_pos:
                        self.drawn_amount += 35 * dt
                        self.last_pencil_point = pencil_pos
                    # to help the transition from drawing to dragging
                    self.mouse_was_down = True
                elif not self.mouse_was_down:
                    pygame.draw.rect(self.display, (255, 255, 0), self.card_pile_rect, 5)
                    # drag card to box
                    self.card_rect.x = mouse_x - 110
                    self.card_rect.y = mouse_y - 60
            else:
                self.last_pencil_point = None
        else:
            self.mouse_was_down = False
            self.last_pencil_point = None

        if self.drawn_amount > 100:
            self.display.blit(self.cover, (860, 300))
        else:
            self.display.blit(self.cover, (823, 243))

        if not pygame.mouse.get_pressed(3)[0] and self.card_pile_rect.colliderect(self.card_rect):
            return self.success(dt)
        else:
            self.display.blit(self.card_surface, (self.card_rect.x, self.card_rect.y))
            if self.drawn_amount < 100:
                endpoint_x = mouse_x + 111 - round(self.drawn_amount * 0.76)
                endpoint_y = mouse_y - 113 + round(self.drawn_amount * 0.76)

                self.display.blit(self.pen, (mouse_x, mouse_y - 150))
                pygame.draw.circle(self.display, (0, 0, 255), (endpoint_x + 1, endpoint_y), 2.5)
                pygame.draw.circle(self.display, (0, 0, 255), (mouse_x + 37, mouse_y - 37), 2.5)
                pygame.draw.line(self.display, (0, 0, 255), (mouse_x + 36, mouse_y - 38), (endpoint_x, endpoint_y), 6)
