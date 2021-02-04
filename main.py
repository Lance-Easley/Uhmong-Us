import pygame, sys, time
from network import Network
from player import Player
from map import Map
from math import ceil
pygame.init()

screen_x = 1920
screen_y = 1080

screen_hx = screen_x // 2
screen_hy = screen_y // 2

display = pygame.display.set_mode((screen_x, screen_y))
map_image = pygame.image.load('images/BCCA_map.jpg')

vent_arrow = pygame.image.load('images/hud/arrow.png').convert()
vent_arrow.set_colorkey((255,255,255))

pygame.display.set_caption("Uhmong-Us")

# last_time = time.time()

pygame.font.init()

font = pygame.font.Font("freesansbold.ttf", 32)


def smooth_scroll(game_map, x, y, level):
    last_x = game_map.x
    last_y = game_map.y
    if game_map.x < x:
        if game_map.y < y:
            while game_map.x < x or game_map.y < y:
                game_map.x -= round(game_map.x - x, 2) / level
                game_map.y -= round(game_map.y - y, 2) / level
                if game_map.x == last_x and game_map.y == last_y:
                    break
                last_x = game_map.x
                last_y = game_map.y
                redrawGameWindow()
        else:
            while game_map.x < x or game_map.y > y:
                game_map.x -= round(game_map.x - x, 2) / level
                game_map.y -= round(game_map.y - y, 2) / level
                if game_map.x == last_x and game_map.y == last_y:
                    break
                last_x = game_map.x
                last_y = game_map.y
                redrawGameWindow()
    else:
        if game_map.y < y:
            while game_map.x > x or game_map.y < y:
                game_map.x -= round(game_map.x - x, 2) / level
                game_map.y -= round(game_map.y - y, 2) / level
                if game_map.x == last_x and game_map.y == last_y:
                    break
                last_x = game_map.x
                last_y = game_map.y
                redrawGameWindow()
        else:
            while game_map.x > x or game_map.y > y:
                game_map.x -= round(game_map.x - x, 2) / level
                game_map.y -= round(game_map.y - y, 2) / level
                if game_map.x == last_x and game_map.y == last_y:
                    break
                last_x = game_map.x
                last_y = game_map.y
                redrawGameWindow()
    game_map.x = x
    game_map.y = y
        

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
        # bcca.x = 786
        # bcca.y = -624
        smooth_scroll(bcca, 786, -624, 7)
    elif player.in_vent == 2:
        # bcca.x = -839
        # bcca.y = -299
        smooth_scroll(bcca, -839, -299, 7)
    elif player.in_vent == 3:
        # bcca.x = -2139
        # bcca.y = -1174
        smooth_scroll(bcca, -2139, -1174, 7)
    elif player.in_vent == 4:
        # bcca.x = -3039
        # bcca.y = 151
        smooth_scroll(bcca, -3039, 151, 7)
    elif player.in_vent == 5:
        # bcca.x = -4564
        # bcca.y = -1374
        smooth_scroll(bcca, -4564, -1374, 7)
    elif player.in_vent == 6:
        # bcca.x = -5264
        # bcca.y = 126
        smooth_scroll(bcca, -5264, 126, 7)
    elif player.in_vent == 7:
        # bcca.x = -6239
        # bcca.y = 51
        smooth_scroll(bcca, -6239, 51, 7)
    elif player.in_vent == 8:
        # bcca.x = -6789
        # bcca.y = -1149
        smooth_scroll(bcca, -6789, -1149, 7)

def draw_vent_arrows(player, image):
    global left_arrow
    global right_arrow
    if player.in_vent == 1:
        left_arrow = None
        right_arrow = display.blit(pygame.transform.rotate(image, 10.0), (1050, 540))
    elif player.in_vent == 2:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 10.0), (870, 570))
        right_arrow = display.blit(pygame.transform.rotate(image, -30.0), (1030, 605))
    elif player.in_vent == 3:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -30.0), (870, 510))
        right_arrow = display.blit(pygame.transform.rotate(image, 45.0), (1020, 490))
    elif player.in_vent == 4:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 45.0), (870, 605))
        right_arrow = None
    
    if player.in_vent == 5:
        left_arrow = display.blit(pygame.transform.rotate(image, 80.0), (970, 450))
        right_arrow = display.blit(pygame.transform.rotate(image, 10.0), (1050, 540))
    elif player.in_vent == 6:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 80.0), (935, 645))
        right_arrow = display.blit(pygame.transform.rotate(image, -8.0), (1045, 570))
    elif player.in_vent == 7:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -8.0), (870, 545))
        right_arrow = display.blit(pygame.transform.rotate(image, -70.0), (985, 640))
    elif player.in_vent == 8:
        left_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), -70.0), (920, 450))
        right_arrow = display.blit(pygame.transform.rotate(pygame.transform.flip(image, True, False), 10.0), (870, 570))

def redrawGameWindow():
    display.fill((255,255,255))
    bcca.draw(display)
    bcca.draw_collision(display)
    bcca.draw_tasks(display)
    bcca.draw_vents(display)
    draw_vent_arrows(p1, vent_arrow)
    bcca.draw_coords(display, font)
    p1.draw(display)
    p1.draw_hitboxes(display)
    pygame.display.update()


