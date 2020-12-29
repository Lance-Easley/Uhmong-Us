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
        self.x = -54
        self.y = -1054
        self.width = map_image.get_rect().width
        self.height = map_image.get_rect().height
        self.x_vel = 5
        self.y_vel = 5

    def draw(self, window):
        window.blit(map_image, (self.x, self.y))

    def wall_objs(self):
        return [
            pygame.Rect(self.x + 50, self.y + 300, 5250, 50), # Outside: classrooms top wall
            pygame.Rect(self.x + 50, self.y + 350, 50, 1750), # Outside: classrooms left wall
            pygame.Rect(self.x + 50, self.y + 2100, 8100, 50), # Outside: classrooms bottom wall
            pygame.Rect(self.x + 4950, self.y + 50, 1450, 50), # Outside: offices top wall
            pygame.Rect(self.x + 4950, self.y + 100, 50, 300), # Outside: offices left wall
            pygame.Rect(self.x + 6350, self.y + 100, 50, 700), # Outside: offices right wall
            pygame.Rect(self.x + 6400, self.y + 400, 1750, 50), # Outside: kitchen top wall
            pygame.Rect(self.x + 8100, self.y + 450, 50, 1650), # Outside: student door wall
            
            pygame.Rect(self.x + 5400, self.y + 300, 500, 50), # BCCA: top office middle wall
            pygame.Rect(self.x + 6000, self.y + 300, 350, 50), # BCCA: top office right wall
            pygame.Rect(self.x + 4950, self.y + 500, 50, 300), # BCCA: left office left wall
            pygame.Rect(self.x + 4900, self.y + 800, 700, 50), # BCCA: left office bottom wall
            pygame.Rect(self.x + 5000, self.y + 550, 600, 50), # BCCA: left office top wall
            pygame.Rect(self.x + 5500, self.y + 600, 50, 200), # BCCA: left office right wall
            pygame.Rect(self.x + 5700, self.y + 550, 650, 50), # BCCA: right office top wall
            pygame.Rect(self.x + 5750, self.y + 600, 50, 200), # BCCA: right office right wall

            pygame.Rect(self.x + 4650, self.y + 350, 50, 450), # BCCA: breakroom right wall
            pygame.Rect(self.x + 4300, self.y + 800, 450, 50), # BCCA: breakroom bottom right wall
            pygame.Rect(self.x + 4150, self.y + 800, 50, 50), # BCCA: breakroom bottom left wall
            pygame.Rect(self.x + 4100, self.y + 350, 50, 750), # BCCA: breakroom left wall

            pygame.Rect(self.x + 3800, self.y + 1050, 300, 50), # BCCA: supply bottom right wall
            pygame.Rect(self.x + 3600, self.y + 600, 50, 450), # BCCA: supply middle wall
            pygame.Rect(self.x + 3350, self.y + 750, 250, 50), # BCCA: supply middle left wall

            pygame.Rect(self.x + 3150, self.y + 1100, 50, 50), # BCCA: hallway top door stud
            pygame.Rect(self.x + 3150, self.y + 1300, 50, 50), # BCCA: hallway bottom door stud

            pygame.Rect(self.x + 3300, self.y + 350, 50, 700), # BCCA: classroom1 right wall
            pygame.Rect(self.x + 2250, self.y + 1050, 1450, 50), # BCCA: classroom1 bottom right wall
            pygame.Rect(self.x + 2500, self.y + 500, 400, 400), # BCCA: classroom1 block
            pygame.Rect(self.x + 1900, self.y + 1050, 250, 50), # BCCA: classroom1 bottom left wall
            pygame.Rect(self.x + 2050, self.y + 350, 50, 100), # BCCA: classroom1 left top wall
            pygame.Rect(self.x + 2050, self.y + 550, 50, 500), # BCCA: classroom1 left bottom wall

            pygame.Rect(self.x + 1500, self.y + 1050, 250, 50), # BCCA: breakoutroom1 bottom left wall
            pygame.Rect(self.x + 1750, self.y + 350, 150, 400), # BCCA: breakoutroom1 table
            pygame.Rect(self.x + 1550, self.y + 350, 50, 100), # BCCA: breakoutroom1 left top wall
            pygame.Rect(self.x + 1550, self.y + 550, 50, 500), # BCCA: breakoutroom1 left bottom wall

            pygame.Rect(self.x + 1100, self.y + 600, 200, 200), # BCCA: classroom3 right block
            pygame.Rect(self.x + 600, self.y + 600, 200, 200), # BCCA: classroom3 left block
            pygame.Rect(self.x + 300, self.y + 900, 50, 150), # BCCA: classroom3 middle wall
            pygame.Rect(self.x + 300, self.y + 1050, 1100, 50), # BCCA: classroom3 bottom left wall
            pygame.Rect(self.x + 250, self.y + 850, 100, 50), # BCCA: classroom3 middle right wall
            pygame.Rect(self.x + 100, self.y + 850, 50, 50), # BCCA: classroom3 middle left wall

            pygame.Rect(self.x + 300, self.y + 1350, 1100, 50), # BCCA: classroom4 bottom left wall
            pygame.Rect(self.x + 300, self.y + 1400, 50, 150), # BCCA: classroom4 middle wall
            pygame.Rect(self.x + 250, self.y + 1550, 100, 50), # BCCA: classroom4 middle right wall
            pygame.Rect(self.x + 100, self.y + 1550, 50, 50), # BCCA: classroom4 middle left wall
            pygame.Rect(self.x + 550, self.y + 1600, 200, 50), # BCCA: classroom4 center top wall
            pygame.Rect(self.x + 550, self.y + 1650, 50, 250), # BCCA: classroom4 center left wall
            pygame.Rect(self.x + 550, self.y + 1900, 500, 50), # BCCA: classroom4 center bottom wall
            pygame.Rect(self.x + 1050, self.y + 1800, 50, 150), # BCCA: classroom4 center right wall

            pygame.Rect(self.x + 7100, self.y + 450, 50, 350), # BCCA: kitchen right wall
            pygame.Rect(self.x + 5700, self.y + 800, 1200, 50), # BCCA: kitchen bottom left wall
            pygame.Rect(self.x + 7000, self.y + 800, 250, 50), # BCCA: kitchen bottom right wall
            
            pygame.Rect(self.x + 7350, self.y + 800, 750, 50), # BCCA: meeting room bottom wall

            pygame.Rect(self.x + 6950, self.y + 1100, 700, 50), # BCCA: incubator top left wall
            pygame.Rect(self.x + 7850, self.y + 1100, 250, 1000), # BCCA: incubator top right wall
            pygame.Rect(self.x + 6950, self.y + 1150, 50, 400), # BCCA: incubator left top wall
            pygame.Rect(self.x + 6950, self.y + 1650, 50, 450), # BCCA: incubator left bottom wall
            pygame.Rect(self.x + 7650, self.y + 1200, 50, 50), # BCCA: incubator top entrance left wall
            pygame.Rect(self.x + 7800, self.y + 1200, 50, 50), # BCCA: incubator top entrance right wall
            pygame.Rect(self.x + 7000, self.y + 1450, 100, 50), # BCCA: incubator top room bottom left wall
            pygame.Rect(self.x + 7200, self.y + 1450, 100, 50), # BCCA: incubator top room bottom right wall
            pygame.Rect(self.x + 7250, self.y + 1400, 50, 50), # BCCA: incubator top room middle wall
            pygame.Rect(self.x + 7250, self.y + 1350, 200, 50), # BCCA: incubator top room middle top wall
            pygame.Rect(self.x + 7550, self.y + 1350, 50, 50), # BCCA: incubator top room bottom right wall
            pygame.Rect(self.x + 7600, self.y + 1150, 50, 250), # BCCA: incubator top room right wall
            pygame.Rect(self.x + 7000, self.y + 1700, 100, 50), # BCCA: incubator bottom room top left wall
            pygame.Rect(self.x + 7200, self.y + 1700, 100, 50), # BCCA: incubator bottom room top right wall
            pygame.Rect(self.x + 7250, self.y + 1750, 50, 50), # BCCA: incubator bottom room middle wall
            pygame.Rect(self.x + 7250, self.y + 1800, 600, 50), # BCCA: incubator bottom room top right wall
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
clock = pygame.time.Clock()
collision_tolerance = max(skeld.x_vel, skeld.y_vel) * 2 + 1
p1 = Player(screen_x // 2, screen_y // 2, (255,0,0), skeld)
ghost = False
run = True
while run:
    clock.tick(60)

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