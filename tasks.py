from constants import *
from random import randint
import math
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 32)


def bold_text(x: int, y: int, surface: pygame.Surface, outline: int):
    success_text = font.render("Task Completed!", True, (0, 0, 0))
    success_text_rect = success_text.get_rect()

    # Outlines
    success_text_rect.center = (x + outline, y + outline)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x + outline, y)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x + outline, y - outline)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x, y + outline)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x, y - outline)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x - outline, y + outline)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x - outline, y)
    surface.blit(success_text, success_text_rect)

    success_text_rect.center = (x - outline, y - outline)
    surface.blit(success_text, success_text_rect)

    success_text = font.render("Task Completed!", True, (255, 255, 255))
    success_text_rect = success_text.get_rect()
    success_text_rect.center = (x, y)
    surface.blit(success_text, success_text_rect)


class BaseTask:
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        self.x = x
        self.y = y
        self.display = surface

        self.task_surface = pygame.Surface((960, 720))
        self.task_surface.set_colorkey((18, 52, 86))

        # Task Completed Overlay Resources
        self.success_text = "Task Completed!"

        self.show_success = False
        self.success_frame = 35

    def success(self, dt: float):
        if self.success_frame > 0:
            bold_text(self.x, self.y, self.display, 2)

            self.success_frame -= 40 * dt
        else:
            return True