#mainloop
bcca = Map(map_image)
clock = pygame.time.Clock()
collision_tolerance = max(bcca.x_vel, bcca.y_vel) * 2 + 1
p1 = Player(screen_hx, screen_hy, (255,0,0), bcca, False, 0)
ghost = False
run = True
left_arrow = None
right_arrow = None
while run:
    # dt = time.time() - last_time
    # dt *= 60
    # last_time = time.time()

    w_coll = True
    a_coll = True
    s_coll = True
    d_coll = True

    m_pos = pygame.mouse.get_pos()

    redrawGameWindow()

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

                    elif bcca.x < -4464 and bcca.x > -4764:
                        if bcca.y < -1274 and bcca.y > -1474:
                            p1.in_vent = 5
                    elif bcca.x < -5164 and bcca.x > -5364:
                        if bcca.y < 226 and bcca.y > 26:
                            p1.in_vent = 6
                    elif bcca.x < -6139 and bcca.x > -6339:
                        if bcca.y < 151 and bcca.y > -51:
                            p1.in_vent = 7
                    elif bcca.x < -6689 and bcca.x > -6889:
                        if bcca.y < -1049 and bcca.y > -1249:
                            p1.in_vent = 8
                else:
                    p1.in_vent = 0

            # elif event.key == pygame.K_w:
            #     if p1.in_vent == 5:
            #         p1.in_vent = 6
            #     elif p1.in_vent == 8:
            #         p1.in_vent = 7

            # elif event.key == pygame.K_s:
            #     if p1.in_vent == 6:
            #         p1.in_vent = 5
            #     elif p1.in_vent == 7:
            #         p1.in_vent = 8

            # elif event.key == pygame.K_a:
            #     if p1.in_vent == 2:
            #         p1.in_vent = 1
            #     elif p1.in_vent == 3:
            #         p1.in_vent = 2
            #     elif p1.in_vent == 4:
            #         p1.in_vent = 3
            #     elif p1.in_vent == 8:
            #         p1.in_vent = 5
            #     elif p1.in_vent == 7:
            #         p1.in_vent = 6

            # elif event.key == pygame.K_d:
            #     if p1.in_vent == 1:
            #         p1.in_vent = 2
            #     elif p1.in_vent == 2:
            #         p1.in_vent = 3
            #     elif p1.in_vent == 3:
            #         p1.in_vent = 4
            #     elif p1.in_vent == 5:
            #         p1.in_vent = 8
            #     elif p1.in_vent == 6:
            #         p1.in_vent = 7

            elif event.key == pygame.K_x:
                ghost = not ghost
            elif event.key == pygame.K_LEFT:
                bcca.x += 1
            elif event.key == pygame.K_RIGHT:
                bcca.x -= 1
            elif event.key == pygame.K_UP:
                bcca.y += 1
            elif event.key == pygame.K_DOWN:
                bcca.y -= 1

            if p1.in_vent != 0:
                transport_vents(p1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if p1.in_vent == 1:
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 2
                elif p1.in_vent == 2:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 1
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 3
                elif p1.in_vent == 3:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 2
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 4
                elif p1.in_vent == 4:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 3
                elif p1.in_vent == 5:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 6
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 8
                elif p1.in_vent == 6:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 5
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 7
                elif p1.in_vent == 7:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 6
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 8
                elif p1.in_vent == 8:
                    if left_arrow:
                        if left_arrow.collidepoint(m_pos):
                            p1.in_vent = 7
                    if right_arrow:
                        if right_arrow.collidepoint(m_pos):
                            p1.in_vent = 5
                if p1.in_vent != 0:
                    transport_vents(p1)

    keys = pygame.key.get_pressed()

    if ghost:
        w_coll = True
        a_coll = True
        s_coll = True
        d_coll = True
    if keys[pygame.K_w]:
        if w_coll and p1.in_vent == 0:
            for pixel in range(bcca.y_vel):
                if collide_check(p1.w_hitbox, bcca.wall_objs()):
                    w_coll = False
                    break
                else:
                    bcca.y += 1
    if keys[pygame.K_a]:
        if a_coll and p1.in_vent == 0:
            for pixel in range(bcca.x_vel):
                if collide_check(p1.a_hitbox, bcca.wall_objs()):
                    a_coll = False
                else:
                    bcca.x += 1
    if keys[pygame.K_s]:
        if s_coll and p1.in_vent == 0:
            for pixel in range(bcca.y_vel):
                if collide_check(p1.s_hitbox, bcca.wall_objs()):
                    s_coll = False
                else:
                    bcca.y -= 1
    if keys[pygame.K_d]:
        if d_coll and p1.in_vent == 0:
            for pixel in range(bcca.x_vel):
                if collide_check(p1.d_hitbox, bcca.wall_objs()):
                    d_coll = False
                else:
                    bcca.x -= 1
    if keys[pygame.K_c]:
        print(bcca.x, bcca.y)

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    clock.tick(60)
pygame.quit()
sys.exit()