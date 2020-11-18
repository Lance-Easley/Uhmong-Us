import pygame

class Player(object):
    def __init__(self, x, y, color, map_obj):
        self.x = x
        self.y = y
        self.width = 52
        self.height = 80
        self.color = color
        self.hitbox = pygame.Rect(self.x, self.y + (self.height // 3) * 2, self.width, self.height // 3)
        self.x_coord = map_obj.x
        self.y_coord = map_obj.y

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
    
    def convert_to_data(self):
        return self.x_coord, self.y_coord, self.color
