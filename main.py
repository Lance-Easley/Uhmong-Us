import pygame, sys
pygame.init()

screen_x = 1920
screen_y = 1080

display = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
map_image = pygame.image.load('Skeld_map.jpg')

pygame.display.set_caption("Skeld")

class Map(object):
    def __init__(self):
        self.x = -3140
        self.y = -2880
        self.width = map_image.get_rect().width
        self.height = map_image.get_rect().height
        self.x_vel = 5
        self.y_vel = 5

    def draw(self, window):
        window.blit(map_image, (self.x, self.y))

    def wall_objs(self):
        return [
            pygame.Rect(self.x + 2494, self.y + 752, 1562, 472), # Medbay: Top hallway
            pygame.Rect(self.x + 3655, self.y + 1402, 401, 272), # Medbay: Bottom right hallway
            pygame.Rect(self.x + 2494, self.y + 1402, 904, 475), # Medbay: Bottom left hallway
            pygame.Rect(self.x + 3710, self.y + 1935, 225, 181), # Medbay: bottom left bed
            pygame.Rect(self.x + 3710, self.y + 1666, 225, 211), # Medbay: Top right bed
            pygame.Rect(self.x + 3171, self.y + 1935, 225, 181), # Medbay: Bottom right bed
            pygame.Rect(self.x + 3917, self.y + 1408, 139, 738), # Medbay: Top left wall
            pygame.Rect(self.x + 3200, self.y + 2524, 1050, 370), # Medbay: Bottom wall

            pygame.Rect(self.x + 1635, self.y + 1150, 700, 400), # Upper Engine: Engine
            pygame.Rect(self.x + 1660, self.y + 1540, 234, 100), # Upper Engine: Shute
            pygame.Rect(self.x + 1850, self.y + 885, 600, 100), # Upper Engine: Top wall
            pygame.Rect(self.x + 1650, self.y + 1000, 100, 150), # Upper Engine: Top left wall

            pygame.Rect(self.x + 1640, self.y + 3375, 700, 370), # Lower Engine: Engine
            pygame.Rect(self.x + 1665, self.y + 3740, 234, 100), # Lower Engine: Shute
            pygame.Rect(self.x + 2490, self.y + 3705, 370, 550), # Lower Engine: Bottom right wall
            pygame.Rect(self.x + 1850, self.y + 3990, 600, 100), # Lower Engine: Bottom wall

            pygame.Rect(self.x + 3026, self.y + 1880, 145, 920), # Security: Right wall
            pygame.Rect(self.x + 2258, self.y + 2570, 310, 650), # Security: Bottom left wall
            pygame.Rect(self.x + 2258, self.y + 1760, 310, 620), # Security: Top left wall
            pygame.Rect(self.x + 2700, self.y + 1835, 225, 181), # Security: Monitor
            pygame.Rect(self.x + 2740, self.y + 2010, 80, 80), # Security: Monitor chair
            pygame.Rect(self.x + 2840, self.y + 2323, 200, 255), # Security: Desk

            pygame.Rect(self.x + 1710, self.y + 1760, 290, 620), # Reactor: Top right wall
            pygame.Rect(self.x + 1425, self.y + 1600, 234, 505), # Reactor: Top middle wall
            pygame.Rect(self.x + 1200, self.y + 1700, 234, 100), # Reactor: Top wall
            pygame.Rect(self.x + 900, self.y + 1880, 145, 1100), # Reactor: Left wall
            pygame.Rect(self.x + 1425, self.y + 2800, 234, 600), # Reactor: Bottom middle wall
            pygame.Rect(self.x + 1200, self.y + 3100, 234, 100), # Reactor: Bottom wall
            pygame.Rect(self.x + 1710, self.y + 2570, 290, 650), # Reactor: Bottom right wall

            pygame.Rect(self.x + 4232, self.y + 2279, 681, 848), # Cafeteria: Bottom right wall
            pygame.Rect(self.x + 2491, self.y + 2795, 820, 730), # Cafeteria: Bottom right wall

            pygame.Rect(self.x + 3950, self.y + 2825, 300, 100), # Electrical: Top right box
            pygame.Rect(self.x + 3128, self.y + 2812, 204, 1220), # Electrical: Left wall
            pygame.Rect(self.x + 3350, self.y + 3170, 440, 200), # Electrical: Middle left box
            pygame.Rect(self.x + 4010, self.y + 3170, 250, 600), # Electrical: Right Wall
            pygame.Rect(self.x + 3580, self.y + 3718, 680, 315), # Electrical: Top hallway wall
            pygame.Rect(self.x + 2900, self.y + 4212, 1358, 100), # Electrical: Bottom hallway wall
        ]
    
    def draw_collision(self, window):
        for wall in self.wall_objs():
            pygame.draw.rect(window, (0,255,0), wall, 1)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y + (self.height // 3) * 2, self.width, self.height // 3)

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

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
p1 = Player(screen_x // 2, screen_y // 2, 80, 120)
collision_tolerance = max(skeld.x_vel, skeld.y_vel) * 2 + 1
ghost = False
run = True
while run:
    pygame.time.delay(12)

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    redrawGameWindow()
    skeld.wall_objs()

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