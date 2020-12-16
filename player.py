import pygame

class Player(object):
    def __init__(self, x, y, color, map_obj):
        self.x = x
        self.y = y
        self.width = 52
        self.height = 82
        self.color = color
        self.hitbox = pygame.Rect(self.x - 2, self.y - 2, self.width + 2, self.height + 2)
        self.x_coord = map_obj.x
        self.y_coord = map_obj.y

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
    
    def convert_to_data(self):
        return self.x_coord, self.y_coord, self.color
