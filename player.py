import pygame

class Player:
    """Base class for a controllable player character

    Holds basic player logic, like movement and player variables.
    """
    def __init__(self, x, y, width, height, color, username):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color =  blue green red pink
        self.username = username
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 3

    def draw(self, win):
        """Draw the character as a rectangle on the pygame display
        """
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        """Update the player's position for .draw()
        """
        self.rect = (self.x, self.y, self.width, self.height)
    
    def move(self):
        """Allows the player to move using wasd
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_d]:
            self.x += self.vel


# class Crewmate(Player):
#     """Class for player type Crewmate
#     """
#     def __init__(self, x, y, width, height, color, username, vision):
#         super().__init__(x, y, width, height, color, username)
#         self.vision = vision


# class Impostor(Player):
#     """Class for player type Impostor
#     """
#     def __init__(self, x, y, width, height, color, username, vision):
#         super().__init__(x, y, width, height, color, username)
#         self.vision = vision

#     def murder(self, other_player):
#         """Logic for allowing Imposter to kill others
#         """
