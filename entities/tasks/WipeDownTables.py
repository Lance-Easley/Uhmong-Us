from entities.tasks.BaseTask import *
from random import randint
import pygame


class WipeDownTables(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

        # Resources
        self.table_background = pygame.image.load("images/tasks/wipe_down_tables/tabletop.png").convert()

        self.table_mark1 = pygame.image.load("images/tasks/wipe_down_tables/mark1.png").convert()
        self.table_mark1.set_colorkey((255, 255, 255))
        self.table_mark2 = pygame.image.load("images/tasks/wipe_down_tables/mark2.png").convert()
        self.table_mark2.set_colorkey((255, 255, 255))
        self.table_mark3 = pygame.image.load("images/tasks/wipe_down_tables/mark3.png").convert()
        self.table_mark3.set_colorkey((255, 255, 255))

        self.rag = pygame.image.load("images/tasks/wipe_down_tables/rag.png").convert()
        self.rag.set_colorkey((255, 255, 255))

        self.dirty_layer = pygame.Surface((960, 720))
        self.dirty_layer.set_colorkey("#123456")

        self.mark_coords = ((randint(60, 750), randint(60, 510)),
                            (randint(60, 750), randint(60, 510)),
                            (randint(60, 800), randint(60, 560)))

        self.clean_status = (
            [
                False, False, False,
                False, False, False,
                False, False, False
            ],
            [
                False, False, False,
                False, False, False,
                False, False, False
            ],
            [
                False, False, False,
                False, False, False,
                False, False, False
            ]
        )

        self.dirty_layer.fill("#123456")
        self.dirty_layer.blit(self.table_mark1, self.mark_coords[0])
        self.dirty_layer.blit(self.table_mark2, self.mark_coords[1])
        self.dirty_layer.blit(self.table_mark3, self.mark_coords[2])

    def renew_task_surface(self):
        self.frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.mark_coords = ((randint(60, 750), randint(60, 510)),
                            (randint(60, 750), randint(60, 510)),
                            (randint(60, 800), randint(60, 560)))

        self.clean_status = (
            [
                False, False, False,
                False, False, False,
                False, False, False
            ],
            [
                False, False, False,
                False, False, False,
                False, False, False
            ],
            [
                False, False, False,
                False, False, False,
                False, False, False
            ]
        )

        self.dirty_layer.fill("#123456")
        self.dirty_layer.blit(self.table_mark1, self.mark_coords[0])
        self.dirty_layer.blit(self.table_mark2, self.mark_coords[1])
        self.dirty_layer.blit(self.table_mark3, self.mark_coords[2])

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.table_background, (480, 180))

        if not self.show_success:
            clean_rect = pygame.Rect(mouse_x - 575, mouse_y - 275,
                                     self.rag.get_width() - 10,
                                     self.rag.get_height() - 10)

            if pygame.mouse.get_pressed(3)[0]:
                pygame.draw.rect(self.dirty_layer, "#123456", clean_rect)
                for i in range(3):
                    coord = self.mark_coords[i]
                    # Image size: 100x100, coord referenced top left corner
                    coord = (coord[0] + 50, coord[1] + 50)

                    if clean_rect.collidepoint(coord[0] - 25, coord[1] - 25):
                        self.clean_status[i][0] = True
                    if clean_rect.collidepoint(coord[0], coord[1] - 25):
                        self.clean_status[i][1] = True
                    if clean_rect.collidepoint(coord[0] + 25, coord[1] - 25):
                        self.clean_status[i][2] = True

                    if clean_rect.collidepoint(coord[0] - 25, coord[1]):
                        self.clean_status[i][3] = True
                    if clean_rect.collidepoint(coord[0], coord[1]):
                        self.clean_status[i][4] = True
                    if clean_rect.collidepoint(coord[0] + 25, coord[1]):
                        self.clean_status[i][5] = True

                    if clean_rect.collidepoint(coord[0] - 25, coord[1] + 25):
                        self.clean_status[i][6] = True
                    if clean_rect.collidepoint(coord[0], coord[1] + 25):
                        self.clean_status[i][7] = True
                    if clean_rect.collidepoint(coord[0] + 25, coord[1] + 25):
                        self.clean_status[i][8] = True

                is_done = True

                for status_map in self.clean_status:
                    for point in status_map:
                        if not point:
                            is_done = False
                            break

                if is_done:
                    self.show_success = True

            self.display.blit(self.dirty_layer, (480, 180))
            self.display.blit(self.rag, (mouse_x - 100, mouse_y - 100))
        else:
            return self.success(dt)
