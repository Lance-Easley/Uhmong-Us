import pygame, sys
from network import Network
from player import Player
from map import Map
pygame.init()

screen_x = 1920
screen_y = 1080

display = pygame.display.set_mode((screen_x, screen_y))
map_image = pygame.image.load('BCCA_map.jpg')

pygame.display.set_caption("Skeld")


def collide_check(rect, colls):
    collisions = []
    for wall in colls:
        if rect.colliderect(wall):
            collisions.append(skeld.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(skeld.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(skeld.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(skeld.wall_objs().index(wall))
    return collisions

def redrawGameWindow():
    skeld.draw(display)
    skeld.draw_collision(display)
    skeld.draw_tasks(display)
    p1.draw(display)
    p1.draw_hitboxes(display)
    pygame.display.update()

#mainloop
skeld = Map(map_image)
clock = pygame.time.Clock()
collision_tolerance = max(skeld.x_vel, skeld.y_vel) * 2 + 1
p1 = Player(screen_x // 2, screen_y // 2, (255,0,0), skeld, False)
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
    
    # coll_index = collide_check(p1.hitboxes, skeld.wall_objs())
    # if coll_index != []:
    #     for i in coll_index:
    #         if abs(skeld.wall_objs()[i].bottom - p1.w_hitbox.top) < collision_tolerance:
    #             w_coll = False
    #         if abs(skeld.wall_objs()[i].right - p1.a_hitbox.left) < collision_tolerance:
    #             a_coll = False
    #         if abs(skeld.wall_objs()[i].top - p1.s_hitbox.bottom) < collision_tolerance:
    #             s_coll = False
    #         if abs(skeld.wall_objs()[i].left - p1.d_hitbox.right) < collision_tolerance:
    #             d_coll = False

    if collide_check(p1.w_hitbox, skeld.wall_objs()):
        w_coll = False
    if collide_check(p1.a_hitbox, skeld.wall_objs()):
        a_coll = False
    if collide_check(p1.s_hitbox, skeld.wall_objs()):
        s_coll = False
    if collide_check(p1.d_hitbox, skeld.wall_objs()):
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