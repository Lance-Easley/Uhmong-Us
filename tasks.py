from random import *
import pygame

pygame.init()


class TaskHandler:
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        self.x = x
        self.y = y
        self.display = surface

        self.task_surface = pygame.Surface((960, 720))
        self.task_surface.set_colorkey((18, 52, 86))

        # Task Completed Overlay Resources
        pygame.font.init()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.success_text = self.font.render(
            "Task Completed!",
            True, (255, 255, 255))
        self.success_text_rect = self.success_text.get_rect()
        self.success_text_rect.center = (self.x, self.y)

        self.show_success = False
        self.success_frame = 35

        # Clean Window Resources
        self.clean_window_background = pygame.image.load('images/tasks/window_background.png').convert()

        self.window_mark1 = pygame.image.load('images/tasks/window_mark1.png').convert()
        self.window_mark1.set_colorkey((255, 255, 255))

        self.window_mark2 = pygame.image.load('images/tasks/window_mark2.png').convert()
        self.window_mark2.set_colorkey((255, 255, 255))

        self.window_mark3 = pygame.image.load('images/tasks/window_mark3.png').convert()
        self.window_mark3.set_colorkey((255, 255, 255))

        self.squeegee = pygame.image.load('images/tasks/squeegee.png').convert()
        self.squeegee.set_colorkey((255, 255, 255))

        self.dirty_layer = pygame.Surface((960, 720))
        self.dirty_layer.set_colorkey("#123456")

        self.mark_coords = ((randint(150, 700), randint(50, 600)),
                            (randint(150, 700), randint(50, 600)),
                            (randint(150, 700), randint(50, 600)))

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
        self.dirty_layer.blit(self.window_mark1, self.mark_coords[0])
        self.dirty_layer.blit(self.window_mark2, self.mark_coords[1])
        self.dirty_layer.blit(self.window_mark3, self.mark_coords[2])

    def renew_task_surface(self):
        self.success_frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.mark_coords = ((randint(150, 700), randint(50, 600)),
                            (randint(150, 700), randint(50, 600)),
                            (randint(150, 700), randint(50, 600)))

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
        self.dirty_layer.blit(self.window_mark1, self.mark_coords[0])
        self.dirty_layer.blit(self.window_mark2, self.mark_coords[1])
        self.dirty_layer.blit(self.window_mark3, self.mark_coords[2])

    def success(self):
        if self.success_frame > 0:
            self.display.blit(self.success_text, self.success_text_rect)

            self.success_frame -= 1
        else:
            return True

    def task_clean_windows(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.clean_window_background, (self.x - 480, self.y - 360))

        if not self.show_success:
            clean_rect = pygame.Rect(mouse_x - 579, mouse_y - 278, 197, 15)

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

            self.display.blit(self.dirty_layer, (self.x - 480, self.y - 360))
            self.display.blit(self.squeegee, (mouse_x - 100, mouse_y - 100))
        else:
            done = self.success()
            if done:
                return True

    def show_task(self, task_name: str):
        done = False

        if task_name == "Clean Windows":
            done = self.task_clean_windows()

        if done:
            return True
