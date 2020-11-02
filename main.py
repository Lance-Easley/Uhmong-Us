import pygame, sys, pylygon
pygame.init()

screen_x = 1920
screen_y = 1080

display = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
map_image = pygame.image.load('Skeld_map.jpg')

pygame.display.set_caption("Skeld")

class Map(object):
    def __init__(self):
        self.x = -3500
        self.y = -900
        self.width = map_image.get_rect().width
        self.height = map_image.get_rect().height
        self.x_vel = 5
        self.y_vel = 5

    def draw(self, window):
        window.blit(map_image, (self.x, self.y))

    def wall_objs(self, window):
        wall_0 = pygame.Rect(self.x + 2494, self.y + 752, 1562, 472)
        wall_1 = pygame.Rect(self.x + 3655, self.y + 1402, 401, 480)
        wall_2 = pygame.Rect(self.x + 2494, self.y + 1402, 904, 480)
        wall_2 = pygame.Rect(self.x + 2494, self.y + 1402, 904, 480)
        wall_2 = pygame.transform.rotate(window, 45)
        return [wall_0, wall_1, wall_2]
    
    def draw_collision(self, window):
        for wall in self.wall_objs(window):
            pygame.draw.rect(window, (0,255,0), wall, 1)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y + (self.height // 2), self.width, self.height // 2)

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

def redrawGameWindow():
    skeld.draw(display)
    skeld.draw_collision(display)
    p1.draw(display)
    pygame.display.update()

#mainloop
skeld = Map()
p1 = Player(screen_x // 2, screen_y // 2, 80, 120)
collision_tolerance = max(skeld.x_vel, skeld.y_vel) + 1
run = True
while run:
    pygame.time.delay(16)

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    redrawGameWindow()
    skeld.wall_objs(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    coll_index = p1.hitbox.collidelist(skeld.wall_objs())
    if coll_index != -1:
        if abs(skeld.wall_objs()[coll_index].bottom - p1.hitbox.top) < collision_tolerance:
            w_coll = False
        if abs(skeld.wall_objs()[coll_index].right - p1.hitbox.left) < collision_tolerance:
            a_coll = False
        if abs(skeld.wall_objs()[coll_index].top - p1.hitbox.bottom) < collision_tolerance:
            s_coll = False
        if abs(skeld.wall_objs()[coll_index].left - p1.hitbox.right) < collision_tolerance:
            d_coll = False

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
    
    if keys[pygame.K_ESCAPE]:
        display = pygame.display.set_mode((screen_x, screen_y))
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()