from entities.tasks.BaseTask import *
from random import randint
import pygame


class PlugInLaptops(BaseTask):
    def __init__(self, surface: pygame.Surface):
        super().__init__(surface)

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
        self.frame = 35
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

        self.display.blit(self.computer_cart, (480, 180))

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
