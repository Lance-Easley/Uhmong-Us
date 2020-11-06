import pygame

class Player(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hitbox = pygame.Rect(self.x, self.y + (self.height // 3) * 2, self.width, self.height // 3)

    def get_pos(self, map_obj):
        x_coord = self.x
        y_coord = self.y
        return x_coord, y_coord

    def draw(self, window, map_obj):
        pygame.draw.rect(window, self.color, (self.get_pos(map_obj)[0], self.get_pos(map_obj)[1], self.width, self.height))
