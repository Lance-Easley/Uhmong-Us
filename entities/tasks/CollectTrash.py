from entities.tasks.BaseTask import *
import pygame


class CollectTrash(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.pull_up_arrow_hover = pygame.image.load('images/tasks/collect_trash/pull_up_arrow_hover.png').convert()
        self.pull_up_arrow = pygame.image.load('images/tasks/collect_trash/pull_up_arrow.png').convert()
        self.replaced_bag = pygame.image.load('images/tasks/collect_trash/replaced_bag.png').convert()
        self.grabbed_bag = pygame.image.load('images/tasks/collect_trash/grabbed_bag.png').convert()
        self.sacked_bag = pygame.image.load('images/tasks/collect_trash/sacked_bag.png').convert()
        self.full_bag = pygame.image.load('images/tasks/collect_trash/full_bag.png').convert()
        self.new_bag = pygame.image.load('images/tasks/collect_trash/new_bag.png').convert()
        self.wall = pygame.image.load('images/tasks/collect_trash/wall.png').convert()
        self.bin = pygame.image.load('images/tasks/collect_trash/bin.png').convert()

        self.pull_up_arrow_hover.set_colorkey((255, 255, 255))
        self.pull_up_arrow.set_colorkey((255, 255, 255))
        self.replaced_bag.set_colorkey((255, 255, 255))
        self.grabbed_bag.set_colorkey((255, 255, 255))
        self.sacked_bag.set_colorkey((255, 255, 255))
        self.full_bag.set_colorkey((255, 255, 255))
        self.new_bag.set_colorkey((255, 255, 255))
        self.bin.set_colorkey((255, 255, 255))

        self.bag_rect = pygame.Rect(745, 557, 420, 60)
        self.new_bag_rect = pygame.Rect(500, 445, 50, 440)
        self.trash_lifted_rect = pygame.Rect(855, 180, 200, 127)

        self.task_phase = 0

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_phase = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.wall, (480, 180))

        mouse_over_bag_rect = self.bag_rect.collidepoint(mouse_x, mouse_y)
        mouse_over_trash_lifted_rect = self.trash_lifted_rect.collidepoint(mouse_x, mouse_y)

        # Phase 0 & 1: sack and remove trash bag
        # Phase 2 & 3: place new bag
        # Phase 4: Task Complete

        if self.task_phase < 2:
            if pygame.mouse.get_pressed(3)[0]:
                if mouse_over_bag_rect:
                    self.task_phase = 1

                if self.task_phase == 1:
                    # Hover Highlight
                    if mouse_over_trash_lifted_rect:
                        self.display.blit(self.pull_up_arrow_hover,
                                          (self.trash_lifted_rect.x, self.trash_lifted_rect.y + 20))
                    else:
                        self.display.blit(self.pull_up_arrow, (self.trash_lifted_rect.x, self.trash_lifted_rect.y + 20))

                    self.display.blit(self.sacked_bag, (mouse_x - 175, mouse_y))
            else:
                if mouse_over_trash_lifted_rect and self.task_phase == 1:
                    self.task_phase = 2
                else:
                    self.task_phase = 0

        elif self.task_phase < 4:
            if pygame.mouse.get_pressed(3)[0]:
                if self.new_bag_rect.collidepoint(mouse_x, mouse_y):
                    self.task_phase = 3
            else:
                if mouse_over_bag_rect and self.task_phase == 3:
                    self.task_phase = 4
                else:
                    self.task_phase = 2

        self.display.blit(self.bin, (747, 590))

        # Images/Rects required to draw over trash bin
        if self.task_phase == 0:
            self.display.blit(self.full_bag, (745, 558))
        elif self.task_phase == 2:
            self.display.blit(self.new_bag, self.new_bag_rect)
        elif self.task_phase == 3:
            # Hover Highlight
            if mouse_over_bag_rect:
                pygame.draw.rect(self.display, (254, 254, 254), self.bag_rect, 5)
            else:
                pygame.draw.rect(self.display, (255, 255, 0), self.bag_rect, 5)

            self.display.blit(self.grabbed_bag, (mouse_x - 175, mouse_y))
        elif self.task_phase == 4:
            self.display.blit(self.replaced_bag, (745, 588))
            return self.success(dt)
