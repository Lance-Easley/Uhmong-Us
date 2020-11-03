import pygame, sys
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

    def wall_objs(self):
        return [
            pygame.Rect(self.x + 2494, self.y + 752, 1562, 472), # Top medbay hallway
            pygame.Rect(self.x + 3655, self.y + 1402, 401, 272), # Bottom right medbay hallway
            pygame.Rect(self.x + 2494, self.y + 1402, 904, 475), # Bottom left medbay hallway
            pygame.Rect(self.x + 3710, self.y + 1935, 225, 181), # Bottom right medbay bed
            pygame.Rect(self.x + 3710, self.y + 1666, 225, 211) # Top right medbay bed
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

def redrawGameWindow():
    skeld.draw(display)
    skeld.draw_collision(display)
    p1.draw(display)
    pygame.display.update()

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    print(hit_list)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

#mainloop
skeld = Map()
p1 = Player(screen_x // 2, screen_y // 2, 80, 120)
wall_rects = skeld.wall_objs()
run = True
while run:
    pygame.time.delay(16)

    skeld_movement = [0, 0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        skeld_movement[1] += skeld.y_vel
    if keys[pygame.K_a]:
        skeld_movement[0] += skeld.x_vel
    if keys[pygame.K_s]:
        skeld_movement[1] -= skeld.y_vel
    if keys[pygame.K_d]:
        skeld_movement[0] -= skeld.x_vel

    skeld_rect, collisions = move(p1.hitbox, skeld_movement, wall_rects)

    skeld.x += skeld_movement[0]
    skeld.y += skeld_movement[1]

    redrawGameWindow()
    skeld.wall_objs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    # coll_index = p1.hitbox.collidelist(skeld.wall_objs())
    # if coll_index != -1:
    #     if abs(skeld.wall_objs()[coll_index].bottom - p1.hitbox.top) < collision_tolerance:
    #         w_coll = False
    #     else:
    #         w_coll = True
    #     if abs(skeld.wall_objs()[coll_index].right - p1.hitbox.left) < collision_tolerance:
    #         a_coll = False
    #     else:
    #         a_coll = True
    #     if abs(skeld.wall_objs()[coll_index].top - p1.hitbox.bottom) < collision_tolerance:
    #         s_coll = False
    #     else:
    #         s_coll = True
    #     if abs(skeld.wall_objs()[coll_index].left - p1.hitbox.right) < collision_tolerance:
    #         d_coll = False
    #     else:
    #         d_coll = True
    # else:
    #     w_coll = True
    #     a_coll = True
    #     s_coll = True
    #     d_coll = True


    
    if keys[pygame.K_ESCAPE]:
        display = pygame.display.set_mode((screen_x, screen_y))
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()