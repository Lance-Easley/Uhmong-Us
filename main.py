import pygame, sys, time
from network import Network
from player import Player
from map import Map
from math import floor
pygame.init()

screen_x = 1920
screen_y = 1080

display = pygame.display.set_mode((screen_x, screen_y))
map_image = pygame.image.load('BCCA_map.jpg')

pygame.display.set_caption("Uhmong-Us")

last_time = time.time()

pygame.font.init()

font = pygame.font.Font("freesansbold.ttf", 32)


def collide_check(rect, colls):
    collisions = []
    for wall in colls:
        if rect.colliderect(wall):
            collisions.append(bcca.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(bcca.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(bcca.wall_objs().index(wall))
        if rect.colliderect(wall):
            collisions.append(bcca.wall_objs().index(wall))
    return collisions

def transport_vents(player):
    if player.in_vent == 0:
        pass
    elif player.in_vent == 1:
        bcca.x = 786
        bcca.y = -624
    elif player.in_vent == 2:
        bcca.x = -839
        bcca.y = -299
    elif player.in_vent == 3:
        bcca.x = -2139
        bcca.y = -1174
    elif player.in_vent == 4:
        bcca.x = -3039
        bcca.y = 151
    

def redrawGameWindow():
    bcca.draw(display)
    bcca.draw_collision(display)
    bcca.draw_tasks(display)
    bcca.draw_vents(display)
    bcca.draw_coords(display, font)
    p1.draw(display)
    p1.draw_hitboxes(display)
    pygame.display.update()

#mainloop
bcca = Map(map_image)
clock = pygame.time.Clock()
collision_tolerance = max(bcca.x_vel, bcca.y_vel) * 2 + 1
p1 = Player(screen_x // 2, screen_y // 2, (255,0,0), bcca, False, 0)
ghost = False
run = True
while run:
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    display.fill((255,255,255))

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    redrawGameWindow()
    # bcca.wall_objs()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                if p1.in_vent == 0:
                    if bcca.x < 886 and bcca.x > 686:
                        if bcca.y < -524 and bcca.y > -724:
                            p1.in_vent = 1
                    elif bcca.x < -739 and bcca.x > -939:
                        if bcca.y < -199 and bcca.y > -399:
                            p1.in_vent = 2
                    elif bcca.x < -2039 and bcca.x > -2239:
                        if bcca.y < -1074 and bcca.y > -1274:
                            p1.in_vent = 3
                    elif bcca.x < -2939 and bcca.x > -3139:
                        if bcca.y < 251 and bcca.y > 51:
                            p1.in_vent = 4
                else:
                    p1.in_vent = 0
            elif event.key == pygame.K_a:
                if p1.in_vent == 2:
                    p1.in_vent = 1
                elif p1.in_vent == 3:
                    p1.in_vent = 2
                elif p1.in_vent == 4:
                    p1.in_vent = 3
            elif event.key == pygame.K_d:
                if p1.in_vent == 1:
                    p1.in_vent = 2
                elif p1.in_vent == 2:
                    p1.in_vent = 3
                elif p1.in_vent == 3:
                    p1.in_vent = 4
            elif event.key == pygame.K_x:
                ghost = not ghost

    keys = pygame.key.get_pressed()

    if collide_check(p1.w_hitbox, bcca.wall_objs()):
        w_coll = False
    if collide_check(p1.a_hitbox, bcca.wall_objs()):
        a_coll = False
    if collide_check(p1.s_hitbox, bcca.wall_objs()):
        s_coll = False
    if collide_check(p1.d_hitbox, bcca.wall_objs()):
        d_coll = False

    if ghost:
        w_coll = True
        a_coll = True
        s_coll = True
        d_coll = True
    if keys[pygame.K_w]:
        if w_coll and p1.in_vent == 0:
            bcca.y += floor(bcca.y_vel * dt)
    if keys[pygame.K_a]:
        if a_coll and p1.in_vent == 0:
            bcca.x += floor(bcca.x_vel * dt)
    if keys[pygame.K_s]:
        if s_coll and p1.in_vent == 0:
            bcca.y -= floor(bcca.y_vel * dt)
    if keys[pygame.K_d]:
        if d_coll and p1.in_vent == 0:
            bcca.x -= floor(bcca.x_vel * dt)
    if keys[pygame.K_c]:
        pos_text = font.render(f"X: {bcca.x}\nY: {bcca.y}", True, (255,0,0))
        pos_textRect = pos_text.get_rect()
        pos_textRect.center = (0, 0)
        display.blit(pos_text, pos_textRect)
        print(bcca.x, bcca.y)
    
    transport_vents(p1)
    

    if keys[pygame.K_ESCAPE]:
        display = pygame.display.set_mode((screen_x, screen_y))
        pygame.quit()
        sys.exit()

    clock.tick(120)
pygame.quit()
sys.exit()