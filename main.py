import pygame, sys
from network import Network
from player import Player
pygame.init()

screen_x = 1920
screen_y = 1080

display = pygame.display.set_mode((screen_x, screen_y))
map_image = pygame.image.load('BCCA_map.jpg')

pygame.display.set_caption("Skeld")

class Map(object):
    def __init__(self):
        self.x = -6004
        self.y = -4
        self.width = map_image.get_rect().width
        self.height = map_image.get_rect().height
        self.x_vel = 5
        self.y_vel = 5

    def draw(self, window):
        window.blit(map_image, (self.x, self.y))

    def wall_objs(self):
        return [
            pygame.Rect(self.x + 50, self.y + 300, 4700, 50), # Outside: classrooms top wall
            pygame.Rect(self.x + 50, self.y + 350, 50, 3600), # Outside: classrooms left wall
            pygame.Rect(self.x + 4950, self.y + 50, 1450, 50), # Outside: offices top wall
            pygame.Rect(self.x + 4950, self.y + 100, 50, 300), # Outside: offices left wall
            pygame.Rect(self.x + 4900, self.y + 300, 150, 50), # Outside: main door right wall
            pygame.Rect(self.x + 6350, self.y + 100, 50, 700), # Outside: offices right wall
            pygame.Rect(self.x + 6400, self.y + 400, 1750, 50), # Outside: kitchen top wall
            pygame.Rect(self.x + 8100, self.y + 450, 50, 3500), # Outside: student door wall
        ]
    
    def draw_collision(self, window):
        for wall in self.wall_objs():
            pygame.draw.rect(window, (0,255,0), wall, 1)


def collide_check(rect, colls):
    collisions = []
    for wall in colls:
        if rect.colliderect(wall):
            collisions.append(skeld.wall_objs().index(wall))
    return collisions

def redrawGameWindow():
    skeld.draw(display)
    skeld.draw_collision(display)
    p1.draw(display)
    pygame.display.update()

#mainloop
skeld = Map()
collision_tolerance = max(skeld.x_vel, skeld.y_vel) * 2 + 1
p1 = Player(screen_x // 2, screen_y // 2, (255,0,0), skeld)
ghost = False
run = True
while run:
    pygame.time.Clock().tick(120)

    display.fill((255,255,255))

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    redrawGameWindow()
    # skeld.wall_objs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    coll_index = collide_check(p1.hitbox, skeld.wall_objs())
    if coll_index != []:
        for i in coll_index:
            if abs(skeld.wall_objs()[i].bottom - p1.hitbox.top) < collision_tolerance:
                w_coll = False
            if abs(skeld.wall_objs()[i].right - p1.hitbox.left) < collision_tolerance:
                a_coll = False
            if abs(skeld.wall_objs()[i].top - p1.hitbox.bottom) < collision_tolerance:
                s_coll = False
            if abs(skeld.wall_objs()[i].left - p1.hitbox.right) < collision_tolerance:
                d_coll = False

    if keys[pygame.K_x]:
        ghost = not ghost
    if ghost:
        w_coll = True
        a_coll = True
        s_coll = True
        d_coll = True
    if keys[pygame.K_w]:
        if w_coll:
            skeld.y += skeld.y_vel
    if keys[pygame.K_a]:
        if a_coll:
            skeld.x += skeld.x_vel
    if keys[pygame.K_s]:
        if s_coll:
            skeld.y -= skeld.y_vel
    if keys[pygame.K_d]:
        if d_coll:
            skeld.x -= skeld.x_vel
    if keys[pygame.K_c]:
        print(skeld.x, skeld.y)
    

    if keys[pygame.K_ESCAPE]:
        display = pygame.display.set_mode((screen_x, screen_y))
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()