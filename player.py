import pygame

class Player(object):
    def __init__(self, x, y, color, map_object, is_traitor, in_vent):
        self.width = 52
        self.height = 82
        self.half_width = self.width // 2
        self.half_height = self.height // 2

        self.x = x - self.half_width
        self.y = y - self.half_height
        self.x_coord = map_object.x
        self.y_coord = map_object.y

        self.color = color

        self.hitbox_depth = 1
        self.w_hitbox = pygame.Rect(
            self.x + self.hitbox_depth, 
            self.y, 
            self.width - self.hitbox_depth * 2, 
            self.hitbox_depth
        )
        self.a_hitbox = pygame.Rect(
            self.x, 
            self.y + self.hitbox_depth, 
            self.hitbox_depth, 
            self.height - self.hitbox_depth * 2
        )
        self.s_hitbox = pygame.Rect(
            self.x + self.hitbox_depth, 
            self.y + self.height - self.hitbox_depth, 
            self.width - self.hitbox_depth * 2, 
            self.hitbox_depth
        )
        self.d_hitbox = pygame.Rect(
            self.x + self.width - self.hitbox_depth, 
            self.y + self.hitbox_depth, 
            self.hitbox_depth, 
            self.height - self.hitbox_depth * 2
        )
        self.hitboxes = [self.w_hitbox, self.a_hitbox, self.s_hitbox, self.d_hitbox]
        
        self.is_traitor = is_traitor
        self.in_vent = in_vent

    def draw_player(self, window):
        # `self.in_vent = 0` Represents a player not in a vent
        if self.in_vent == 0:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def draw_hitboxes(self, window):
        pygame.draw.rect(window, (0,0,255), self.w_hitbox)
        pygame.draw.rect(window, (0,0,255), self.a_hitbox)
        pygame.draw.rect(window, (0,0,255), self.s_hitbox)
        pygame.draw.rect(window, (0,0,255), self.d_hitbox)
    
    @property
    def get_player_data(self):
        return self.x_coord, self.y_coord, self.color
