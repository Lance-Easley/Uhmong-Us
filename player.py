import pygame

class Player(object):
    def __init__(self, x, y, color, map_obj, traitor):
        self.x = x
        self.y = y
        self.width = 52
        self.height = 82
        self.color = color
        self.hl = 1
        self.a_hitbox = pygame.Rect(self.x, self.y + self.hl, self.hl, self.height - self.hl * 2)
        self.d_hitbox = pygame.Rect(self.x + self.width - self.hl, self.y + self.hl, self.hl, self.height - self.hl * 2)
        self.w_hitbox = pygame.Rect(self.x + self.hl, self.y, self.width - self.hl * 2, self.hl)
        self.s_hitbox = pygame.Rect(self.x + self.hl, self.y + self.height - self.hl, self.width - self.hl * 2, self.hl)
        self.x_coord = map_obj.x
        self.y_coord = map_obj.y
        self.hitboxes = [self.w_hitbox, self.a_hitbox, self.s_hitbox, self.d_hitbox]
        self.is_traitor = traitor

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def draw_hitboxes(self, window):
        pygame.draw.rect(window, (0,0,255), self.w_hitbox)
        pygame.draw.rect(window, (0,0,255), self.a_hitbox)
        pygame.draw.rect(window, (0,0,255), self.s_hitbox)
        pygame.draw.rect(window, (0,0,255), self.d_hitbox)
    
    def convert_to_data(self):
        return self.x_coord, self.y_coord, self.color
