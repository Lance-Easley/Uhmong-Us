from entities.tasks.BaseTask import *
import pygame


class RefillHandSanitizer(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.wall = pygame.image.load('images/tasks/refill_hand_sanitizer/wall.png').convert()
        self.buckle = pygame.image.load('images/tasks/refill_hand_sanitizer/buckle.png').convert()
        self.new_sanitizer = pygame.image.load('images/tasks/refill_hand_sanitizer/new_sanitizer.png').convert()
        self.old_sanitizer = pygame.image.load('images/tasks/refill_hand_sanitizer/old_sanitizer.png').convert()
        self.unlatched_buckle = pygame.image.load(
            'images/tasks/refill_hand_sanitizer/unlatched_buckle.png').convert()
        self.up_arrow_hover = pygame.image.load(
            'images/tasks/refill_hand_sanitizer/pull_up_arrow_hover.png').convert()
        self.up_arrow = pygame.image.load('images/tasks/refill_hand_sanitizer/pull_up_arrow.png').convert()

        self.wall.set_colorkey((255, 255, 255))
        self.buckle.set_colorkey((255, 255, 255))
        self.new_sanitizer.set_colorkey((255, 255, 255))
        self.old_sanitizer.set_colorkey((255, 255, 255))
        self.unlatched_buckle.set_colorkey((255, 255, 255))
        self.up_arrow_hover.set_colorkey((255, 255, 255))
        self.up_arrow.set_colorkey((255, 255, 255))

        self.lock_rect = pygame.Rect(920, 782, 80, 90)
        self.unlock_rect = pygame.Rect(920, 682, 80, 100)
        self.grab_old_sanitizer_rect = pygame.Rect(830, 382, 260, 394)
        self.sanitizer_lifted_rect = pygame.Rect(855, 180, 200, 127)
        self.grab_new_sanitizer_rect = pygame.Rect(500, 486, 260, 394)

        # difference between an object's coords and the mouse position
        self.grab_offset = (0, 0)

        self.task_phase = 0

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.task_phase = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.wall, (480, 180))

        if self.task_phase < 3:
            self.display.blit(self.old_sanitizer, (830, 382))
        elif self.task_phase == 4:
            self.display.blit(self.new_sanitizer, (500, 486))
        elif self.task_phase > 5:
            self.display.blit(self.new_sanitizer, (830, 382))

        if self.task_phase < 2 or self.task_phase == 8:
            self.display.blit(self.buckle, (830, 682))
        else:
            self.display.blit(self.unlatched_buckle, (830, 772))

        mouse_over_buckle = self.unlock_rect.collidepoint(mouse_x, mouse_y)
        mouse_over_sanitizer_slot = self.grab_old_sanitizer_rect.collidepoint(mouse_x, mouse_y)
        mouse_over_up_arrow = self.sanitizer_lifted_rect.collidepoint(mouse_x, mouse_y)
        mouse_over_new_sanitizer = self.grab_new_sanitizer_rect.collidepoint(mouse_x, mouse_y)
        mouse_over_unlocked_buckle = self.lock_rect.collidepoint(mouse_x, mouse_y)

        # pygame.draw.rect(self.display, (255, 255, 0), self.lock_rect, 3)

        # Phase 1 & 2: Sanitizer unlocked
        # Phase 3 & 4: Take out old sanitizer
        # Phase 5 & 6: Put in new sanitizer
        # Phase 7 & 8: Lock & Task Complete

        if self.task_phase < 2:
            if pygame.mouse.get_pressed(3)[0]:
                if mouse_over_buckle:
                    self.task_phase = 1
            else:
                # wait for mouse up before continuing
                if self.task_phase == 1:
                    self.task_phase = 2

            # Hover Highlight
            if mouse_over_buckle:
                pygame.draw.rect(self.display, (254, 254, 254), self.unlock_rect, 5)
            else:
                pygame.draw.rect(self.display, (255, 255, 0), self.unlock_rect, 5)

        elif self.task_phase < 4:
            if pygame.mouse.get_pressed(3)[0]:
                if mouse_over_sanitizer_slot:
                    if self.task_phase == 2:
                        self.grab_offset = (830 - mouse_x, 382 - mouse_y)
                        self.task_phase = 3

                if self.task_phase == 3:
                    # Hover Highlight
                    if mouse_over_up_arrow:
                        self.display.blit(self.up_arrow_hover,
                                          (self.sanitizer_lifted_rect.x, self.sanitizer_lifted_rect.y))
                    else:
                        self.display.blit(self.up_arrow,
                                          (self.sanitizer_lifted_rect.x, self.sanitizer_lifted_rect.y))
            else:
                if self.task_phase == 3 and mouse_over_up_arrow:
                    self.task_phase = 4
                else:
                    self.task_phase = 2

                    # Hover Highlight
                    if mouse_over_sanitizer_slot:
                        pygame.draw.rect(self.display, (255, 255, 0), self.grab_old_sanitizer_rect, 5)
                    else:
                        pygame.draw.rect(self.display, (254, 254, 254), self.grab_old_sanitizer_rect, 5)

        elif self.task_phase < 6:
            if pygame.mouse.get_pressed(3)[0]:
                if mouse_over_new_sanitizer:
                    if self.task_phase == 4:
                        self.grab_offset = (500 - mouse_x, 486 - mouse_y)
                        self.task_phase = 5

                if self.task_phase == 5:
                    # Hover Highlight
                    if mouse_over_new_sanitizer:
                        pygame.draw.rect(self.display, (255, 255, 0), self.grab_old_sanitizer_rect, 5)
                    else:
                        pygame.draw.rect(self.display, (254, 254, 254), self.grab_old_sanitizer_rect, 5)
            else:
                if self.task_phase == 5 and mouse_over_sanitizer_slot:
                    self.task_phase = 6
                else:
                    self.task_phase = 4

                    # Hover Highlight
                    if mouse_over_new_sanitizer:
                        pygame.draw.rect(self.display, (255, 255, 0), self.grab_new_sanitizer_rect, 5)
                    else:
                        pygame.draw.rect(self.display, (254, 254, 254), self.grab_new_sanitizer_rect, 5)
        elif self.task_phase < 8:
            if pygame.mouse.get_pressed(3)[0]:
                if mouse_over_unlocked_buckle:
                    self.task_phase = 7
            else:
                # wait for mouse up before continuing
                if self.task_phase == 7:
                    self.task_phase = 8
                else:
                    # Hover Highlight
                    if mouse_over_unlocked_buckle:
                        pygame.draw.rect(self.display, (254, 254, 254), self.lock_rect, 5)
                    else:
                        pygame.draw.rect(self.display, (255, 255, 0), self.lock_rect, 5)

        # Draw over all (drag phases & success)
        if self.task_phase == 3:
            self.display.blit(self.old_sanitizer, (self.grab_offset[0] + mouse_x, self.grab_offset[1] + mouse_y))
        elif self.task_phase == 5:
            self.display.blit(self.new_sanitizer, (self.grab_offset[0] + mouse_x, self.grab_offset[1] + mouse_y))
        elif self.task_phase == 8:
            return self.success(dt)