class WipeDownTables(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

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
        self.success_frame = 35
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

        self.display.blit(self.table_background, (self.x - 480, self.y - 360))

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

            self.display.blit(self.dirty_layer, (self.x - 480, self.y - 360))
            self.display.blit(self.rag, (mouse_x - 100, mouse_y - 100))
        else:
            return self.success(dt)


class CleanWindows(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

        # Resources
        self.clean_window_background = pygame.image.load('images/tasks/clean_windows/window_background.png').convert()

        self.window_mark1 = pygame.image.load('images/tasks/clean_windows/window_mark1.png').convert()
        self.window_mark1.set_colorkey((255, 255, 255))

        self.window_mark2 = pygame.image.load('images/tasks/clean_windows/window_mark2.png').convert()
        self.window_mark2.set_colorkey((255, 255, 255))

        self.window_mark3 = pygame.image.load('images/tasks/clean_windows/window_mark3.png').convert()
        self.window_mark3.set_colorkey((255, 255, 255))

        self.squeegee = pygame.image.load('images/tasks/clean_windows/squeegee.png').convert()
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

    def task(self, dt: float):
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
            return self.success(dt)


class ResetWifi(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

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
        print(self.wifi_text_rect.width)
        self.wifi_text_rect.center = (SCREEN_HALF_X, SCREEN_HALF_Y)

        self.reset_button_rect = pygame.Rect(933, 508, 54, 64)

        self.loading_progress = 0
        self.has_clicked_reset = False

    def renew_task_surface(self):
        self.success_frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.loading_progress = 0
        self.has_clicked_reset = False

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.desktop_background, (self.x - 480, self.y - 360))

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


class PlugInLaptops(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

        # Resources
        self.progress_modifier = 1
        self.computer_cart = pygame.image.load('images/tasks/plug-in-laptops/computer_cart.png').convert()
        self.computer = pygame.image.load('images/tasks/plug-in-laptops/computer.png').convert()
        self.active_charger = pygame.image.load('images/tasks/plug-in-laptops/active_charger.png').convert()
        self.inactive_charger = pygame.image.load('images/tasks/plug-in-laptops/inactive_charger.png').convert()

        self.computer.set_colorkey((255, 255, 255))
        self.active_charger.set_colorkey((255, 255, 255))
        self.inactive_charger.set_colorkey((255, 255, 255))

        self.computer_statuses = [
            True, True, True, True, True, True,
            True, True, True, True, True, True
        ]

        self.computer_positions = (
            (713 + randint(-20, 20), 327),
            (806 + randint(-20, 20), 327),
            (899 + randint(-20, 20), 327),
            (992 + randint(-20, 20), 327),
            (1085 + randint(-20, 20), 327),
            (1178 + randint(-20, 20), 327),
            # 2nd Layer
            (713 + randint(-20, 20), 577),
            (806 + randint(-20, 20), 577),
            (899 + randint(-20, 20), 577),
            (992 + randint(-20, 20), 577),
            (1085 + randint(-20, 20), 577),
            (1178 + randint(-20, 20), 577)
        )

        self.charger_positions = (
            (703, 800), (796, 800), (889, 800), (982, 800), (1075, 800), (1168, 800),
            (723, 850), (816, 850), (909, 850), (1002, 850), (1095, 850), (1188, 850)
        )

        self.charger_rects = (
            pygame.Rect(703, 800, 31, 31),
            pygame.Rect(796, 800, 31, 31),
            pygame.Rect(889, 800, 31, 31),
            pygame.Rect(982, 800, 31, 31),
            pygame.Rect(1075, 800, 31, 31),
            pygame.Rect(1168, 800, 31, 31),
            # 2nd Layer
            pygame.Rect(723, 850, 31, 31),
            pygame.Rect(816, 850, 31, 31),
            pygame.Rect(909, 850, 31, 31),
            pygame.Rect(1002, 850, 31, 31),
            pygame.Rect(1095, 850, 31, 31),
            pygame.Rect(1188, 850, 31, 31)
        )

        self.dragged_charger = None

    def renew_task_surface(self):
        self.success_frame = 35
        self.show_success = False

        self.computer_statuses = [
            True, True, True, True, True, True,
            True, True, True, True, True, True
        ]

        self.computer_positions = (
            (713 + randint(-20, 20), 327),
            (806 + randint(-20, 20), 327),
            (899 + randint(-20, 20), 327),
            (992 + randint(-20, 20), 327),
            (1085 + randint(-20, 20), 327),
            (1178 + randint(-20, 20), 327),
            # 2nd Layer
            (713 + randint(-20, 20), 577),
            (806 + randint(-20, 20), 577),
            (899 + randint(-20, 20), 577),
            (992 + randint(-20, 20), 577),
            (1085 + randint(-20, 20), 577),
            (1178 + randint(-20, 20), 577)
        )

        self.dragged_charger = None

        computers_to_plug_in = 4
        used_indexes = set()

        for i in range(computers_to_plug_in):
            while True:
                index = (randint(0, 11))
                if index not in used_indexes:
                    used_indexes.add(index)
                    self.computer_statuses[index] = False
                    break

        self.task_surface.fill((18, 52, 86))

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.computer_cart, (self.x - 480, self.y - 360))

        cord_width = 3

        for coord in self.computer_positions:
            self.display.blit(self.computer, coord)

        for i, coord in enumerate(self.charger_positions):
            if self.computer_statuses[i]:
                self.display.blit(self.active_charger, coord)
            else:
                self.display.blit(self.inactive_charger, coord)

        for stat, comp, charge in zip(self.computer_statuses, self.computer_positions, self.charger_positions):
            if stat:
                pygame.draw.circle(self.display, (100, 100, 100), (comp[0] + 19, comp[1] + 188), 7)
                pygame.draw.circle(self.display, (100, 100, 100), (charge[0] + 16, charge[1] + 16), 7)

                cord_x, cord_y = min(charge[0] + 15, comp[0] + 18), min(charge[1] + 15, comp[1] + 187)
                cord_rect_width = max(charge[0] + 17, comp[0] + 21) - cord_x
                cord_rect_height = max(charge[1] + 17, comp[1] + 190) - cord_y

                cord_surface = pygame.Surface(
                    (max(cord_rect_width + 1, cord_width), max(cord_rect_height + 1, cord_width)))
                cord_surface.set_colorkey("#000000")

                if cord_x == comp[0] + 18:
                    pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                        (
                                            0,
                                            -cord_rect_height,
                                            cord_rect_width * 2,
                                            cord_rect_height * 2
                                        ), cord_width)
                else:
                    pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                        (
                                            -cord_rect_width,
                                            -cord_rect_height,
                                            cord_rect_width * 2,
                                            cord_rect_height * 2
                                        ), cord_width)

                self.display.blit(cord_surface, (cord_x, cord_y, cord_rect_width, cord_rect_height))

        if pygame.mouse.get_pressed(3)[0]:
            if self.dragged_charger is None:
                for index, charger_rect in enumerate(self.charger_rects):
                    if not self.computer_statuses[index] and charger_rect.collidepoint(mouse_x, mouse_y):
                        self.dragged_charger = index
                        break
            else:
                pygame.draw.circle(self.display, (100, 100, 100), (mouse_x, mouse_y), 7)
                pygame.draw.circle(self.display,
                                   (100, 100, 100),
                                   (
                                       self.charger_positions[self.dragged_charger][0] + 16,
                                       self.charger_positions[self.dragged_charger][1] + 16
                                   ),
                                   7)

                cord_x = min(self.charger_positions[self.dragged_charger][0] + 15, mouse_x)
                cord_y = min(self.charger_positions[self.dragged_charger][1] + 15, mouse_y)
                cord_rect_width = max(self.charger_positions[self.dragged_charger][0] + 17, mouse_x) - cord_x
                cord_rect_height = max(self.charger_positions[self.dragged_charger][1] + 17, mouse_y) - cord_y

                # pygame.draw.arc did not draw a solid line in this case
                # fix: draw ellipse and show one quarter of the circle, forming an arc
                cord_surface = pygame.Surface(
                    (max(cord_rect_width + 1, cord_width), max(cord_rect_height + 1, cord_width)))
                cord_surface.set_colorkey("#000000")

                if cord_x == mouse_x:
                    if cord_y == mouse_y:
                        pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                            (
                                                0,
                                                -cord_rect_height,
                                                cord_rect_width * 2,
                                                cord_rect_height * 2
                                            ), cord_width)
                    else:
                        pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                            (
                                                -cord_rect_width,
                                                -cord_rect_height,
                                                cord_rect_width * 2,
                                                cord_rect_height * 2
                                            ), cord_width)
                else:
                    if cord_y == mouse_y:
                        pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                            (
                                                -cord_rect_width,
                                                -cord_rect_height,
                                                cord_rect_width * 2,
                                                cord_rect_height * 2
                                            ), cord_width)
                    else:
                        pygame.draw.ellipse(cord_surface, (25, 25, 25),
                                            (
                                                0,
                                                -cord_rect_height,
                                                cord_rect_width * 2,
                                                cord_rect_height * 2
                                            ), cord_width)

                self.display.blit(cord_surface, (cord_x, cord_y, cord_rect_width, cord_rect_height))

        elif self.dragged_charger is not None:
            port = self.computer_positions[self.dragged_charger]
            if pygame.Rect(port[0] + 14, port[1] + 183, 21, 21).collidepoint(mouse_x, mouse_y):
                self.computer_statuses[self.dragged_charger] = True
                self.dragged_charger = None
            self.dragged_charger = None

        if all(self.computer_statuses):
            return self.success(dt)


class CheckTemperature(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

        # Resources
        self.scanner = pygame.image.load('images/tasks/check-temperature/scanner.png').convert()
        self.scanner_rect = pygame.Rect(810, 420, 300, 300)

        self.progress = 0

    def renew_task_surface(self):
        self.success_frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.progress = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.scanner, (self.x - 480, self.y - 360))

        # Visuals
        if pygame.mouse.get_pressed(3)[0] and self.scanner_rect.collidepoint(mouse_x, mouse_y) and self.progress < 150:
            self.progress += 40 * dt
            pygame.draw.rect(self.display, (255, 255, 255), (785, 420 + (self.progress * 2), 350, 10))
        elif self.progress >= 150:
            return self.success(dt)
        else:
            self.progress = 0


class NominateForAwards(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

        # Resources
        self.desk = pygame.image.load('images/tasks/nominate_for_awards/desk.png').convert()
        self.cover = pygame.image.load('images/tasks/nominate_for_awards/cover.png').convert()
        self.card = pygame.image.load('images/tasks/nominate_for_awards/card.png').convert()
        self.pen = pygame.image.load('images/tasks/nominate_for_awards/pen.png').convert()

        self.pen.set_colorkey((255, 255, 255))

        self.card_surface = pygame.Surface((220, 120))
        self.card_rect = pygame.Rect(self.x - 110, self.y - 60, 220, 120)
        self.card_pile_rect = pygame.Rect(self.x + 140, self.y - 295, 220, 120)

        self.drawn_amount = 0
        self.last_pencil_point = None

        self.mouse_was_down = False

    def renew_task_surface(self):
        self.success_frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.card_surface.blit(self.card, (0, 0))
        self.card_rect = pygame.Rect(self.x - 110, self.y - 60, 220, 120)

        self.last_pencil_point = None
        self.drawn_amount = 0

        self.mouse_was_down = False

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pencil_pos = (mouse_x - self.card_rect.x, mouse_y - self.card_rect.y)

        self.display.blit(self.desk, (self.x - 480, self.y - 360))

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
            self.display.blit(self.cover, (self.x - 100, self.y - 240))
        else:
            self.display.blit(self.cover, (self.x + 137, self.y - 297))

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


class CollectTrash(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

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
        self.success_frame = 35
        self.show_success = False

        self.task_phase = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.wall, (self.x - 480, self.y - 360))

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

        self.display.blit(self.bin, (self.x - 213, self.y + 50))

        # Images/Rects required to draw over trash bin
        if self.task_phase == 0:
            self.display.blit(self.full_bag, (self.x - 215, self.y + 18))
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
            self.display.blit(self.replaced_bag, (self.x - 215, self.y + 48))
            return self.success(dt)


class RefillHandSanitizer(BaseTask):
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        super().__init__(x, y, surface)

        # Resources
        self.wall = pygame.image.load('images/tasks/refill_hand_sanitizer/wall.png').convert()
        self.buckle = pygame.image.load('images/tasks/refill_hand_sanitizer/buckle.png').convert()
        self.new_sanitizer = pygame.image.load('images/tasks/refill_hand_sanitizer/new_sanitizer.png').convert()
        self.old_sanitizer = pygame.image.load('images/tasks/refill_hand_sanitizer/old_sanitizer.png').convert()
        self.unlatched_buckle = pygame.image.load('images/tasks/refill_hand_sanitizer/unlatched_buckle.png').convert()
        self.up_arrow_hover = pygame.image.load('images/tasks/refill_hand_sanitizer/pull_up_arrow_hover.png').convert()
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
        self.success_frame = 35
        self.show_success = False

        self.task_surface.fill((18, 52, 86))

        self.task_phase = 0

    def task(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.display.blit(self.wall, (self.x - 480, self.y - 360))

        if self.task_phase < 3:
            self.display.blit(self.old_sanitizer, (self.x - 130, self.y - 158))
        elif self.task_phase == 4:
            self.display.blit(self.new_sanitizer, (500, 486))
        elif self.task_phase > 5:
            self.display.blit(self.new_sanitizer, (self.x - 130, self.y - 158))

        if self.task_phase < 2 or self.task_phase == 8:
            self.display.blit(self.buckle, (self.x - 130, self.y + 142))
        else:
            self.display.blit(self.unlatched_buckle, (self.x - 130, self.y + 232))

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
